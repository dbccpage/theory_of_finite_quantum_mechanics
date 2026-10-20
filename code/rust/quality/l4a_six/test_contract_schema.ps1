param([string]$Contract = 'code/rust/src/homology/exact_scalar.rs.contract.yaml')
$ErrorActionPreference = 'Stop'
$schemaPath = Join-Path $PSScriptRoot 'contract.schema.json'
$schema = [IO.File]::ReadAllText($schemaPath)
$source = [IO.File]::ReadAllText((Join-Path (Get-Location) $Contract))
$json = $source.Substring($source.IndexOf("`n") + 1)
if (-not (Test-Json -Json $json -Schema $schema)) { throw 'Positive contract control refused' }
$cases = @(
    @{ id = 'authority'; mutate = { param($v) $v.AuthorityEffect = 'Promote' } },
    @{ id = 'digest'; mutate = { param($v) $v.artifact.sha256 = 'not-a-digest' } },
    @{ id = 'outside-scope'; mutate = { param($v) $v.artifact.path = 'other/source.rs' } },
    @{ id = 'missing-gate'; mutate = { param($v) $v.requirements = @($v.requirements[0..3]) } },
    @{ id = 'duplicate-gate'; mutate = { param($v) $v.requirements[4].id = 'G4' } },
    @{ id = 'wrong-boolean'; mutate = { param($v) $v.compilation.disabled_by_cfg_any = 'false' } },
    @{ id = 'missing-resource-boundary'; mutate = { param($v) $v.Remove('resource_boundary') } },
    @{ id = 'empty-evidence'; mutate = { param($v) $v.evidence = @() } },
    @{ id = 'unknown-field'; mutate = { param($v) $v['unreviewed_promotion'] = $true } }
)
$results = @()
foreach ($case in $cases) {
    $candidate = $json | ConvertFrom-Json -AsHashtable
    $null = & $case.mutate $candidate
    $encoded = $candidate | ConvertTo-Json -Depth 100
    $accepted = Test-Json -Json $encoded -Schema $schema -ErrorAction SilentlyContinue
    if ($accepted) { throw "Schema accepted malformed control: $($case.id)" }
    $results += @{ id = $case.id; rejected = $true }
}
[ordered]@{
    AuthorityEffect = 'None'
    scope = 'Schema sensitivity only; no source custody or semantic grade is inferred.'
    positive_control = $Contract
    positive_accepted = $true
    rejected_controls = $results
    schema_sha256 = (Get-FileHash -LiteralPath $schemaPath -Algorithm SHA256).Hash.ToLowerInvariant()
    script_sha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
} | ConvertTo-Json -Depth 10
