package com.budgetwise.strategy;

import com.budgetwise.model.SpendingSummary;
import com.budgetwise.model.Transaction;
import java.time.YearMonth;
import java.util.List;

/**
 * Strategy interface for compiling monthly spending aggregations and historical trend baselines.
 */
public interface SpendingAnalysisStrategy {
    SpendingSummary analyze(YearMonth month, List<Transaction> allTransactions);
    String getStrategyName();
}
