package com.budgetwise.strategy;

/**
 * Abstract strategy base class providing normalized description preprocessing across all categorization algorithms.
 */
public abstract class AbstractCategorizationStrategy implements TransactionCategorizationStrategy {
    
    protected String normalize(String description) {
        if (description == null) return "";
        return description.trim().toLowerCase().replaceAll("\\s+", " ");
    }
}
