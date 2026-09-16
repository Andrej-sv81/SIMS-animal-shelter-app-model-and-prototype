package com.shelter.api.Models.DTOs;

public record VolunteerRequestDto(
    String firstName,
    String lastName,
    String email,
    String phone,
    String password
) {
}
