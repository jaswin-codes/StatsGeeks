# Export the new companion deck only. Requires desktop PowerPoint; no model execution.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$inputDeck = Join-Path $PSScriptRoot 'Coordinate-RF_Judges.pptx'
$pdf = Join-Path $PSScriptRoot 'Coordinate-RF_Judges.pdf'
$images = Join-Path $root 'reproducibility\release\slide_render'
New-Item -ItemType Directory -Force $images | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $app.Presentations.Open($inputDeck, $true, $false, $false)
    $deck.SaveAs($pdf, 32)
    $deck.Export($images, 'PNG', 1600, 900)
    $layout = @()
    foreach ($slide in $deck.Slides) {
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
                $range = $shape.TextFrame.TextRange
                if (($range.BoundTop + $range.BoundHeight) -gt ($shape.Top + $shape.Height + 3)) {
                    $layout += "Slide $($slide.SlideIndex): $($shape.Name): text exceeds shape height"
                }
            }
        }
    }
    ConvertTo-Json -InputObject @($layout) | Set-Content (Join-Path $root 'reproducibility\release\powerpoint_layout.json')
    if ($layout.Count -ne 0) { throw 'Text overflow detected; companion manifest was not updated.' }
    # Seal only the presentation companion; never rewrite the scientific-package seal.
    $names = @(
        'presentation/Coordinate-RF_Judges.pptx',
        'presentation/Coordinate-RF_Judges.pdf',
        'presentation/judge_learning_curve.png',
        'presentation/build_judge_deck.py',
        'presentation/export_judge_deck.ps1',
        'docs/judge/WRITTEN_JUSTIFICATION.md',
        'FINAL_SUBMISSION/results_summary/learning_curve.csv'
    )
    $hashes = [ordered]@{}
    foreach ($name in $names) {
        $hashes[$name] = (Get-FileHash (Join-Path $root $name) -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    $manifest = [ordered]@{
        scope = 'Presentation-only companion; repository-relative paths; original scientific seal unchanged; self excluded.'
        scientific_execution = $false
        locked_macro_f1 = '0.749299'
        files = $hashes
    }
    $manifestPath = Join-Path $root 'reproducibility\release\companion_manifest.json'
    [IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding($false)))
    Write-Output "Exported $($deck.Slides.Count) PDF pages and PNG slides; layout flags: $($layout.Count); companion seal updated"
} finally {
    if ($null -ne $deck) { $deck.Close() }
    $app.Quit()
}
