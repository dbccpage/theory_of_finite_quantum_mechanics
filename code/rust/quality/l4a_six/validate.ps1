param([Parameter(Mandatory = $true)][string]$ReceiptDirectory)
$ErrorActionPreference = 'Stop'
$reviewRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$receiptRoot = [IO.Path]::GetFullPath((Join-Path $reviewRoot $ReceiptDirectory))
$schemaText = [IO.File]::ReadAllText((Join-Path $reviewRoot 'SCORING.md'))
$schemaMatch = [regex]::Match($schemaText, '```json\s*(?<body>[\s\S]*?)```')
if (-not $schemaMatch.Success) { throw 'Cannot locate the canonical JSON schema' }
$reviewSchema = $schemaMatch.Groups['body'].Value.Trim()
$contractSchemaPath = Join-Path $PSScriptRoot 'contract.schema.json'
$contractSchema = [IO.File]::ReadAllText($contractSchemaPath)
$sidecarManifest = Get-Content -LiteralPath (Join-Path $receiptRoot 'sidecars.json') -Raw | ConvertFrom-Json
$hashCache = @{}
function Get-ReviewHash([string]$Path) {
    if (-not $hashCache.ContainsKey($Path)) {
        $hashCache[$Path] = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    return $hashCache[$Path]
}
function Read-ReviewYamlJson([string]$Path) {
    $text = [IO.File]::ReadAllText($Path)
    if (-not $text.StartsWith('# YAML 1.2 (JSON syntax). AuthorityEffect: None.')) {
        throw "Unexpected sidecar encoding: $Path"
    }
    return $text.Substring($text.IndexOf("`n") + 1)
}
$reviewGrades = @('E', 'D', 'C', 'B', 'A', 'A+')
$reviewCount = 0
$contractCount = 0
$knownE = @()
$openCount = 0
foreach ($entry in $sidecarManifest.sidecars) {
    $path = Join-Path $reviewRoot $entry.path
    if ((Get-ReviewHash $path) -ne $entry.sha256) { throw "Sidecar digest mismatch: $($entry.path)" }
    $json = Read-ReviewYamlJson $path
    $value = $json | ConvertFrom-Json
    $subject = Join-Path $reviewRoot $value.artifact.path
    if ((Get-ReviewHash $subject) -ne $value.artifact.sha256) { throw "Stale subject: $subject" }
    foreach ($reference in $value.evidence) {
        if ((Get-ReviewHash (Join-Path $reviewRoot $reference.path)) -ne $reference.sha256) {
            throw "Evidence digest mismatch: $($reference.path)"
        }
    }
    if ($entry.path.EndsWith('.contract.yaml')) {
        if (-not (Test-Json -Json $json -Schema $contractSchema)) { throw "Contract schema refusal: $($entry.path)" }
        $gateIds = @($value.requirements | ForEach-Object { $_.id } | Sort-Object)
        if (($gateIds -join ',') -ne 'G1,G2,G3,G4,G5') { throw "Missing or duplicate contract gate: $path" }
        $contractCount++
        continue
    }
    if (-not (Test-Json -Json $json -Schema $reviewSchema)) { throw "Schema refusal: $($entry.path)" }
    $gateValues = @('G1', 'G2', 'G3', 'G4', 'G5') | ForEach-Object { $value.gates.$_ }
    $complete = @($gateValues | Where-Object { $null -eq $_ }).Count -eq 0
    if ($complete -ne $value.is_complete) { throw "Completeness mismatch: $path" }
    if ($complete) {
        $minimum = ($gateValues | Sort-Object { [array]::IndexOf($reviewGrades, $_) })[0]
        if ($value.composite_grade -ne $minimum -or $value.score_token -ne ($value.level + $minimum)) {
            throw "Five-gate minimum mismatch: $path"
        }
    } elseif ($gateValues -contains 'E') {
        # SCORING.md 1.4 / scenario 4 preserves a demonstrated E even when incomplete.
        if ($value.composite_grade -ne 'E' -or $value.score_token -ne ($value.level + 'E')) {
            throw "Known E was hidden: $path"
        }
        $knownE += $value.artifact.path
    } elseif ($null -ne $value.composite_grade -or $null -ne $value.score_token) {
        throw "Incomplete assessment emitted a completed score: $path"
    }
    if (-not $complete) { $openCount++ }
    $contract = Join-Path $reviewRoot $value.contract.path
    if ((Get-ReviewHash $contract) -ne $value.contract.sha256) { throw "Contract digest mismatch: $path" }
    $mutation = $value.mutation_accounting
    $eligible = $mutation.killed + $mutation.survived + $mutation.inconclusive + $mutation.unrun
    if ($eligible -eq 0) {
        if ($null -ne $mutation.conservative_ratio) { throw "Empty mutation denominator: $path" }
    } elseif ($mutation.conservative_ratio -ne ($mutation.killed / $eligible)) {
        throw "Mutation ratio mismatch: $path"
    }
    $reviewCount++
}
$output = [ordered]@{
    AuthorityEffect = 'None'
    tool = 'PowerShell Test-Json against SCORING.md Draft 2020-12 schema plus independent custody/grade checks'
    powershell_version = $PSVersionTable.PSVersion.ToString()
    module_version = (Get-Command Test-Json).Version.ToString()
    command = @($PSCommandPath, '-ReceiptDirectory', $ReceiptDirectory)
    cwd = (Get-Location).Path
    exit_code = 0
    script_sha256 = Get-ReviewHash $PSCommandPath
    schema_source_sha256 = Get-ReviewHash (Join-Path $reviewRoot 'SCORING.md')
    contract_schema_sha256 = Get-ReviewHash $contractSchemaPath
    sidecar_manifest_sha256 = Get-ReviewHash (Join-Path $receiptRoot 'sidecars.json')
    scoring_records_validated = $reviewCount
    contract_integrity_checks = $contractCount
    contract_schema_checks = $contractCount
    contract_semantics_certified = $false
    incomplete_assessments = $openCount
    known_E_subjects = $knownE
    checked_file_hashes = $hashCache
    goal_complete = $false
}
$output | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $receiptRoot 'sidecar_validation.json') -Encoding utf8NoBOM
Write-Output "Scoring schema/custody: $reviewCount passed. Contract schema/custody: $contractCount passed. $openCount assessments remain incomplete."
