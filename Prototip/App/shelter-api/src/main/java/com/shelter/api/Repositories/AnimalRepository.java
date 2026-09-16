package com.shelter.api.Repositories;

import java.util.List;
import java.util.Optional;
import com.shelter.api.Models.Animal;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AnimalRepository extends JpaRepository<Animal, Long> {
	List<Animal> findAll();
	List<Animal> findAllByOrganizationId(Long organizationId);

	Optional<Animal> findByIdAndOrganizationId(Long id, Long organizationId);

	boolean existsByIdAndOrganizationId(Long id, Long organizationId);
}
