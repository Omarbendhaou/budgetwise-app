package com.budgetwise.rule;

import com.budgetwise.model.Alert;
import com.budgetwise.model.AnalysisContext;
import java.util.List;

/**
 * Abstract spending rule applying the Template Method pattern: guarantees disabled rules never fire.
 */
public abstract class AbstractSpendingRule implements SpendingRule {
    private final String name;
    private boolean enabled = true;

    protected AbstractSpendingRule(String name) {
        this.name = name;
    }

    @Override
    public final String name() {
        return name;
    }

    @Override
    public final boolean isEnabled() {
        return enabled;
    }

    @Override
    public final void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    @Override
    public final List<Alert> evaluate(AnalysisContext context) {
        if (!enabled) {
            return List.of();
        }
        return doEvaluate(context); // Template Method
    }

    /**
     * Specialized rule evaluation logic executed only when the rule is enabled.
     */
    protected abstract List<Alert> doEvaluate(AnalysisContext context);
}
