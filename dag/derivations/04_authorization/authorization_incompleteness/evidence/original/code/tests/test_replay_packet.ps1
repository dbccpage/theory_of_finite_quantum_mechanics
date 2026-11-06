param(
  [string]$RepositoryRoot = (Resolve-Path (
      Join-Path $PSScriptRoot "..\..\..\..\.."
    )).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$packetRoot = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet"
$modulePath = Join-Path $RepositoryRoot "$packetRoot/replay_packet.psm1"
Import-Module $modulePath -Force

function Assert-Equal {
  param(
    [Parameter(Mandatory)]$Actual,
    [Parameter(Mandatory)]$Expected,
    [Parameter(Mandatory)][string]$Label
  )

  if ($Actual -ne $Expected) {
    throw "$Label expected '$Expected' but got '$Actual'"
  }
}

function Assert-Throws {
  param(
    [Parameter(Mandatory)][scriptblock]$Action,
    [Parameter(Mandatory)][string]$Needle,
    [Parameter(Mandatory)][string]$Label
  )

  $caught = $null
  try {
    & $Action
  } catch {
    $caught = $_.Exception
  }
  if ($null -eq $caught) {
    throw "$Label did not throw"
  }
  if ($caught.Message -notlike "*$Needle*") {
    throw "$Label expected an error containing '$Needle' but got '$($caught.Message)'"
  }
}

function Get-JsonObject {
  param([Parameter(Mandatory)][string]$Path)

  return ([System.IO.File]::ReadAllText(
      $Path,
      [System.Text.UTF8Encoding]::new($false)
    ) | ConvertFrom-Json -Depth 64)
}

function Write-JsonObject {
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)][object]$Value
  )

  $text = $Value | ConvertTo-Json -Depth 64
  [System.IO.File]::WriteAllText(
    $Path,
    $text + [Environment]::NewLine,
    [System.Text.UTF8Encoding]::new($false)
  )
}

function New-FixtureRoot {
  $root = Join-Path ([System.IO.Path]::GetTempPath()) (
    "ait-replay-packet-" + [guid]::NewGuid().ToString("N")
  )
  $null = New-Item -ItemType Directory -Path $root
  $files = @(
    "$packetRoot/packet_manifest.json",
    "$packetRoot/transition_proposal.json",
    "$packetRoot/transition_contract.json",
    "$packetRoot/terminal_policy.json",
    "$packetRoot/replay_packet.psm1",
    "$packetRoot/verify_transition_packet.ps1",
    "coda_university/coda_research/authorization_an_incompleteness_theory/formal/tape_transition_invariant_models.lean",
    "coda_university/coda_research/authorization_an_incompleteness_theory/formal/tape_control_authorization_models.lean",
    "lean4/genx/lean-toolchain"
  )
  foreach ($relative in $files) {
    $source = Join-Path $RepositoryRoot $relative
    $destination = Join-Path $root $relative
    $parent = Split-Path -Parent $destination
    $null = New-Item -ItemType Directory -Path $parent -Force
    Copy-Item -LiteralPath $source -Destination $destination
  }
  return $root
}

function Remove-FixtureRoot {
  param([Parameter(Mandatory)][string]$Root)

  $fullRoot = [System.IO.Path]::GetFullPath($Root)
  $tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
  if (-not $fullRoot.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
      -not (Split-Path -Leaf $fullRoot).StartsWith("ait-replay-packet-")) {
    throw "Refusing to remove unexpected fixture root $fullRoot"
  }
  Remove-Item -LiteralPath $fullRoot -Recurse -Force
}

function Set-ArtifactDigest {
  param(
    [Parameter(Mandatory)][string]$Root,
    [Parameter(Mandatory)][string]$Role
  )

  $manifestPath = Join-Path $Root "$packetRoot/packet_manifest.json"
  $manifest = Get-JsonObject -Path $manifestPath
  $artifact = @($manifest.artifacts | Where-Object { $_.role -eq $Role })
  if ($artifact.Count -ne 1) {
    throw "No unique artifact role $Role"
  }
  $artifactPath = Join-Path $Root $artifact[0].path
  $artifact[0].sha256 = (
    Get-FileHash -LiteralPath $artifactPath -Algorithm SHA256
  ).Hash.ToLowerInvariant()
  Write-JsonObject -Path $manifestPath -Value $manifest
}

