package com.budgetwise.rule;

import com.budgetwise.model.*;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

/**
 * Fires alerts when monthly category spending enters WARNING or EXCEEDED states.
 */
public class BudgetThresholdRule extends AbstractSpendingRule {

    public BudgetThresholdRule() {
        super("Budget Threshold Breach Rule");
    }

    @Override
    protected List<Alert> doEvaluate(AnalysisContext context) {
        List<Alert> alerts = new ArrayList<>();
        for (BudgetStatus status : context.budgetStatuses()) {
            if (status.state() == BudgetState.EXCEEDED) {
                BigDecimal overspend = status.spent().subtract(status.budget().getLimit());
                alerts.add(new Alert(
                        AlertSeverity.CRITICAL,
                        name(),
                        String.format("%s budget exceeded by %s (Spent: %s, Limit: %s)",
                                status.budget().getCategory().getName(), overspend, status.spent(), status.budget().getLimit()),
                        status.spent(),
                        String.format("Utilization reached %s%% exceeding 100%% limit", status.utilizationPercentage())
                ));
            } else if (status.state() == BudgetState.WARNING || status.state() == BudgetState.LIMIT_REACHED) {
                alerts.add(new Alert(
                        AlertSeverity.WARNING,
                        name(),
                        String.format("%s budget reached warning state (%s%% used)",
                                status.budget().getCategory().getName(), status.utilizationPercentage()),
                        status.spent(),
                        "Spending reached or exceeded warning threshold"
                ));
            }
        }
        return alerts;
    }
}
