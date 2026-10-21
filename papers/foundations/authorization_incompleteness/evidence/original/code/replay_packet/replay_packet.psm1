Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:PacketSchema = "coda.authorization_incompleteness.replay-packet.v1"
$script:ManifestSchema = "coda.authorization_incompleteness.packet-manifest.v1"
$script:PacketId = "AIT-G3-FINITE-TRANSITION-REPLAY-V4"
$script:ProposalSchema = "coda.authorization_incompleteness.transition-proposal.v1"
$script:ContractSchema = "coda.authorization_incompleteness.transition-contract.v1"
$script:PolicySchema = "coda.authorization_incompleteness.terminal-policy.v1"

$script:ExpectedArtifact = [ordered]@{
  proposal = @{
    path = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/transition_proposal.json"
    kind = "proposal"
  }
  contract = @{
    path = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/transition_contract.json"
    kind = "contract"
  }
  terminal_policy = @{
    path = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/terminal_policy.json"
    kind = "terminal_policy"
  }
  evaluator = @{
    path = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/replay_packet.psm1"
    kind = "evaluator"
  }
  verifier = @{
    path = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/verify_transition_packet.ps1"
    kind = "verifier"
  }
  formal_model = @{
    path = "coda_university/coda_research/authorization_an_incompleteness_theory/formal/tape_transition_invariant_models.lean"
    kind = "formal_model"
  }
  formal_dependency = @{
    path = "coda_university/coda_research/authorization_an_incompleteness_theory/formal/tape_control_authorization_models.lean"
    kind = "formal_dependency"
  }
  lean_toolchain = @{
    path = "lean4/genx/lean-toolchain"
    kind = "lean_toolchain"
  }
}

function Throw-ReplayPacketRefusal {
  param([Parameter(Mandatory)][string]$Message)

  throw "REPLAY_PACKET_REFUSED: $Message"
}

function Assert-ExactKeys {
  param(
    [Parameter(Mandatory)][object]$Object,
    [Parameter(Mandatory)][string[]]$Expected,
    [Parameter(Mandatory)][string]$Context
  )

  if ($null -eq $Object -or $Object -isnot [pscustomobject]) {
    Throw-ReplayPacketRefusal "$Context must be a JSON object"
  }

  $actual = @($Object.PSObject.Properties.Name)
  $actualSet = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::Ordinal
  )
  $expectedSet = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::Ordinal
  )
  foreach ($name in $actual) { [void]$actualSet.Add($name) }
  foreach ($name in $Expected) { [void]$expectedSet.Add($name) }
  $missing = @($Expected | Where-Object { -not $actualSet.Contains($_) })
  $extra = @($actual | Where-Object { -not $expectedSet.Contains($_) })
  if ($missing.Count -gt 0 -or $extra.Count -gt 0) {
    $parts = [System.Collections.Generic.List[string]]::new()
    if ($missing.Count -gt 0) {
      $parts.Add("missing: $($missing -join ', ')")
    }
    if ($extra.Count -gt 0) {
      $parts.Add("extra: $($extra -join ', ')")
    }
    Throw-ReplayPacketRefusal "$Context has an invalid field set ($($parts -join '; '))"
  }
}

function Assert-NonEmptyString {
  param(
    [Parameter(Mandatory)][object]$Value,
    [Parameter(Mandatory)][string]$Context
  )

  if ($Value -isnot [string] -or [string]::IsNullOrWhiteSpace($Value)) {
    Throw-ReplayPacketRefusal "$Context must be a non-empty string"
  }
}

function Assert-ExactStringSet {
  param(
    [Parameter(Mandatory)][object]$Value,
    [Parameter(Mandatory)][string[]]$Expected,
    [Parameter(Mandatory)][string]$Context
  )

  if ($null -eq $Value -or $Value -is [string]) {
    Throw-ReplayPacketRefusal "$Context must be an array of strings"
  }

  $actual = @($Value)
  foreach ($item in $actual) {
    if ($item -isnot [string]) {
      Throw-ReplayPacketRefusal "$Context must contain only strings"
    }
  }

  $actualSet = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::Ordinal
  )
  foreach ($item in $actual) {
    if (-not $actualSet.Add($item)) {
      Throw-ReplayPacketRefusal "$Context contains duplicate values"
    }
  }
  $expectedSet = [System.Collections.Generic.HashSet[string]]::new(
    $Expected,
    [System.StringComparer]::Ordinal
  )
  $missing = @($Expected | Where-Object { -not $actualSet.Contains($_) })
  $extra = @($actual | Where-Object { -not $expectedSet.Contains($_) })
  if ($missing.Count -gt 0 -or $extra.Count -gt 0) {
    Throw-ReplayPacketRefusal "$Context differs from its declared finite carrier"
  }
}

