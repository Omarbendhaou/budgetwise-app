package com.budgetwise.service;

import com.budgetwise.exception.DuplicateBudgetException;
import com.budgetwise.model.*;
import com.budgetwise.repository.BudgetRepository;
import com.budgetwise.repository.TransactionRepository;
import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;

public class BudgetService {
    private final BudgetRepository budgetRepo;
    private final TransactionRepository transactionRepo;
    private final BudgetPolicy policy;

    public BudgetService(BudgetRepository budgetRepo, TransactionRepository transactionRepo, BudgetPolicy policy) {
        this.budgetRepo = budgetRepo;
        this.transactionRepo = transactionRepo;
        this.policy = policy;
    }

    public Budget createBudget(Category category, YearMonth month, BigDecimal limit) {
        if (budgetRepo.findByCategoryAndMonth(category, month).isPresent()) {
            throw new DuplicateBudgetException(String.format("Budget already exists for %s in %s", category.getName(), month));
        }
        Budget budget = new Budget(category, month, limit);
        budgetRepo.save(budget);
        return budget;
    }

    public BudgetStatus getBudgetStatus(Category category, YearMonth month) {
        Budget budget = budgetRepo.findByCategoryAndMonth(category, month)
                .orElse(null);
        if (budget == null) return null;

        BigDecimal spent = BigDecimal.ZERO;
        for (Transaction t : transactionRepo.findByMonth(month)) {
            if (t.getCategory().equals(category) && t.getType() == TransactionType.EXPENSE) {
                spent = spent.add(t.getAmount());
            }
        }
        return BudgetStatus.compute(budget, spent, policy);
    }

    public List<BudgetStatus> getAllStatusesForMonth(YearMonth month) {
        List<BudgetStatus> statuses = new ArrayList<>();
        for (Budget b : budgetRepo.findByMonth(month)) {
            statuses.add(getBudgetStatus(b.getCategory(), month));
        }
        return statuses;
    }
}
