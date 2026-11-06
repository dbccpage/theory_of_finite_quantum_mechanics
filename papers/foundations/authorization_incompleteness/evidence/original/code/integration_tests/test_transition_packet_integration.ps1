param(
  [string]$RepositoryRoot = (Resolve-Path (
      Join-Path $PSScriptRoot "..\..\..\..\.."
    )).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$packetRoot = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet"
$verifier = Join-Path $RepositoryRoot "$packetRoot/verify_transition_packet.ps1"
$raw = & $verifier -RepositoryRoot $RepositoryRoot -RunFormalReplay
if ($LASTEXITCODE -ne 0) {
  throw "Packet verifier exited with $LASTEXITCODE"
}

$result = ($raw -join [Environment]::NewLine) | ConvertFrom-Json -Depth 64
if ($result.verification_status -ne "verified") {
  throw "Expected verified packet but got $($result.verification_status)"
}
if ($result.terminal -ne "open") {
  throw "Expected open terminal but got $($result.terminal)"
}
if ($result.formal_replay -ne "pass") {
  throw "Expected passing formal replay but got $($result.formal_replay)"
}
if ($result.evaluation.control_only_report_adequate -ne $false) {
  throw "Control-only report unexpectedly became adequate"
}
if ($result.evaluation.control_only_authorization -ne "open_due_to_inadequate_report") {
  throw "Control-only authorization did not remain open"
}

Write-Output "Replay packet integration test passed: finite evaluator and target-local Lean closure replayed."
