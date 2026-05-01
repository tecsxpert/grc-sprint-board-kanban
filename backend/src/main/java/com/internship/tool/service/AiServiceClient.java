package com.internship.tool.service;

import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import org.springframework.http.client.SimpleClientHttpRequestFactory;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;

    // AI service base URL
    private static final String AI_BASE_URL = "http://localhost:5000";
    private static final int TIMEOUT_MS = 10000; // 10 seconds
    
    // ===== CRITICAL FIX CRT-002: Authentication =====
    private static final String AI_SERVICE_API_KEY = System.getenv("AI_SERVICE_API_KEY");
    private static final String AUTH_HEADER_KEY = "X-API-Key";

    public AiServiceClient() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(TIMEOUT_MS);
        factory.setReadTimeout(TIMEOUT_MS);
        this.restTemplate = new RestTemplate(factory);
    }

    /**
     * Create headers with authentication (CRT-002 fix)
     */
    private HttpHeaders createAuthenticatedHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        // Add API key authentication
        if (AI_SERVICE_API_KEY != null && !AI_SERVICE_API_KEY.isEmpty()) {
            headers.set(AUTH_HEADER_KEY, AI_SERVICE_API_KEY);
        }
        
        return headers;
    }

    // ===========================
    // Health Check
    // ===========================
    public String healthCheck() {
        try {
            String url = AI_BASE_URL + "/health";
            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    HttpEntity.EMPTY,
                    String.class
            );
            return response.getBody();
        } catch (RestClientException e) {
            System.err.println("AI health check error: " + e.getMessage());
            return null;
        }
    }

    // ===========================
    // Generate Report
    // ===========================
    public String generateReport(Object requestBody) {
        try {
            String url = AI_BASE_URL + "/generate-report";
            HttpEntity<Object> request = new HttpEntity<>(requestBody, createAuthenticatedHeaders());

            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    String.class
            );
            return response.getBody();

        } catch (RestClientException e) {
            System.err.println("AI generateReport error: " + e.getMessage());
            return null;
        }
    }

    // ===========================
    // Recommend Tasks
    // ===========================
    public String getRecommendations(Object requestBody) {
        try {
            String url = AI_BASE_URL + "/recommend";
            HttpEntity<Object> request = new HttpEntity<>(requestBody, createAuthenticatedHeaders());

            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    String.class
            );
            return response.getBody();

        } catch (RestClientException e) {
            System.err.println("AI recommend error: " + e.getMessage());
            return null;
        }
    }

    // ===========================
    // Describe Task
    // ===========================
    public String describeTask(Object requestBody) {
        try {
            String url = AI_BASE_URL + "/describe";
            HttpEntity<Object> request = new HttpEntity<>(requestBody, createAuthenticatedHeaders());

            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    String.class
            );
            return response.getBody();

        } catch (RestClientException e) {
            System.err.println("AI describe error: " + e.getMessage());
            return null;
        }
    }

    // ===========================
    // Test Endpoint
    // ===========================
    public String testConnection() {
        try {
            String url = AI_BASE_URL + "/test";
            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    HttpEntity.EMPTY,
                    String.class
            );
            return response.getBody();

        } catch (RestClientException e) {
            System.err.println("AI test connection error: " + e.getMessage());
            return null;
        }
    }
}