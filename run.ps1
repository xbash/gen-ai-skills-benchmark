param(
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateSet("doctor", "list", "run", "analyze", "judge")]
    [string]$Command,
    [Parameter(Position = 1)]
    [string]$Experiment = "",
    [switch]$DryRun,
    [switch]$Resume,
    [ValidateRange(1, 10000)]
    [int]$Limit
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = "python"

function Invoke-PythonScript {
    param([string[]]$Arguments)

    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

switch ($Command) {
    "doctor" {
        Invoke-PythonScript @("$Root\scripts\runner.py", "doctor")
    }
    "list" {
        Invoke-PythonScript @("$Root\scripts\runner.py", "list")
    }
    "run" {
        if ([string]::IsNullOrWhiteSpace($Experiment)) {
            throw "Indica un experimento o all. Usa .\run.ps1 list para ver las opciones."
        }

        $Arguments = @("$Root\scripts\runner.py", "run", $Experiment)
        if ($DryRun) { $Arguments += "--dry-run" }
        if ($Resume) { $Arguments += "--resume" }
        if ($PSBoundParameters.ContainsKey("Limit")) {
            $Arguments += @("--limit", $Limit.ToString())
        }
        Invoke-PythonScript $Arguments
    }
    "analyze" {
        Invoke-PythonScript @("$Root\scripts\analyze.py")
    }
    "judge" {
        if ([string]::IsNullOrWhiteSpace($Experiment)) {
            throw "Indica el experimento que se debe juzgar."
        }
        Invoke-PythonScript @("$Root\scripts\judge.py", $Experiment)
    }
}
