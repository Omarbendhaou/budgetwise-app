package com.budgetwise.repository;

import com.budgetwise.exception.BudgetWiseException;
import com.budgetwise.model.*;
import java.io.*;
import java.math.BigDecimal;
import java.nio.file.*;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.*;

/**
 * Demonstrates storage polymorphism: CSV-backed transaction repository.
 * Owned by Member 4 to fortify their OOP architectural defense.
 */
public class FileTransactionRepository implements TransactionRepository {
    private final Path filePath;
    private final InMemoryTransactionRepository memoryCache = new InMemoryTransactionRepository();
    private final CategoryRepository categoryRepo;

    public FileTransactionRepository(Path filePath, CategoryRepository categoryRepo) {
        this.filePath = filePath;
        this.categoryRepo = categoryRepo;
        loadFromFile();
    }

    private synchronized void loadFromFile() {
        if (!Files.exists(filePath)) return;
        try (BufferedReader reader = Files.newBufferedReader(filePath)) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty() || line.startsWith("#")) continue;
                String[] parts = line.split(",", -1);
                if (parts.length < 7) continue;

                Category category = categoryRepo.findById(parts[6])
                        .orElse(Category.UNCATEGORIZED);

                Transaction t = new Transaction(
                        parts[0], parts[1], LocalDate.parse(parts[2]),
                        parts[3], new BigDecimal(parts[4]),
                        TransactionType.valueOf(parts[5]), category
                );
                memoryCache.save(t);
            }
        } catch (IOException e) {
            throw new BudgetWiseException("Failed to read transaction CSV file", e);
        }
    }

    private synchronized void flushToFile() {
        try {
            if (filePath.getParent() != null) {
                Files.createDirectories(filePath.getParent());
            }
            try (BufferedWriter writer = Files.newBufferedWriter(filePath)) {
                for (Transaction t : memoryCache.findAll()) {
                    writer.write(String.format("%s,%s,%s,%s,%s,%s,%s%n",
                            t.getId(), t.getAccountId(), t.getDate(),
                            t.getDescription(), t.getAmount(), t.getType(),
                            t.getCategory().getId()));
                }
            }
        } catch (IOException e) {
            throw new BudgetWiseException("Failed to write transaction CSV file", e);
        }
    }

    @Override
    public synchronized void save(Transaction transaction) {
        memoryCache.save(transaction);
        flushToFile();
    }

    @Override
    public Optional<Transaction> findById(String id) {
        return memoryCache.findById(id);
    }

    @Override
    public List<Transaction> findAll() {
        return memoryCache.findAll();
    }

    @Override
    public List<Transaction> findByMonth(YearMonth month) {
        return memoryCache.findByMonth(month);
    }

    @Override
    public List<Transaction> findByAccount(String accountId) {
        return memoryCache.findByAccount(accountId);
    }

    @Override
    public synchronized void clear() {
        memoryCache.clear();
        flushToFile();
    }
}
