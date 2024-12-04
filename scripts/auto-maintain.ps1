# Set UTF-8 encoding
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Log function
function Write-Log {
    param(
        [string]$Level,
        [string]$Message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

# Initialize
Write-Log "SUCCESS" "Auto-maintenance service started"

# Main loop
while ($true) {
    try {
        Write-Log "INFO" "Starting maintenance cycle..."
        
        # Get current directory
        $projectRoot = Split-Path -Parent $PSScriptRoot
        Set-Location $projectRoot
        
        # Check if there are changes
        $status = git status --porcelain
        if ($status) {
            # Changes detected
            Write-Log "INFO" "Changes detected, preparing commit..."
            
            # Stage all changes
            git add .
            
            # Get latest commit message
            $lastMessage = git log -1 --pretty=%B
            if ($lastMessage -match "Auto-commit:") {
                # Update existing auto-commit
                $commitMessage = $lastMessage
            } else {
                # Create new auto-commit message
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                $commitMessage = "Auto-commit: Changes at $timestamp"
            }
            
            # Commit changes
            git commit -m $commitMessage
            Write-Log "SUCCESS" "Changes committed successfully"
            
            # Push changes
            git push
            Write-Log "SUCCESS" "Changes pushed to remote"
        } else {
            Write-Log "INFO" "No changes detected"
        }
    }
    catch {
        Write-Log "ERROR" "Maintenance cycle failed: $_"
    }
    
    # Wait for next cycle
    Write-Log "INFO" "Waiting 600 seconds for next maintenance cycle..."
    Start-Sleep -Seconds 600
} 