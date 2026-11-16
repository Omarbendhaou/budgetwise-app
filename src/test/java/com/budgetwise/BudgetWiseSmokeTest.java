package com.budgetwise;

import com.budgetwise.factory.DefaultApplicationFactory;
import com.budgetwise.model.*;
import com.budgetwise.service.TransactionService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.LocalDate;
import static org.junit.jupiter.api.Assertions.*;

public class BudgetWiseSmokeTest {
    private DefaultApplicationFactory factory;

    @BeforeEach
    void setUp() {
        factory = new DefaultApplicationFactory();
    }

    @Test
    @DisplayName("Smoke Test: Verify Application Assembly, Injection, and Balance Computation")
    void testBasicTransactionFlow() {
        CheckingAccount acc = new CheckingAccount("ACC-01", "Checking Account", new BigDecimal("500.00"));
        factory.getAccountRepo().save(acc);

        TransactionService service = factory.getTransactionService();
        assertEquals(new BigDecimal("500.00"), service.calculateBalance("ACC-01"));

        // Record an income
        service.recordTransaction("TX-01", "ACC-01", LocalDate.now(), "Salary",
                new BigDecimal("1000.00"), TransactionType.INCOME, null);

        assertEquals(new BigDecimal("1500.00"), service.calculateBalance("ACC-01"));

        // Record an expense
        service.recordTransaction("TX-02", "ACC-01", LocalDate.now(), "Grocery store",
                new BigDecimal("200.00"), TransactionType.EXPENSE, null);

        assertEquals(new BigDecimal("1300.00"), service.calculateBalance("ACC-01"));
    }
}
