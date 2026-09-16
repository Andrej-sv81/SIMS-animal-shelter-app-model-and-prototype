package com.shelter.api.Models.DTOs;

import java.util.List;

public record AnimalDto(
	Long id,
	String name,
	String species,
	Integer age,
	String gender,
	String healthDescription,
	String behaviorNotes,
	String status,
	String imageUrl,
	List<String> imageUrls,
	String adopter,
	Long organizationId,
	String organizationName
) {
}