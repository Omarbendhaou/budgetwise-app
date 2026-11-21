package com.budgetwise.service;

import com.budgetwise.model.Alert;
import com.budgetwise.model.Budget;
import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import com.budgetwise.rule.BudgetThresholdRule;
import com.budgetwise.rule.LargePurchaseRule;
import com.budgetwise.rule.SpendingRule;
import com.budgetwise.strategy.MonthlyTotalStrategy;
import com.budgetwise.strategy.SpendingStrategy;
import java.math.BigDecimal;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;

/**
 * Controller service orchestrating transactions, budgets, strategies, and anomaly rules.
 */
public class SpendingAnalyzer {
    private SpendingStrategy strategy;
    private final List<SpendingRule> rules;

    public SpendingAnalyzer(SpendingStrategy strategy) {
        this.strategy = strategy != null ? strategy : new MonthlyTotalStrategy();
        this.rules = new ArrayList<>();
        this.rules.add(new BudgetThresholdRule());
        this.rules.add(new LargePurchaseRule());
    }

    public SpendingAnalyzer() {
        this(new MonthlyTotalStrategy());
    }

    public void setStrategy(SpendingStrategy strategy) {
        if (strategy != null) {
            this.strategy = strategy;
        }
    }

    public SpendingStrategy getStrategy() {
        return strategy;
    }

    public void addRule(SpendingRule rule) {
        if (rule != null) {
            this.rules.add(rule);
        }
    }

    public List<SpendingRule> getRules() {
        return rules;
    }

    public BigDecimal calculateSpending(YearMonth month, Category category, List<Transaction> transactions) {
        return strategy.calculateSpending(month, category, transactions);
    }

    public List<Alert> runAnalysis(YearMonth month, List<Transaction> transactions, List<Budget> budgets) {
        List<Alert> alerts = new ArrayList<>();
        if (transactions == null) return alerts;

        for (Transaction tx : transactions) {
            if (YearMonth.from(tx.getDate()).equals(month)) {
                Budget matchingBudget = null;
                if (budgets != null) {
                    for (Budget b : budgets) {
                        if (b.getCategory() == tx.getCategory() && b.getMonth().equals(month)) {
                            matchingBudget = b;
                            break;
                        }
                    }
                }
                for (SpendingRule rule : rules) {
                    Alert alert = rule.evaluate(tx, transactions, matchingBudget);
                    if (alert != null) {
                        alerts.add(alert);
                    }
                }
            }
        }
        return alerts;
    }
}
