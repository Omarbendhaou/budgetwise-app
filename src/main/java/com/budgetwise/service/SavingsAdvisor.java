package com.budgetwise.service;

import com.budgetwise.model.*;
import com.budgetwise.repository.GoalRepository;
import com.budgetwise.rule.SavingsSuggestionRule;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;

public class SavingsAdvisor {
    private final GoalRepository goalRepo;
    private final List<SavingsSuggestionRule> rules = new ArrayList<>();

    public SavingsAdvisor(GoalRepository goalRepo) {
        this.goalRepo = goalRepo;
    }

    public void addRule(SavingsSuggestionRule rule) {
        rules.add(rule);
    }

    public List<SavingsRecommendation> generateSuggestions(AnalysisContext ctx, YearMonth current) {
        List<FinancialGoal> goals = goalRepo.findAll();
        List<SavingsRecommendation> suggestions = new ArrayList<>();

        for (SavingsSuggestionRule rule : rules) {
            suggestions.addAll(rule.suggest(ctx, goals, current));
        }
        return suggestions;
    }
}
