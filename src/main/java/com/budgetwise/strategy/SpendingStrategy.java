package com.budgetwise.strategy;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.List;

/**
 * Strategy interface defining spending calculation algorithms.
 * Demonstrates the Strategy Design Pattern for pluggable analytics.
 */
public interface SpendingStrategy {
    BigDecimal calculateSpending(YearMonth month, Category category, List<Transaction> transactions);
    String getStrategyName();
}
