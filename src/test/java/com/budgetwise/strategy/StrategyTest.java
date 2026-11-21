package com.budgetwise.strategy;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class StrategyTest {

    @Test
    public void testMonthlyTotalStrategyAggregatesCorrectly() {
        List<Transaction> txs = new ArrayList<>();
        txs.add(new Transaction("TX1", "A1", LocalDate.of(2026, 11, 5), "Groceries", new BigDecimal("50.00"), Transaction.Type.EXPENSE, Category.FOOD));
        txs.add(new Transaction("TX2", "A1", LocalDate.of(2026, 11, 10), "Dinner", new BigDecimal("75.00"), Transaction.Type.EXPENSE, Category.FOOD));
        txs.add(new Transaction("TX3", "A1", LocalDate.of(2026, 10, 20), "Old Groceries", new BigDecimal("100.00"), Transaction.Type.EXPENSE, Category.FOOD)); // Different month!
        txs.add(new Transaction("TX4", "A1", LocalDate.of(2026, 11, 15), "Salary", new BigDecimal("2000.00"), Transaction.Type.INCOME, Category.OTHER)); // Income, not expense!

        SpendingStrategy strategy = new MonthlyTotalStrategy();
        BigDecimal total = strategy.calculateSpending(YearMonth.of(2026, 11), Category.FOOD, txs);
        assertEquals(new BigDecimal("125.00"), total);
    }

    @Test
    public void testRollingAverageStrategyComputesCorrectAverage() {
        List<Transaction> txs = new ArrayList<>();
        // Month 11: $100
        txs.add(new Transaction("TX1", "A1", LocalDate.of(2026, 11, 5), "Food", new BigDecimal("100.00"), Transaction.Type.EXPENSE, Category.FOOD));
        // Month 10: $200
        txs.add(new Transaction("TX2", "A1", LocalDate.of(2026, 10, 5), "Food", new BigDecimal("200.00"), Transaction.Type.EXPENSE, Category.FOOD));
        // Month 9: $300
        txs.add(new Transaction("TX3", "A1", LocalDate.of(2026, 9, 5), "Food", new BigDecimal("300.00"), Transaction.Type.EXPENSE, Category.FOOD));

        // 3-month average of 100 + 200 + 300 = 600 / 3 = 200
        RollingAverageStrategy strategy = new RollingAverageStrategy(3);
        BigDecimal avg = strategy.calculateSpending(YearMonth.of(2026, 11), Category.FOOD, txs);
        assertEquals(new BigDecimal("200.00"), avg);
    }
}
