$ErrorActionPreference="Stop"

$Project="C:\Users\Md Shakil Hossain\ShakilAI"
$Source="$Project\backups"

# 1. Create local backup
& "$Project\ShakilAI_Backup.ps1"

# 2. External drive
$USB="E:\ShakilAI_Backups"

if(Test-Path "E:\"){
    New-Item -ItemType Directory -Force -Path $USB | Out-Null
    Copy-Item "$Source\*" "$USB\" -Recurse -Force
    Write-Host "USB backup updated."
}
else{
    Write-Warning "E: drive is not connected."
}

# 3. Google Drive
$Google="C:\Users\Md Shakil Hossain\Google Drive\My Drive\ShakilAI_Backups"

if(Test-Path "C:\Users\Md Shakil Hossain\Google Drive"){
    New-Item -ItemType Directory -Force -Path $Google | Out-Null
    Copy-Item "$Source\*" "$Google\" -Recurse -Force
    Write-Host "Google Drive backup updated."
}
else{
    Write-Warning "Google Drive is not available."
}

Write-Host "================================"
Write-Host "ALL BACKUPS COMPLETE"
Write-Host "================================"
