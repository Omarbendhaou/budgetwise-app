package com.budgetwise.rule;

import com.budgetwise.model.Alert;
import com.budgetwise.model.AnalysisContext;
import java.util.List;

/**
 * Contract for rules that evaluate spending patterns and produce explainable alerts.
 */
public interface SpendingRule {
    String name();
    List<Alert> evaluate(AnalysisContext context);
    boolean isEnabled();
    void setEnabled(boolean enabled);
}
