package com.budgetwise.model;

/**
 * Represents the health status of a monthly budget.
 */
public enum BudgetState {
    NORMAL,         // Spent < 80% of limit
    WARNING,        // Spent between 80% and < 100%
    LIMIT_REACHED,  // Spent exactly 100%
    EXCEEDED        // Spent > 100%
}
