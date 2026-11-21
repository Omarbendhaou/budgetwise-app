package com.budgetwise.model;

import java.math.BigDecimal;
import java.util.Objects;

/**
 * Abstract base class representing a bank account with fundamental financial invariants.
 */
public abstract class Account {
    private final String id;
    private final String name;
    protected BigDecimal balance;

    protected Account(String id, String name, BigDecimal balance) {
        this.id = Objects.requireNonNull(id, "Account ID cannot be null");
        this.name = Objects.requireNonNull(name, "Account name cannot be null");
        this.balance = Objects.requireNonNull(balance, "Balance cannot be null");
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public BigDecimal getBalance() { return balance; }

    public void deposit(BigDecimal amount) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Deposit amount must be strictly positive");
        }
        this.balance = this.balance.add(amount);
    }

    /**
     * Polymorphic withdrawal validation rule.
     */
    public abstract boolean canWithdraw(BigDecimal amount);

    /**
     * Polymorphic withdrawal execution.
     */
    public abstract void withdraw(BigDecimal amount);

    /**
     * Account classification label.
     */
    public abstract String getAccountType();

    @Override
    public String toString() {
        return String.format("[%s] %s (ID: %s) - Balance: $%.2f", getAccountType(), name, id, balance);
    }
}
