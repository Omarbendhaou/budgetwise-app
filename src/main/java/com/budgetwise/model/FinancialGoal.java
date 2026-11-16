package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import java.math.BigDecimal;
import java.time.YearMonth;

/**
 * Represents a user-defined savings target with deadline tracking.
 */
public class FinancialGoal {
    private final String id;
    private final String name;
    private final BigDecimal targetAmount;
    private BigDecimal savedAmount;
    private final YearMonth targetMonth;

    public FinancialGoal(String id, String name, BigDecimal targetAmount, BigDecimal savedAmount, YearMonth targetMonth) {
        if (id == null || id.trim().isEmpty()) throw new ValidationException("Goal ID cannot be empty.");
        if (name == null || name.trim().isEmpty()) throw new ValidationException("Goal name cannot be empty.");
        if (targetAmount == null || targetAmount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new ValidationException("Target amount must be strictly positive.");
        }
        if (savedAmount == null || savedAmount.compareTo(BigDecimal.ZERO) < 0) {
            throw new ValidationException("Saved amount cannot be negative.");
        }
        if (targetMonth == null) throw new ValidationException("Target month cannot be null.");

        this.id = id.trim();
        this.name = name.trim();
        this.targetAmount = targetAmount;
        this.savedAmount = savedAmount;
        this.targetMonth = targetMonth;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public BigDecimal getTargetAmount() { return targetAmount; }
    public BigDecimal getSavedAmount() { return savedAmount; }
    public YearMonth getTargetMonth() { return targetMonth; }

    public synchronized void addSavings(BigDecimal amount) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new ValidationException("Savings addition must be strictly positive.");
        }
        this.savedAmount = this.savedAmount.add(amount);
    }

    public boolean isCompleted() {
        return savedAmount.compareTo(targetAmount) >= 0;
    }

    public boolean isOverdue(YearMonth currentMonth) {
        return !isCompleted() && targetMonth.isBefore(currentMonth);
    }

    public BigDecimal getRemainingAmount() {
        return targetAmount.subtract(savedAmount).max(BigDecimal.ZERO);
    }
}
