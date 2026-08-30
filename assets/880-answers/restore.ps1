# 把 part.* 分卷还原成原始 PDF（放回 302math 项目根目录）并校验 sha256。
# Windows 用法：在本目录右键「使用 PowerShell 运行」，或
#   powershell -ExecutionPolicy Bypass -File .\restore.ps1
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$parts = Get-ChildItem -Filter 'part.*' | Sort-Object Name
if ($parts.Count -eq 0) {
    Write-Host '✗ 当前目录没有 part.* 分卷，确认已完整 clone/pull' -ForegroundColor Red
    exit 1
}

$projectRoot = (Resolve-Path '..\..').Path
$out = Join-Path $projectRoot '【PDF】27版880参考答案(1).pdf'

$fs = [System.IO.File]::Create($out)
try {
    foreach ($p in $parts) {
        $bytes = [System.IO.File]::ReadAllBytes($p.FullName)
        $fs.Write($bytes, 0, $bytes.Length)
    }
} finally {
    $fs.Close()
}
Write-Host "已还原：$out"

$expected = ((Get-Content 'SHA256SUMS.txt' -Raw) -split '\s+')[0].Trim().ToLower()
$actual = (Get-FileHash $out -Algorithm SHA256).Hash.ToLower()
if ($expected -eq $actual) {
    Write-Host '✓ sha256 校验通过，与服务器上的原件完全一致' -ForegroundColor Green
} else {
    Write-Host "✗ sha256 不一致（期望 $expected，实际 $actual），分卷可能不完整" -ForegroundColor Red
    exit 1
}
