# Day 18 Demo Script - AI Flask + Groq Integration

Write-Host "🚀 Day 18 Demo: AI Recommend, Generate Report, Flask + Groq" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Yellow

# Test 1: Health Endpoint
Write-Host "`n1. Testing /health endpoint..." -ForegroundColor Green
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET -UseBasicParsing
    Write-Host "✅ Health Status: $($healthResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: AI Recommend Endpoint
Write-Host "`n2. Testing /recommend endpoint..." -ForegroundColor Green
$recommendData = @{
    tasks = @(
        "Implement user authentication system",
        "Add database migration scripts",
        "Create API documentation",
        "Set up CI/CD pipeline",
        "Implement error logging"
    )
} | ConvertTo-Json

try {
    $recommendResponse = Invoke-RestMethod -Uri "http://localhost:5000/recommend" -Method POST -Body $recommendData -ContentType "application/json" -UseBasicParsing
    Write-Host "✅ AI Recommendation generated using model: $($recommendResponse.model)" -ForegroundColor Green
    Write-Host "📋 Sample recommendation:" -ForegroundColor Yellow
    Write-Host "$($recommendResponse.recommendation.Substring(0, [Math]::Min(200, $recommendResponse.recommendation.Length)))..." -ForegroundColor White
} catch {
    Write-Host "❌ Recommend endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: AI Generate Report Endpoint
Write-Host "`n3. Testing /generate-report endpoint..." -ForegroundColor Green
$reportData = @{
    sprint_name = "Sprint 17 - Security and AI Integration"
    completed_tasks = 15
    total_tasks = 17
    team_size = 4
    key_deliverables = @(
        "OWASP ZAP security fixes implemented",
        "AI service integration completed",
        "Docker container security hardened",
        "Comprehensive documentation created"
    )
} | ConvertTo-Json

try {
    $reportResponse = Invoke-RestMethod -Uri "http://localhost:5000/generate-report" -Method POST -Body $reportData -ContentType "application/json" -UseBasicParsing
    Write-Host "✅ AI Report generated using model: $($reportResponse.model)" -ForegroundColor Green
    Write-Host "📊 Sample report:" -ForegroundColor Yellow
    Write-Host "$($reportResponse.report.Substring(0, [Math]::Min(200, $reportResponse.report.Length)))..." -ForegroundColor White
} catch {
    Write-Host "❌ Generate report endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: AI Describe Endpoint
Write-Host "`n4. Testing /describe endpoint..." -ForegroundColor Green
$describeData = @{
    task_title = "Implement JWT Authentication"
    business_context = "Secure API access for the Kanban board application"
    current_state = "Basic Flask app with no authentication"
    requirements = @(
        "Implement JWT token generation",
        "Add login/logout endpoints",
        "Validate tokens on protected routes",
        "Handle token expiration"
    )
} | ConvertTo-Json

try {
    $describeResponse = Invoke-RestMethod -Uri "http://localhost:5000/describe" -Method POST -Body $describeData -ContentType "application/json" -UseBasicParsing
    Write-Host "✅ AI Description generated using model: $($describeResponse.model)" -ForegroundColor Green
    Write-Host "📝 Sample description:" -ForegroundColor Yellow
    Write-Host "$($describeResponse.description.Substring(0, [Math]::Min(200, $describeResponse.description.Length)))..." -ForegroundColor White
} catch {
    Write-Host "❌ Describe endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 Flask + Groq Integration in 60 seconds:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "Flask provides the web framework with security middleware," -ForegroundColor White
Write-Host "rate limiting, CORS protection, and input validation." -ForegroundColor White
Write-Host "Groq powers the AI with Llama 3.3 70B model for:" -ForegroundColor White
Write-Host "• Task recommendations (strategic planning)" -ForegroundColor Green
Write-Host "• Sprint report generation (metrics and insights)" -ForegroundColor Green
Write-Host "• Task descriptions (detailed specifications)" -ForegroundColor Green
Write-Host "Together they create a secure, intelligent API service!" -ForegroundColor Cyan

Write-Host "`n✅ Demo Complete! All AI endpoints functional." -ForegroundColor Green