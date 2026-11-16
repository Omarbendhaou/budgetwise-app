package com.budgetwise.strategy;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import java.util.*;

/**
 * Categorization strategy matching normalized keywords against configured categories.
 */
public class KeywordCategorizationStrategy extends AbstractCategorizationStrategy {
    private final Map<String, Category> keywordMap = new LinkedHashMap<>();

    public void registerKeyword(String keyword, Category category) {
        keywordMap.put(normalize(keyword), category);
    }

    @Override
    public Optional<Category> categorize(String description, List<Transaction> history) {
        String normalized = normalize(description);
        for (Map.Entry<String, Category> entry : keywordMap.entrySet()) {
            if (normalized.contains(entry.getKey())) {
                return Optional.of(entry.getValue());
            }
        }
        return Optional.empty();
    }

    @Override
    public String getStrategyName() {
        return "Keyword Rule-Based Categorization";
    }
}
