package com.shelter.api.Models.DTOs;

public record OrganizationDto(
    Long id,
    String name,
    String description,
    String bankAccount,
    AdminDto admin
) {
}