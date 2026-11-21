# BudgetWise — Plain-English Project Guide

> **Project:** AI-Assisted Personal Finance and Budgeting Application  
> **Course:** UVT Object-Oriented Programming (2026)  
> **Architecture:** Clean Student Model (14 Classes)  
> **Technology:** Java 21 LTS, Apache Maven, JUnit 5  

---

## 1. What is BudgetWise? (The Big Picture)

Imagine **BudgetWise** as a smart personal banking dashboard and financial copilot that lives on your computer. It does what modern financial apps (like Revolut or Apple Card) do, but built in clean, pure Java:
1. **Tracks Your Money:** Manages checking accounts (cash) and credit accounts (borrowed money).
2. **Watches Your Spending:** Categorizes every purchase (Food, Housing, Entertainment, etc.) and keeps you within monthly budgets.
3. **Acts as a Watchdog:** Alerts you immediately if you exceed 80% or 100% of a budget, or if a single purchase is abnormally high (> $150).
4. **Coaches Your Savings (AI Advisor):** Analyzes your past habits, calculates your pace toward financial goals (like saving $1,200 for a laptop), and suggests realistic monthly cuts on discretionary spending.
5. **Saves Your Data:** Stores all accounts and transactions into human-readable CSV files so your data persists between sessions.

---

## 2. The 4 Pillars & 14 Java Classes

The codebase is organized into four clean, focused packages:

```
src/main/java/com/budgetwise/
 ├── model/
 │    ├── Category.java            (Enum: FOOD, HOUSING, TRANSPORT, ENTERTAINMENT, UTILITIES, OTHER)
 │    ├── Account.java             (Abstract base class: id, ownerName, balance, transactions)
 │    ├── CheckingAccount.java     (Cash account: prevents negative balance)
 │    ├── CreditAccount.java       (Credit card: enforces credit limit)
 │    ├── Transaction.java         (Immutable record of a money movement)
 │    ├── Budget.java              (Monthly spending limits per category)
 │    ├── FinancialGoal.java       (Savings target with target date)
 │    └── Alert.java               (Warning or critical notification)
 ├── strategy/
 │    ├── SpendingStrategy.java    (Interface: defines calculateSpending contract)
 │    ├── MonthlyTotalStrategy.java(Sums spending within current calendar month)
 │    └── RollingAverageStrategy.java (Calculates 3-month rolling average)
 ├── rule/
 │    ├── SpendingRule.java        (Interface: evaluate transaction against state)
 │    ├── BudgetThresholdRule.java (Fires WARNING at 80% and CRITICAL at 100% of budget)
 │    └── LargePurchaseRule.java   (Fires WARNING if a single purchase > $150.00)
 ├── service/
 │    ├── SpendingAnalyzer.java    (Uses SpendingStrategy to summarize category trends)
 │    └── SavingsAdvisor.java      (Calculates required monthly savings & recommends cuts)
 ├── storage/
 │    └── CsvStorage.java          (Saves and loads accounts and transactions via CSV)
 └── ui/
      └── Main.java                (Console application with interactive menu & 3 live demo scenarios)
```

---

## 3. How the Core Features Work (In Simple Terms)

### A. Checking vs. Credit Accounts (Inheritance & Polymorphism)
- **`Account` (Abstract):** Contains common logic (account ID, owner name, balance, and transaction history). It declares an abstract method: `public abstract boolean withdraw(BigDecimal amount, String description, Category category);`.
- **`CheckingAccount`:** Overrides `withdraw()`. It enforces the rule: `balance - amount >= 0`. If you have $50 and try to spend $60, it rejects the transaction.
- **`CreditAccount`:** Overrides `withdraw()`. It allows spending on credit up to a `creditLimit`. Balance represents debt. If your limit is $1,000 and current balance is $900, attempting a $150 charge is rejected because it exceeds the limit.

### B. Why `BigDecimal` for Money?
Standard numbers (`double` or `float`) in computers cause binary rounding errors (e.g., `0.1 + 0.2` becomes `0.30000000000000004`). In banking applications, rounding errors lose real cents. `BigDecimal` provides exact decimal arithmetic with explicit rounding (`RoundingMode.HALF_UP`).

### C. The Strategy Pattern (Flexible Analytics)
Users want to see spending trends in different ways:
- **`MonthlyTotalStrategy`:** Sums spending in the current month.
- **`RollingAverageStrategy`:** Averages the past 3 months to see long-term habits.
Instead of messy `if/else` statements, `SpendingAnalyzer` accepts any class implementing `SpendingStrategy`. You can switch strategies at runtime:
```java
analyzer.setStrategy(new RollingAverageStrategy(3));
```

### D. The Watchdog Rule Engine
Every time a purchase occurs, it is evaluated by active rules:
1. `BudgetThresholdRule`: Checks category budget utilization.
   - **80% - 100%:** Generates a `WARNING` alert.
   - **Over 100%:** Generates a `CRITICAL` alert.
2. `LargePurchaseRule`: Generates a `WARNING` if an expense exceeds $150.00.

### E. AI Savings Advisor
When you create a `FinancialGoal` (e.g., Target: $1,200 in 6 months):
1. `SavingsAdvisor` computes the monthly savings target: $\frac{\$1,200}{6} = \$200\text{/month}$.
2. It compares monthly income against total expenses.
3. If there is a shortfall, it identifies discretionary categories (like `FOOD` dining out or `ENTERTAINMENT`) and recommends specific dollar cuts.

---

## 4. The 3 Automated Demonstration Scenarios

When you run `Main.java` (or choose Option 1), it demonstrates three realistic scenarios:

- **Scenario 1: Safe Spending & Cash Floor Invariant**  
  Owner deposits $500 into Checking. Spends $45 on groceries (balance: $455). Then tries to withdraw $600. The system rejects it: *"Insufficient funds (Balance cannot drop below zero)"*.
- **Scenario 2: Excessive Credit Spending & Alert Watchdog**  
  Owner charges a $240 luxury dinner on a Credit Card. The rule engine triggers:
  1. `[WARNING]` Large purchase detected ($240 > $150 threshold).
  2. `[CRITICAL]` Budget exceeded (Food budget at 145% utilization).
- **Scenario 3: Strategy Swapping & AI Goal Coaching**  
  Switches analyzer from Calendar Total ($290.00) to 3-Month Rolling Average ($96.67/mo). Goal advisor evaluates a $1,200 emergency fund goal (6 months) and recommends cutting discretionary Food spending by $90.00/month.