function Resolve-ReplayPacketPath {
  param(
    [Parameter(Mandatory)][string]$RepositoryRoot,
    [Parameter(Mandatory)][string]$RelativePath,
    [Parameter(Mandatory)][string]$Context
  )

  Assert-NonEmptyString -Value $RelativePath -Context "$Context path"
  if ([System.IO.Path]::IsPathRooted($RelativePath)) {
    Throw-ReplayPacketRefusal "$Context path is not repository-relative"
  }

  $segments = $RelativePath -split '[\\/]'
  if ($segments -ccontains "..") {
    Throw-ReplayPacketRefusal "$Context path contains a parent escape"
  }

  $root = [System.IO.Path]::GetFullPath($RepositoryRoot).TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
  )
  $candidate = [System.IO.Path]::GetFullPath(
    (Join-Path -Path $root -ChildPath $RelativePath)
  )
  $prefix = $root + [System.IO.Path]::DirectorySeparatorChar
  if ($candidate -ne $root -and -not $candidate.StartsWith(
      $prefix, [System.StringComparison]::OrdinalIgnoreCase
    )) {
    Throw-ReplayPacketRefusal "$Context path resolves outside the repository"
  }

  if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
    Throw-ReplayPacketRefusal "$Context path does not name a file"
  }

  $current = $root
  foreach ($segment in $segments) {
    $current = Join-Path -Path $current -ChildPath $segment
    $pathItem = Get-Item -LiteralPath $current -Force
    if (($pathItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
      Throw-ReplayPacketRefusal "$Context path may not traverse a reparse point"
    }
  }

  $item = Get-Item -LiteralPath $candidate -Force
  return $item.FullName
}

function Get-ReplayPacketSha256 {
  param([Parameter(Mandatory)][string]$Path)

  return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Read-ReplayPacketJson {
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)][string]$Context
  )

  try {
    $utf8 = [System.Text.UTF8Encoding]::new($false, $true)
    $text = $utf8.GetString([System.IO.File]::ReadAllBytes($Path))
    $document = [System.Text.Json.JsonDocument]::Parse($text)
    try {
      Assert-NoDuplicateJsonProperties -Element $document.RootElement -Context $Context
    } finally {
      $document.Dispose()
    }
    $value = $text | ConvertFrom-Json -Depth 64
  } catch {
    Throw-ReplayPacketRefusal "$Context is not valid UTF-8 JSON: $($_.Exception.Message)"
  }

  if ($null -eq $value -or $value -isnot [pscustomobject]) {
    Throw-ReplayPacketRefusal "$Context must be a JSON object"
  }

  return $value
}

function Assert-NoDuplicateJsonProperties {
  param(
    [Parameter(Mandatory)][System.Text.Json.JsonElement]$Element,
    [Parameter(Mandatory)][string]$Context
  )

  if ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Object) {
    $seen = [System.Collections.Generic.HashSet[string]]::new(
      [System.StringComparer]::Ordinal
    )
    foreach ($property in $Element.EnumerateObject()) {
      if (-not $seen.Add($property.Name)) {
        Throw-ReplayPacketRefusal "$Context contains duplicate JSON property $($property.Name)"
      }
      Assert-NoDuplicateJsonProperties -Element $property.Value -Context $Context
    }
  } elseif ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Array) {
    foreach ($item in $Element.EnumerateArray()) {
      Assert-NoDuplicateJsonProperties -Element $item -Context $Context
    }
  }
}

