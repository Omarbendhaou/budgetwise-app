package com.budgetwise.strategy;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.List;

/**
 * Standard strategy: aggregates all expenses occurring within the specified calendar month.
 */
public class MonthlyTotalStrategy implements SpendingStrategy {

    @Override
    public BigDecimal calculateSpending(YearMonth month, Category category, List<Transaction> transactions) {
        BigDecimal total = BigDecimal.ZERO;
        if (transactions == null || month == null) return total;

        for (Transaction tx : transactions) {
            if (tx.getType() == Transaction.Type.EXPENSE) {
                YearMonth txMonth = YearMonth.from(tx.getDate());
                if (txMonth.equals(month) && (category == null || tx.getCategory() == category)) {
                    total = total.add(tx.getAmount());
                }
            }
        }
        return total;
    }

    @Override
    public String getStrategyName() {
        return "Calendar Month Total Strategy";
    }
}
