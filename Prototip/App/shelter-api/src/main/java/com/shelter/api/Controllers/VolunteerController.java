package com.shelter.api.Controllers;

import java.util.List;
import com.shelter.api.Models.DTOs.VolunteerDto;
import com.shelter.api.Models.DTOs.VolunteerRequestDto;
import com.shelter.api.Services.VolunteerService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/organizations/{organizationId}/volunteers")
@CrossOrigin(origins = {"http://localhost:4200", "http://127.0.0.1:4200"})
public class VolunteerController {
    private final VolunteerService volunteerService;

    public VolunteerController(VolunteerService volunteerService) {
        this.volunteerService = volunteerService;
    }

    @GetMapping
    public List<VolunteerDto> listVolunteers(@PathVariable Long organizationId) {
        return volunteerService.getVolunteers(organizationId);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public VolunteerDto createVolunteer(
        @PathVariable Long organizationId,
        @RequestBody VolunteerRequestDto request
    ) {
        return volunteerService.createVolunteer(organizationId, request);
    }

    @PatchMapping("/{volunteerId}/active")
    public VolunteerDto toggleActive(
        @PathVariable Long organizationId,
        @PathVariable Long volunteerId
    ) {
        return volunteerService.toggleActive(organizationId, volunteerId);
    }
}