function Get-ManifestArtifactPaths {
  param(
    [Parameter(Mandatory)][object]$Manifest,
    [Parameter(Mandatory)][string]$RepositoryRoot
  )

  if ($Manifest.artifacts -is [string] -or $null -eq $Manifest.artifacts) {
    Throw-ReplayPacketRefusal "manifest artifacts must be an array"
  }

  $artifacts = @($Manifest.artifacts)
  if ($artifacts.Count -ne $script:ExpectedArtifact.Count) {
    Throw-ReplayPacketRefusal "manifest does not bind the exact artifact inventory"
  }

  $seen = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::Ordinal
  )
  $paths = @{}
  foreach ($artifact in $artifacts) {
    Assert-ExactKeys -Object $artifact -Expected @("role", "path", "kind", "sha256") -Context "manifest artifact"
    Assert-NonEmptyString -Value $artifact.role -Context "manifest artifact role"
    if (-not $seen.Add($artifact.role)) {
      Throw-ReplayPacketRefusal "manifest contains a duplicate artifact role"
    }

    if (-not (@($script:ExpectedArtifact.Keys) -ccontains $artifact.role)) {
      Throw-ReplayPacketRefusal "manifest names an unlicensed artifact role $($artifact.role)"
    }

    $expected = $script:ExpectedArtifact[$artifact.role]
    $actualPath = Resolve-ReplayPacketPath -RepositoryRoot $RepositoryRoot -RelativePath $artifact.path -Context "artifact $($artifact.role)"
    if ($artifact.path -cne $expected.path) {
      Throw-ReplayPacketRefusal "artifact $($artifact.role) does not use its licensed path"
    }
    if ($artifact.kind -cne $expected.kind) {
      Throw-ReplayPacketRefusal "artifact $($artifact.role) does not use its licensed kind"
    }
    if ($artifact.sha256 -isnot [string] -or $artifact.sha256 -notmatch '^[a-f0-9]{64}$') {
      Throw-ReplayPacketRefusal "artifact $($artifact.role) has an invalid SHA-256 digest"
    }
    if ((Get-ReplayPacketSha256 -Path $actualPath) -cne $artifact.sha256) {
      Throw-ReplayPacketRefusal "artifact digest mismatch for $($artifact.role)"
    }
    $paths[$artifact.role] = $actualPath
  }

  foreach ($role in $script:ExpectedArtifact.Keys) {
    if (-not $seen.Contains($role)) {
      Throw-ReplayPacketRefusal "manifest omits artifact role $role"
    }
  }

  return $paths
}

