package com.shelter.api.config;

import com.shelter.api.Models.User;
import com.shelter.api.Models.Volunteer;
import com.shelter.api.Repositories.UserRepository;
import com.shelter.api.Repositories.VolunteerRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.annotation.Transactional;

@Configuration
public class VolunteerUserMigration {
    @Bean
    CommandLineRunner migrateLegacyVolunteers(UserRepository userRepository, VolunteerRepository volunteerRepository) {
        return args -> migrate(userRepository, volunteerRepository);
    }

    @Transactional
    void migrate(UserRepository userRepository, VolunteerRepository volunteerRepository) {
        for (Volunteer legacyVolunteer : volunteerRepository.findAll()) {
            userRepository.findByEmailIgnoreCase(legacyVolunteer.getEmail()).ifPresent(user -> {
                user.setOrganization(legacyVolunteer.getOrganization());
                user.setActive(legacyVolunteer.isActive());
                user.setJoinedAt(legacyVolunteer.getJoinedAt());
                user.setPasswordHash(legacyVolunteer.getPasswordHash());
                if (!"VOLUNTEER".equals(user.getRole())) {
                    user.setRole("VOLUNTEER");
                }
                userRepository.save(user);
            });
        }
    }
}
