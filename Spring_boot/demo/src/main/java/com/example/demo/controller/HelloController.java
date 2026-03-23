package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 测试控制器
 */
@RestController
public class HelloController {

    @GetMapping("/")
    public String home() {
        return "🚀 Spring Boot应用运行正常！";
    }

    @GetMapping("/hello")
    public String hello() {
        return "✅ Hello from Spring Boot!";
    }

    @GetMapping("/health")
    public String health() {
        return "🟢 系统健康状态：正常";
    }
}
