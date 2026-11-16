package com.budgetwise.model;

import java.math.BigDecimal;

/**
 * Represents the direction of a financial transaction.
 * Uses a signed multiplier for exact balance arithmetic.
 */
public enum TransactionType {
    INCOME(BigDecimal.ONE),
    EXPENSE(new BigDecimal("-1"));

    private final BigDecimal multiplier;

    TransactionType(BigDecimal multiplier) {
        this.multiplier = multiplier;
    }

    public BigDecimal getMultiplier() {
        return multiplier;
    }
}
