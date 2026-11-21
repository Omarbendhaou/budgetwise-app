package com.budgetwise.storage;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import java.io.File;
import java.io.IOException;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class CsvStorageTest {

    @Test
    public void testSaveAndLoadTransactionsRoundTrip(@TempDir File tempDir) throws IOException {
        File csvFile = new File(tempDir, "test_tx.csv");

        List<Transaction> original = new ArrayList<>();
        original.add(new Transaction("T1", "A100", LocalDate.of(2026, 11, 1), "Salary", new BigDecimal("3000.00"), Transaction.Type.INCOME, Category.OTHER));
        original.add(new Transaction("T2", "A100", LocalDate.of(2026, 11, 2), "Coffee", new BigDecimal("4.50"), Transaction.Type.EXPENSE, Category.FOOD));

        CsvStorage.saveTransactions(csvFile, original);
        assertTrue(csvFile.exists());

        List<Transaction> loaded = CsvStorage.loadTransactions(csvFile);
        assertEquals(2, loaded.size());
        assertEquals("T1", loaded.get(0).getId());
        assertEquals(new BigDecimal("3000.00"), loaded.get(0).getAmount());
        assertEquals(Category.FOOD, loaded.get(1).getCategory());
    }
}
