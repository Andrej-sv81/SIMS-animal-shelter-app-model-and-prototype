package com.shelter.api.Repositories;

import java.util.List;
import com.shelter.api.Models.Volunteer;
import org.springframework.data.jpa.repository.JpaRepository;

public interface VolunteerRepository extends JpaRepository<Volunteer, Long> {
    List<Volunteer> findAllByOrganizationId(Long organizationId);
    boolean existsByEmailIgnoreCase(String email);
    java.util.Optional<Volunteer> findByEmailIgnoreCase(String email);
}
