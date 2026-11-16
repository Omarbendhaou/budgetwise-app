package com.budgetwise.exception;

/**
 * Thrown when an account withdrawal authorization fails due to insufficient balance or credit limit breach.
 */
public class InsufficientFundsException extends BudgetWiseException {
    public InsufficientFundsException(String message) {
        super(message);
    }
}
