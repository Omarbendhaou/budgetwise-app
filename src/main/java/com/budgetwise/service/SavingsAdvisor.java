package com.budgetwise.service;

import com.budgetwise.model.Category;
import com.budgetwise.model.FinancialGoal;
import com.budgetwise.model.Transaction;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * AI-assisted decision support service generating personalized savings recommendations.
 */
public class SavingsAdvisor {

    public List<String> generateAdvice(FinancialGoal goal, YearMonth currentMonth, List<Transaction> transactions) {
        List<String> advice = new ArrayList<>();
        if (goal == null) return advice;

        BigDecimal remainingGoal = goal.getRemainingAmount();
        if (remainingGoal.compareTo(BigDecimal.ZERO) <= 0) {
            advice.add("Congratulations! You have fully achieved your financial goal: " + goal.getName());
            return advice;
        }

        BigDecimal monthlyNeeded = goal.calculateMonthlySavingsPace(currentMonth);
        advice.add(String.format("Goal '%s': Target $%.2f | Saved $%.2f | Still Needed: $%.2f",
                goal.getName(), goal.getTargetAmount(), goal.getSavedAmount(), remainingGoal));
        advice.add(String.format("Required Monthly Savings Pace: $%.2f/month until %s", monthlyNeeded, goal.getTargetMonth()));

        // Analyze discretionary spending in current month
        Map<Category, BigDecimal> spendingByCategory = new HashMap<>();
        BigDecimal totalExpenses = BigDecimal.ZERO;

        if (transactions != null) {
            for (Transaction tx : transactions) {
                if (tx.getType() == Transaction.Type.EXPENSE && YearMonth.from(tx.getDate()).equals(currentMonth)) {
                    spendingByCategory.put(tx.getCategory(),
                            spendingByCategory.getOrDefault(tx.getCategory(), BigDecimal.ZERO).add(tx.getAmount()));
                    totalExpenses = totalExpenses.add(tx.getAmount());
                }
            }
        }

        if (totalExpenses.compareTo(BigDecimal.ZERO) > 0) {
            for (Map.Entry<Category, BigDecimal> entry : spendingByCategory.entrySet()) {
                Category cat = entry.getKey();
                BigDecimal spent = entry.getValue();
                double percentOfTotal = spent.divide(totalExpenses, 4, RoundingMode.HALF_UP).doubleValue() * 100.0;

                // Recommend cuts on discretionary categories (Food, Entertainment, Other) if >= 20% of expenses
                if ((cat == Category.FOOD || cat == Category.ENTERTAINMENT || cat == Category.OTHER) && percentOfTotal >= 20.0) {
                    BigDecimal suggestedCut = spent.multiply(new BigDecimal("0.25")).setScale(2, RoundingMode.HALF_UP);
                    double coverage = (monthlyNeeded.compareTo(BigDecimal.ZERO) > 0)
                            ? Math.min(100.0, suggestedCut.divide(monthlyNeeded, 2, RoundingMode.HALF_UP).doubleValue() * 100.0)
                            : 100.0;

                    advice.add(String.format("AI Suggestion: You spent $%.2f (%.1f%% of expenses) on %s. Reducing this by 25%% (save $%.2f) covers %.0f%% of your monthly goal target!",
                            spent, percentOfTotal, cat, suggestedCut, coverage));
                }
            }
        }

        return advice;
    }
}
