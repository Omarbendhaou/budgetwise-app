package com.budgetwise.repository;

import com.budgetwise.model.FinancialGoal;
import java.util.List;
import java.util.Optional;

public interface GoalRepository {
    void save(FinancialGoal goal);
    Optional<FinancialGoal> findById(String id);
    List<FinancialGoal> findAll();
}
