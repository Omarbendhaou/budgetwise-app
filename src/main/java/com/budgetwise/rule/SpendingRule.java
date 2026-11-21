package com.budgetwise.rule;

import com.budgetwise.model.Alert;
import com.budgetwise.model.Budget;
import com.budgetwise.model.Transaction;
import java.util.List;

/**
 * Rule interface for anomaly detection and spending policy checks.
 */
public interface SpendingRule {
    Alert evaluate(Transaction transaction, List<Transaction> allTransactions, Budget budget);
    String getRuleName();
}
