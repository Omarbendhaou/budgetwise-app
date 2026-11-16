package com.budgetwise.repository;

import com.budgetwise.model.Transaction;
import java.time.YearMonth;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * In-memory thread-safe implementation of TransactionRepository.
 */
public class InMemoryTransactionRepository implements TransactionRepository {
    private final Map<String, Transaction> storage = new ConcurrentHashMap<>();

    @Override
    public void save(Transaction transaction) {
        storage.put(transaction.getId(), transaction);
    }

    @Override
    public Optional<Transaction> findById(String id) {
        return Optional.ofNullable(storage.get(id));
    }

    @Override
    public List<Transaction> findAll() {
        return new ArrayList<>(storage.values());
    }

    @Override
    public List<Transaction> findByMonth(YearMonth month) {
        return storage.values().stream()
                .filter(t -> YearMonth.from(t.getDate()).equals(month))
                .toList();
    }

    @Override
    public List<Transaction> findByAccount(String accountId) {
        return storage.values().stream()
                .filter(t -> t.getAccountId().equalsIgnoreCase(accountId))
                .toList();
    }

    @Override
    public void clear() {
        storage.clear();
    }
}
