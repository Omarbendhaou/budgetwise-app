package com.budgetwise.model;

import java.math.BigDecimal;

/**
 * Single source of truth for budget warning thresholds across services and rules.
 */
public class BudgetPolicy {
    private static final BigDecimal DEFAULT_WARNING_PERCENTAGE = new BigDecimal("80.00");
    private final BigDecimal warningPercentage;

    public BudgetPolicy() {
        this(DEFAULT_WARNING_PERCENTAGE);
    }

    public BudgetPolicy(BigDecimal warningPercentage) {
        this.warningPercentage = warningPercentage;
    }

    public BigDecimal getWarningPercentage() {
        return warningPercentage;
    }
}
