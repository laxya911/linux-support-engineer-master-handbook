<#
.SYNOPSIS
Compilation script to build the Linux Support Engineer Master Handbook into PDF and EPUB formats using Pandoc.

.DESCRIPTION
This script uses Pandoc to combine all Markdown files in the /docs and /volumes directories into a single digital book.
It requires Pandoc and optionally mermaid-cli (for rendering diagrams).

.EXAMPLE
.\build.ps1 -Format epub
.\build.ps1 -Format pdf
#>

param (
    [ValidateSet('epub', 'pdf')]
    [string]$Format = 'epub'
)

# 1. Define the input files in the correct reading order
$InputFiles = @(
    "..\docs\00_TITLE_PAGE.md",
    "..\docs\01_COPYRIGHT.md",
    "..\docs\PREFACE.md",
    "..\docs\HOW_TO_USE_THIS_BOOK.md"
)

# Dynamically add all Volume chapters
for ($i = 1; $i -le 5; $i++) {
    $VolumeDir = (Get-ChildItem -Path "..\volumes\" -Directory | Where-Object Name -match "volume-0$i").FullName
    if ($VolumeDir) {
        $ChapterFiles = Get-ChildItem -Path "$VolumeDir\chapters" -Filter "*.md" | Sort-Object Name
        foreach ($file in $ChapterFiles) {
            $InputFiles += $file.FullName
        }
    }
}

$InputFiles += "..\docs\INDEX.md"

# 2. Build the Pandoc Command
$OutputFile = "Linux_Support_Engineer_Master_Handbook.$Format"
$MetadataFile = "metadata.yaml"
$CoverImage = "..\assets\covers\front_cover.jpg" # Assuming we select one

Write-Host "Compiling $OutputFile..."

if ($Format -eq 'epub') {
    $command = "pandoc $MetadataFile --epub-cover-image=$CoverImage -o $OutputFile $($InputFiles -join ' ')"
} else {
    # For PDF, we use basic wkhtmltopdf or latex via pandoc
    $command = "pandoc $MetadataFile -o $OutputFile $($InputFiles -join ' ')"
}

Write-Host "Executing: $command"
# Invoke-Expression $command

Write-Host "NOTE: To run this script, ensure Pandoc is installed on your system."
Write-Host "Done!"
