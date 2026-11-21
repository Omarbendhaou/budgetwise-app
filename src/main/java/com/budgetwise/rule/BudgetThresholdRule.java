package com.budgetwise.rule;

import com.budgetwise.model.Alert;
import com.budgetwise.model.Budget;
import com.budgetwise.model.Transaction;
import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.List;

/**
 * Anomaly rule checking if category spending has exceeded 80% (Warning) or 100% (Critical) of budget.
 */
public class BudgetThresholdRule implements SpendingRule {

    @Override
    public Alert evaluate(Transaction transaction, List<Transaction> allTransactions, Budget budget) {
        if (budget == null || transaction == null || transaction.getType() != Transaction.Type.EXPENSE) {
            return null;
        }
        if (transaction.getCategory() != budget.getCategory()) {
            return null;
        }
        YearMonth currentMonth = budget.getMonth();
        if (!YearMonth.from(transaction.getDate()).equals(currentMonth)) {
            return null;
        }

        // Sum up all expenses in this category for this month
        BigDecimal totalSpent = BigDecimal.ZERO;
        for (Transaction tx : allTransactions) {
            if (tx.getType() == Transaction.Type.EXPENSE && tx.getCategory() == budget.getCategory() &&
                YearMonth.from(tx.getDate()).equals(currentMonth)) {
                totalSpent = totalSpent.add(tx.getAmount());
            }
        }

        double usage = budget.calculateUsagePercentage(totalSpent);
        if (usage >= 100.0) {
            return new Alert(getRuleName(),
                String.format("Budget EXCEEDED for %s in %s! Spent $%.2f of $%.2f limit (%.1f%%)",
                    budget.getCategory(), currentMonth, totalSpent, budget.getLimit(), usage),
                Alert.Severity.CRITICAL);
        } else if (usage >= 80.0) {
            return new Alert(getRuleName(),
                String.format("Budget WARNING for %s in %s: Spent $%.2f of $%.2f limit (%.1f%%)",
                    budget.getCategory(), currentMonth, totalSpent, budget.getLimit(), usage),
                Alert.Severity.WARNING);
        }
        return null;
    }

    @Override
    public String getRuleName() {
        return "Budget Threshold Rule";
    }
}
