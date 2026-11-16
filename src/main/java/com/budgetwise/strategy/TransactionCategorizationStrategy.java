package com.budgetwise.strategy;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import java.util.List;
import java.util.Optional;

/**
 * Strategy interface for automatically inferring transaction categories from description and history.
 */
public interface TransactionCategorizationStrategy {
    Optional<Category> categorize(String description, List<Transaction> history);
    String getStrategyName();
}
