package com.budgetwise.exception;

/**
 * Thrown when domain validation fails (e.g. negative amounts, empty names, more than 2 decimal places).
 */
public class ValidationException extends BudgetWiseException {
    public ValidationException(String message) {
        super(message);
    }
}
