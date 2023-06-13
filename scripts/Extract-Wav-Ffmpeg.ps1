param (
    [Parameter(Mandatory = $true,
        Position = 0,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true,
        HelpMessage = "Working path")]
    [Alias("PSPath")]
    [ValidateNotNullOrEmpty()]
    [string]
    $Path,

    [Parameter(Position = 1,
        HelpMessage = "Show operations without actually running")]
    [switch]
    $WhatIf
)

$files = Get-ChildItem -Path $Path -File
foreach ($f in $files) {
    $out_path = "$Path\$($f.BaseName).wav"

    if ($WhatIf) {
        Write-Output "ffmpeg.exe -i $($f.FullName) -vn $out_path"
    } else {
        ffmpeg.exe -i $($f.FullName) -vn $out_path
    }
}