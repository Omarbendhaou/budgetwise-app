import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        if self._pageNumber > 1:
            self.drawString(36, 756, "BudgetWise — Individual Member Action Guide & Defense Playbook")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)
            
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 25, text)
        self.drawString(36, 25, "Confidential — UVT Object-Oriented Programming 2026 | Project 4")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 35, 576, 35)
        self.restoreState()

def create_member_pdf(filename, member_name, title, branch, classes_owned, oop_focus, tests, duties, qna):
    base_dir = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\documentation"
    pdf_path = os.path.join(base_dir, filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#1E3A8A")
    secondary_color = colors.HexColor("#0284C7")
    text_dark = colors.HexColor("#1F2937")
    bg_light = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=primary_color, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=14.5,
        textColor=colors.HexColor("#475569"), spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=primary_color, spaceBefore=10, spaceAfter=4
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13.5,
        textColor=secondary_color, spaceBefore=6, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.8, leading=12.5,
        textColor=text_dark, spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=text_dark, leftIndent=12, spaceAfter=2.5
    )
    callout_style = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13,
        textColor=colors.HexColor("#1E293B")
    )
    qa_q_style = ParagraphStyle(
        'QA_Q', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12.5,
        textColor=colors.HexColor("#B91C1C"), spaceBefore=4
    )
    qa_a_style = ParagraphStyle(
        'QA_A', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=colors.HexColor("#15803D"), spaceAfter=5
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph(f"BudgetWise — {member_name} Action Guide", title_style))
    story.append(Paragraph(f"<b>Assigned Role:</b> {title} | Git Branch: <code>{branch}</code> | UVT OOP 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    # Summary Card
    box_content = (
        f"<b>Role Focus:</b> As <b>{title}</b>, you own 25% of the codebase. Your job is to understand your specific classes, "
        f"ensure your unit tests pass, and confidently explain your OOP concepts during the oral defense. This guide gives you "
        f"everything you need to get a 20/20 mark on your section."
    )
    summary_table = Table([[Paragraph(box_content, callout_style)]], colWidths=[540])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    # Section 1: Classes Owned
    story.append(Paragraph("1. Classes & Code You Own", h1_style))
    for cls_name, cls_desc in classes_owned:
        story.append(Paragraph(f"&bull; <b><code>{cls_name}</code>:</b> {cls_desc}", bullet_style))

    # Section 2: Core OOP Principles You Must Defend
    story.append(Paragraph("2. OOP Principles You Demonstrate", h1_style))
    for oop_title, oop_desc in oop_focus:
        story.append(Paragraph(f"&bull; <b>{oop_title}:</b> {oop_desc}", bullet_style))

    # Section 3: Unit Tests
    story.append(Paragraph("3. Your Unit Tests to Run & Show", h1_style))
    for t_file, t_desc in tests:
        story.append(Paragraph(f"&bull; <b><code>{t_file}</code>:</b> {t_desc}", bullet_style))

    story.append(PageBreak())

    # Page 2: Weekly Duties & Oral Defense Questions
    story.append(Paragraph("4. Step-by-Step Checklist for This Week", h1_style))
    for step_num, step_text in duties:
        story.append(Paragraph(f"<b>Step {step_num}:</b> {step_text}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("5. Oral Defense Questions & Winning Answers (Prof Exam Prep)", h1_style))
    story.append(Paragraph("The professor will ask you specific questions about your classes. Memorize these simple, winning answers:", body_style))

    for q, a in qna:
        story.append(Paragraph(f"<b>Q: {q}</b>", qa_q_style))
        story.append(Paragraph(f"<b>Winning Answer:</b> <i>\"{a}\"</i>", qa_a_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated Member PDF: {pdf_path}")

def generate_all_members():
    # -------------------------------------------------------------
    # MEMBER 1: DOMAIN & STORAGE
    # -------------------------------------------------------------
    create_member_pdf(
        filename="BudgetWise_Member1_Guide.pdf",
        member_name="Member 1",
        title="Domain Core & CSV Storage Lead",
        branch="feature/domain-and-storage",
        classes_owned=[
            ("Account.java", "Abstract base class defining shared account state (id, name, balance), deposit logic, and abstract withdraw() contracts."),
            ("CheckingAccount.java", "Subclass enforcing a strict cash balance floor. Rejects withdrawals if amount > balance with an IllegalStateException."),
            ("CreditAccount.java", "Subclass allowing spending into the negative up to a configured credit limit (available funds = balance + creditLimit)."),
            ("Transaction.java", "Strictly immutable entity representing an income or expense. Uses private final fields and scale-2 BigDecimal currency math."),
            ("Category.java", "Enum representing fixed spending categories: FOOD, HOUSING, TRANSPORTATION, ENTERTAINMENT, HEALTHCARE, UTILITIES, OTHER."),
            ("CsvStorage.java", "File persistence utility using standard BufferedReader and PrintWriter to load and save transactions to data/transactions.csv.")
        ],
        oop_focus=[
            ("Inheritance & Polymorphism", "Account is an abstract class with polymorphic withdraw() and canWithdraw() methods overridden differently by CheckingAccount and CreditAccount."),
            ("Encapsulation & Immutability", "Transaction has private final fields and no setters. Once created, a financial transaction can never be altered."),
            ("Data Integrity (BigDecimal)", "Replaces double/float with BigDecimal (RoundingMode.HALF_UP) to prevent IEEE 754 floating-point rounding errors in money.")
        ],
        tests=[
            ("src/test/java/com/budgetwise/model/AccountTest.java", "Verifies deposits, checking account zero-floor rejection, and credit limit overdraft allowance."),
            ("src/test/java/com/budgetwise/storage/CsvStorageTest.java", "Verifies that transactions are correctly written to and read back from a CSV file (round-trip test).")
        ],
        duties=[
            (1, "Clone the repo: <code>git clone https://github.com/Omarbendhaou/budgetwise-app.git</code>"),
            (2, "Create and checkout your branch: <code>git checkout -b feature/domain-and-storage</code>"),
            (3, "Open in NetBeans, Eclipse, or IntelliJ via <b>File -> Import -> Existing Maven Projects</b>."),
            (4, "Run <code>AccountTest.java</code> and <code>CsvStorageTest.java</code> to confirm all green tests."),
            (5, "Push your branch to GitHub and notify Member 4 to open a Pull Request.")
        ],
        qna=[
            ("Why is Account an abstract class instead of a regular class?",
             "Because in real life, a generic 'Account' doesn't exist. You either have a Checking Account or a Credit Card. They have completely different withdrawal rules, so Account defines the template, and subclasses provide the specific withdrawal behavior."),
            ("Why is Transaction immutable?",
             "In accounting and banking systems, an audit trail is critical. Once a transaction is executed, its date, amount, and category must never be modified. Immutability guarantees thread-safety and prevents accidental data tampering."),
            ("Why use BufferedReader instead of Scanner for CSV storage?",
             "BufferedReader is the industry-standard Java class for efficient line-by-line file reading, consuming far less memory overhead than Scanner.")
        ]
    )

    # -------------------------------------------------------------
    # MEMBER 2: BUDGETS & STRATEGY
    # -------------------------------------------------------------
    create_member_pdf(
        filename="BudgetWise_Member2_Guide.pdf",
        member_name="Member 2",
        title="Budgets & Spending Analytics Lead",
        branch="feature/budgets-and-strategy",
        classes_owned=[
            ("Budget.java", "Represents monthly category spending limits (e.g. $400 Food in Nov 2026) and calculates usage percentage."),
            ("SpendingStrategy.java", "The Strategy Pattern interface defining the calculateSpending(month, category, transactions) contract."),
            ("MonthlyTotalStrategy.java", "Concrete strategy that aggregates all expenses occurring within a single calendar month."),
            ("RollingAverageStrategy.java", "Alternative concrete strategy that computes average monthly spending over a 3-month historical window."),
            ("SpendingAnalyzer.java", "Controller holding the active strategy and orchestrating spending calculations across budgets.")
        ],
        oop_focus=[
            ("Strategy Design Pattern", "Decouples the spending calculation algorithm from SpendingAnalyzer. Algorithms can be swapped at runtime via analyzer.setStrategy(...) without modifying SpendingAnalyzer."),
            ("Open/Closed Principle", "New calculation strategies (e.g. YearToDateStrategy) can be added simply by implementing SpendingStrategy without touching existing code."),
            ("Exact Financial Calculations", "Calculates usage percentages and totals with scale-4 BigDecimal math, eliminating precision drift.")
        ],
        tests=[
            ("src/test/java/com/budgetwise/strategy/StrategyTest.java", "Tests that MonthlyTotalStrategy correctly sums November expenses and ignores other months/income, and tests 3-month rolling averages.")
        ],
        duties=[
            (1, "Clone the repo and checkout your branch: <code>git checkout -b feature/budgets-and-strategy</code>"),
            (2, "Import the project into your IDE (NetBeans/Eclipse/IntelliJ)."),
            (3, "Run <code>StrategyTest.java</code> to confirm both strategies calculate accurately."),
            (4, "Understand how <code>Main.java</code> Scenario 3 swaps between the two strategies dynamically at runtime."),
            (5, "Push your branch to GitHub and open your Pull Request.")
        ],
        qna=[
            ("What problem does the Strategy Pattern solve in your project?",
             "Instead of hardcoding spending math inside SpendingAnalyzer with huge if-else blocks, the Strategy Pattern lets us swap between standard monthly totals and multi-month rolling averages dynamically at runtime, keeping the code clean and extensible."),
            ("How does Budget calculate its usage percentage?",
             "It takes the spent amount and divides it by the limit using BigDecimal.divide(limit, 4, RoundingMode.HALF_UP), then multiplies by 100 to get a precise percentage without floating-point errors."),
            ("What happens if you want to add a WeeklySpendingStrategy?",
             "I simply create a new class implementing SpendingStrategy and write calculateSpending(). SpendingAnalyzer does not need a single line of code changed.")
        ]
    )

    # -------------------------------------------------------------
    # MEMBER 3: RULES & AI ADVISOR
    # -------------------------------------------------------------
    create_member_pdf(
        filename="BudgetWise_Member3_Guide.pdf",
        member_name="Member 3",
        title="Rule Engine & AI Decision Support Lead",
        branch="feature/rules-and-advisor",
        classes_owned=[
            ("SpendingRule.java", "Interface defining the rule contract: evaluate(transaction, allTransactions, budget) -> Alert."),
            ("BudgetThresholdRule.java", "Rule that monitors monthly category spending, issuing a WARNING alert at 80% and a CRITICAL alert at 100%+."),
            ("LargePurchaseRule.java", "Rule that flags individual transactions exceeding a configured threshold (e.g. > $150.00)."),
            ("SavingsAdvisor.java", "AI decision support service that analyzes discretionary spending leaks and generates actionable savings advice."),
            ("FinancialGoal.java", "Tracks goal target amounts, saved amounts, deadlines, and calculates required monthly pace: (target - saved) / months."),
            ("Alert.java", "Value object encapsulating the rule name, message, and severity (INFO, WARNING, CRITICAL).")
        ],
        oop_focus=[
            ("Rule Engine Architecture", "Pluggable rule evaluation where SpendingAnalyzer maintains a List<SpendingRule> and runs all active rules polymorphically."),
            ("AI Decision Support Heuristics", "SavingsAdvisor analyzes spending concentration ratios across categories and recommends 25% cuts to fund goals."),
            ("Value Objects & Enums", "Alert and Alert.Severity provide structured, immutable anomaly reporting.")
        ],
        tests=[
            ("src/test/java/com/budgetwise/rule/SpendingRuleTest.java", "Tests that BudgetThresholdRule triggers 80% warnings and 100% critical alerts, and LargePurchaseRule flags > $150 purchases."),
            ("src/test/java/com/budgetwise/service/SavingsAdvisorTest.java", "Tests goal pace calculation ($200/mo needed) and AI category reduction suggestions.")
        ],
        duties=[
            (1, "Clone the repo and checkout your branch: <code>git checkout -b feature/rules-and-advisor</code>"),
            (2, "Import the project into your IDE."),
            (3, "Run <code>SpendingRuleTest.java</code> and <code>SavingsAdvisorTest.java</code>."),
            (4, "Review how Scenario 2 triggers alerts and Scenario 3 generates savings advice in <code>Main.java</code>."),
            (5, "Push your branch and submit your Pull Request.")
        ],
        qna=[
            ("How does your rule engine detect anomalies?",
             "Every rule implements SpendingRule. When runAnalysis() executes, it iterates through registered rules. BudgetThresholdRule sums spending in the transaction's category and compares against the budget limit; LargePurchaseRule checks if the single transaction exceeds $150."),
            ("How does the AI Savings Advisor formulate its recommendations?",
             "First, it calculates the required monthly savings pace: (targetAmount - savedAmount) / monthsRemaining. Then it inspects discretionary categories (Food, Entertainment). If a category represents more than 20% of expenses, it suggests cutting 25% of that spending and computes what percentage of the monthly goal that cut covers."),
            ("How do you add a new rule, like WeekendSpikeRule?",
             "I create a class WeekendSpikeRule implementing SpendingRule, implement evaluate(), and register it with analyzer.addRule(). Nothing else breaks.")
        ]
    )

    # -------------------------------------------------------------
    # MEMBER 4: ARCHITECTURE & UI (USER)
    # -------------------------------------------------------------
    create_member_pdf(
        filename="BudgetWise_Member4_Guide.pdf",
        member_name="Member 4 (You)",
        title="System Architecture & Integration Lead",
        branch="main (Integrator)",
        classes_owned=[
            ("Main.java", "Application entrypoint containing the interactive Scanner menu and automated 3-scenario defense demonstrations."),
            ("pom.xml", "Maven build configuration configuring Java 21 LTS release, compiler plugins, and JUnit 5 Jupiter test dependencies."),
            ("BudgetWise_UML_Diagram.drawio", "Clean 4-column planar UML class diagram with zero line crossings."),
            ("Overall Integration", "Glues together domain models, strategies, rules, CSV persistence, and advisory services.")
        ],
        oop_focus=[
            ("Separation of Concerns", "UI layer handles only presentation; business logic resides strictly in models, strategies, and rules."),
            ("Deterministic Scenario Demos", "Built-in automated execution of the 3 scenarios required by the professor's specification."),
            ("Clean Architecture Coordination", "Ensures build stability, clean Git history, and cohesive integration across all team contributions.")
        ],
        tests=[
            ("All Test Suites", "Runs AccountTest, StrategyTest, SpendingRuleTest, CsvStorageTest, and SavingsAdvisorTest to verify 100% passing tests.")
        ],
        duties=[
            (1, "Publish clean code to GitHub: <code>git push -u origin main</code>"),
            (2, "Distribute the 3 member guide PDFs to your teammates."),
            (3, "Review and merge incoming Pull Requests from feature branches into <code>main</code>."),
            (4, "Lead the final presentation and run <code>Main.java demo</code> during the oral defense.")
        ],
        qna=[
            ("Walk me through the 3 defense scenarios implemented in your project.",
             "Scenario 1 demonstrates normal spending, deposits, and verifies that CheckingAccount rejects an overdraft attempt. Scenario 2 adds a $240 luxury dinner, triggering both a Critical Budget Exceeded alert and a Warning Large Purchase alert. Scenario 3 demonstrates runtime Strategy swapping (Calendar Total to Rolling Average) and generates AI savings advice toward a laptop goal."),
            ("How did you ensure monetary precision across the entire app?",
             "Every single financial calculation uses BigDecimal with scale-2 and RoundingMode.HALF_UP. We strictly banned double/float for money to prevent floating-point rounding errors."),
            ("How was the team organized and coordinated?",
             "We established a modular Git feature-branch workflow. Member 1 owned domain accounts & CSV storage, Member 2 owned budgets & strategy analytics, Member 3 owned the rule engine & AI advisor, and I coordinated architecture, the UI, and final integration.")
        ]
    )

if __name__ == '__main__':
    generate_all_members()
