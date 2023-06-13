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

    [Parameter(Mandatory = $true,
        Position = 1,
        HelpMessage = "Name for new filelist")]
    [Alias("FN")]
    [ValidateNotNullOrEmpty()]
    [string]
    $FilelistName,

    [Parameter(Mandatory = $false,
        Position = 2,
        HelpMessage = "Character for indicating punctuation")]
    [Alias("PC")]
    [ValidateNotNullOrEmpty()]
    [char]
    $PunctChar = ","
)

Write-Output $PunctChar

$filelist_items = [System.Collections.Generic.List[string]]::new()

$files = Get-ChildItem -Path $Path -File

$wav_files = $files | Where-Object { $_.Extension.ToLower() -eq ".wav" }
$txt_files = $files | Where-Object { $_.Extension.ToLower() -eq ".txt" }
foreach ($f in $wav_files) {
    $escaped_wav_name = [regex]::escape($f.BaseName)
    $matched_txt = $txt_files | Where-Object { $_.BaseName.Trim() -cmatch "^$escaped_wav_name.*$" }
    $matched_txt_count = $matched_txt | Measure-Object | ForEach-Object { $_.Count }
    if ($matched_txt_count -gt 1) {
        Write-Warning "$($f.Name): multiple transcriptions found, skipping"
        continue
    }
    
    $transcription = Get-Content -Path $matched_txt[0].FullName
    $transcription = $transcription -replace "\s+", "$PunctChar"
    if ($transcription.Length -eq 0) {
        Write-Warning "$($f.Name): transcription empty, skipping"
        continue
    }

    $filelist_items.Add("$($f.FullName)|$transcription")
}

$final_content = $filelist_items -join [System.Environment]::NewLine
Set-Content -Path $FilelistName -Value $final_content
