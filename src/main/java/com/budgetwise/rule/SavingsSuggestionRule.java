package com.budgetwise.rule;

import com.budgetwise.model.AnalysisContext;
import com.budgetwise.model.FinancialGoal;
import com.budgetwise.model.SavingsRecommendation;
import java.time.YearMonth;
import java.util.List;

/**
 * Contract for generating intelligent savings suggestions based on spending patterns and active goals.
 */
public interface SavingsSuggestionRule {
    List<SavingsRecommendation> suggest(AnalysisContext ctx, List<FinancialGoal> goals, YearMonth current);
}
