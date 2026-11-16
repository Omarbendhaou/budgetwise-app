package com.budgetwise.ui;

import com.budgetwise.factory.DefaultApplicationFactory;
import com.budgetwise.model.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.List;

public class ConsoleMenu {
    private final DefaultApplicationFactory factory;

    public ConsoleMenu(DefaultApplicationFactory factory) {
        this.factory = factory;
    }

    public void runDemoScenarioB() {
        System.out.println("=================================================================");
        System.out.println("  BudgetWise - Running Demo Scenario B (Assignment Overspending) ");
        System.out.println("=================================================================");

        // Setup Account
        CheckingAccount checking = new CheckingAccount("ACC-01", "Main Checking", new BigDecimal("1000.00"));
        factory.getAccountRepo().save(checking);

        // Setup Category & Budget
        Category dining = factory.getCategoryRepo().findByName("Dining").orElseThrow();
        YearMonth currentMonth = YearMonth.of(2026, 11);
        factory.getBudgetService().createBudget(dining, currentMonth, new BigDecimal("300.00"));

        // Setup Financial Goal
        FinancialGoal emergencyFund = new FinancialGoal(
                "GOAL-01", "Emergency Fund", new BigDecimal("1200.00"),
                new BigDecimal("600.00"), YearMonth.of(2027, 5));
        factory.getGoalRepo().save(emergencyFund);

        // Step 1: Initial expenses approaching warning threshold
        System.out.println("\n-> Recording initial dining expenses of 290.00...");
        factory.getTransactionService().recordTransaction(
                "TX-01", "ACC-01", LocalDate.of(2026, 11, 5), "Dinner at Bistro",
                new BigDecimal("290.00"), TransactionType.EXPENSE, dining
        );

        BudgetStatus status1 = factory.getBudgetService().getBudgetStatus(dining, currentMonth);
        System.out.printf("   Current Status: Spent: %s | Remaining: %s | Utilization: %s%% | State: %s%n",
                status1.spent(), status1.remaining(), status1.utilizationPercentage(), status1.state());

        // Step 2: New transaction causing budget breach
        System.out.println("\n-> Adding a 50.00 restaurant transaction...");
        factory.getTransactionService().recordTransaction(
                "TX-02", "ACC-01", LocalDate.of(2026, 11, 15), "Starbucks & Lunch",
                new BigDecimal("50.00"), TransactionType.EXPENSE, dining
        );

        BudgetStatus status2 = factory.getBudgetService().getBudgetStatus(dining, currentMonth);
        System.out.printf("   Updated Status: Spent: %s | Remaining: %s | Utilization: %s%% | State: %s%n",
                status2.spent(), status2.remaining(), status2.utilizationPercentage(), status2.state());

        // Step 3: Run Analysis & Anomaly Detection
        System.out.println("\n-> Running Spending Analyzer & Rule Engine...");
        List<Alert> alerts = factory.getSpendingAnalyzer().analyzeMonth(currentMonth, List.of(status2));
        for (Alert a : alerts) {
            System.out.println("   ALERT: " + a);
        }

        // Step 4: Run Intelligent Savings Advisor
        System.out.println("\n-> Running Savings Advisor (Goal-Linked Suggestions)...");
        AnalysisContext ctx = new AnalysisContext(
                new SpendingSummary(currentMonth, status2.spent(), java.util.Map.of(dining, status2.spent()),
                        factory.getTransactionService().getTransactions(), java.util.Map.of()),
                List.of(status2)
        );
        List<SavingsRecommendation> suggestions = factory.getSavingsAdvisor().generateSuggestions(ctx, currentMonth);
        for (SavingsRecommendation s : suggestions) {
            System.out.println("   RECOMMENDATION: " + s);
        }
        System.out.println("\nDemo B completed successfully!");
    }
}
