$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$TargetPath = Join-Path $ProjectRoot "start_desktop_app.bat"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Office-AI-OS.lnk"

if (-not (Test-Path $TargetPath)) {
    throw "没有找到启动脚本：$TargetPath"
}

$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "Office-AI-OS 桌面办公助手"
$Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,167"
$Shortcut.Save()

Write-Host "已创建桌面图标：$ShortcutPath"
