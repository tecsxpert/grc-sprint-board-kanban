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

    public AiServiceClient() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(TIMEOUT_MS);
        factory.setReadTimeout(TIMEOUT_MS);
        this.restTemplate = new RestTemplate(factory);
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
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Object> request = new HttpEntity<>(requestBody, headers);

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
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Object> request = new HttpEntity<>(requestBody, headers);

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
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Object> request = new HttpEntity<>(requestBody, headers);

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