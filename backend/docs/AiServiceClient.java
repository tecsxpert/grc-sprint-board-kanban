/*
 * Reference integration helper for the Spring backend.
 *
 * Endpoints:
 * POST /describe
 * Request: {"task_title":"Build auth API","business_context":"Sprint board","requirements":["JSON"]}
 * Response: {"success":true,"data":{"description":{"content":"..."}},"message":"AI response generated"}
 *
 * POST /recommend
 * Request: {"tasks":["Fix bug","Write tests"],"sprint_goal":"Demo ready","team_capacity":4}
 * Response: {"success":true,"data":{"recommendation":{"content":"..."}},"message":"AI response generated"}
 *
 * POST /generate-report
 * Request: {"sprint_name":"Sprint 20","completed_tasks":18,"total_tasks":20}
 * Response: {"success":true,"data":{"report":{"content":"..."}},"message":"AI response generated"}
 *
 * Timeout expectation: set connect timeout to 3 seconds and read timeout to 30 seconds.
 * Error handling: treat 400 as validation failure, 429 as retry-after/backoff, 503 as AI fallback.
 */
public final class AiServiceClient {
    private final java.net.http.HttpClient httpClient;
    private final String baseUrl;

    public AiServiceClient(String baseUrl) {
        this.baseUrl = baseUrl;
        this.httpClient = java.net.http.HttpClient.newBuilder()
                .connectTimeout(java.time.Duration.ofSeconds(3))
                .build();
    }

    public String post(String path, String jsonBody) throws java.io.IOException, InterruptedException {
        java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
                .uri(java.net.URI.create(baseUrl + path))
                .timeout(java.time.Duration.ofSeconds(30))
                .header("Content-Type", "application/json")
                .POST(java.net.http.HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        java.net.http.HttpResponse<String> response = httpClient.send(
                request,
                java.net.http.HttpResponse.BodyHandlers.ofString()
        );

        if (response.statusCode() >= 500) {
            throw new java.io.IOException("AI service unavailable: " + response.statusCode());
        }
        return response.body();
    }
}
