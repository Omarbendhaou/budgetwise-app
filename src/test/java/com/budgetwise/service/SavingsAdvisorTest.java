package com.budgetwise.service;

import com.budgetwise.model.Category;
import com.budgetwise.model.FinancialGoal;
import com.budgetwise.model.Transaction;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class SavingsAdvisorTest {

    @Test
    public void testGoalPaceCalculationAndRecommendations() {
        // Goal: $1200 target, $400 saved, 4 months to deadline -> $200/month needed
        FinancialGoal goal = new FinancialGoal("Emergency", new BigDecimal("1200.00"), new BigDecimal("400.00"), YearMonth.of(2027, 3));
        assertEquals(new BigDecimal("200.00"), goal.calculateMonthlySavingsPace(YearMonth.of(2026, 11)));

        List<Transaction> txs = new ArrayList<>();
        txs.add(new Transaction("T1", "A1", LocalDate.of(2026, 11, 2), "Restaurant Dinner", new BigDecimal("250.00"), Transaction.Type.EXPENSE, Category.FOOD));
        txs.add(new Transaction("T2", "A1", LocalDate.of(2026, 11, 5), "Groceries", new BigDecimal("150.00"), Transaction.Type.EXPENSE, Category.FOOD));

        SavingsAdvisor advisor = new SavingsAdvisor();
        List<String> advice = advisor.generateAdvice(goal, YearMonth.of(2026, 11), txs);

        assertFalse(advice.isEmpty());
        // Should contain advice suggesting food reduction
        assertTrue(advice.stream().anyMatch(msg -> msg.contains("AI Suggestion") && msg.contains("FOOD")));
    }
}
