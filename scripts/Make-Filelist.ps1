<#
.SYNOPSIS
    Match WAV audio files with their TXT transcriptions.

.DESCRIPTION
    This script iterates over all WAV files in given path, finding its
    TXT transcription file in the same path, whose name contains the base
    name of the WAV file as its prefix. It then produces a TXT filelist
    containing matched pairs with path to audio and content of transcription,
    separated by given delimiter.

.NOTES
    WAV files having multiple transcriptions will be skipped. Having only one
    contentless transcription will also cause the WAV file to be skipped.

    This script is licensed under an MIT license.
    Copyright (c) 2023 Rong Bao <baorong2005@126.com>

.PARAMETER Path
    Working path to find video files in.
.PARAMETER FilelistName
    Name of filelist to create.
.PARAMETER Delim
    Character used as delimiter.
.PARAMETER PunctChar
    Character substituting line breaks and spaces.
#>

<#
 # Copyright (c) 2023 Rong Bao <baorong2005@126.com>
 # 
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 # 
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 # 
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
 #>

param (
    [Parameter(Mandatory = $true,
        Position = 0,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true)]
    [Alias("PSPath")]
    [ValidateNotNullOrEmpty()]
    [string]
    $Path,

    [Parameter(Mandatory = $true, Position = 1)]
    [Alias("FN")]
    [ValidateNotNullOrEmpty()]
    [string]
    $FilelistName,

    [Parameter(Mandatory = $false, Position = 2)]
    [Alias("D")]
    [ValidateNotNullOrEmpty()]
    [char]
    $Delim = "|",

    [Parameter(Mandatory = $false, Position = 3)]
    [Alias("PC")]
    [ValidateNotNullOrEmpty()]
    [char]
    $PunctChar = ","
)

$filelist_items = [System.Collections.Generic.List[string]]::new()

$files = Get-ChildItem -Path $Path -File

$wav_files = $files | Where-Object { $_.Extension.ToLower() -eq ".wav" }
$txt_files = $files | Where-Object { $_.Extension.ToLower() -eq ".txt" }

$wav_files_count = $wav_files | Measure-Object | ForEach-Object { $_.Count }
$i = 0
Write-Progress -Activity "Processing" -Status "$i in $wav_files_count" -PercentComplete $($i / $wav_files_count * 100)

foreach ($f in $wav_files) {
    $i += 1
    $escaped_wav_name = [regex]::escape($f.BaseName)
    Write-Progress -Activity "Processing" -Status "$i in $wav_files_count" -PercentComplete $($i / $wav_files_count * 100)
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

    $filelist_items.Add("$($f.FullName)$Delim$transcription")
}

$final_content = $filelist_items -join [System.Environment]::NewLine
Set-Content -Path $FilelistName -Value $final_content
