package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import java.math.BigDecimal;
import java.util.Objects;

/**
 * Abstract domain base class representing a financial account.
 * Demonstrates domain entity inheritance: subclasses enforce specialized withdrawal authorization policies.
 */
public abstract class Account {
    private final String id;
    private final String name;
    private final BigDecimal openingBalance;

    protected Account(String id, String name, BigDecimal openingBalance) {
        if (id == null || id.trim().isEmpty()) {
            throw new ValidationException("Account ID cannot be null or empty.");
        }
        if (name == null || name.trim().isEmpty()) {
            throw new ValidationException("Account name cannot be null or empty.");
        }
        if (openingBalance == null || openingBalance.compareTo(BigDecimal.ZERO) < 0) {
            throw new ValidationException("Opening balance must be non-negative.");
        }
        if (openingBalance.scale() > 2) {
            throw new ValidationException("Opening balance cannot have more than 2 decimal places.");
        }
        this.id = id.trim();
        this.name = name.trim();
        this.openingBalance = openingBalance;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public BigDecimal getOpeningBalance() { return openingBalance; }

    /**
     * Polymorphic authorization method: determines if a withdrawal of the given amount can proceed.
     */
    public abstract boolean canWithdraw(BigDecimal amount, BigDecimal currentBalance);

    /**
     * Calculates available funds considering opening balance, current transactions, and credit limits.
     */
    public abstract BigDecimal calculateAvailableFunds(BigDecimal currentBalance);

    public abstract String getAccountType();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Account account)) return false;
        return id.equalsIgnoreCase(account.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id.toLowerCase());
    }

    @Override
    public String toString() {
        return String.format("[%s] %s (%s)", getAccountType(), name, id);
    }
}
