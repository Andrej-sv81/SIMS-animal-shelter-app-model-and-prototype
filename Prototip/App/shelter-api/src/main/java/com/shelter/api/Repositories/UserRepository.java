package com.shelter.api.Repositories;

import com.shelter.api.Models.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    boolean existsByEmail(String email);

    java.util.Optional<User> findByEmail(String email);

    List<User> findAllByOrganizationIdAndRole(Long organizationId, String role);

    Optional<User> findByIdAndOrganizationIdAndRole(Long id, Long organizationId, String role);

    Optional<User> findByEmailIgnoreCase(String email);
}