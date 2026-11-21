package com.budgetwise.model;

import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

public class AccountTest {

    @Test
    public void testCheckingAccountDepositAndValidWithdraw() {
        CheckingAccount acc = new CheckingAccount("CHK-1", "Test Checking", new BigDecimal("100.00"));
        acc.deposit(new BigDecimal("50.00"));
        assertEquals(new BigDecimal("150.00"), acc.getBalance());

        assertTrue(acc.canWithdraw(new BigDecimal("150.00")));
        acc.withdraw(new BigDecimal("50.00"));
        assertEquals(new BigDecimal("100.00"), acc.getBalance());
    }

    @Test
    public void testCheckingAccountZeroOverdraftFloor() {
        CheckingAccount acc = new CheckingAccount("CHK-1", "Test Checking", new BigDecimal("50.00"));
        assertFalse(acc.canWithdraw(new BigDecimal("50.01")));
        assertThrows(IllegalStateException.class, () -> acc.withdraw(new BigDecimal("50.01")));
    }

    @Test
    public void testCreditAccountAllowsSpendingIntoCreditLimit() {
        CreditAccount acc = new CreditAccount("CRD-1", "Test Credit", new BigDecimal("0.00"), new BigDecimal("500.00"));
        assertTrue(acc.canWithdraw(new BigDecimal("300.00")));
        acc.withdraw(new BigDecimal("300.00"));
        assertEquals(new BigDecimal("-300.00"), acc.getBalance());

        // Attempting to withdraw beyond credit limit should fail
        assertFalse(acc.canWithdraw(new BigDecimal("250.00"))); // 300 + 250 = 550 > 500
        assertThrows(IllegalStateException.class, () -> acc.withdraw(new BigDecimal("250.00")));
    }
}
