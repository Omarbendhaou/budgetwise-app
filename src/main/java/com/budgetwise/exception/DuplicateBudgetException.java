package com.budgetwise.exception;

/**
 * Thrown when attempting to define a budget for a category and period that already has a registered budget.
 */
public class DuplicateBudgetException extends BudgetWiseException {
    public DuplicateBudgetException(String message) {
        super(message);
    }
}
