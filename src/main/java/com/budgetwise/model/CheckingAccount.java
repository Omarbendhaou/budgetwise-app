package com.budgetwise.model;

import java.math.BigDecimal;

/**
 * Cash checking account enforcing a strict zero-overdraft balance floor.
 */
public class CheckingAccount extends Account {

    public CheckingAccount(String id, String name, BigDecimal balance) {
        super(id, name, balance);
    }

    @Override
    public boolean canWithdraw(BigDecimal amount) {
        return amount != null && amount.compareTo(BigDecimal.ZERO) > 0 && balance.compareTo(amount) >= 0;
    }

    @Override
    public void withdraw(BigDecimal amount) {
        if (!canWithdraw(amount)) {
            throw new IllegalStateException("CheckingAccount overdraft blocked: balance $" + balance + " cannot cover withdrawal of $" + amount);
        }
        this.balance = this.balance.subtract(amount);
    }

    @Override
    public String getAccountType() {
        return "Checking";
    }
}
