# Read original receipt-addressed records after their physical files were merged.
function Get-ContractScoreText([string]$Path) {
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        return [IO.File]::ReadAllText($Path)
    }
    $reader = Join-Path $PSScriptRoot 'contract_scores.py'
    $lines = & py -3 $reader read $Path
    if ($LASTEXITCODE -ne 0) { throw "Cannot resolve contract/score record: $Path" }
    return ($lines -join "`n")
}

function Get-ContractScoreHash([string]$Path) {
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    $reader = Join-Path $PSScriptRoot 'contract_scores.py'
    $value = & py -3 $reader hash $Path
    if ($LASTEXITCODE -ne 0) { throw "Cannot hash contract/score record: $Path" }
    return $value.Trim()
}
