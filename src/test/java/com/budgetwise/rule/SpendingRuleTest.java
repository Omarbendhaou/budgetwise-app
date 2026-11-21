package com.budgetwise.rule;

import com.budgetwise.model.*;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class SpendingRuleTest {

    @Test
    public void testBudgetThresholdRuleDetectsWarningAndExceeded() {
        Budget budget = new Budget(Category.FOOD, YearMonth.of(2026, 11), new BigDecimal("100.00"));
        BudgetThresholdRule rule = new BudgetThresholdRule();

        List<Transaction> txs = new ArrayList<>();
        Transaction tx1 = new Transaction("T1", "A1", LocalDate.of(2026, 11, 2), "Groceries", new BigDecimal("85.00"), Transaction.Type.EXPENSE, Category.FOOD);
        txs.add(tx1);

        Alert warningAlert = rule.evaluate(tx1, txs, budget);
        assertNotNull(warningAlert);
        assertEquals(Alert.Severity.WARNING, warningAlert.getSeverity());

        // Add expense pushing past 100%
        Transaction tx2 = new Transaction("T2", "A1", LocalDate.of(2026, 11, 4), "Snacks", new BigDecimal("25.00"), Transaction.Type.EXPENSE, Category.FOOD);
        txs.add(tx2);

        Alert criticalAlert = rule.evaluate(tx2, txs, budget);
        assertNotNull(criticalAlert);
        assertEquals(Alert.Severity.CRITICAL, criticalAlert.getSeverity());
    }

    @Test
    public void testLargePurchaseRuleFlagsExpensesAboveThreshold() {
        LargePurchaseRule rule = new LargePurchaseRule(new BigDecimal("150.00"));

        Transaction smallTx = new Transaction("T1", "A1", LocalDate.now(), "Book", new BigDecimal("45.00"), Transaction.Type.EXPENSE, Category.ENTERTAINMENT);
        assertNull(rule.evaluate(smallTx, List.of(smallTx), null));

        Transaction largeTx = new Transaction("T2", "A1", LocalDate.now(), "TV Monitor", new BigDecimal("250.00"), Transaction.Type.EXPENSE, Category.ENTERTAINMENT);
        Alert alert = rule.evaluate(largeTx, List.of(largeTx), null);
        assertNotNull(alert);
        assertEquals(Alert.Severity.WARNING, alert.getSeverity());
    }
}
