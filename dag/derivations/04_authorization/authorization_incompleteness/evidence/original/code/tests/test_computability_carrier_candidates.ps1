param(
  [string]$RepositoryRoot = (Resolve-Path (
      Join-Path $PSScriptRoot "..\..\..\..\.."
    )).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$recordRelativePath =
  "coda_university/coda_research/authorization_an_incompleteness_theory/" +
  "computability_carrier_candidates.json"

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

function Get-Record {
  param([Parameter(Mandatory)][string]$Root)

  $path = Join-Path $Root $recordRelativePath
  return [System.IO.File]::ReadAllText(
    $path,
    [System.Text.UTF8Encoding]::new($false)
  ) | ConvertFrom-Json -AsHashtable -Depth 64
}

function Copy-Record {
  param([Parameter(Mandatory)][hashtable]$Record)

  return $Record | ConvertTo-Json -Depth 64 |
    ConvertFrom-Json -AsHashtable -Depth 64
}

function Test-CarrierRecord {
  param(
    [Parameter(Mandatory)][hashtable]$Record,
    [Parameter(Mandatory)][string]$Root
  )

  $requiredTopLevel = @(
    "schema_version",
    "authority_effect",
    "admission_status",
    "required_admission_fields",
    "candidates"
  )
  if ($Record.Keys.Count -ne $requiredTopLevel.Count) {
    throw "record has an invalid top-level field set"
  }
  foreach ($key in $requiredTopLevel) {
    if (-not $Record.ContainsKey($key)) {
      throw "record is missing required top-level field $key"
    }
  }
  if ($Record.schema_version -ne "ait.computability_carrier_candidates.v1") {
    throw "record schema version is not supported"
  }
  if ($Record.authority_effect -ne "None") {
    throw "record authority effect must be None"
  }
  if ($Record.admission_status -ne "open") {
    throw "record must remain globally open"
  }

  $requiredFields = @($Record.required_admission_fields)
  if ($requiredFields.Count -ne 8) {
    throw "record must name exactly eight admission fields"
  }
  if (@($requiredFields | Sort-Object -Unique).Count -ne $requiredFields.Count) {
    throw "record admission fields must be unique"
  }

  $seenIds = [System.Collections.Generic.HashSet[string]]::new()
  foreach ($candidate in @($Record.candidates)) {
    if (-not $seenIds.Add([string]$candidate.id)) {
      throw "candidate identifiers must be unique"
    }
    if ($candidate.selected) {
      throw "record is globally open; candidate $($candidate.id) cannot be selected"
    }
    if ($candidate.admission_status -eq "admitted") {
      throw "candidate $($candidate.id) cannot be admitted while the record is open"
    }
    if ($candidate.admission_status -notin @("open", "partial")) {
      throw "candidate $($candidate.id) has an invalid admission status"
    }
    if ($candidate.fields.Keys.Count -ne $requiredFields.Count) {
      throw "candidate $($candidate.id) has an invalid admission field set"
    }

    foreach ($fieldName in $requiredFields) {
      if (-not $candidate.fields.ContainsKey($fieldName)) {
        throw "candidate $($candidate.id) is missing field $fieldName"
      }
      $field = $candidate.fields[$fieldName]
      if ($field.status -notin @("open", "partial", "closed")) {
        throw "candidate $($candidate.id) field $fieldName has an invalid status"
      }
      if ($field.status -eq "closed" -and (
          -not $field.ContainsKey("closure_basis") -or
          [string]::IsNullOrWhiteSpace([string]$field.closure_basis)
        )) {
        throw "candidate $($candidate.id) field $fieldName closed field lacks closure basis"
      }
      if ([string]::IsNullOrWhiteSpace([string]$field.ceiling)) {
        throw "candidate $($candidate.id) field $fieldName lacks a ceiling"
      }
      if (@($field.evidence).Count -eq 0) {
        throw "candidate $($candidate.id) field $fieldName lacks evidence"
      }
      foreach ($relativePath in @($field.evidence)) {
        if ([System.IO.Path]::IsPathRooted([string]$relativePath) -or
            ([string]$relativePath).Split("/") -contains "..") {
          throw "candidate $($candidate.id) field $fieldName has unsafe evidence path"
        }
        if (-not (Test-Path -LiteralPath (Join-Path $Root $relativePath))) {
          throw "candidate $($candidate.id) field $fieldName evidence is absent"
        }
      }
    }
  }

  $requiredIds = @("AIT-DTM0", "PO-022", "PO-023", "AIT-PACKET4")
  $actualIds = @($seenIds | Sort-Object)
  $expectedIds = @($requiredIds | Sort-Object)
  if (($actualIds -join ",") -ne ($expectedIds -join ",")) {
    throw "record candidate identifiers do not match the declared inventory"
  }

  $direct = @($Record.candidates | Where-Object { $_.id -eq "AIT-DTM0" })
  if ($direct.Count -ne 1) {
    throw "direct-machine candidate is not unique"
  }
  Assert-Equal -Actual $direct[0].admission_status -Expected "partial" -Label "direct candidate status"
  Assert-Equal -Actual $direct[0].fields.syntax_and_encoding.status -Expected "partial" -Label "direct syntax ceiling"
  Assert-Equal -Actual $direct[0].fields.execution_semantics.status -Expected "partial" -Label "direct execution ceiling"
  Assert-Equal -Actual $direct[0].fields.universality.status -Expected "open" -Label "direct universality ceiling"

  $po22Path = Join-Path $Root (
    "lean4/coda_research/projection_obstruction/" +
    "022_finite_presentation_calculus_for_computation/" +
    "finite_presentation_calculus_for_computation.lean"
  )
  $po23Path = Join-Path $Root (
    "lean4/coda_research/projection_obstruction/" +
    "023_halting_as_a_non_faithful_quotient/" +
    "halting_as_a_non_faithful_quotient.lean"
  )
  if ((Get-Content -Raw -LiteralPath $po22Path) -notmatch "theorem PO22_C1 : True") {
    throw "PO-022 scaffold ceiling is not present"
  }
  if ((Get-Content -Raw -LiteralPath $po23Path) -notmatch "theorem PO23_C1 : True") {
    throw "PO-023 scaffold ceiling is not present"
  }
}

$testCount = 0
$record = Get-Record -Root $RepositoryRoot
Test-CarrierRecord -Record $record -Root $RepositoryRoot
$testCount += 1

$selectedMutation = Copy-Record -Record $record
$selectedMutation.candidates[0].selected = $true
Assert-Throws -Action {
  Test-CarrierRecord -Record $selectedMutation -Root $RepositoryRoot
} -Needle "globally open" -Label "premature selection mutation"
$testCount += 1

$admittedMutation = Copy-Record -Record $record
$admittedMutation.candidates[0].admission_status = "admitted"
Assert-Throws -Action {
  Test-CarrierRecord -Record $admittedMutation -Root $RepositoryRoot
} -Needle "cannot be admitted" -Label "premature admission mutation"
$testCount += 1

$universalMutation = Copy-Record -Record $record
$universalMutation.candidates[0].fields.universality.status = "closed"
Assert-Throws -Action {
  Test-CarrierRecord -Record $universalMutation -Root $RepositoryRoot
} -Needle "closed field lacks closure basis" -Label "unsupported closure mutation"
$testCount += 1

$pathMutation = Copy-Record -Record $record
$pathMutation.candidates[0].fields.syntax_and_encoding.evidence[0] = "../outside.lean"
Assert-Throws -Action {
  Test-CarrierRecord -Record $pathMutation -Root $RepositoryRoot
} -Needle "unsafe evidence path" -Label "evidence path escape mutation"
$testCount += 1

$fieldMutation = Copy-Record -Record $record
$fieldMutation.candidates[0].fields.Remove("universality")
Assert-Throws -Action {
  Test-CarrierRecord -Record $fieldMutation -Root $RepositoryRoot
} -Needle "invalid admission field set" -Label "missing field mutation"
$testCount += 1

Write-Output (
  "Computability carrier candidate tests passed: $testCount cases; " +
  "five premature-promotion or malformed-record mutations were rejected."
)
