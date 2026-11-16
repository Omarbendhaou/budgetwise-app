# BudgetWise
### AI-Assisted Personal Finance and Budgeting Application
**UVT Object-Oriented Programming Course Project (2026)**  
**Team of 4 Students | NetBeans + Maven + Java 21 | Submission: Dec 1, 2026**

---

### Project Overview
BudgetWise is an object-oriented personal finance management and intelligent decision-support application built in Java.
It allows users to track accounts, record categorized transactions, define monthly category budgets with real-time threshold monitoring, detect unusual spending using configurable rules, and receive actionable savings advice tied to financial goals.

---

### How to Open & Run in Apache NetBeans
1. Launch **Apache NetBeans**.
2. Select **File &rarr; Open Project...**
3. Browse to this directory (`OOP project`), select it (NetBeans will recognize the Maven icon), and click **Open Project**.
4. Right-click the project &rarr; **Clean and Build**.
5. To run the application: Right-click the project &rarr; **Run** (or execute `com.budgetwise.ui.Main`).
6. To run all unit tests: Right-click the project &rarr; **Test**.

---

### Architecture & Package Structure
```
com.budgetwise
 ├── model        -> Core domain entities (Account, Transaction, Budget, FinancialGoal)
 ├── exception    -> Domain exception hierarchy (BudgetWiseException and subclasses)
 ├── strategy     -> Strategy Pattern contracts and implementations (Categorization & Analysis)
 ├── rule         -> Template Method pattern for Spending Rules & Savings Suggestions
 ├── repository   -> Repository contracts, In-Memory and CSV File implementations
 ├── service      -> Application business services (Transaction, Budget, Analyzer, Advisor)
 ├── factory      -> Factory Pattern & Dependency Injection assembly
 └── ui           -> Console interface, deterministic demo harness, and application entry point
```

---

### Team Roles & Ownership Matrix
* **Member 1:** Core Financial Domain & In-Memory Storage (`Account`, `CheckingAccount`, `CreditAccount`, `Transaction`, `Category`, `InMemoryTransactionRepository`, Exceptions).
* **Member 2:** Budgeting & Trend Analysis (`Budget`, `BudgetPolicy`, `BudgetService`, `BudgetStatus`, `SpendingSummary`, `MonthlyTotalAnalysisStrategy`, `RollingAverageAnalysisStrategy`).
* **Member 3:** Intelligence & Rules Engine (`AbstractSpendingRule` hierarchy, `AbstractCategorizationStrategy` hierarchy, `SpendingAnalyzer`, `SavingsAdvisor`).
* **Member 4:** Architecture, Persistence & UI (`BudgetWiseApplicationFactory`, `DefaultApplicationFactory`, `FileTransactionRepository` CSV persistence, `ConsoleMenu`, `Main`, integration demos).
