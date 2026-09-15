package com.shelter.api.Models.DTOs;

import java.time.LocalDateTime;

public record AdminDto(
	Long id,
	String firstName,
	String lastName,
	String email,
	String phone,
	boolean active,
	LocalDateTime joinedAt
) {
}