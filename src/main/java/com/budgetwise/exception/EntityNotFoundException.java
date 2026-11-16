package com.budgetwise.exception;

/**
 * Thrown when an entity (Account, Category, Budget, or Goal) is not found by its identifier.
 */
public class EntityNotFoundException extends BudgetWiseException {
    public EntityNotFoundException(String message) {
        super(message);
    }
}
