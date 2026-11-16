package com.budgetwise.exception;

/**
 * Base unchecked exception for all domain errors within BudgetWise.
 * Callers can catch this parent exception for generic presentation or catch specific subclasses for recovery.
 */
public class BudgetWiseException extends RuntimeException {
    public BudgetWiseException(String message) {
        super(message);
    }

    public BudgetWiseException(String message, Throwable cause) {
        super(message, cause);
    }
}
