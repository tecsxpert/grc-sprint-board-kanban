# Run the full Docker E2E container test for the AI service

Set-Location -LiteralPath $PSScriptRoot

docker compose up --build -d
Write-Host "Waiting for service to start..."
Start-Sleep -Seconds 15

try {
    $response = Invoke-RestMethod -Uri http://localhost:5000/health -UseBasicParsing
    Write-Host "Health check response:" $response
    Write-Host "Docker E2E container test succeeded."
} catch {
    Write-Host "Docker E2E container test failed:" $_.Exception.Message
    exit 1
} finally {
    docker compose down
}
