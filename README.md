# BudgetWise — AI-Assisted Personal Finance & Budgeting Application

> **Institution:** University of Tunis (UVT) — Object-Oriented Programming (2026)  
> **Team Size:** 4 Students | **Technology:** Java 21 LTS, Apache Maven, JUnit 5  
> **Architecture:** Clean Student Model (14 Classes)  

---

## 📁 Repository Structure: Team Materials vs. Java Code

To make navigation easy during preparation, development, and the final oral exam, this repository is organized into distinct sections:

```
OOP project/
 │
 ├── 👥 team_deliverables/                     <-- ALL TEAM & PRESENTATION MATERIALS
 │    ├── 01_member_task_guides/              <-- Individual 2-page oral defense guides (PDF)
 │    │    ├── BudgetWise_Member1_Guide.pdf
 │    │    ├── BudgetWise_Member2_Guide.pdf
 │    │    ├── BudgetWise_Member3_Guide.pdf
 │    │    └── BudgetWise_Member4_Guide.pdf
 │    ├── 02_project_overview_and_evaluation/ <-- Plain English manuals & grading reports
 │    │    ├── BudgetWise_Plain_English_Project_Guide.pdf
 │    │    ├── PROJECT_EXPLANATION.md
 │    │    └── ACADEMIC_EVALUATION_98_100.md
 │    └── 03_uml_class_diagrams/              <-- Official UML Class Diagrams
 │         ├── BudgetWise_UML_Exact_Style.png (High-Res image for slides)
 │         ├── BudgetWise_UML_Diagram.drawio  (Editable Draw.io XML)
 │         ├── BudgetWise_UML_Exact_Style.svg (Vector graphic)
 │         ├── budgetwise.puml                (PlantUML source)
 │         └── uml_diagram_viewer.html        (Browser visualizer)
 │
 ├── 💻 src/                                  <-- PURE JAVA SOURCE CODE & UNIT TESTS
 │    ├── main/java/com/budgetwise/
 │    │    ├── model/                         (Account, CheckingAccount, CreditAccount, Transaction, Category, Budget, FinancialGoal, Alert)
 │    │    ├── strategy/                      (SpendingStrategy, MonthlyTotalStrategy, RollingAverageStrategy)
 │    │    ├── rule/                          (SpendingRule, BudgetThresholdRule, LargePurchaseRule)
 │    │    ├── service/                       (SpendingAnalyzer, SavingsAdvisor)
 │    │    ├── storage/                       (CsvStorage)
 │    │    └── ui/                            (Main)
 │    └── test/java/com/budgetwise/           (JUnit 5 Unit Test Suites)
 │         ├── model/AccountTest.java
 │         ├── strategy/StrategyTest.java
 │         ├── rule/SpendingRuleTest.java
 │         ├── service/SavingsAdvisorTest.java
 │         └── storage/CsvStorageTest.java
 │
 ├── 📄 pom.xml                               <-- Maven Build Configuration
 ├── 📄 README.md                             <-- Project Guide & Quickstart
 └── 🛠️ documentation/tools/                  <-- Internal generator scripts (Python)
```

---

## 👥 Team Roles & Ownership Matrix

| Member | Assigned Package / Role | Classes Owned | Key OOP Concepts to Defend |
|:---|:---|:---|:---|
| **Member 1** | **Core Financial Domain** | `Account`, `CheckingAccount`, `CreditAccount`, `Transaction`, `Category` | Abstraction, Inheritance, Polymorphism in `withdraw()`, Immutability, `BigDecimal` precision. |
| **Member 2** | **Spending Analytics & Strategy** | `SpendingStrategy`, `MonthlyTotalStrategy`, `RollingAverageStrategy`, `SpendingAnalyzer` | GoF Strategy Pattern, Open/Closed Principle, Runtime strategy swapping, Rolling averages. |
| **Member 3** | **Budgeting & Rule Watchdog** | `Budget`, `SpendingRule`, `BudgetThresholdRule`, `LargePurchaseRule`, `Alert` | Decoupled Rule Engine, Anomaly detection, Utilization thresholds (80% & 100%), Enums. |
| **Member 4** | **Financial Goals, AI & Storage** | `FinancialGoal`, `SavingsAdvisor`, `CsvStorage`, `Main` | Pacing calculations, Discretionary spending cut suggestions, Standard Java I/O (`BufferedReader`/`PrintWriter`). |

---

## 🚀 How to Run the Application

### Option A: In Apache NetBeans
1. Open **Apache NetBeans**.
2. Select **File &rarr; Open Project...** and choose this `OOP project` directory.
3. Right-click the project &rarr; **Clean and Build**.
4. Right-click &rarr; **Run** (Runs `com.budgetwise.ui.Main`).
5. To execute all unit tests: Right-click &rarr; **Test**.

### Option B: From Command Line (Maven / Java)
```powershell
# Run the application (Interactive menu + 3 automated scenarios)
mvn compile exec:java -Dexec.mainClass="com.budgetwise.ui.Main"

# Run all JUnit 5 tests
mvn test
```

---

## 🎯 The 3 Live Scenarios Demonstrated
1. **Scenario 1 (Cash Floor Invariant):** Safe checking account spending with strict rejection of negative balance.
2. **Scenario 2 (Credit Limit & Alerts):** Excessive credit spending triggering real-time `LargePurchaseRule` and `BudgetThresholdRule` alerts.
3. **Scenario 3 (Strategy Swapping & AI Coaching):** Runtime swap from Monthly Total to 3-Month Rolling Average and AI discretionary cut recommendations.
