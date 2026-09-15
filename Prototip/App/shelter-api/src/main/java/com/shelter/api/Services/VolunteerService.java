package com.shelter.api.Services;

import java.util.List;
import com.shelter.api.Models.Organization;
import com.shelter.api.Models.User;
import com.shelter.api.Models.DTOs.VolunteerDto;
import com.shelter.api.Models.DTOs.VolunteerRequestDto;
import com.shelter.api.Repositories.OrganizationRepository;
import com.shelter.api.Repositories.UserRepository;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
public class VolunteerService {
    private final OrganizationRepository organizationRepository;
    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public VolunteerService(OrganizationRepository organizationRepository, UserRepository userRepository) {
        this.organizationRepository = organizationRepository;
        this.userRepository = userRepository;
    }

    public List<VolunteerDto> getVolunteers(Long organizationId) {
        findOrganization(organizationId);
        return userRepository.findAllByOrganizationIdAndRole(organizationId, "VOLUNTEER").stream()
            .map(this::toDto)
            .toList();
    }

    @Transactional
    public VolunteerDto createVolunteer(Long organizationId, VolunteerRequestDto request) {
        Organization organization = findOrganization(organizationId);
        validate(request);
        String email = request.email().trim().toLowerCase();
        if (userRepository.existsByEmail(email)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "This volunteer email is already registered.");
        }
        String passwordHash = passwordEncoder.encode(request.password());
        User user = new User(
            request.firstName().trim(), request.lastName().trim(), email, request.phone(), passwordHash, "VOLUNTEER"
        );
        user.setOrganization(organization);
        userRepository.save(user);
        return toDto(user);
    }

    @Transactional
    public VolunteerDto toggleActive(Long organizationId, Long volunteerId) {
        findOrganization(organizationId);
        User volunteer = userRepository.findByIdAndOrganizationIdAndRole(volunteerId, organizationId, "VOLUNTEER")
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Volunteer not found"));
        boolean active = !volunteer.isActive();
        volunteer.setActive(active);
        return toDto(userRepository.save(volunteer));
    }

    private Organization findOrganization(Long id) {
        return organizationRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Organization not found"));
    }

    private void validate(VolunteerRequestDto request) {
        if (request.firstName() == null || request.firstName().isBlank()
            || request.lastName() == null || request.lastName().isBlank()
            || request.email() == null || request.email().isBlank()
            || request.password() == null || request.password().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "First name, last name, email, and password are required");
        }
    }

    private VolunteerDto toDto(User volunteer) {
        return new VolunteerDto(
            volunteer.getId(), volunteer.getFirstName(), volunteer.getLastName(), volunteer.getEmail(),
            volunteer.getPhone(), volunteer.isActive(), volunteer.getJoinedAt(), volunteer.getOrganization().getId()
        );
    }
}
