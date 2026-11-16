package com.budgetwise.model;

import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * Immutable aggregation of a month's expenses, category totals, and historical baselines.
 */
public record SpendingSummary(
        YearMonth month,
        BigDecimal totalExpenses,
        Map<Category, BigDecimal> categoryTotals,
        List<Transaction> monthlyTransactions,
        Map<Category, BigDecimal> historicalBaselines
) {
    public SpendingSummary {
        categoryTotals = Collections.unmodifiableMap(categoryTotals);
        monthlyTransactions = List.copyOf(monthlyTransactions);
        historicalBaselines = Collections.unmodifiableMap(historicalBaselines);
    }
}
