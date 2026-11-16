package com.budgetwise.strategy;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import java.util.List;
import java.util.Optional;

/**
 * Intelligent categorization strategy that learns from previously categorized transactions.
 */
public class MerchantHistoryStrategy extends AbstractCategorizationStrategy {

    @Override
    public Optional<Category> categorize(String description, List<Transaction> history) {
        String normalized = normalize(description);
        if (history == null || history.isEmpty()) return Optional.empty();

        // Search backward from most recent transaction
        for (int i = history.size() - 1; i >= 0; i--) {
            Transaction t = history.get(i);
            if (normalize(t.getDescription()).equals(normalized) &&
                    !t.getCategory().equals(Category.UNCATEGORIZED)) {
                return Optional.of(t.getCategory());
            }
        }
        return Optional.empty();
    }

    @Override
    public String getStrategyName() {
        return "Merchant History Adaptive Categorization";
    }
}
