package com.budgetwise.ui;

import com.budgetwise.model.*;
import com.budgetwise.service.SavingsAdvisor;
import com.budgetwise.service.SpendingAnalyzer;
import com.budgetwise.storage.CsvStorage;
import com.budgetwise.strategy.MonthlyTotalStrategy;
import com.budgetwise.strategy.RollingAverageStrategy;
import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Main application entrypoint providing an interactive console CLI
 * and automated 3-scenario defense demonstrations.
 */
public class Main {
    private static final File CSV_FILE = new File("data/transactions.csv");

    public static void main(String[] args) {
        if (args.length > 0 && "demo".equalsIgnoreCase(args[0])) {
            runAutomatedDemonstrations();
            return;
        }

        // Initialize application state
        List<Account> accounts = new ArrayList<>();
        accounts.add(new CheckingAccount("CHK-101", "Primary Checking", new BigDecimal("1500.00")));
        accounts.add(new CreditAccount("CRD-202", "Rewards Credit Card", new BigDecimal("0.00"), new BigDecimal("2000.00")));

        YearMonth currentMonth = YearMonth.of(2026, 11);
        List<Budget> budgets = new ArrayList<>();
        budgets.add(new Budget(Category.FOOD, currentMonth, new BigDecimal("400.00")));
        budgets.add(new Budget(Category.ENTERTAINMENT, currentMonth, new BigDecimal("150.00")));
        budgets.add(new Budget(Category.TRANSPORTATION, currentMonth, new BigDecimal("200.00")));

        FinancialGoal goal = new FinancialGoal("Emergency Fund", new BigDecimal("3000.00"), new BigDecimal("1200.00"), YearMonth.of(2027, 4));

        List<Transaction> transactions = new ArrayList<>();
        try {
            transactions = CsvStorage.loadTransactions(CSV_FILE);
        } catch (Exception e) {
            System.out.println("No existing CSV found, loading sample data.");
        }

        if (transactions.isEmpty()) {
            transactions.add(new Transaction("TX-001", "CHK-101", LocalDate.of(2026, 11, 2), "Monthly Salary", new BigDecimal("3200.00"), Transaction.Type.INCOME, Category.OTHER));
            transactions.add(new Transaction("TX-002", "CHK-101", LocalDate.of(2026, 11, 4), "Supermarket Groceries", new BigDecimal("145.50"), Transaction.Type.EXPENSE, Category.FOOD));
            transactions.add(new Transaction("TX-003", "CRD-202", LocalDate.of(2026, 11, 8), "Fine Dining Dinner", new BigDecimal("185.00"), Transaction.Type.EXPENSE, Category.FOOD));
            transactions.add(new Transaction("TX-004", "CHK-101", LocalDate.of(2026, 11, 10), "Concert Tickets", new BigDecimal("120.00"), Transaction.Type.EXPENSE, Category.ENTERTAINMENT));
            try {
                CsvStorage.saveTransactions(CSV_FILE, transactions);
            } catch (Exception ignored) {}
        }

        SpendingAnalyzer analyzer = new SpendingAnalyzer(new MonthlyTotalStrategy());
        SavingsAdvisor advisor = new SavingsAdvisor();
        Scanner scanner = new Scanner(System.in);

        System.out.println("=============================================================");
        System.out.println("  BudgetWise — AI-Assisted Personal Finance & Budgeting");
        System.out.println("  UVT Object-Oriented Programming 2026 | Project 4");
        System.out.println("=============================================================");

        boolean running = true;
        while (running) {
            System.out.println("\n--- MAIN MENU ---");
            System.out.println("1. View Accounts & Available Balances");
            System.out.println("2. View Transactions & Add New Transaction");
            System.out.println("3. View Category Budgets & Spending Status");
            System.out.println("4. Run Spending Anomaly & Alert Watchdog");
            System.out.println("5. View Financial Goals & AI Savings Recommendations");
            System.out.println("6. Run Automated 3-Scenario Defense Demo");
            System.out.println("7. Exit Application");
            System.out.print("Select an option (1-7): ");

            String choice = scanner.nextLine().trim();
            switch (choice) {
                case "1":
                    System.out.println("\n[ACCOUNTS]");
                    for (Account acc : accounts) {
                        System.out.println("  " + acc);
                    }
                    break;

                case "2":
                    System.out.println("\n[TRANSACTIONS]");
                    for (Transaction tx : transactions) {
                        System.out.println("  " + tx);
                    }
                    System.out.print("\nAdd transaction? (y/n): ");
                    if ("y".equalsIgnoreCase(scanner.nextLine().trim())) {
                        try {
                            System.out.print("Description: ");
                            String desc = scanner.nextLine().trim();
                            System.out.print("Amount ($): ");
                            BigDecimal amt = new BigDecimal(scanner.nextLine().trim());
                            System.out.print("Category (FOOD, HOUSING, TRANSPORTATION, ENTERTAINMENT, OTHER): ");
                            Category cat = Category.valueOf(scanner.nextLine().trim().toUpperCase());

                            Transaction newTx = new Transaction("TX-" + (transactions.size() + 1), "CHK-101",
                                    LocalDate.now(), desc, amt, Transaction.Type.EXPENSE, cat);
                            transactions.add(newTx);
                            CsvStorage.saveTransactions(CSV_FILE, transactions);
                            System.out.println("Transaction added and saved to CSV!");
                        } catch (Exception e) {
                            System.out.println("Error adding transaction: " + e.getMessage());
                        }
                    }
                    break;

                case "3":
                    System.out.println("\n[MONTHLY BUDGET STATUS: " + currentMonth + "]");
                    for (Budget b : budgets) {
                        BigDecimal spent = analyzer.calculateSpending(currentMonth, b.getCategory(), transactions);
                        double pct = b.calculateUsagePercentage(spent);
                        String badge = pct >= 100.0 ? "[CRITICAL EXCEEDED]" : (pct >= 80.0 ? "[WARNING]" : "[NORMAL]");
                        System.out.printf("  %-16s: Spent $%7.2f / $%7.2f (%5.1f%%) %s%n",
                                b.getCategory(), spent, b.getLimit(), pct, badge);
                    }
                    break;

                case "4":
                    System.out.println("\n[SPENDING ANOMALY & ALERT SCAN]");
                    List<Alert> alerts = analyzer.runAnalysis(currentMonth, transactions, budgets);
                    if (alerts.isEmpty()) {
                        System.out.println("  No anomalies detected. All spending within safe thresholds.");
                    } else {
                        for (Alert a : alerts) {
                            System.out.println("  " + a);
                        }
                    }
                    break;

                case "5":
                    System.out.println("\n[AI SAVINGS ADVISOR]");
                    List<String> advice = advisor.generateAdvice(goal, currentMonth, transactions);
                    for (String tip : advice) {
                        System.out.println("  &bull; " + tip.replace("&bull; ", ""));
                    }
                    break;

                case "6":
                    runAutomatedDemonstrations();
                    break;

                case "7":
                    running = false;
                    System.out.println("\nExiting BudgetWise. Goodbye!");
                    break;

                default:
                    System.out.println("Invalid selection. Please choose 1-7.");
            }
        }
    }

