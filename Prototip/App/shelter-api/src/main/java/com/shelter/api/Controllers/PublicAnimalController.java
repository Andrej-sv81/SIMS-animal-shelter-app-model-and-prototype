package com.shelter.api.Controllers;

import java.util.List;
import com.shelter.api.Models.DTOs.AnimalDto;
import com.shelter.api.Services.AnimalService;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/animals")
@CrossOrigin(origins = {"http://localhost:4200", "http://127.0.0.1:4200"})
public class PublicAnimalController {
    private final AnimalService animalService;

    public PublicAnimalController(AnimalService animalService) {
        this.animalService = animalService;
    }

    @GetMapping
    public List<AnimalDto> listAllAnimals() {
        return animalService.getAllAnimals();
    }
}