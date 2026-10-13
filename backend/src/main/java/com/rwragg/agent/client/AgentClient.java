package com.rwragg.agent.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Component
public class AgentClient {

    private final RestTemplate restTemplate;
    private final String agentUrl;

    public AgentClient(RestTemplate restTemplate,
                       @Value("${agent.url:http://localhost:8000}") String agentUrl) {
        this.restTemplate = restTemplate;
        this.agentUrl = agentUrl;
    }

    public Map<String, Object> ask(String prompt, String model) {
        Map<String, String> body = Map.of(
                "prompt", prompt == null ? "" : prompt,
                "model", model == null ? "llama3.2" : model
        );
        return restTemplate.postForObject(agentUrl + "/agent/ask", body, Map.class);
    }
}