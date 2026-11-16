package com.budgetwise.factory;

import com.budgetwise.service.*;
import com.budgetwise.strategy.SpendingAnalysisStrategy;
import com.budgetwise.strategy.TransactionCategorizationStrategy;

/**
 * Factory and Dependency Injection container contract owned by Member 4.
 */
public interface BudgetWiseApplicationFactory {
    TransactionService getTransactionService();
    BudgetService getBudgetService();
    SpendingAnalyzer getSpendingAnalyzer();
    SavingsAdvisor getSavingsAdvisor();
    void setCategorizationStrategy(TransactionCategorizationStrategy strategy);
    void setSpendingAnalysisStrategy(SpendingAnalysisStrategy strategy);
}
