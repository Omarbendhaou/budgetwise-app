package com.budgetwise.strategy;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.YearMonth;
import java.util.List;

/**
 * Alternative strategy: calculates average monthly spending over a rolling window of N months.
 */
public class RollingAverageStrategy implements SpendingStrategy {
    private final int monthsToAverage;

    public RollingAverageStrategy(int monthsToAverage) {
        this.monthsToAverage = Math.max(1, monthsToAverage);
    }

    public RollingAverageStrategy() {
        this(3); // default 3-month rolling baseline
    }

    @Override
    public BigDecimal calculateSpending(YearMonth month, Category category, List<Transaction> transactions) {
        BigDecimal sum = BigDecimal.ZERO;
        if (transactions == null || transactions.isEmpty() || month == null) return sum;

        for (int i = 0; i < monthsToAverage; i++) {
            YearMonth targetMonth = month.minusMonths(i);
            for (Transaction tx : transactions) {
                if (tx.getType() == Transaction.Type.EXPENSE) {
                    if (YearMonth.from(tx.getDate()).equals(targetMonth) && (category == null || tx.getCategory() == category)) {
                        sum = sum.add(tx.getAmount());
                    }
                }
            }
        }
        return sum.divide(BigDecimal.valueOf(monthsToAverage), 2, RoundingMode.HALF_UP);
    }

    @Override
    public String getStrategyName() {
        return monthsToAverage + "-Month Rolling Average Strategy";
    }
}
