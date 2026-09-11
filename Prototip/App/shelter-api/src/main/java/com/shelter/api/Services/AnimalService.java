package com.shelter.api.Services;

import java.util.List;
import java.util.stream.Collectors;
import com.shelter.api.Models.Animal;
import com.shelter.api.Models.DTOs.AnimalDto;
import com.shelter.api.Repositories.AnimalRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class AnimalService {
    private final AnimalRepository animalRepository;

    public AnimalService(AnimalRepository animalRepository) {
        this.animalRepository = animalRepository;
    }

    public List<AnimalDto> getAnimals() {
        return animalRepository.findAll().stream()
            .map(this::toDto)
            .collect(Collectors.toList());
    }

    public AnimalDto createAnimal(AnimalDto animalDto) {
        Animal animal = new Animal(animalDto.name(), animalDto.status(), animalDto.imageUrl());
        return toDto(animalRepository.save(animal));
    }

    public AnimalDto updateAnimal(Long id, AnimalDto animalDto) {
        Animal animal = findAnimal(id);
        animal.setName(animalDto.name());
        animal.setStatus(animalDto.status());
        animal.setImageUrl(animalDto.imageUrl());
        return toDto(animalRepository.save(animal));
    }

    public void deleteAnimal(Long id) {
        if (!animalRepository.existsById(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Animal not found");
        }
        animalRepository.deleteById(id);
    }

    private Animal findAnimal(Long id) {
        return animalRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Animal not found"));
    }

    private AnimalDto toDto(Animal animal) {
        return new AnimalDto(animal.getId(), animal.getName(), animal.getStatus(), animal.getImageUrl());
    }
}
