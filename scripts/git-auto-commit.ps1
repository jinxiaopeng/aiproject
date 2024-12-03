# Git Auto Commit Script
Write-Host "Git Auto Commit Script" -ForegroundColor Green

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git Version: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git not found. Please make sure Git is installed and added to PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Get current time
$datetime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    # Add all changes
    Write-Host "Adding changes..." -ForegroundColor Yellow
    git add .

    # Commit changes
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git commit -m "Auto commit: $datetime"
    if ($?) {
        Write-Host "[SUCCESS] Changes committed" -ForegroundColor Green
        
        # Try to push to remote
        Write-Host "Pushing to remote..." -ForegroundColor Yellow
        git push
        if ($?) {
            Write-Host "[SUCCESS] Changes pushed to remote" -ForegroundColor Green
        } else {
            Write-Host "[WARNING] Failed to push to remote. Please push manually" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[ERROR] Commit failed" -ForegroundColor Red
    }
} else {
    Write-Host "[INFO] No changes to commit" -ForegroundColor Blue
}

Read-Host "Press Enter to exit" 