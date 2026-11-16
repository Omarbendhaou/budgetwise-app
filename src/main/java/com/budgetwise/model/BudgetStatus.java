package com.budgetwise.model;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Read-only result object communicating the current state of a monthly category budget.
 */
public record BudgetStatus(
        Budget budget,
        BigDecimal spent,
        BigDecimal remaining,
        BigDecimal utilizationPercentage,
        BudgetState state
) {
    public static BudgetStatus compute(Budget budget, BigDecimal spent, BudgetPolicy policy) {
        BigDecimal limit = budget.getLimit();
        BigDecimal remaining = limit.subtract(spent);

        // Utilization for display: spent * 100 / limit
        BigDecimal utilization = spent.multiply(new BigDecimal("100"))
                .divide(limit, 2, RoundingMode.HALF_UP);

        // Exact boundary evaluation using cross-multiplication: spent * 100 vs limit * threshold
        BigDecimal spentX100 = spent.multiply(new BigDecimal("100"));
        BigDecimal thresholdBoundary = limit.multiply(policy.getWarningPercentage());

        BudgetState state;
        if (spent.compareTo(limit) > 0) {
            state = BudgetState.EXCEEDED;
        } else if (spent.compareTo(limit) == 0) {
            state = BudgetState.LIMIT_REACHED;
        } else if (spentX100.compareTo(thresholdBoundary) >= 0) {
            state = BudgetState.WARNING;
        } else {
            state = BudgetState.NORMAL;
        }

        return new BudgetStatus(budget, spent, remaining, utilization, state);
    }
}
