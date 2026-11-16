package com.budgetwise.repository;

import com.budgetwise.model.Category;
import java.util.List;
import java.util.Optional;

public interface CategoryRepository {
    void save(Category category);
    Optional<Category> findById(String id);
    Optional<Category> findByName(String name);
    List<Category> findAll();
}
