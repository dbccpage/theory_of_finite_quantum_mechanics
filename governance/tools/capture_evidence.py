"""Run governance checks against the existing sources, with owned process lifetimes.

Commands are offline. A Windows job (or POSIX process group) contains descendants.
Output is streamed to a file; a polling limit is not a hard filesystem quota.
Receipts bind inputs before and after execution; callers must exclude other writers.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import signal
import stat
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
CRATE = ROOT / "code/rust/src/governance"
MANIFEST = ROOT / "governance/Cargo.toml"
MAX_SOURCE = 2 * 1024 * 1024
MAX_FILES = 128
SUPERVISOR = "import json,subprocess,sys,os; a,e=json.loads(sys.stdin.readline()); env=dict(os.environ); env.update(e); sys.exit(subprocess.run(a,env=env).returncode)"


class State(str, Enum):
    COMPLETED = "COMPLETED"
    TIMEOUT = "TIMEOUT"
    OUTPUT_LIMIT = "OUTPUT_LIMIT"
    EXECUTION_ERROR = "EXECUTION_ERROR"
    CLEANUP_ERROR = "CLEANUP_ERROR"


@dataclass(frozen=True)
class Limits:
    seconds: float = 240
    output_bytes: int = 4 * 1024 * 1024

    def validate(self) -> None:
        if not 0 < self.seconds <= 3600 or not 1 <= self.output_bytes <= 64 * 1024 * 1024:
            raise ValueError("limits must be 0 < seconds <= 3600 and 1 <= bytes <= 64 MiB")


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    state: State
    exit_status: int | None
    log: str
    log_sha256: str
    output_bytes: int
    seconds: float
    error: str = ""

    @property
    def passed(self) -> bool:
        return self.state == State.COMPLETED and self.exit_status == 0


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def source_hashes(crate: Path) -> dict[str, str]:
    paths = sorted((crate / "src").rglob("*.rs")) + [crate / "Cargo.toml", crate / "clippy.toml"]
    if len(paths) > MAX_FILES:
        raise ValueError("too many source files")
    result = {}
    for path in paths:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_SOURCE or path.resolve().is_relative_to(crate.resolve()) is False:
            raise ValueError("source must be a bounded regular file inside the crate: " + str(path))
        result[path.relative_to(crate).as_posix()] = sha(path)
    return result


class WindowsJob:
    """Own one Windows Job handle. Child startup is gated until assignment."""
    def __init__(self) -> None:
        from ctypes import wintypes as w
        class Basic(ctypes.Structure):
            _fields_ = [("process_time", ctypes.c_int64), ("job_time", ctypes.c_int64),
                        ("flags", w.DWORD), ("min_ws", ctypes.c_size_t), ("max_ws", ctypes.c_size_t),
                        ("active_limit", w.DWORD), ("affinity", ctypes.c_size_t),
                        ("priority", w.DWORD), ("scheduling", w.DWORD)]
        class Extended(ctypes.Structure):
            _fields_ = [("basic", Basic), ("io", ctypes.c_uint64 * 6),
                        ("process_mem", ctypes.c_size_t), ("job_mem", ctypes.c_size_t),
                        ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]
        self.api = ctypes.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL),
            "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
            "OpenProcess": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "QueryInformationJobObject": ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p], w.BOOL),
            "CloseHandle": ([w.HANDLE], w.BOOL),
        }
        for name, (args, result) in signatures.items():
            function = getattr(self.api, name)
            function.argtypes, function.restype = args, result
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        config = Extended()
        config.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(config), ctypes.sizeof(config)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.api.CloseHandle(self.handle)
            raise error

    def assign(self, pid: int) -> None:
        handle = self.api.OpenProcess(0x0101, False, pid)  # SET_QUOTA | TERMINATE
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            if not self.api.AssignProcessToJobObject(self.handle, handle):
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            self.api.CloseHandle(handle)

    def close(self) -> None:
        error = None
        try:
            if not self.api.TerminateJobObject(self.handle, 125):
                raise ctypes.WinError(ctypes.get_last_error())
            # BASIC_ACCOUNTING_INFORMATION: four int64 times, then four DWORDs.
            accounting = (ctypes.c_uint64 * 6)()
            deadline = time.monotonic() + 5
            while True:
                if not self.api.QueryInformationJobObject(self.handle, 1, ctypes.byref(accounting), 48, None):
                    raise ctypes.WinError(ctypes.get_last_error())
                active = ctypes.c_uint32.from_buffer(accounting, 40).value
                if active == 0:
                    break
                if time.monotonic() >= deadline:
                    raise OSError("job descendants did not terminate within 5 seconds")
                time.sleep(0.01)
        except OSError as failure:
            error = failure
        finally:
            if not self.api.CloseHandle(self.handle) and error is None:
                error = ctypes.WinError(ctypes.get_last_error())
        if error:
            raise error


def stop_tree(proc: subprocess.Popen[bytes], job: WindowsJob | None) -> None:
    if job:
        job.close()
    elif sys.platform != "win32":
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif proc.poll() is None:
        proc.kill()
    proc.wait(timeout=5)


def poll(proc: subprocess.Popen[bytes], log: Path, limits: Limits, deadline: float) -> State:
    while True:
        if log.stat().st_size > limits.output_bytes:
            return State.OUTPUT_LIMIT
        if proc.poll() is not None:
            return State.COMPLETED
        if time.monotonic() >= deadline:
            return State.TIMEOUT
        time.sleep(0.02)


def await_log_release(log: Path) -> None:
    """Observe closure of inherited log handles after asynchronous Windows termination."""
    if os.name != "nt":
        return
    from ctypes import wintypes as w
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    api.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, ctypes.c_void_p, w.DWORD, w.DWORD, w.HANDLE]
    api.CreateFileW.restype = w.HANDLE
    api.CloseHandle.argtypes = [w.HANDLE]
    api.CloseHandle.restype = w.BOOL
    deadline = time.monotonic() + 5
    while True:
        handle = api.CreateFileW(str(log.resolve()), 0x80000000, 0, None, 3, 0x80, None)
        if handle != ctypes.c_void_p(-1).value:
            if not api.CloseHandle(handle):
                raise ctypes.WinError(ctypes.get_last_error())
            return
        error = ctypes.get_last_error()
        if error != 32 or time.monotonic() >= deadline:
            raise ctypes.WinError(error)
        time.sleep(0.01)


def run(command: Sequence[str], cwd: Path, env: Mapping[str, str], log: Path,
        limits: Limits = Limits()) -> CommandResult:
    limits.validate()
    if not command or any(not isinstance(arg, str) or "\0" in arg for arg in command):
        raise ValueError("command must be a nonempty argument vector without NUL")
    command = list(command)
    env = dict(env)
    child_env: dict[str, str] = {}
    # Windows Store activation and venv redirectors may broker a process outside a job.
    # Launch the physical interpreter directly while preserving the current venv.
    direct_python = str(Path(sys.base_prefix) / "python.exe") if os.name == "nt" else sys.executable
    if os.name == "nt" and Path(command[0]).resolve() == Path(sys.executable).resolve():
        command[0] = direct_python
        child_env["__PYVENV_LAUNCHER__"] = sys.executable
    started = time.monotonic()
    state, error, code = State.EXECUTION_ERROR, "", None
    proc = None
    job = None
    with log.open("xb") as stream:
        try:
            if os.name == "nt":
                job = WindowsJob()
            elif os.name != "posix":
                raise OSError("unsupported process ownership platform")
            proc = subprocess.Popen([direct_python, "-I", "-S", "-c", SUPERVISOR], cwd=cwd,
                                    env=env, stdin=subprocess.PIPE, stdout=stream, stderr=stream,
                                    start_new_session=os.name == "posix")
            if job:
                job.assign(proc.pid)
            if proc.stdin is None:
                raise OSError("supervisor startup pipe is absent")
            proc.stdin.write((json.dumps([list(command), child_env]) + "\n").encode())
            proc.stdin.close()
            state = poll(proc, log, limits, started + limits.seconds)
            code = proc.poll()
        except (OSError, ValueError) as failure:
            error = str(failure)
        finally:
            try:
                if proc:
                    if proc.stdin and not proc.stdin.closed:
                        proc.stdin.close()
                    # Assignment can fail: the supervisor is still blocked and has no children.
                    if state == State.EXECUTION_ERROR and proc.poll() is None:
                        proc.kill()
                    stop_tree(proc, job)
                elif job:
                    job.close()
            except (OSError, subprocess.TimeoutExpired) as failure:
                state, error = State.CLEANUP_ERROR, str(failure)
    try:
        await_log_release(log)
    except OSError as failure:
        state, error = State.CLEANUP_ERROR, str(failure)
    size = log.stat().st_size
    if state == State.COMPLETED and size > limits.output_bytes:
        state = State.OUTPUT_LIMIT
    return CommandResult(tuple(command), state, code, str(log), sha(log), size, time.monotonic() - started, error)


def read_output(result: CommandResult, limit: int = 4 * 1024 * 1024) -> str:
    with Path(result.log).open("rb") as stream:
        return stream.read(limit).decode("utf-8", errors="replace")


def build_env() -> dict[str, str]:
    env = dict(os.environ, CARGO_TARGET_DIR=str(ROOT / "governance/target"),
               CLIPPY_CONF_DIR=str(CRATE), CARGO_PROFILE_DEV_DEBUG="0", CARGO_TERM_COLOR="never")
    env.pop("TFQM_GOVERNANCE", None)
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    try:
        captured = source_hashes(CRATE)
        captured["build_manifest"] = sha(MANIFEST)
        captured["build_lock"] = sha(MANIFEST.with_name("Cargo.lock"))
        out.mkdir(parents=True, exist_ok=True)
        commands = {
            "cargo-version": ["cargo", "--version"],
            "rustc-version": ["rustc", "--version"],
            "clippy-version": ["cargo", "clippy", "--version"],
            "test": ["cargo", "test", "--offline", "--locked", "--manifest-path", str(MANIFEST)],
            "clippy": ["cargo", "clippy", "--offline", "--locked", "--manifest-path", str(MANIFEST),
                       "--lib", "--bins", "--", "-D", "warnings", "-D", "clippy::cognitive_complexity", "-D", "clippy::excessive_nesting"],
            "lizard": [sys.executable, "-I", "-m", "lizard", "-l", "rust", "--csv", str(CRATE / "src")],
        }
        steps = {name: run(cmd, ROOT, build_env(), out / (name + ".log")) for name, cmd in commands.items()}
        after = source_hashes(CRATE)
        after["build_manifest"], after["build_lock"] = sha(MANIFEST), sha(MANIFEST.with_name("Cargo.lock"))
        receipt = {"schema": "tfqm.governance-evidence.v2", "AuthorityEffect": "None", "sources": captured,
                   "runner_sha256": sha(Path(__file__)), "python": sys.version,
                   "sources_unchanged": after == captured, "steps": {k: asdict(v) for k, v in steps.items()},
                   "limits": asdict(Limits()), "boundary": "No source copy; exclude concurrent writers. Polling output limit is not a hard disk quota."}
        with (out / "receipt.json").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(receipt, indent=2) + "\n")
        return 0 if after == captured and all(s.passed for s in steps.values()) else 1
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

