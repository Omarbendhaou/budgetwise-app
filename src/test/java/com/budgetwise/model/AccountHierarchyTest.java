package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

public class AccountHierarchyTest {

    @Test
    @DisplayName("CheckingAccount rejects withdrawals exceeding current balance")
    void testCheckingAccountOverdraft() {
        CheckingAccount checking = new CheckingAccount("ACC-01", "Checking", new BigDecimal("100.00"));
        
        assertTrue(checking.canWithdraw(new BigDecimal("50.00"), new BigDecimal("100.00")));
        assertTrue(checking.canWithdraw(new BigDecimal("100.00"), new BigDecimal("100.00")));
        assertFalse(checking.canWithdraw(new BigDecimal("100.01"), new BigDecimal("100.00")));
    }

    @Test
    @DisplayName("CreditAccount allows overdraft up to credit limit")
    void testCreditAccountOverdraft() {
        CreditAccount credit = new CreditAccount("ACC-02", "Credit Card",
                new BigDecimal("100.00"), new BigDecimal("500.00"));
        
        // Available funds = 100 + 500 = 600
        assertTrue(credit.canWithdraw(new BigDecimal("550.00"), new BigDecimal("100.00")));
        assertTrue(credit.canWithdraw(new BigDecimal("600.00"), new BigDecimal("100.00")));
        assertFalse(credit.canWithdraw(new BigDecimal("600.01"), new BigDecimal("100.00")));
    }

    @Test
    @DisplayName("Account validates scale and rejects 3+ decimals in opening balance")
    void testAccountValidation() {
        assertThrows(ValidationException.class, () ->
                new CheckingAccount("ACC-ERR", "Invalid", new BigDecimal("100.555")));
    }
}