function Test-ReplayPacket {
  [OutputType([pscustomobject])]
  param(
    [Parameter(Mandatory)][string]$RepositoryRoot,
    [string]$ManifestPath = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/packet_manifest.json"
  )

  if ($PSVersionTable.PSVersion.ToString() -cne "7.6.3") {
    Throw-ReplayPacketRefusal "runtime is not the declared PowerShell 7.6.3 profile"
  }

  $manifestFile = Resolve-ReplayPacketPath -RepositoryRoot $RepositoryRoot -RelativePath $ManifestPath -Context "manifest"
  $manifest = Read-ReplayPacketJson -Path $manifestFile -Context "manifest"
  Assert-ExactKeys -Object $manifest -Expected @(
    "schema_version",
    "packet_id",
    "authority_effect",
    "manifest_trust_boundary",
    "terminal_policy",
    "evidence_ceiling",
    "tcb",
    "execution_profile",
    "artifacts"
  ) -Context "manifest"

  if ($manifest.schema_version -cne $script:ManifestSchema) {
    Throw-ReplayPacketRefusal "manifest schema version is not supported"
  }
  if ($manifest.packet_id -cne $script:PacketId) {
    Throw-ReplayPacketRefusal "manifest packet identifier is not licensed"
  }
  if ($manifest.authority_effect -cne "None") {
    Throw-ReplayPacketRefusal "manifest must declare AuthorityEffect None"
  }
  if ($manifest.manifest_trust_boundary -cne "fixed_outside_proposal_bytes") {
    Throw-ReplayPacketRefusal "manifest does not declare its proposal-external trust boundary"
  }
  if ($manifest.terminal_policy -cne "open_after_verified") {
    Throw-ReplayPacketRefusal "manifest terminal policy is not the bounded open policy"
  }
  Assert-NonEmptyString -Value $manifest.evidence_ceiling -Context "manifest evidence ceiling"

  Assert-ExactKeys -Object $manifest.tcb -Expected @(
    "hash_algorithm",
    "collision_resistance_assumption",
    "evaluator_soundness_assumption",
    "custody_assumption"
  ) -Context "manifest trusted computing base"
  if ($manifest.tcb.hash_algorithm -cne "SHA-256") {
    Throw-ReplayPacketRefusal "manifest names an unsupported hash algorithm"
  }
  foreach ($field in @(
      "collision_resistance_assumption",
      "evaluator_soundness_assumption",
      "custody_assumption"
    )) {
    Assert-NonEmptyString -Value $manifest.tcb.$field -Context "manifest tcb $field"
  }

  Assert-ExactKeys -Object $manifest.execution_profile -Expected @(
    "runtime",
    "json_parser",
    "lean_toolchain",
    "formal_replay_command",
    "formal_replay_workdir"
  ) -Context "manifest execution profile"
  if ($manifest.execution_profile.runtime -cne "PowerShell 7.6.3; Lean 4.32.2") {
    Throw-ReplayPacketRefusal "manifest execution profile is not the declared bounded profile"
  }
  if ($manifest.execution_profile.json_parser -cne "PowerShell ConvertFrom-Json 7.6.3") {
    Throw-ReplayPacketRefusal "manifest JSON parser is not the declared bounded parser"
  }
  if ($manifest.execution_profile.lean_toolchain -cne "leanprover/lean4:v4.32.2") {
    Throw-ReplayPacketRefusal "manifest Lean toolchain is not the declared bounded toolchain"
  }
  if ($manifest.execution_profile.formal_replay_command -cne "elan run leanprover/lean4:v4.32.2 lean") {
    Throw-ReplayPacketRefusal "manifest formal replay command is not licensed"
  }
  if ($manifest.execution_profile.formal_replay_workdir -cne "coda_university/coda_research/authorization_an_incompleteness_theory/formal") {
    Throw-ReplayPacketRefusal "manifest formal replay work directory is not licensed"
  }

  $artifactPaths = Get-ManifestArtifactPaths -Manifest $manifest -RepositoryRoot $RepositoryRoot
  $declaredToolchain = [System.IO.File]::ReadAllText(
    $artifactPaths.lean_toolchain,
    [System.Text.UTF8Encoding]::new($false, $true)
  ).Trim()
  if ($declaredToolchain -cne $manifest.execution_profile.lean_toolchain) {
    Throw-ReplayPacketRefusal "Lean toolchain file does not match the declared runtime"
  }
  return [pscustomobject]@{
    valid = $true
    manifest = $manifest
    artifact_paths = [pscustomobject]$artifactPaths
  }
}

