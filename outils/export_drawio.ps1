# Exporte des fichiers .drawio en PNG, un par un (draw.io plante si plusieurs instances coexistent).
# Usage : powershell -NoProfile -File outils\export_drawio.ps1 <source.drawio> <cible.png> [<source2> <cible2> ...]
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$pairs)
$exe = "C:\Program Files\draw.io\draw.io.exe"
function Kill-Drawio { Get-Process -Name "draw.io" -ErrorAction SilentlyContinue | Stop-Process -Force -Confirm:$false -ErrorAction SilentlyContinue; Start-Sleep -Milliseconds 800 }
for ($i = 0; $i -lt $pairs.Count; $i += 2) {
    $src = $pairs[$i]; $dst = $pairs[$i + 1]
    Kill-Drawio
    $p = Start-Process -FilePath $exe -ArgumentList '-x', '-f', 'png', '-s', '2', '-b', '10', '-o', $dst, $src -PassThru -NoNewWindow
    if (-not $p.WaitForExit(60000)) { "TIMEOUT $src"; Kill-Drawio } else { "$src -> $dst (exit $($p.ExitCode))" }
    Start-Sleep -Milliseconds 500
}
Kill-Drawio
