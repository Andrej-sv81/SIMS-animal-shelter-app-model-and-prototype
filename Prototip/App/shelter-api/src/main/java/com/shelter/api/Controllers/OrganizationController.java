package com.shelter.api.Controllers;

import java.util.List;
import com.shelter.api.Models.DTOs.OrganizationDto;
import com.shelter.api.Models.DTOs.OrganizationRequestDto;
import com.shelter.api.Services.OrganizationService;
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
@RequestMapping("/api/organizations")
@CrossOrigin(origins = "http://localhost:4200")
public class OrganizationController {
    private final OrganizationService organizationService;

    public OrganizationController(OrganizationService organizationService) {
        this.organizationService = organizationService;
    }

    @GetMapping
    public List<OrganizationDto> listOrganizations() {
        return organizationService.getOrganizations();
    }

    @GetMapping("/{id}")
    public OrganizationDto getOrganization(@PathVariable Long id) {
        return organizationService.getOrganization(id);
    }

    @GetMapping("/mine/{adminId}")
    public OrganizationDto getOrganizationForAdmin(@PathVariable Long adminId) {
        return organizationService.getOrganizationForAdmin(adminId);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrganizationDto createOrganization(@RequestBody OrganizationRequestDto request) {
        return organizationService.createOrganization(request);
    }

    @PutMapping("/{id}")
    public OrganizationDto updateOrganization(
        @PathVariable Long id,
        @RequestBody OrganizationRequestDto request
    ) {
        return organizationService.updateOrganization(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteOrganization(@PathVariable Long id) {
        organizationService.deleteOrganization(id);
    }
}