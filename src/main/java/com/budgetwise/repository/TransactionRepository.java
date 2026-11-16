package com.budgetwise.repository;

import com.budgetwise.model.Transaction;
import java.time.YearMonth;
import java.util.List;
import java.util.Optional;

public interface TransactionRepository {
    void save(Transaction transaction);
    Optional<Transaction> findById(String id);
    List<Transaction> findAll();
    List<Transaction> findByMonth(YearMonth month);
    List<Transaction> findByAccount(String accountId);
    void clear();
}
