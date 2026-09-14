package com.shelter.api.Models;

import java.util.ArrayList;
import java.util.List;
import jakarta.persistence.Entity;
import jakarta.persistence.CollectionTable;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "animals")
public class Animal {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private String name;
	private String species;
	private Integer age;
	private String gender;
	private String healthDescription;
	private String behaviorNotes;
	private String status;
	private String imageUrl;
	private String adopter;

	@ElementCollection
	@CollectionTable(name = "animal_images", joinColumns = @JoinColumn(name = "animal_id"))
	private List<String> imageUrls = new ArrayList<>();

	@ManyToOne(optional = false)
	@JoinColumn(name = "organization_id", nullable = false)
	private Organization organization;

	protected Animal() {
	}

	public Animal(
		String name,
		String species,
		Integer age,
		String gender,
		String healthDescription,
		String behaviorNotes,
		String status,
		String imageUrl,
		String adopter,
		Organization organization
	) {
		this.name = name;
		this.species = species;
		this.age = age;
		this.gender = gender;
		this.healthDescription = healthDescription;
		this.behaviorNotes = behaviorNotes;
		this.status = status;
		this.imageUrl = imageUrl;
		this.adopter = adopter;
		this.organization = organization;
	}

	public Long getId() {
		return id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getSpecies() {
		return species;
	}

	public void setSpecies(String species) {
		this.species = species;
	}

	public Integer getAge() {
		return age;
	}

	public void setAge(Integer age) {
		this.age = age;
	}

	public String getGender() {
		return gender;
	}

	public void setGender(String gender) {
		this.gender = gender;
	}

	public String getHealthDescription() {
		return healthDescription;
	}

	public void setHealthDescription(String healthDescription) {
		this.healthDescription = healthDescription;
	}

	public String getBehaviorNotes() {
		return behaviorNotes;
	}

	public void setBehaviorNotes(String behaviorNotes) {
		this.behaviorNotes = behaviorNotes;
	}

	public String getStatus() {
		return status;
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public String getImageUrl() {
		return imageUrl;
	}

	public void setImageUrl(String imageUrl) {
		this.imageUrl = imageUrl;
	}

	public List<String> getImageUrls() {
		return imageUrls;
	}

	public void setImageUrls(List<String> imageUrls) {
		this.imageUrls = imageUrls == null ? new ArrayList<>() : new ArrayList<>(imageUrls);
	}

	public String getAdopter() {
		return adopter;
	}

	public void setAdopter(String adopter) {
		this.adopter = adopter;
	}

	public Organization getOrganization() {
		return organization;
	}
}
