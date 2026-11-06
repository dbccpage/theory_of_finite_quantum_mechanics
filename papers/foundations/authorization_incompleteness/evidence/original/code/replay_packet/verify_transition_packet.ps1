[CmdletBinding()]
param(
  [string]$RepositoryRoot = (Get-Location).Path,
  [string]$ManifestPath = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/packet_manifest.json",
  [switch]$RunFormalReplay
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$modulePath = Join-Path $PSScriptRoot "replay_packet.psm1"
Import-Module $modulePath -Force

try {
  $packet = Test-ReplayPacket -RepositoryRoot $RepositoryRoot -ManifestPath $ManifestPath
  $result = Invoke-ReplayPacket -RepositoryRoot $RepositoryRoot -ManifestPath $ManifestPath
  $formalReplay = "not_requested"

  if ($RunFormalReplay) {
    $workdir = Join-Path $RepositoryRoot $packet.manifest.execution_profile.formal_replay_workdir
    if (-not (Test-Path -LiteralPath $workdir -PathType Container)) {
      throw "REPLAY_PACKET_REFUSED: formal replay work directory is absent"
    }
    $controlSource = $packet.artifact_paths.formal_dependency
    $transitionSource = $packet.artifact_paths.formal_model
    $temporaryRoot = Join-Path ([System.IO.Path]::GetTempPath()) (
      "ait-formal-replay-" + [guid]::NewGuid().ToString("N")
    )
    $null = New-Item -ItemType Directory -Path $temporaryRoot
    $priorLeanPath = $env:LEAN_PATH
    $priorElanHome = $env:ELAN_HOME
    $setElanHome = $false
    if (-not $env:ELAN_HOME -and $env:USERPROFILE) {
      $candidateElanHome = Join-Path $env:USERPROFILE ".elan"
      if (Test-Path -LiteralPath $candidateElanHome -PathType Container) {
        $env:ELAN_HOME = $candidateElanHome
        $setElanHome = $true
      }
    }

    Push-Location $workdir
    try {
      $null = & elan run $packet.manifest.execution_profile.lean_toolchain lean -o (
        Join-Path $temporaryRoot "tape_control_authorization_models.olean"
      ) $controlSource 2>&1
      if ($LASTEXITCODE -ne 0) {
        throw "REPLAY_PACKET_REFUSED: local formal dependency compilation failed"
      }
      $env:LEAN_PATH = $temporaryRoot
      $null = & elan run $packet.manifest.execution_profile.lean_toolchain lean $transitionSource 2>&1
      if ($LASTEXITCODE -ne 0) {
        throw "REPLAY_PACKET_REFUSED: local formal model compilation failed"
      }
    } finally {
      $env:LEAN_PATH = $priorLeanPath
      if ($setElanHome) {
        $env:ELAN_HOME = $priorElanHome
      }
      Pop-Location
      Remove-Item -LiteralPath $temporaryRoot -Recurse -Force
    }
    $formalReplay = "pass"
  }

  $result | Add-Member -NotePropertyName formal_replay -NotePropertyValue $formalReplay
  $result | ConvertTo-Json -Depth 16
} catch {
  [pscustomobject]@{
    schema_version = "coda.authorization_incompleteness.replay-packet.v1"
    authority_effect = "None"
    verification_status = "refused"
    terminal = "open"
    reason = $_.Exception.Message
  } | ConvertTo-Json -Depth 8
  exit 1
}
