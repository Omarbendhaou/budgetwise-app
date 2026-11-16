package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import java.math.BigDecimal;

/**
 * Credit card / overdraft account: allows withdrawals beyond zero up to a configured credit limit.
 */
public class CreditAccount extends Account {
    private final BigDecimal creditLimit;

    public CreditAccount(String id, String name, BigDecimal openingBalance, BigDecimal creditLimit) {
        super(id, name, openingBalance);
        if (creditLimit == null || creditLimit.compareTo(BigDecimal.ZERO) < 0) {
            throw new ValidationException("Credit limit must be non-negative.");
        }
        if (creditLimit.scale() > 2) {
            throw new ValidationException("Credit limit cannot have more than 2 decimal places.");
        }
        this.creditLimit = creditLimit;
    }

    public BigDecimal getCreditLimit() {
        return creditLimit;
    }

    @Override
    public boolean canWithdraw(BigDecimal amount, BigDecimal currentBalance) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new ValidationException("Withdrawal amount must be strictly positive.");
        }
        BigDecimal totalAvailable = currentBalance.add(creditLimit);
        return totalAvailable.compareTo(amount) >= 0;
    }

    @Override
    public BigDecimal calculateAvailableFunds(BigDecimal currentBalance) {
        return currentBalance.add(creditLimit);
    }

    @Override
    public String getAccountType() {
        return "CREDIT";
    }
}
