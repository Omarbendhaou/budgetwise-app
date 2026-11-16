package com.budgetwise.service;

import com.budgetwise.exception.EntityNotFoundException;
import com.budgetwise.exception.InsufficientFundsException;
import com.budgetwise.model.*;
import com.budgetwise.repository.AccountRepository;
import com.budgetwise.repository.TransactionRepository;
import com.budgetwise.strategy.TransactionCategorizationStrategy;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

public class TransactionService {
    private final TransactionRepository transactionRepo;
    private final AccountRepository accountRepo;
    private TransactionCategorizationStrategy categorizationStrategy;

    public TransactionService(TransactionRepository transactionRepo,
                              AccountRepository accountRepo,
                              TransactionCategorizationStrategy categorizationStrategy) {
        this.transactionRepo = transactionRepo;
        this.accountRepo = accountRepo;
        this.categorizationStrategy = categorizationStrategy;
    }

    public synchronized void setCategorizationStrategy(TransactionCategorizationStrategy strategy) {
        this.categorizationStrategy = strategy;
    }

    public Transaction recordTransaction(String id, String accountId, LocalDate date, String description,
                                         BigDecimal amount, TransactionType type, Category manualCategory) {
        Account account = accountRepo.findById(accountId)
                .orElseThrow(() -> new EntityNotFoundException("Account not found: " + accountId));

        BigDecimal currentBalance = calculateBalance(accountId);

        // Domain polymorphism: Account authorizes withdrawal
        if (type == TransactionType.EXPENSE && !account.canWithdraw(amount, currentBalance)) {
            throw new InsufficientFundsException(String.format(
                    "Withdrawal of %s rejected by %s account policy (Current Balance: %s)",
                    amount, account.getAccountType(), currentBalance));
        }

        // Categorization precedence: Manual > Strategy > Uncategorized
        Category finalCategory = manualCategory;
        if (finalCategory == null) {
            finalCategory = categorizationStrategy.categorize(description, transactionRepo.findAll())
                    .orElse(Category.UNCATEGORIZED);
        }

        Transaction t = new Transaction(id, accountId, date, description, amount, type, finalCategory);
        transactionRepo.save(t);
        return t;
    }

    public BigDecimal calculateBalance(String accountId) {
        Account account = accountRepo.findById(accountId)
                .orElseThrow(() -> new EntityNotFoundException("Account not found: " + accountId));

        BigDecimal balance = account.getOpeningBalance();
        for (Transaction t : transactionRepo.findByAccount(accountId)) {
            balance = balance.add(t.getSignedAmount());
        }
        return balance;
    }

    public List<Transaction> getTransactions() {
        return transactionRepo.findAll();
    }
}
