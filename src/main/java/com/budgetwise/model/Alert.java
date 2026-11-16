package com.budgetwise.model;

import java.math.BigDecimal;

/**
 * Immutable alert emitted when spending violates a configured rule.
 */
public record Alert(
        AlertSeverity severity,
        String ruleName,
        String message,
        BigDecimal triggerAmount,
        String basisExplanation
) {
    @Override
    public String toString() {
        return String.format("[%s] %s: %s (Basis: %s)", severity, ruleName, message, basisExplanation);
    }
}
