# ============================================================
# CARACTERIZAR - Update Manager
# Version detection + menu (Latest / Specific Tag / Exit)
# ============================================================

# --- Configuration ---
$basePath    = "$env:USERPROFILE\Documents\GITHUB\Python"
$projectPath = "$env:USERPROFILE\Documents\GITHUB\Python\Caracterizar"
$repoUrl     = "https://github.com/SergiCNM/caracterizar.git"
$branchName  = "main"

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "        CARACTERIZAR UPDATE MANAGER" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# Detect installed version
# ============================================================
$installedVersion = "Not installed"

if (Test-Path "$projectPath\.git") {

    try {
        Set-Location $projectPath

        # Check if current commit matches an exact tag
        $exactTag = git describe --tags --exact-match 2>$null

        if ($exactTag) {
            $installedVersion = $exactTag
        }
        else {
            $branch = git rev-parse --abbrev-ref HEAD 2>$null
            $commit = git rev-parse --short HEAD 2>$null

            if ($branch -eq "HEAD") {
                $installedVersion = "Detached HEAD ($commit)"
            }
            elseif ($branch) {
                $installedVersion = "$branch ($commit)"
            }
        }
    }
    catch {
        $installedVersion = "Installed (version unknown)"
    }
}

Write-Host "Installed version on this machine:" -ForegroundColor Yellow
Write-Host "  $installedVersion" -ForegroundColor Green
Write-Host ""

# ============================================================
# IMPORTANT NOTICE
# ============================================================
Write-Host "IMPORTANT NOTICE" -ForegroundColor Yellow
Write-Host "----------------" -ForegroundColor Yellow
Write-Host "During the update process, the following folders and files will be preserved:" -ForegroundColor Cyan
Write-Host "  - results/" -ForegroundColor Cyan
Write-Host "  - venv/, .venv/, DeepDetection-env/" -ForegroundColor Cyan
Write-Host "  - proves/" -ForegroundColor Cyan
Write-Host "  - config/default/wafermaps/ (User modifications are backed up and restored)" -ForegroundColor Cyan
Write-Host ""
Write-Host "User-created wafermap files will NOT be deleted." -ForegroundColor Green
Write-Host "Tracked repository files MAY be updated." -ForegroundColor Green
Write-Host ""

# ============================================================
# Menu selection
# ============================================================
Write-Host "Select an option:" -ForegroundColor Cyan
Write-Host "1) Update to latest version (default)" -ForegroundColor White
Write-Host "2) Update to a specific version (tag)" -ForegroundColor White
Write-Host "3) Exit (do nothing)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter option [1/2/3] (default = 1)"

if ([string]::IsNullOrWhiteSpace($choice)) {
    $choice = "1"
}

switch ($choice) {
    "1" { Write-Host "Selected: Update to latest version" -ForegroundColor Cyan }
    "2" { Write-Host "Selected: Update to a specific version" -ForegroundColor Cyan }
    "3" {
        Write-Host ""
        Write-Host "Exit selected. No changes will be made." -ForegroundColor Yellow
        Read-Host "`nPress ENTER to close"
        exit
    }
    default {
        Write-Host "Invalid option. Using default: Latest version." -ForegroundColor Yellow
        $choice = "1"
    }
}

Write-Host ""

# ============================================================
# Create base folder if needed
# ============================================================
if (!(Test-Path $basePath)) {
    Write-Host "Creating base folder: $basePath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $basePath | Out-Null
}

# ============================================================
# Clone repository if not present or invalid
# ============================================================
if (!(Test-Path $projectPath)) {

    Write-Host "Repository not found. Cloning into $projectPath..." -ForegroundColor Yellow
    git clone $repoUrl $projectPath
}
elseif (!(Test-Path "$projectPath\.git")) {

    Write-Host "Folder exists but is NOT a Git repository." -ForegroundColor Red
    Write-Host "Deleting old folder and cloning again..." -ForegroundColor Yellow

    Remove-Item $projectPath -Recurse -Force
    git clone $repoUrl $projectPath
}

# ============================================================
# Prepare repository
# ============================================================
Write-Host "Preparing repository..." -ForegroundColor Cyan
Set-Location $projectPath

# Mark as safe directory (multi-user systems / Windows)
$gitPath = $projectPath -replace "\\", "/"
git config --global --add safe.directory $gitPath

# Warn if local changes exist
$localChanges = git status --porcelain
if ($localChanges) {
    Write-Host ""
    Write-Host "WARNING: Local changes detected!" -ForegroundColor Yellow
    Write-Host "Tracked files modified locally may be overwritten." -ForegroundColor Yellow
    Write-Host ""
}

# ============================================================
# Wafermaps Backup
# ============================================================
$wafermapsDir = "config/default/wafermaps"
$backupDir = "$env:TEMP\caracterizar_wafermaps_backup"
$hasWafermapBackups = $false

