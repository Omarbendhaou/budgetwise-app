package com.budgetwise.rule;

import com.budgetwise.model.*;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.YearMonth;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Intelligent savings rule that calculates required monthly contribution towards active financial goals.
 */
public class GoalContributionRule implements SavingsSuggestionRule {

    @Override
    public List<SavingsRecommendation> suggest(AnalysisContext ctx, List<FinancialGoal> goals, YearMonth current) {
        List<SavingsRecommendation> recommendations = new ArrayList<>();

        for (FinancialGoal goal : goals) {
            if (goal.isCompleted()) continue;

            if (goal.isOverdue(current)) {
                recommendations.add(new SavingsRecommendation(
                        "Overdue Goal: " + goal.getName(),
                        "Goal deadline passed with " + goal.getRemainingAmount() + " remaining.",
                        goal.getRemainingAmount(),
                        Optional.of(goal),
                        RecommendationPriority.HIGH
                ));
                continue;
            }

            // Month counting: inclusive of current month
            long monthsRemaining = ChronoUnit.MONTHS.between(current, goal.getTargetMonth()) + 1;
            if (monthsRemaining <= 0) monthsRemaining = 1;

            BigDecimal requiredMonthly = goal.getRemainingAmount()
                    .divide(BigDecimal.valueOf(monthsRemaining), 2, RoundingMode.CEILING);

            recommendations.add(new SavingsRecommendation(
                    "Monthly Contribution for " + goal.getName(),
                    String.format("Save %s/month across %d remaining months to reach %s target",
                            requiredMonthly, monthsRemaining, goal.getTargetAmount()),
                    requiredMonthly,
                    Optional.of(goal),
                    RecommendationPriority.MEDIUM
            ));
        }

        return recommendations;
    }
}
