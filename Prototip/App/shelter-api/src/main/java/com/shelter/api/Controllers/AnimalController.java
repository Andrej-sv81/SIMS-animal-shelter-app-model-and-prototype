package com.shelter.api.Controllers;

import java.util.List;
import com.shelter.api.Models.DTOs.AnimalDto;
import com.shelter.api.Services.AnimalService;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/organizations/{organizationId}/animals")
@CrossOrigin(origins = "http://localhost:4200")
public class AnimalController {
    private final AnimalService animalService;

    public AnimalController(AnimalService animalService) {
        this.animalService = animalService;
    }

    @GetMapping
    public List<AnimalDto> listAnimals(@PathVariable Long organizationId) {
        return animalService.getAnimals(organizationId);
    }

    @GetMapping("/{id}")
    public AnimalDto getAnimal(@PathVariable Long organizationId, @PathVariable Long id) {
        return animalService.getAnimal(organizationId, id);
    }

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @ResponseStatus(HttpStatus.CREATED)
    public AnimalDto createAnimal(
        @PathVariable Long organizationId,
        @RequestParam String name,
        @RequestParam String species,
        @RequestParam Integer age,
        @RequestParam String gender,
        @RequestParam(required = false, defaultValue = "") String healthDescription,
        @RequestParam(required = false, defaultValue = "") String behaviorNotes,
        @RequestParam String status,
        @RequestParam(required = false, defaultValue = "") String adopter,
        @RequestParam(required = false, name = "image") MultipartFile[] images
    ) {
        return animalService.createAnimal(
            organizationId, name, species, age, gender, healthDescription, behaviorNotes, status, adopter, images
        );
    }

    @PutMapping(value = "/{id}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public AnimalDto updateAnimal(
        @PathVariable Long organizationId,
        @PathVariable Long id,
        @RequestParam String name,
        @RequestParam String species,
        @RequestParam Integer age,
        @RequestParam String gender,
        @RequestParam(required = false, defaultValue = "") String healthDescription,
        @RequestParam(required = false, defaultValue = "") String behaviorNotes,
        @RequestParam String status,
        @RequestParam(required = false, defaultValue = "") String adopter,
        @RequestParam(required = false, name = "image") MultipartFile[] images
    ) {
        return animalService.updateAnimal(
            organizationId, id, name, species, age, gender, healthDescription, behaviorNotes, status, adopter, images
        );
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteAnimal(@PathVariable Long organizationId, @PathVariable Long id) {
        animalService.deleteAnimal(organizationId, id);
    }

    @DeleteMapping("/{id}/images")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteAnimalImage(
        @PathVariable Long organizationId,
        @PathVariable Long id,
        @RequestParam String imageUrl
    ) {
        animalService.deleteAnimalImage(organizationId, id, imageUrl);
    }
}