function Get-TransitionEvaluation {
  [OutputType([pscustomobject])]
  param(
    [Parameter(Mandatory)][object]$Proposal,
    [Parameter(Mandatory)][object]$Contract
  )

  Assert-ExactKeys -Object $Proposal -Expected @(
    "schema_version",
    "proposal_id",
    "authority_effect",
    "source_claimed_pass",
    "transitions"
  ) -Context "proposal"
  if ($Proposal.schema_version -cne $script:ProposalSchema) {
    Throw-ReplayPacketRefusal "proposal schema version is not supported"
  }
  if ($Proposal.proposal_id -cne "finite-transition-table-v1") {
    Throw-ReplayPacketRefusal "proposal identifier is not licensed"
  }
  if ($Proposal.authority_effect -cne "None") {
    Throw-ReplayPacketRefusal "proposal must declare AuthorityEffect None"
  }
  if ($Proposal.source_claimed_pass -isnot [bool]) {
    Throw-ReplayPacketRefusal "proposal source_claimed_pass must be Boolean"
  }
  if ($Proposal.transitions -is [string] -or $null -eq $Proposal.transitions) {
    Throw-ReplayPacketRefusal "proposal transitions must be an array"
  }

  $configurations = @(
    "runningBlank",
    "runningMarked",
    "haltedBlank",
    "haltedMarked"
  )
  $outcomes = @("advance", "stay", "halt")
  $transitions = @($Proposal.transitions)
  if ($transitions.Count -ne $configurations.Count) {
    Throw-ReplayPacketRefusal "proposal does not contain one transition for every configuration"
  }

  $table = @{}
  foreach ($row in $transitions) {
    Assert-ExactKeys -Object $row -Expected @("from", "outcome", "to") -Context "transition row"
    foreach ($field in @("from", "outcome", "to")) {
      Assert-NonEmptyString -Value $row.$field -Context "transition $field"
    }
    if ($row.from -cnotin $configurations -or $row.to -cnotin $configurations) {
      Throw-ReplayPacketRefusal "transition configuration is outside the declared carrier"
    }
    if ($row.outcome -cnotin $outcomes) {
      Throw-ReplayPacketRefusal "transition outcome is outside the declared carrier"
    }
    if ($table.ContainsKey($row.from)) {
      Throw-ReplayPacketRefusal "proposal contains a duplicate transition source"
    }
    $table[$row.from] = $row
  }
  foreach ($configuration in $configurations) {
    if (-not $table.ContainsKey($configuration)) {
      Throw-ReplayPacketRefusal "proposal omits transition source $configuration"
    }
  }

  Assert-ExactKeys -Object $Contract -Expected @(
    "schema_version",
    "contract_id",
    "authority_effect",
    "clean_terminal_rejects",
    "marked_cell_accepts",
    "reports",
    "expected"
  ) -Context "contract"
  if ($Contract.schema_version -cne $script:ContractSchema) {
    Throw-ReplayPacketRefusal "contract schema version is not supported"
  }
  if ($Contract.contract_id -cne "finite-transition-adequacy-v1") {
    Throw-ReplayPacketRefusal "contract identifier is not licensed"
  }
  if ($Contract.authority_effect -cne "None") {
    Throw-ReplayPacketRefusal "contract must declare AuthorityEffect None"
  }
  Assert-ExactStringSet -Value $Contract.clean_terminal_rejects -Expected @("haltedMarked") -Context "contract clean_terminal_rejects"
  Assert-ExactStringSet -Value $Contract.marked_cell_accepts -Expected @("runningMarked", "haltedMarked") -Context "contract marked_cell_accepts"
  Assert-ExactKeys -Object $Contract.reports -Expected @("full_report", "control_only_report") -Context "contract reports"
  if ($Contract.reports.full_report -cne "configuration" -or $Contract.reports.control_only_report -cne "transition_control") {
    Throw-ReplayPacketRefusal "contract report interfaces are not the declared pair"
  }
  Assert-ExactKeys -Object $Contract.expected -Expected @(
    "clean_terminal_preserved",
    "required_marked_countertrace",
    "full_report_adequate",
    "control_only_report_adequate",
    "control_only_authorization"
  ) -Context "contract expected results"
  foreach ($field in @(
      "clean_terminal_preserved",
      "full_report_adequate",
      "control_only_report_adequate"
    )) {
    if ($Contract.expected.$field -isnot [bool]) {
      Throw-ReplayPacketRefusal "contract expected $field must be Boolean"
    }
  }
  if ($Contract.expected.required_marked_countertrace -isnot [string] -or
      $Contract.expected.required_marked_countertrace -cne "runningMarked") {
    Throw-ReplayPacketRefusal "contract expected required_marked_countertrace is not licensed"
  }
  if ($Contract.expected.control_only_authorization -isnot [string] -or
      $Contract.expected.control_only_authorization -cne "open_due_to_inadequate_report") {
    Throw-ReplayPacketRefusal "contract expected control_only_authorization is not licensed"
  }

  $cleanRejects = @($Contract.clean_terminal_rejects)
  $markedAccepts = @($Contract.marked_cell_accepts)
  $cleanTerminalPreserved = $true
  $markedCountertraces = [System.Collections.Generic.List[object]]::new()
  foreach ($configuration in $configurations) {
    $successor = $table[$configuration].to
    if ($successor -cin $cleanRejects) {
      $cleanTerminalPreserved = $false
    }
    if ($configuration -cin $markedAccepts -and $successor -cnotin $markedAccepts) {
      $markedCountertraces.Add([pscustomobject]@{
        source = $configuration
        successor = $successor
      })
    }
  }

  $groups = @{}
  foreach ($configuration in $configurations) {
    $report = $table[$configuration].outcome
    if (-not $groups.ContainsKey($report)) {
      $groups[$report] = [System.Collections.Generic.List[string]]::new()
    }
    $groups[$report].Add($configuration)
  }

  $controlCounterexample = $null
  foreach ($report in $groups.Keys) {
    $group = @($groups[$report])
    for ($leftIndex = 0; $leftIndex -lt $group.Count; $leftIndex += 1) {
      for ($rightIndex = $leftIndex + 1; $rightIndex -lt $group.Count; $rightIndex += 1) {
        $left = $group[$leftIndex]
        $right = $group[$rightIndex]
        if (($left -cin $markedAccepts) -ne ($right -cin $markedAccepts)) {
          $controlCounterexample = [pscustomobject]@{
            report = $report
            first = $left
            second = $right
          }
          break
        }
      }
      if ($null -ne $controlCounterexample) {
        break
      }
    }
    if ($null -ne $controlCounterexample) {
      break
    }
  }

  $controlOnlyAdequate = ($null -eq $controlCounterexample)
  $controlOnlyAuthorization = if ($controlOnlyAdequate) {
    "eligible_for_scoped_decision"
  } else {
    "open_due_to_inadequate_report"
  }

  $evaluation = [pscustomobject]@{
    clean_terminal_preserved = $cleanTerminalPreserved
    marked_countertraces = @($markedCountertraces)
    full_report_adequate = $true
    control_only_report_adequate = $controlOnlyAdequate
    control_only_counterexample = $controlCounterexample
    control_only_authorization = $controlOnlyAuthorization
    source_claimed_pass_used = $false
  }

  if ($evaluation.clean_terminal_preserved -ne $Contract.expected.clean_terminal_preserved) {
    Throw-ReplayPacketRefusal "evaluator disagrees with the declared clean-terminal result"
  }
  if ($evaluation.full_report_adequate -ne $Contract.expected.full_report_adequate) {
    Throw-ReplayPacketRefusal "evaluator disagrees with the declared full-report adequacy result"
  }
  if ($evaluation.control_only_report_adequate -ne $Contract.expected.control_only_report_adequate) {
    Throw-ReplayPacketRefusal "evaluator disagrees with the declared control-only adequacy result"
  }
  if ($evaluation.control_only_authorization -cne $Contract.expected.control_only_authorization) {
    Throw-ReplayPacketRefusal "evaluator disagrees with the declared control-only authorization route"
  }
  if (@($evaluation.marked_countertraces.source) -cnotcontains $Contract.expected.required_marked_countertrace) {
    Throw-ReplayPacketRefusal "evaluator did not find the required marked-cell countertrace"
  }

  return $evaluation
}

