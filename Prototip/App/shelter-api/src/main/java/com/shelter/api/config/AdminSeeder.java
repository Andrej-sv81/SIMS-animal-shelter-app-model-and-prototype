package com.shelter.api.config;

import com.shelter.api.Models.User;
import com.shelter.api.Repositories.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Configuration
public class AdminSeeder {
    private static final String ADMIN_EMAIL = "admin";

    @Bean
    CommandLineRunner seedSuperAdministrator(UserRepository userRepository) {
        return args -> {
            User existingAdmin = userRepository.findByEmail(ADMIN_EMAIL).orElse(null);
            if (existingAdmin != null) {
                if (!existingAdmin.isActive()) {
                    existingAdmin.setActive(true);
                    userRepository.save(existingAdmin);
                }
                return;
            }

            BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
            User admin = new User(
                "Super",
                "Administrator",
                ADMIN_EMAIL,
                "",
                passwordEncoder.encode("admin"),
                "SUPER_ADMIN"
            );
            userRepository.save(admin);
        };
    }
}
