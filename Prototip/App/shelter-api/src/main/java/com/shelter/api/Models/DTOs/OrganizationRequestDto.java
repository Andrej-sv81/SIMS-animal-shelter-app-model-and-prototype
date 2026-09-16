package com.shelter.api.Models.DTOs;

public record OrganizationRequestDto(
    String name,
    String description,
    String bankAccount,
    String adminFirstName,
    String adminLastName,
    String adminEmail,
    String adminPhone,
    String adminPassword
) {
}