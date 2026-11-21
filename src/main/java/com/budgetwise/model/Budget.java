package com.budgetwise.model;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.YearMonth;
import java.util.Objects;

/**
 * Monthly budget allocation entity defining category spending limits.
 */
public class Budget {
    private final Category category;
    private final YearMonth month;
    private final BigDecimal limit;

    public Budget(Category category, YearMonth month, BigDecimal limit) {
        this.category = Objects.requireNonNull(category, "Category cannot be null");
        this.month = Objects.requireNonNull(month, "Month cannot be null");
        if (limit == null || limit.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Budget limit must be strictly positive");
        }
        this.limit = limit.setScale(2, RoundingMode.HALF_UP);
    }

    public Category getCategory() { return category; }
    public YearMonth getMonth() { return month; }
    public BigDecimal getLimit() { return limit; }

    /**
     * Calculates budget utilization percentage with exact decimal arithmetic.
     */
    public double calculateUsagePercentage(BigDecimal spent) {
        if (spent == null || spent.compareTo(BigDecimal.ZERO) <= 0) return 0.0;
        return spent.divide(limit, 4, RoundingMode.HALF_UP).doubleValue() * 100.0;
    }

    @Override
    public String toString() {
        return String.format("Budget [%s - %s]: Limit $%.2f", month, category, limit);
    }
}
