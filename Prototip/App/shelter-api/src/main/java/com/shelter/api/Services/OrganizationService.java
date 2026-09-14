package com.shelter.api.Services;

import java.util.List;
import java.util.stream.Collectors;
import com.shelter.api.Models.Organization;
import com.shelter.api.Models.User;
import com.shelter.api.Models.DTOs.AdminDto;
import com.shelter.api.Models.DTOs.OrganizationDto;
import com.shelter.api.Models.DTOs.OrganizationRequestDto;
import com.shelter.api.Repositories.OrganizationRepository;
import com.shelter.api.Repositories.UserRepository;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class OrganizationService {
    private static final String ADMIN_ROLE = "ORGANIZATION_ADMIN";

    private final OrganizationRepository organizationRepository;
    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public OrganizationService(OrganizationRepository organizationRepository, UserRepository userRepository) {
        this.organizationRepository = organizationRepository;
        this.userRepository = userRepository;
    }

    public List<OrganizationDto> getOrganizations() {
        return organizationRepository.findAll().stream()
            .map(this::toDto)
            .collect(Collectors.toList());
    }

    public OrganizationDto getOrganization(Long id) {
        return toDto(findOrganization(id));
    }

    public OrganizationDto createOrganization(OrganizationRequestDto request) {
        validateRequest(request);
        if (userRepository.existsByEmail(request.adminEmail())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "This administrator email is already registered. Please use a different email address.");
        }

        User admin = new User(
            request.adminFirstName(),
            request.adminLastName(),
            request.adminEmail(),
            request.adminPhone(),
            passwordEncoder.encode(request.adminPassword()),
            ADMIN_ROLE
        );
        Organization organization = new Organization(
            request.name(),
            request.description(),
            request.bankAccount(),
            admin
        );
        return toDto(organizationRepository.save(organization));
    }

    public OrganizationDto updateOrganization(Long id, OrganizationRequestDto request) {
        validateOrganizationDetails(request);
        String newPassword = request.adminPassword() == null ? null : request.adminPassword().trim();
        Organization organization = findOrganization(id);
        User admin = organization.getAdmin();

        if (!admin.getEmail().equals(request.adminEmail()) && userRepository.existsByEmail(request.adminEmail())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "This administrator email is already registered. Please use a different email address.");
        }

        organization.setName(request.name());
        organization.setDescription(request.description());
        organization.setBankAccount(request.bankAccount());
        admin.setFirstName(request.adminFirstName());
        admin.setLastName(request.adminLastName());
        admin.setEmail(request.adminEmail());
        admin.setPhone(request.adminPhone());
        if (newPassword != null && !newPassword.isBlank()) {
            admin.setPasswordHash(passwordEncoder.encode(newPassword));
        }
        organizationRepository.save(organization);
        return toDto(organization);
    }

    public void deleteOrganization(Long id) {
        if (!organizationRepository.existsById(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Organization not found");
        }
        organizationRepository.deleteById(id);
    }

    private Organization findOrganization(Long id) {
        return organizationRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Organization not found"));
    }

    private void validateRequest(OrganizationRequestDto request) {
        validateOrganizationDetails(request);
        if (request.name() == null || request.name().isBlank()
            || request.adminEmail() == null || request.adminEmail().isBlank()
            || request.adminPassword() == null || request.adminPassword().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Organization name, admin email, and admin password are required");
        }
    }

    private void validateOrganizationDetails(OrganizationRequestDto request) {
        if (request.name() == null || request.name().isBlank()
            || request.adminEmail() == null || request.adminEmail().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Organization name and admin email are required");
        }
    }

    private OrganizationDto toDto(Organization organization) {
        User admin = organization.getAdmin();
        AdminDto adminDto = new AdminDto(
            admin.getId(),
            admin.getFirstName(),
            admin.getLastName(),
            admin.getEmail(),
            admin.getPhone()
        );
        return new OrganizationDto(
            organization.getId(),
            organization.getName(),
            organization.getDescription(),
            organization.getBankAccount(),
            adminDto
        );
    }
}