package com.budgetwise.service;

import com.budgetwise.model.*;
import com.budgetwise.repository.TransactionRepository;
import com.budgetwise.rule.SpendingRule;
import com.budgetwise.strategy.SpendingAnalysisStrategy;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;

public class SpendingAnalyzer {
    private final TransactionRepository transactionRepo;
    private SpendingAnalysisStrategy analysisStrategy;
    private final List<SpendingRule> rules = new ArrayList<>();

    public SpendingAnalyzer(TransactionRepository transactionRepo, SpendingAnalysisStrategy strategy) {
        this.transactionRepo = transactionRepo;
        this.analysisStrategy = strategy;
    }

    public void addRule(SpendingRule rule) {
        rules.add(rule);
    }

    public void setStrategy(SpendingAnalysisStrategy strategy) {
        this.analysisStrategy = strategy;
    }

    public List<Alert> analyzeMonth(YearMonth month, List<BudgetStatus> budgetStatuses) {
        SpendingSummary summary = analysisStrategy.analyze(month, transactionRepo.findAll());
        AnalysisContext context = new AnalysisContext(summary, budgetStatuses);

        List<Alert> allAlerts = new ArrayList<>();
        // Polymorphism: iterating through heterogeneous rules
        for (SpendingRule rule : rules) {
            allAlerts.addAll(rule.evaluate(context));
        }
        return allAlerts;
    }
}
