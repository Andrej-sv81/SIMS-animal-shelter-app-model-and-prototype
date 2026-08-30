package com.shelter.api;

import java.util.List;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/animals")
@CrossOrigin(origins = "http://localhost:4200")
public class AnimalController {
    @GetMapping
    public List<Animal> listAnimals() {
        return List.of(
            new Animal(1L, "Luna", "FREE", "/assets/animals/Luna.png"),
            new Animal(2L, "Mika", "FREE", "/assets/animals/Mika.png"),
            new Animal(3L, "Rex", "IN_PROCESS", "/assets/animals/Rex.png")
        );
    }
}
