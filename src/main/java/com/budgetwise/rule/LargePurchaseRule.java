package com.budgetwise.rule;

import com.budgetwise.model.Alert;
import com.budgetwise.model.Budget;
import com.budgetwise.model.Transaction;
import java.math.BigDecimal;
import java.util.List;

/**
 * Anomaly rule detecting unusually large individual transactions exceeding a configured threshold.
 */
public class LargePurchaseRule implements SpendingRule {
    private final BigDecimal threshold;

    public LargePurchaseRule(BigDecimal threshold) {
        this.threshold = threshold != null ? threshold : new BigDecimal("150.00");
    }

    public LargePurchaseRule() {
        this(new BigDecimal("150.00"));
    }

    @Override
    public Alert evaluate(Transaction transaction, List<Transaction> allTransactions, Budget budget) {
        if (transaction != null && transaction.getType() == Transaction.Type.EXPENSE &&
            transaction.getAmount().compareTo(threshold) >= 0) {
            return new Alert(getRuleName(),
                String.format("Large expense flagged: $%.2f on '%s' (%s) exceeds $%.2f threshold",
                    transaction.getAmount(), transaction.getDescription(), transaction.getCategory(), threshold),
                Alert.Severity.WARNING);
        }
        return null;
    }

    @Override
    public String getRuleName() {
        return "Large Purchase Anomaly Rule";
    }
}