$testCount = 0

$result = Invoke-ReplayPacket -RepositoryRoot $RepositoryRoot
Assert-Equal -Actual $result.verification_status -Expected "verified" -Label "good packet status"
Assert-Equal -Actual $result.terminal -Expected "open" -Label "good packet terminal"
Assert-Equal -Actual $result.source_claimed_pass_used -Expected $false -Label "source pass use"
Assert-Equal -Actual $result.evaluation.clean_terminal_preserved -Expected $true -Label "clean terminal preservation"
Assert-Equal -Actual $result.evaluation.full_report_adequate -Expected $true -Label "full report adequacy"
Assert-Equal -Actual $result.evaluation.control_only_report_adequate -Expected $false -Label "control report adequacy"
Assert-Equal -Actual $result.evaluation.control_only_authorization -Expected "open_due_to_inadequate_report" -Label "inadequate control route"
$testCount += 1

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  $proposal = Get-JsonObject -Path $proposalPath
  $proposal.source_claimed_pass = $false
  Write-JsonObject -Path $proposalPath -Value $proposal
  Set-ArtifactDigest -Root $fixture -Role "proposal"
  $result = Invoke-ReplayPacket -RepositoryRoot $fixture
  Assert-Equal -Actual $result.verification_status -Expected "verified" -Label "self-pass false status"
  Assert-Equal -Actual $result.source_claimed_pass_used -Expected $false -Label "self-pass false use"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  $bytes = [System.Collections.Generic.List[byte]]::new(
    [System.IO.File]::ReadAllBytes($proposalPath)
  )
  $bytes.Add(0xff)
  [System.IO.File]::WriteAllBytes($proposalPath, $bytes.ToArray())
  Set-ArtifactDigest -Root $fixture -Role "proposal"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "not valid UTF-8 JSON" -Label "invalid UTF-8 proposal"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  $text = [System.IO.File]::ReadAllText($proposalPath)
  $text = $text.Replace(
    '"schema_version":',
    '"schema_version":"duplicate", "schema_version":'
  )
  [System.IO.File]::WriteAllText(
    $proposalPath,
    $text,
    [System.Text.UTF8Encoding]::new($false)
  )
  Set-ArtifactDigest -Root $fixture -Role "proposal"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "duplicate JSON property schema_version" -Label "duplicate JSON property"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  $text = [System.IO.File]::ReadAllText($proposalPath).Replace(
    '"schema_version":',
    '"Schema_Version":'
  )
  [System.IO.File]::WriteAllText(
    $proposalPath,
    $text,
    [System.Text.UTF8Encoding]::new($false)
  )
  Set-ArtifactDigest -Root $fixture -Role "proposal"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "proposal has an invalid field set" -Label "case-variant JSON property"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  $proposal = Get-JsonObject -Path $proposalPath
  $proposal.proposal_id = "Finite-transition-table-v1"
  Write-JsonObject -Path $proposalPath -Value $proposal
  Set-ArtifactDigest -Root $fixture -Role "proposal"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "proposal identifier is not licensed" -Label "case-variant protocol value"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $contractPath = Join-Path $fixture "$packetRoot/transition_contract.json"
  $contract = Get-JsonObject -Path $contractPath
  $contract.expected.clean_terminal_preserved = 1
  Write-JsonObject -Path $contractPath -Value $contract
  Set-ArtifactDigest -Root $fixture -Role "contract"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "clean_terminal_preserved must be Boolean" -Label "coercible expected result"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  [System.IO.File]::AppendAllText(
    $proposalPath,
    [Environment]::NewLine,
    [System.Text.UTF8Encoding]::new($false)
  )
  Assert-Throws -Action {
    Test-ReplayPacket -RepositoryRoot $fixture
  } -Needle "artifact digest mismatch for proposal" -Label "tampered source self-pass"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $manifestPath = Join-Path $fixture "$packetRoot/packet_manifest.json"
  $manifest = Get-JsonObject -Path $manifestPath
  (@($manifest.artifacts | Where-Object { $_.role -eq "contract" }))[0].path = "../outside.json"
  Write-JsonObject -Path $manifestPath -Value $manifest
  Assert-Throws -Action {
    Test-ReplayPacket -RepositoryRoot $fixture
  } -Needle "parent escape" -Label "manifest path escape"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

