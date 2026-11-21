package com.budgetwise.model;

import java.math.BigDecimal;
import java.util.Objects;

/**
 * Credit card account allowing spending into the negative up to a configured credit limit.
 */
public class CreditAccount extends Account {
    private final BigDecimal creditLimit;

    public CreditAccount(String id, String name, BigDecimal balance, BigDecimal creditLimit) {
        super(id, name, balance);
        this.creditLimit = Objects.requireNonNull(creditLimit, "Credit limit cannot be null");
    }

    public BigDecimal getCreditLimit() {
        return creditLimit;
    }

    @Override
    public boolean canWithdraw(BigDecimal amount) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) return false;
        BigDecimal availableFunds = balance.add(creditLimit);
        return availableFunds.compareTo(amount) >= 0;
    }

    @Override
    public void withdraw(BigDecimal amount) {
        if (!canWithdraw(amount)) {
            throw new IllegalStateException("Credit limit exceeded: withdrawal of $" + amount + " exceeds limit of $" + creditLimit);
        }
        this.balance = this.balance.subtract(amount);
    }

    @Override
    public String getAccountType() {
        return "Credit";
    }
}
