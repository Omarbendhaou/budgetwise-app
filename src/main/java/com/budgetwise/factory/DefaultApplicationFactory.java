package com.budgetwise.factory;

import com.budgetwise.model.BudgetPolicy;
import com.budgetwise.model.Category;
import com.budgetwise.repository.*;
import com.budgetwise.rule.*;
import com.budgetwise.service.*;
import com.budgetwise.strategy.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Concrete application factory: wires all repositories, services, strategies, and rules via constructor injection.
 */
public class DefaultApplicationFactory implements BudgetWiseApplicationFactory {
    private final TransactionRepository transactionRepo;
    private final AccountRepository accountRepo;
    private final CategoryRepository categoryRepo;
    private final BudgetRepository budgetRepo;
    private final GoalRepository goalRepo;

    private final TransactionService transactionService;
    private final BudgetService budgetService;
    private final SpendingAnalyzer spendingAnalyzer;
    private final SavingsAdvisor savingsAdvisor;

    public DefaultApplicationFactory() {
        // In-memory repositories
        this.transactionRepo = new InMemoryTransactionRepository();
        this.accountRepo = new InMemoryAccountRepository();
        this.categoryRepo = new InMemoryCategoryRepository();
        this.budgetRepo = new InMemoryBudgetRepository();
        this.goalRepo = new InMemoryGoalRepository();

        // Register default categories
        categoryRepo.save(Category.UNCATEGORIZED);
        categoryRepo.save(new Category("CAT-001", "Dining", false));
        categoryRepo.save(new Category("CAT-002", "Groceries", false));
        categoryRepo.save(new Category("CAT-003", "Transport", false));

        // Default strategies
        KeywordCategorizationStrategy defaultCatStrategy = new KeywordCategorizationStrategy();
        categoryRepo.findByName("Dining").ifPresent(c -> defaultCatStrategy.registerKeyword("restaurant", c));
        categoryRepo.findByName("Dining").ifPresent(c -> defaultCatStrategy.registerKeyword("starbucks", c));
        categoryRepo.findByName("Groceries").ifPresent(c -> defaultCatStrategy.registerKeyword("supermarket", c));

        SpendingAnalysisStrategy defaultAnalysisStrategy = new MonthlyTotalAnalysisStrategy();

        // Assemble services
        this.transactionService = new TransactionService(transactionRepo, accountRepo, defaultCatStrategy);
        this.budgetService = new BudgetService(budgetRepo, transactionRepo, new BudgetPolicy());
        this.spendingAnalyzer = new SpendingAnalyzer(transactionRepo, defaultAnalysisStrategy);
        this.spendingAnalyzer.addRule(new BudgetThresholdRule());

        this.savingsAdvisor = new SavingsAdvisor(goalRepo);
        this.savingsAdvisor.addRule(new GoalContributionRule());
    }

    @Override public TransactionService getTransactionService() { return transactionService; }
    @Override public BudgetService getBudgetService() { return budgetService; }
    @Override public SpendingAnalyzer getSpendingAnalyzer() { return spendingAnalyzer; }
    @Override public SavingsAdvisor getSavingsAdvisor() { return savingsAdvisor; }

    @Override
    public void setCategorizationStrategy(TransactionCategorizationStrategy strategy) {
        transactionService.setCategorizationStrategy(strategy);
    }

    @Override
    public void setSpendingAnalysisStrategy(SpendingAnalysisStrategy strategy) {
        spendingAnalyzer.setStrategy(strategy);
    }

    public AccountRepository getAccountRepo() { return accountRepo; }
    public CategoryRepository getCategoryRepo() { return categoryRepo; }
    public BudgetRepository getBudgetRepo() { return budgetRepo; }
    public GoalRepository getGoalRepo() { return goalRepo; }

    // Lightweight in-memory repository implementations
    private static class InMemoryAccountRepository implements AccountRepository {
        private final Map<String, com.budgetwise.model.Account> map = new ConcurrentHashMap<>();
        @Override public void save(com.budgetwise.model.Account a) { map.put(a.getId(), a); }
        @Override public Optional<com.budgetwise.model.Account> findById(String id) { return Optional.ofNullable(map.get(id)); }
        @Override public List<com.budgetwise.model.Account> findAll() { return new ArrayList<>(map.values()); }
    }

    private static class InMemoryCategoryRepository implements CategoryRepository {
        private final Map<String, Category> map = new ConcurrentHashMap<>();
        @Override public void save(Category c) { map.put(c.getId(), c); }
        @Override public Optional<Category> findById(String id) { return Optional.ofNullable(map.get(id)); }
        @Override public Optional<Category> findByName(String name) {
            return map.values().stream().filter(c -> c.getName().equalsIgnoreCase(name)).findFirst();
        }
        @Override public List<Category> findAll() { return new ArrayList<>(map.values()); }
    }

    private static class InMemoryBudgetRepository implements BudgetRepository {
        private final List<com.budgetwise.model.Budget> list = new ArrayList<>();
        @Override public synchronized void save(com.budgetwise.model.Budget b) { list.add(b); }
        @Override public synchronized Optional<com.budgetwise.model.Budget> findByCategoryAndMonth(Category c, java.time.YearMonth m) {
            return list.stream().filter(b -> b.getCategory().equals(c) && b.getMonth().equals(m)).findFirst();
        }
        @Override public synchronized List<com.budgetwise.model.Budget> findByMonth(java.time.YearMonth m) {
            return list.stream().filter(b -> b.getMonth().equals(m)).toList();
        }
        @Override public synchronized List<com.budgetwise.model.Budget> findAll() { return new ArrayList<>(list); }
    }

    private static class InMemoryGoalRepository implements GoalRepository {
        private final Map<String, com.budgetwise.model.FinancialGoal> map = new ConcurrentHashMap<>();
        @Override public void save(com.budgetwise.model.FinancialGoal g) { map.put(g.getId(), g); }
        @Override public Optional<com.budgetwise.model.FinancialGoal> findById(String id) { return Optional.ofNullable(map.get(id)); }
        @Override public List<com.budgetwise.model.FinancialGoal> findAll() { return new ArrayList<>(map.values()); }
    }
}
