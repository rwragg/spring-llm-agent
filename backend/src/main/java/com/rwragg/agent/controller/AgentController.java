package com.rwragg.agent.controller;

import com.rwragg.agent.client.AgentClient;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/agent")
public class AgentController {

    private final AgentClient agentClient;

    public AgentController(AgentClient agentClient) {
        this.agentClient = agentClient;
    }

    public record AskRequest(@NotBlank String prompt, String model) {}

    @PostMapping("/ask")
    public Map<String, Object> ask(@Valid @RequestBody AskRequest request) {
        return agentClient.ask(request.prompt(), request.model());
    }
}