# vAIbe-OS installer (base level, Windows).
param(
  [string]$Version = "latest"
)
$ErrorActionPreference = "Stop"
$Repo = "vaibe-studio/vaibe-os"
$Dest = if ($env:VAIBE_OS_HOME) { $env:VAIBE_OS_HOME } else { "$env:LOCALAPPDATA\Programs\vaibe-os" }
New-Item -ItemType Directory -Force -Path $Dest | Out-Null

if ($Version -eq "latest") {
  $rel = Invoke-RestMethod "https://api.github.com/repos/$Repo/releases/latest"
  $Version = $rel.tag_name
}
$asset = "vaibe-os_${Version}_windows_amd64.zip"
$url = "https://github.com/$Repo/releases/download/$Version/$asset"
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP "vaibe-os-install")

Write-Host "Downloading $url"
Invoke-WebRequest $url -OutFile (Join-Path $tmp $asset)
Expand-Archive (Join-Path $tmp $asset) -DestinationPath $tmp -Force
Copy-Item (Join-Path $tmp "vaibe-os.exe") -Destination $Dest -Force

Write-Host "Installed: $Dest\vaibe-os.exe ($Version)"
Write-Host "Next: vaibe-os init ~\Projects\my-os"