function Invoke-ReplayPacket {
  [OutputType([pscustomobject])]
  param(
    [Parameter(Mandatory)][string]$RepositoryRoot,
    [string]$ManifestPath = "coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/packet_manifest.json"
  )

  $packet = Test-ReplayPacket -RepositoryRoot $RepositoryRoot -ManifestPath $ManifestPath
  $proposal = Read-ReplayPacketJson -Path $packet.artifact_paths.proposal -Context "proposal"
  $contract = Read-ReplayPacketJson -Path $packet.artifact_paths.contract -Context "contract"
  $policy = Read-ReplayPacketJson -Path $packet.artifact_paths.terminal_policy -Context "terminal policy"
  Assert-ExactKeys -Object $policy -Expected @(
    "schema_version",
    "policy_id",
    "authority_effect",
    "on_verified",
    "on_rejected"
  ) -Context "terminal policy"
  if ($policy.schema_version -cne $script:PolicySchema -or
      $policy.policy_id -cne "leave-verified-open-v1" -or
      $policy.authority_effect -cne "None" -or
      $policy.on_verified -cne "open" -or
      $policy.on_rejected -cne "rejected") {
    Throw-ReplayPacketRefusal "terminal policy is not the declared bounded open policy"
  }

  $evaluation = Get-TransitionEvaluation -Proposal $proposal -Contract $contract
  return [pscustomobject]@{
    schema_version = $script:PacketSchema
    packet_id = $packet.manifest.packet_id
    authority_effect = "None"
    verification_status = "verified"
    terminal = $policy.on_verified
    source_claimed_pass = $proposal.source_claimed_pass
    source_claimed_pass_used = $evaluation.source_claimed_pass_used
    evaluation = $evaluation
  }
}

Export-ModuleMember -Function Test-ReplayPacket, Invoke-ReplayPacket
