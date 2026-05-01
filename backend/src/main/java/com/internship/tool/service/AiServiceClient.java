package com.internship.tool.service;

import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.client.SimpleClientHttpRequestFactory;

import java.util.Map;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;

    // AI service base URL
    private static final String AI_BASE_URL = "http://localhost:5000";

   public AiServiceClient() {
    SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();

    factory.setConnectTimeout(10000); // 10 seconds
    factory.setReadTimeout(10000);

    this.restTemplate = new RestTemplate(factory);
}
    }

    // -----------------------------
    // Generate Report
    // -----------------------------
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

        } catch (Exception e) {
            System.out.println(" AI generateReport error: " + e.getMessage());
            return null; // required as per task
        }
    }

    // -----------------------------
    // Recommend Tasks
    // -----------------------------
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

        } catch (Exception e) {
            System.out.println("AI recommend error: " + e.getMessage());
            return null;
        }
    }

    // -----------------------------
    // Describe Task
    // -----------------------------
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

        } catch (Exception e) {
            System.out.println("AI describe error: " + e.getMessage());
            return null;
        }
    }
}