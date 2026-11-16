package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import java.util.Objects;

/**
 * Represents a transaction category. Supports custom user-defined categories created at runtime.
 */
public class Category {
    public static final Category UNCATEGORIZED = new Category("CAT-000", "Uncategorized", false);

    private final String id;
    private final String name;
    private final boolean isCustom;

    public Category(String id, String name, boolean isCustom) {
        if (id == null || id.trim().isEmpty()) {
            throw new ValidationException("Category ID cannot be null or empty.");
        }
        if (name == null || name.trim().isEmpty()) {
            throw new ValidationException("Category name cannot be null or empty.");
        }
        this.id = id.trim();
        this.name = name.trim();
        this.isCustom = isCustom;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public boolean isCustom() { return isCustom; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Category category)) return false;
        return id.equalsIgnoreCase(category.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id.toLowerCase());
    }

    @Override
    public String toString() {
        return name + (isCustom ? " (Custom)" : "");
    }
}
