package com.shelter.api.Services;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.UUID;
import java.util.stream.Collectors;
import com.shelter.api.Models.Animal;
import com.shelter.api.Models.Organization;
import com.shelter.api.Models.DTOs.AnimalDto;
import com.shelter.api.Repositories.AnimalRepository;
import com.shelter.api.Repositories.OrganizationRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

@Service
public class AnimalService {
    private final AnimalRepository animalRepository;
    private final OrganizationRepository organizationRepository;

    public AnimalService(AnimalRepository animalRepository, OrganizationRepository organizationRepository) {
        this.animalRepository = animalRepository;
        this.organizationRepository = organizationRepository;
    }

    @Transactional(readOnly = true)
    public List<AnimalDto> getAnimals(Long organizationId) {
        ensureOrganizationExists(organizationId);
        return animalRepository.findAllByOrganizationId(organizationId).stream()
            .map(this::toDto)
            .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public AnimalDto getAnimal(Long organizationId, Long id) {
        return toDto(findAnimal(organizationId, id));
    }

    @Transactional
    public AnimalDto createAnimal(
        Long organizationId,
        String name,
        String species,
        Integer age,
        String gender,
        String healthDescription,
        String behaviorNotes,
        String status,
        String adopter,
        MultipartFile[] images
    ) {
        Organization organization = findOrganization(organizationId);
        Animal animal = new Animal(
            name, species, age, gender, healthDescription, behaviorNotes, status, "", adopter, organization
        );
        animal.setImageUrls(storeImages(images));
        animal.setImageUrl(firstImage(animal.getImageUrls()));
        return toDto(animalRepository.save(animal));
    }

    @Transactional
    public AnimalDto updateAnimal(
        Long organizationId,
        Long id,
        String name,
        String species,
        Integer age,
        String gender,
        String healthDescription,
        String behaviorNotes,
        String status,
        String adopter,
        MultipartFile[] images
    ) {
        Animal animal = findAnimal(organizationId, id);
        animal.setName(name);
        animal.setSpecies(species);
        animal.setAge(age);
        animal.setGender(gender);
        animal.setHealthDescription(healthDescription);
        animal.setBehaviorNotes(behaviorNotes);
        animal.setStatus(status);
        animal.setAdopter(adopter);
        if (hasImages(images)) {
            List<String> imageUrls = new ArrayList<>(animal.getImageUrls());
            if (imageUrls.isEmpty() && animal.getImageUrl() != null && !animal.getImageUrl().isBlank()) {
                imageUrls.add(animal.getImageUrl());
            }
            imageUrls.addAll(storeImages(images));
            animal.setImageUrls(imageUrls);
            animal.setImageUrl(firstImage(imageUrls));
        }
        return toDto(animalRepository.save(animal));
    }

    public void deleteAnimal(Long organizationId, Long id) {
        if (!animalRepository.existsByIdAndOrganizationId(id, organizationId)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Animal not found");
        }
        animalRepository.deleteById(id);
    }

    @Transactional
    public void deleteAnimalImage(Long organizationId, Long id, String imageUrl) {
        Animal animal = findAnimal(organizationId, id);
        List<String> imageUrls = new ArrayList<>(animal.getImageUrls());
        if (imageUrls.isEmpty() && animal.getImageUrl() != null && !animal.getImageUrl().isBlank()) {
            imageUrls.add(animal.getImageUrl());
        }

        if (!imageUrls.remove(imageUrl)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Animal image not found");
        }

        animal.setImageUrls(imageUrls);
        animal.setImageUrl(firstImage(imageUrls));
        animalRepository.save(animal);
        deleteStoredImage(imageUrl);
    }

    private Animal findAnimal(Long organizationId, Long id) {
        return animalRepository.findByIdAndOrganizationId(id, organizationId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Animal not found"));
    }

    private Organization findOrganization(Long id) {
        return organizationRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Organization not found"));
    }

    private void ensureOrganizationExists(Long id) {
        findOrganization(id);
    }

    private AnimalDto toDto(Animal animal) {
        return new AnimalDto(
            animal.getId(),
            animal.getName(),
            animal.getSpecies(),
            animal.getAge(),
            animal.getGender(),
            animal.getHealthDescription(),
            animal.getBehaviorNotes(),
            animal.getStatus(),
            firstImage(animal.getImageUrls().isEmpty()
                ? List.of(animal.getImageUrl() == null ? "" : animal.getImageUrl())
                : animal.getImageUrls()),
            animal.getImageUrls().isEmpty()
                ? (animal.getImageUrl() == null || animal.getImageUrl().isBlank() ? List.of() : List.of(animal.getImageUrl()))
                : animal.getImageUrls(),
            animal.getAdopter(),
            animal.getOrganization().getId(),
            animal.getOrganization().getName()
        );
    }

    private List<String> storeImages(MultipartFile[] images) {
        if (!hasImages(images)) return List.of();
        try {
            Path uploadDir = Paths.get("uploads", "animals");
            Files.createDirectories(uploadDir);
            List<String> imageUrls = new ArrayList<>();
            for (MultipartFile image : images) {
                if (image == null || image.isEmpty()) continue;
                String originalName = image.getOriginalFilename();
                String safeName = originalName == null || originalName.isBlank()
                    ? "animal-" + UUID.randomUUID()
                    : originalName.replaceAll("[^a-zA-Z0-9._-]", "_");
                String fileName = UUID.randomUUID() + "-" + safeName;
                Path target = uploadDir.resolve(fileName);
                try (InputStream input = image.getInputStream()) {
                    Files.copy(input, target, StandardCopyOption.REPLACE_EXISTING);
                }
                imageUrls.add("http://localhost:8080/uploads/animals/" + fileName);
            }
            return imageUrls;
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Failed to upload animal image", e);
        }
    }

    private boolean hasImages(MultipartFile[] images) {
        return images != null && Arrays.stream(images).anyMatch(image -> image != null && !image.isEmpty());
    }

    private String firstImage(List<String> imageUrls) {
        return imageUrls == null || imageUrls.isEmpty() ? "" : imageUrls.get(0);
    }

    private void deleteStoredImage(String imageUrl) {
        String fileName = imageUrl.substring(imageUrl.lastIndexOf('/') + 1);
        if (fileName.isBlank() || fileName.contains("..")) return;
        try {
            Files.deleteIfExists(Paths.get("uploads", "animals", fileName));
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Failed to remove animal image", e);
        }
    }
}