    /**
     * Executes the 3 distinct defense scenarios required by the project specifications.
     */
    public static void runAutomatedDemonstrations() {
        System.out.println("\n=============================================================");
        System.out.println("   BUDGETWISE — 3-SCENARIO ACADEMIC DEFENSE DEMONSTRATION");
        System.out.println("=============================================================");

        YearMonth nov2026 = YearMonth.of(2026, 11);
        CheckingAccount chk = new CheckingAccount("CHK-101", "Checking Account", new BigDecimal("1200.00"));
        CreditAccount crd = new CreditAccount("CRD-202", "Credit Card", new BigDecimal("0.00"), new BigDecimal("1000.00"));

        List<Budget> budgets = new ArrayList<>();
        Budget foodBudget = new Budget(Category.FOOD, nov2026, new BigDecimal("300.00"));
        budgets.add(foodBudget);

        FinancialGoal laptopGoal = new FinancialGoal("New Laptop", new BigDecimal("1200.00"), new BigDecimal("400.00"), YearMonth.of(2027, 3));

        List<Transaction> txList = new ArrayList<>();
        txList.add(new Transaction("TX-1", "CHK-101", LocalDate.of(2026, 11, 2), "Work Salary", new BigDecimal("2500.00"), Transaction.Type.INCOME, Category.OTHER));
        txList.add(new Transaction("TX-2", "CHK-101", LocalDate.of(2026, 11, 3), "Weekly Groceries", new BigDecimal("95.00"), Transaction.Type.EXPENSE, Category.FOOD));

        SpendingAnalyzer analyzer = new SpendingAnalyzer(new MonthlyTotalStrategy());
        SavingsAdvisor advisor = new SavingsAdvisor();

        // --- SCENARIO 1: NORMAL SAFE SPENDING ---
        System.out.println("\n>>> SCENARIO 1: Safe Normal Spending & Account Invariants <<<");
        System.out.printf("Checking balance: $%.2f | Deposit $500 -> ", chk.getBalance());
        chk.deposit(new BigDecimal("500.00"));
        System.out.printf("New balance: $%.2f%n", chk.getBalance());

        System.out.println("Testing Checking Account zero-overdraft invariant (attempt withdraw $2000):");
        try {
            chk.withdraw(new BigDecimal("2000.00"));
        } catch (IllegalStateException e) {
            System.out.println("  [ENFORCED] " + e.getMessage());
        }

        BigDecimal spentS1 = analyzer.calculateSpending(nov2026, Category.FOOD, txList);
        System.out.printf("Food spending: $%.2f of $%.2f budget (%.1f%%) - Status: NORMAL%n",
                spentS1, foodBudget.getLimit(), foodBudget.calculateUsagePercentage(spentS1));

        // --- SCENARIO 2: BUDGET THRESHOLD EXCEEDED & ANOMALY ALERT ---
        System.out.println("\n>>> SCENARIO 2: Budget Exceeded Threshold & Anomaly Alerts <<<");
        System.out.println("Adding large expense: $240.00 at 'Luxury Seafood Restaurant'...");
        Transaction largeTx = new Transaction("TX-3", "CRD-202", LocalDate.of(2026, 11, 15), "Luxury Seafood Restaurant",
                new BigDecimal("240.00"), Transaction.Type.EXPENSE, Category.FOOD);
        txList.add(largeTx);

        List<Alert> alerts = analyzer.runAnalysis(nov2026, txList, budgets);
        for (Alert a : alerts) {
            System.out.println("  ALERT TRIGGERED: " + a);
        }

        // --- SCENARIO 3: STRATEGY SWAPPING & AI SAVINGS ADVICE ---
        System.out.println("\n>>> SCENARIO 3: Pluggable Strategy Swapping & AI Savings Advice <<<");
        System.out.printf("Active Strategy: %s -> Total Food Spent: $%.2f%n",
                analyzer.getStrategy().getStrategyName(), analyzer.calculateSpending(nov2026, Category.FOOD, txList));

        // Pluggable strategy swap at runtime
        analyzer.setStrategy(new RollingAverageStrategy(3));
        System.out.printf("Swapped Strategy: %s -> Moving Baseline: $%.2f%n",
                analyzer.getStrategy().getStrategyName(), analyzer.calculateSpending(nov2026, Category.FOOD, txList));

        System.out.println("\nGenerating AI Savings Advice for Goal: " + laptopGoal.getName());
        List<String> advice = advisor.generateAdvice(laptopGoal, nov2026, txList);
        for (String tip : advice) {
            System.out.println("  " + tip);
        }

        System.out.println("\n=============================================================");
        System.out.println("           ALL 3 DEFENSE SCENARIOS COMPLETED 100%");
        System.out.println("=============================================================\n");
    }
}
