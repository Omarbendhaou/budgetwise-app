package com.budgetwise.repository;

import com.budgetwise.model.Budget;
import com.budgetwise.model.Category;
import java.time.YearMonth;
import java.util.List;
import java.util.Optional;

public interface BudgetRepository {
    void save(Budget budget);
    Optional<Budget> findByCategoryAndMonth(Category category, YearMonth month);
    List<Budget> findByMonth(YearMonth month);
    List<Budget> findAll();
}
