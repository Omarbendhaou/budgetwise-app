package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.Objects;

/**
 * Immutable domain entity representing a category budget for a specific calendar month.
 */
public final class Budget {
    private final Category category;
    private final YearMonth month;
    private final BigDecimal limit;

    public Budget(Category category, YearMonth month, BigDecimal limit) {
        if (category == null) {
            throw new ValidationException("Budget category cannot be null.");
        }
        if (month == null) {
            throw new ValidationException("Budget month cannot be null.");
        }
        if (limit == null || limit.compareTo(BigDecimal.ZERO) <= 0) {
            throw new ValidationException("Budget limit must be strictly positive.");
        }
        if (limit.scale() > 2) {
            throw new ValidationException("Budget limit cannot have more than 2 decimal places.");
        }
        this.category = category;
        this.month = month;
        this.limit = limit;
    }

    public Category getCategory() { return category; }
    public YearMonth getMonth() { return month; }
    public BigDecimal getLimit() { return limit; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Budget budget)) return false;
        return category.equals(budget.category) && month.equals(budget.month);
    }

    @Override
    public int hashCode() {
        return Objects.hash(category, month);
    }

    @Override
    public String toString() {
        return String.format("Budget[%s, %s, Limit: %s]", category.getName(), month, limit);
    }
}
