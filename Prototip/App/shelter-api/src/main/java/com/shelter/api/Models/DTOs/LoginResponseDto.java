package com.shelter.api.Models.DTOs;

public record LoginResponseDto(Long userId, String firstName, String lastName, String email, String role, Long organizationId) {
}