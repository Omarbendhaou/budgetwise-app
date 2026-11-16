package com.budgetwise.strategy;

import com.budgetwise.model.*;
import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.*;

/**
 * Basic analysis strategy computing category totals for the requested calendar month only.
 */
public class MonthlyTotalAnalysisStrategy implements SpendingAnalysisStrategy {

    @Override
    public SpendingSummary analyze(YearMonth month, List<Transaction> allTransactions) {
        BigDecimal totalExpenses = BigDecimal.ZERO;
        Map<Category, BigDecimal> categoryTotals = new HashMap<>();
        List<Transaction> monthlyExpenses = new ArrayList<>();

        for (Transaction t : allTransactions) {
            if (YearMonth.from(t.getDate()).equals(month) && t.getType() == TransactionType.EXPENSE) {
                monthlyExpenses.add(t);
                totalExpenses = totalExpenses.add(t.getAmount());
                categoryTotals.merge(t.getCategory(), t.getAmount(), BigDecimal::add);
            }
        }

        return new SpendingSummary(month, totalExpenses, categoryTotals, monthlyExpenses, Map.of());
    }

    @Override
    public String getStrategyName() {
        return "Standard Monthly Total Analysis";
    }
}