$wafermapsToBackup = git ls-files -m -o --exclude-standard "$wafermapsDir/"
if ($wafermapsToBackup) {
    Write-Host "Backing up user-modified and new wafermaps..." -ForegroundColor Cyan
    if (Test-Path $backupDir) { Remove-Item -Recurse -Force $backupDir }
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

    $prefix = "$wafermapsDir/"
    foreach ($file in $wafermapsToBackup) {
        # Check if the file is truly within the directory
        if ($file.StartsWith($prefix)) {
            $sourcePath = Join-Path $projectPath $file
            if (Test-Path $sourcePath -PathType Leaf) {
                $relativePath = $file.Substring($prefix.Length)
                $destPath = Join-Path $backupDir $relativePath
                $destDir = Split-Path $destPath
                if (!(Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
                
                Copy-Item -Path $sourcePath -Destination $destPath -Force
                Write-Host "  Backed up: $relativePath" -ForegroundColor Gray
                $hasWafermapBackups = $true
            }
        }
    }
}

# Reset tracked files
Write-Host "Resetting tracked files..." -ForegroundColor Cyan
git reset --hard

# Clean untracked files but preserve user folders and the script itself
Write-Host "Cleaning untracked files (protected folders preserved)..." -ForegroundColor Cyan
git clean -fd `
    -e results/ `
    -e venv/ `
    -e .venv/ `
    -e DeepDetection-env/ `
    -e proves/ `
    -e update_caracterizar.ps1 `
    -e update.bat

# ============================================================
# Update logic
# ============================================================
$updateSuccess = $false

if ($choice -eq "1") {

    Write-Host "Fetching latest changes from remote repository..." -ForegroundColor Cyan
    git fetch origin

    Write-Host "Switching to branch: $branchName" -ForegroundColor Cyan
    git checkout $branchName

    Write-Host "Pulling latest version..." -ForegroundColor Cyan
    git pull origin $branchName

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Updated successfully to the latest version (branch: $branchName)." -ForegroundColor Green
        $updateSuccess = $true
    } else {
        Write-Host ""
        Write-Host "ERROR: Update failed. Please check the git output above for details." -ForegroundColor Red
    }
}
elseif ($choice -eq "2") {

    Write-Host "Fetching available tags from remote repository..." -ForegroundColor Cyan
    git fetch --tags --force

    $tags = git tag --sort=-creatordate

    if (-not $tags -or $tags.Count -eq 0) {
        Write-Host "No tags found in the repository." -ForegroundColor Red
        Read-Host "`nPress ENTER to close"
        exit
    }

    Write-Host ""
    Write-Host "Available versions (tags):" -ForegroundColor Cyan

    for ($i = 0; $i -lt $tags.Count; $i++) {
        $index = $i + 1
        Write-Host "$index) $($tags[$i])" -ForegroundColor White
    }

    Write-Host ""
    $selection = Read-Host "Select tag number to install"

    if (-not ($selection -as [int])) {
        Write-Host "Invalid selection. Aborting update." -ForegroundColor Red
        Read-Host "`nPress ENTER to close"
        exit
    }

    $selectionIndex = [int]$selection - 1

    if ($selectionIndex -lt 0 -or $selectionIndex -ge $tags.Count) {
        Write-Host "Selection out of range. Aborting update." -ForegroundColor Red
        Read-Host "`nPress ENTER to close"
        exit
    }

    $selectedTag = $tags[$selectionIndex]

    Write-Host ""
    Write-Host "Switching to version: $selectedTag" -ForegroundColor Yellow

    # Checkout specific tag (detached HEAD, forced)
    git checkout "tags/$selectedTag" -f
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repository updated to version: $selectedTag" -ForegroundColor Green
        $updateSuccess = $true
    } else {
        Write-Host "ERROR: Failed to switch to version: $selectedTag" -ForegroundColor Red
    }
}

# ============================================================
# Restore Wafermaps
# ============================================================
if ($updateSuccess -and $hasWafermapBackups) {
    Write-Host ""
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "Hay mapas locales (wafermaps) que fueron guardados antes de actualizar." -ForegroundColor Yellow
    $confirm = Read-Host "Deseas restaurar tus mapas y SOBREESCRIBIR los descargados del servidor? (S/N) (default = S)"
    
    if ([string]::IsNullOrWhiteSpace($confirm) -or $confirm.ToLower() -eq 's') {
        Write-Host "Restaurando mapas locales del usuario..." -ForegroundColor Cyan
        Copy-Item -Path "$backupDir\*" -Destination (Join-Path $projectPath $wafermapsDir) -Recurse -Force
        Write-Host "Mapas restaurados con exito." -ForegroundColor Green
    } else {
        Write-Host "Mapas locales descartados. Se conserva la version descargada del servidor." -ForegroundColor Yellow
    }
}

# Limpiar backup
if (Test-Path $backupDir) {
    Remove-Item -Recurse -Force $backupDir
}

# ============================================================
# Done
# ============================================================
Write-Host ""
Write-Host "Update script finished." -ForegroundColor Green
Read-Host "`nPress ENTER to close"