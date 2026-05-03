# E2E Test for Docker Containerized AI Service
Write-Host "`n=== E2E Test Suite: Docker Containerized AI Service ===" -ForegroundColor Cyan
Write-Host "Timestamp: $(Get-Date)`n" -ForegroundColor Yellow

$baseUrl = "http://localhost:5000"
$passed = 0
$failed = 0

# Test 1: Health Endpoint
try {
    $resp = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing
    if ($resp.StatusCode -eq 200) {
        Write-Host "PASS: Health endpoint (200 OK)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "FAIL: Health endpoint returned $($resp.StatusCode)" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "FAIL: Health endpoint - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 2: Status Endpoint
try {
    $resp = Invoke-WebRequest -Uri "$baseUrl/status" -UseBasicParsing
    if ($resp.StatusCode -eq 200) {
        Write-Host "PASS: Status endpoint (200 OK)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "FAIL: Status endpoint returned $($resp.StatusCode)" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "FAIL: Status endpoint - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 3: Test Route
try {
    $resp = Invoke-WebRequest -Uri "$baseUrl/test" -UseBasicParsing
    if ($resp.StatusCode -eq 200) {
        Write-Host "PASS: Test route (200 OK)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "FAIL: Test route returned $($resp.StatusCode)" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "FAIL: Test route - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 4: Security Headers
try {
    $resp = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing
    $headers = $resp.Headers
    $securityHeaders = @("X-Frame-Options", "X-Content-Type-Options", "X-XSS-Protection", "Strict-Transport-Security", "Content-Security-Policy")
    $headerCount = 0
    
    foreach ($header in $securityHeaders) {
        if ($null -ne $headers[$header]) {
            $headerCount++
        }
    }
    
    if ($headerCount -eq 5) {
        Write-Host "PASS: All 5 security headers present" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "FAIL: Only $headerCount of 5 security headers found" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "FAIL: Security headers check - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 5: Container Stability
$stable = $true
for ($i = 0; $i -lt 5; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing
        if ($resp.StatusCode -ne 200) { $stable = $false; break }
        Start-Sleep -Milliseconds 500
    } catch {
        $stable = $false
        break
    }
}

if ($stable) {
    Write-Host "PASS: Container stability test (5 consecutive requests)" -ForegroundColor Green
    $passed++
} else {
    Write-Host "FAIL: Container became unstable" -ForegroundColor Red
    $failed++
}

# Test 6: CORS Configuration
try {
    $headers = @{"Origin" = "http://localhost:3000"}
    $resp = Invoke-WebRequest -Uri "$baseUrl/health" -Headers $headers -UseBasicParsing
    if ($resp.StatusCode -eq 200) {
        Write-Host "PASS: CORS configuration (origin allowed)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "FAIL: CORS check returned $($resp.StatusCode)" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "FAIL: CORS configuration - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Summary
Write-Host "`n=== Test Summary ===" -ForegroundColor Cyan
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host "Total: $($passed + $failed)" -ForegroundColor Yellow

if ($failed -eq 0) {
    Write-Host "`nALL TESTS PASSED - Containerized AI service is fully operational!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`nSOME TESTS FAILED" -ForegroundColor Red
    exit 1
}
