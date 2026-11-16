package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import java.math.BigDecimal;

/**
 * Standard checking account: rejects any withdrawal that causes the balance to drop below zero.
 */
public class CheckingAccount extends Account {

    public CheckingAccount(String id, String name, BigDecimal openingBalance) {
        super(id, name, openingBalance);
    }

    @Override
    public boolean canWithdraw(BigDecimal amount, BigDecimal currentBalance) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new ValidationException("Withdrawal amount must be strictly positive.");
        }
        return currentBalance.compareTo(amount) >= 0;
    }

    @Override
    public BigDecimal calculateAvailableFunds(BigDecimal currentBalance) {
        return currentBalance.max(BigDecimal.ZERO);
    }

    @Override
    public String getAccountType() {
        return "CHECKING";
    }
}
