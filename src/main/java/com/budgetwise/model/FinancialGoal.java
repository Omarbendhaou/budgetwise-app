package com.budgetwise.model;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.YearMonth;
import java.time.temporal.ChronoUnit;
import java.util.Objects;

/**
 * Financial savings target tracking accumulated savings and target dates.
 */
public class FinancialGoal {
    private final String name;
    private final BigDecimal targetAmount;
    private BigDecimal savedAmount;
    private final YearMonth targetMonth;

    public FinancialGoal(String name, BigDecimal targetAmount, BigDecimal savedAmount, YearMonth targetMonth) {
        this.name = Objects.requireNonNull(name, "Goal name cannot be null");
        if (targetAmount == null || targetAmount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Target amount must be strictly positive");
        }
        this.targetAmount = targetAmount.setScale(2, RoundingMode.HALF_UP);
        this.savedAmount = (savedAmount != null ? savedAmount : BigDecimal.ZERO).setScale(2, RoundingMode.HALF_UP);
        this.targetMonth = Objects.requireNonNull(targetMonth, "Target month cannot be null");
    }

    public String getName() { return name; }
    public BigDecimal getTargetAmount() { return targetAmount; }
    public BigDecimal getSavedAmount() { return savedAmount; }
    public YearMonth getTargetMonth() { return targetMonth; }

    public void addSavings(BigDecimal amount) {
        if (amount != null && amount.compareTo(BigDecimal.ZERO) > 0) {
            this.savedAmount = this.savedAmount.add(amount).setScale(2, RoundingMode.HALF_UP);
        }
    }

    public BigDecimal getRemainingAmount() {
        BigDecimal diff = targetAmount.subtract(savedAmount);
        return diff.compareTo(BigDecimal.ZERO) > 0 ? diff : BigDecimal.ZERO;
    }

    /**
     * Calculates the required monthly savings pace to meet the goal on time.
     */
    public BigDecimal calculateMonthlySavingsPace(YearMonth currentMonth) {
        long monthsRemaining = ChronoUnit.MONTHS.between(currentMonth, targetMonth);
        if (monthsRemaining <= 0) monthsRemaining = 1;
        BigDecimal remaining = getRemainingAmount();
        return remaining.divide(BigDecimal.valueOf(monthsRemaining), 2, RoundingMode.HALF_UP);
    }

    public double getProgressPercentage() {
        if (targetAmount.compareTo(BigDecimal.ZERO) == 0) return 100.0;
        return savedAmount.divide(targetAmount, 4, RoundingMode.HALF_UP).doubleValue() * 100.0;
    }

    @Override
    public String toString() {
        return String.format("Goal: %s | Saved: $%.2f / $%.2f (%.1f%%) | Deadline: %s",
                name, savedAmount, targetAmount, getProgressPercentage(), targetMonth);
    }
}