foreach ($role in @(
    "contract",
    "terminal_policy",
    "evaluator",
    "verifier",
    "formal_model",
    "formal_dependency",
    "lean_toolchain"
  )) {
  $fixture = New-FixtureRoot
  try {
    $manifestPath = Join-Path $fixture "$packetRoot/packet_manifest.json"
    $manifest = Get-JsonObject -Path $manifestPath
    $artifact = @($manifest.artifacts | Where-Object { $_.role -eq $role })[0]
    $artifactPath = Join-Path $fixture $artifact.path
    [System.IO.File]::AppendAllText(
      $artifactPath,
      "# tamper" + [Environment]::NewLine,
      [System.Text.UTF8Encoding]::new($false)
    )
    Assert-Throws -Action {
      Test-ReplayPacket -RepositoryRoot $fixture
    } -Needle "artifact digest mismatch for $role" -Label "$role replacement"
    $testCount += 1
  } finally {
    Remove-FixtureRoot -Root $fixture
  }
}

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  $proposal = Get-JsonObject -Path $proposalPath
  $proposal | Add-Member -NotePropertyName "unlicensed_field" -NotePropertyValue "injected"
  Write-JsonObject -Path $proposalPath -Value $proposal
  Set-ArtifactDigest -Root $fixture -Role "proposal"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "proposal has an invalid field set" -Label "proposal schema injection"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $proposalPath = Join-Path $fixture "$packetRoot/transition_proposal.json"
  $proposal = Get-JsonObject -Path $proposalPath
  $proposal.schema_version = "unlicensed.proposal.v1"
  Write-JsonObject -Path $proposalPath -Value $proposal
  Set-ArtifactDigest -Root $fixture -Role "proposal"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "proposal schema version is not supported" -Label "proposal schema substitution"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $contractPath = Join-Path $fixture "$packetRoot/transition_contract.json"
  $contract = Get-JsonObject -Path $contractPath
  $contract.expected.control_only_report_adequate = $true
  Write-JsonObject -Path $contractPath -Value $contract
  Set-ArtifactDigest -Root $fixture -Role "contract"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "evaluator disagrees with the declared control-only adequacy result" -Label "declared outcome substitution"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $policyPath = Join-Path $fixture "$packetRoot/terminal_policy.json"
  $policy = Get-JsonObject -Path $policyPath
  $policy.on_verified = "authorized"
  Write-JsonObject -Path $policyPath -Value $policy
  Set-ArtifactDigest -Root $fixture -Role "terminal_policy"
  Assert-Throws -Action {
    Invoke-ReplayPacket -RepositoryRoot $fixture
  } -Needle "terminal policy is not the declared bounded open policy" -Label "terminal policy substitution"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $manifestPath = Join-Path $fixture "$packetRoot/packet_manifest.json"
  $manifest = Get-JsonObject -Path $manifestPath
  $manifest.execution_profile.json_parser = "unlicensed parser"
  Write-JsonObject -Path $manifestPath -Value $manifest
  Assert-Throws -Action {
    Test-ReplayPacket -RepositoryRoot $fixture
  } -Needle "JSON parser is not the declared bounded parser" -Label "parser substitution"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $manifestPath = Join-Path $fixture "$packetRoot/packet_manifest.json"
  $manifest = Get-JsonObject -Path $manifestPath
  $manifest.execution_profile.formal_replay_workdir = "unlicensed workdir"
  Write-JsonObject -Path $manifestPath -Value $manifest
  Assert-Throws -Action {
    Test-ReplayPacket -RepositoryRoot $fixture
  } -Needle "formal replay work directory is not licensed" -Label "workdir substitution"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

$fixture = New-FixtureRoot
try {
  $manifestPath = Join-Path $fixture "$packetRoot/packet_manifest.json"
  $manifest = Get-JsonObject -Path $manifestPath
  $manifest.execution_profile.formal_replay_command = "unlicensed command"
  Write-JsonObject -Path $manifestPath -Value $manifest
  Assert-Throws -Action {
    Test-ReplayPacket -RepositoryRoot $fixture
  } -Needle "formal replay command is not licensed" -Label "command substitution"
  $testCount += 1
} finally {
  Remove-FixtureRoot -Root $fixture
}

Write-Output "Replay packet unit tests passed: $testCount cases; twenty-one tamper mutations were rejected."
