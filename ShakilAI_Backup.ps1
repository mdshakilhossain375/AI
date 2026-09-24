$ErrorActionPreference="Stop"

$Project="C:\Users\Md Shakil Hossain\ShakilAI"
$BackupRoot="$Project\backups"
$Stamp=Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$Dest="$BackupRoot\$Stamp"

New-Item -ItemType Directory -Force -Path $Dest | Out-Null

$Db="$Project\websites\student_management\students.db"

if(Test-Path $Db){
    Copy-Item $Db "$Dest\students.db" -Force
}

$ProjectCopy="$Dest\ShakilAI"
New-Item -ItemType Directory -Force -Path $ProjectCopy | Out-Null

Get-ChildItem $Project -Force |
Where-Object {$_.Name -ne "backups"} |
ForEach-Object {
    Copy-Item $_.FullName $ProjectCopy -Recurse -Force
}

$Backups=Get-ChildItem $BackupRoot -Directory |
Sort-Object CreationTime -Descending

if($Backups.Count -gt 14){
    $Backups |
    Select-Object -Skip 14 |
    Remove-Item -Recurse -Force
}

Write-Host "BACKUP COMPLETE: $Dest"
