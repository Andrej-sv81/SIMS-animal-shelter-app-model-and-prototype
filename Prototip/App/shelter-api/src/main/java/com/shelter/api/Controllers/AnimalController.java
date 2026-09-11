package com.shelter.api.Controllers;

import java.util.List;
import com.shelter.api.Models.DTOs.AnimalDto;
import com.shelter.api.Services.AnimalService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/animals")
@CrossOrigin(origins = "http://localhost:4200")
public class AnimalController {
    private final AnimalService animalService;

    public AnimalController(AnimalService animalService) {
        this.animalService = animalService;
    }

    @GetMapping
    public List<AnimalDto> listAnimals() {
        return animalService.getAnimals();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public AnimalDto createAnimal(@RequestBody AnimalDto animalDto) {
        return animalService.createAnimal(animalDto);
    }

    @PutMapping("/{id}")
    public AnimalDto updateAnimal(@PathVariable Long id, @RequestBody AnimalDto animalDto) {
        return animalService.updateAnimal(id, animalDto);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteAnimal(@PathVariable Long id) {
        animalService.deleteAnimal(id);
    }
}
