package com.budgetwise.model;

import java.util.List;

/**
 * Contextual input provided to all spending rules and intelligent savings advisor components.
 */
public record AnalysisContext(
        SpendingSummary summary,
        List<BudgetStatus> budgetStatuses
) {
    public AnalysisContext {
        budgetStatuses = List.copyOf(budgetStatuses);
    }
}
