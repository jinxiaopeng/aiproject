# Git Auto Commit Script
Write-Host "Git Auto Commit Script - Auto Mode" -ForegroundColor Green

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git Version: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git not found. Please make sure Git is installed and added to PATH" -ForegroundColor Red
    exit 1
}

# Function to perform git operations
function Perform-GitOperations {
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
                Write-Host "[WARNING] Failed to push to remote" -ForegroundColor Yellow
            }
        } else {
            Write-Host "[ERROR] Commit failed" -ForegroundColor Red
        }
    } else {
        Write-Host "[INFO] No changes to commit" -ForegroundColor Blue
    }
}

# Main loop
Write-Host "Auto commit will run every 10 minutes. Press Ctrl+C to stop." -ForegroundColor Cyan
while ($true) {
    $currentTime = Get-Date -Format "HH:mm:ss"
    Write-Host "`nChecking for changes at $currentTime..." -ForegroundColor Cyan
    
    Perform-GitOperations
    
    Write-Host "Waiting for next check in 10 minutes..." -ForegroundColor Cyan
    Start-Sleep -Seconds 600
} 