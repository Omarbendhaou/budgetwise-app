import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
)
from reportlab.pdfgen import canvas

# Professional Executive Palette
C_PRIMARY = colors.HexColor("#1E3A8A")       # Deep Navy
C_SECONDARY = colors.HexColor("#0284C7")     # Ocean Blue
C_ACCENT = colors.HexColor("#0D9488")        # Deep Teal
C_TEXT = colors.HexColor("#1F2937")          # Charcoal
C_MUTED = colors.HexColor("#4B5563")         # Slate Muted
C_LIGHT_BG = colors.HexColor("#F8FAFC")      # Slate 50
C_ALT_ROW = colors.HexColor("#F1F5F9")       # Slate 100
C_BORDER = colors.HexColor("#CBD5E1")        # Slate 300
C_CALLOUT_BORDER = colors.HexColor("#2563EB")# Royal Blue

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        page_w, page_h = letter
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(C_PRIMARY)
            self.drawString(36, page_h - 22, "BudgetWise")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(C_MUTED)
            self.drawString(92, page_h - 22, "|   OOP Project Action Plan v3 (Guaranteed 100% Benchmark Edition)")
            
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(36, page_h - 25, page_w - 36, page_h - 25)

        # Footer (All pages)
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(36, 26, page_w - 36, 26)

        self.setFont("Helvetica", 7.0)
        self.setFillColor(C_MUTED)
        self.drawString(36, 16, "UVT Object-Oriented Programming 2026 | Project 4 (Team of 4) | Final Submission: Dec 1, 2026")
        
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - 36, 16, page_str)
        self.restoreState()

def create_action_plan_pdf(output_path):
    # Total height 792 pt. Top/Bottom margins 30 pt. Usable height = 732 pt.
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=19,
        textColor=C_PRIMARY
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=C_SECONDARY
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=C_MUTED
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=12,
        textColor=C_PRIMARY,
        spaceBefore=5,
        spaceAfter=2.5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=C_SECONDARY,
        spaceBefore=3.5,
        spaceAfter=1.5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.4,
        textColor=C_TEXT
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.6,
        textColor=C_TEXT
    )
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.white
    )
    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.6,
        leading=8.4,
        textColor=C_TEXT
    )
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.3,
        leading=7.8,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    def build_table(headers, data, col_widths):
        table_rows = []
        if headers:
            table_rows.append([Paragraph(h, th_style) for h in headers])
        for row in data:
            formatted_row = []
            for item in row:
                if isinstance(item, str):
                    formatted_row.append(Paragraph(item, td_style))
                elif isinstance(item, Paragraph):
                    formatted_row.append(item)
                else:
                    formatted_row.append(item)
            table_rows.append(formatted_row)

        t = Table(table_rows, colWidths=col_widths, repeatRows=1 if headers else 0)
        t_style = [
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]
        if headers:
            t_style.extend([
                ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 2.5),
                ('TOPPADDING', (0, 0), (-1, 0), 2.5),
            ])
            for i in range(1, len(table_rows)):
                if i % 2 == 0:
                    t_style.append(('BACKGROUND', (0, i), (-1, i), C_ALT_ROW))
        t.setStyle(TableStyle(t_style))
        return t

    # ==================== PAGE 1: TITLE, GOAL, SEC 0 & SEC 1 ====================
    story.append(Paragraph("BudgetWise", title_style))
    story.append(Paragraph("AI-Assisted Personal Finance and Budgeting Application", subtitle_style))
    story.append(Paragraph("<b>Object-Oriented Programming Action Plan & Specification &mdash; Version 3 (Guaranteed 100% Benchmark)</b><br/>"
                           "Team of Four | Java (JDK 21 LTS) | NetBeans + Maven | Console-First | Submission: Dec 1, 2026 | Defense: Dec 1&ndash;3, 2026", meta_style))
    story.append(Spacer(1, 3))

    goal_html = (
        "<b>100% Grade Benchmark Mission:</b> Deliver a small, mathematically rigorous, impeccably decoupled Java application where every "
        "team member can defend their OOP design individually. The architecture directly satisfies all 5 rubric criteria: "
        "<b>(1) OOP Design & UML (25%)</b>, <b>(2) Implementation & Functionality (25%)</b>, <b>(3) Inheritance, Polymorphism, Interfaces & Composition (20%)</b>, "
        "<b>(4) Testing & Edge Cases (15%)</b>, and <b>(5) Extensibility & Documentation (15%)</b>. "
        "Version 3 patches all academic vulnerabilities: domain-level inheritance in <code>Account</code>, fortified architectural ownership for Member 4, "
        "and multi-dimensional contextual intelligence in <code>SavingsAdvisor</code>."
    )
    goal_table = Table([[Paragraph(goal_html, callout_style)]], colWidths=[540])
    goal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_CALLOUT_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(goal_table)
    story.append(Spacer(1, 4))

    # Section 0
    story.append(Paragraph("0. What Changed in Version 3 (Fixing the 3 Academic Vulnerabilities)", h1_style))
    v3_changes = [
        ["Academic Gap Found in v2", "Strategic Engineering Fix in v3", "Rubric & Sec"],
        ["<b>Domain Entity Inheritance Missing:</b> Inheritance only existed in rules and exceptions. Academic evaluators frequently demand domain-level business inheritance.",
         "<b>Created Domain Hierarchy:</b> Abstract <code>Account</code> base class defining <code>canWithdraw()</code>, extended by <code>CheckingAccount</code> (zero-floor) and <code>CreditAccount</code> (credit limit and overdraft rules). Establishes <b>4 genuine hierarchies</b>.",
         "Rubric: 20%<br/>Sec 4, 5"],
        ["<b>Member 4 Defense Vulnerability:</b> Member 4 was assigned UI, integration, and report coordination, leaving them vulnerable to claims of lighter OOP workload.",
         "<b>Fortified Architectural Ownership:</b> Member 4 owns the <code>BudgetWiseApplicationFactory</code> (Dependency Injection / graph assembly) and co-owns <code>FileTransactionRepository</code> (CSV persistence polymorphism).",
         "Rubric: 25%<br/>Sec 7, 13"],
        ["<b>'AI-Assisted' Depth Questionable:</b> Static text templates risk evaluator skepticism regarding intelligent decision support.",
         "<b>Multi-Factor Contextual Advisor:</b> Upgraded <code>SavingsAdvisor</code> to compute spending velocity, category concentration ratios (% of total expenses), historical baseline deviations, and exact slippage on active <code>FinancialGoal</code>s.",
         "Rubric: 25%<br/>Sec 6, 11"],
        ["<b>Persistence Demoted as Stretch:</b> Without persistence, evaluators might consider data handling basic.",
         "<b>Elevated File Repository to Core Tier-1:</b> Dual repository implementations (In-Memory + CSV File) committed to prove runtime polymorphism without changing service logic.",
         "Rubric: 20%<br/>Sec 2, 4"]
    ]
    story.append(build_table(v3_changes[0], v3_changes[1:], [130, 345, 65]))
    story.append(Spacer(1, 4))

    # Section 1
    story.append(Paragraph("1. Define What Finished Means (Requirements & Rubric Alignment)", h1_style))
    req_data = [
        ["Core Requirement [REQ]", "Implementation Architecture", "Verification & Defense Evidence"],
        ["1. Accounts, income, expenses, categories", "<code>Account</code> hierarchy (<code>Checking</code>, <code>Credit</code>), immutable <code>Transaction</code>, <code>Category</code> entity", "Calculated balance with overdraft rules; custom runtime categories"],
        ["2. Budgets by category and period", "Immutable <code>Budget</code> (Category + YearMonth + Limit), <code>BudgetPolicy</code>", "Spent, remaining, exact percentage utilization, state transitions"],
        ["3. Totals & budget usage calculations", "<code>BudgetService</code>, <code>SpendingSummary</code>, exact cross-multiplication", "Monthly category totals, exact utilization percentage, no rounding bias"],
        ["4. Detect unusual spending (transparent rules)", "<code>AbstractSpendingRule</code> hierarchy (Threshold, LargeTransaction, AboveAverage)", "Dynamic alert generation naming the exact numbers, rule name, and severity"],
        ["5. Generate savings suggestions from goals", "<code>SavingsAdvisor</code>, <code>SavingsSuggestionRule</code>, <code>FinancialGoal</code>", "Contextual advice with spending concentration ratio and goal timeline impact"],
        ["6. Alternative categorization & analysis", "Strategy Pattern: <code>TransactionCategorizationStrategy</code> & <code>SpendingAnalysisStrategy</code>", "Zero-downtime runtime strategy switching without modifying service code"]
    ]
    story.append(build_table(req_data[0], req_data[1:], [125, 235, 180]))
    story.append(Spacer(1, 4))

    rubric_data = [
        ["Criterion (Weight)", "How the Architecture Earns Maximum Marks", "Individual Defense Evidence"],
        ["<b>OOP Design & UML (25%)</b>", "Layered architecture, strict SRP, 4 hierarchies, zero God classes, PlantUML synchronized line-by-line with code.", "Present clean PlantUML on screen; explain interface contracts and loose coupling."],
        ["<b>Implementation & Functionality (25%)</b>", "All 6 core requirements fully functional; robust <code>BigDecimal</code> math, deterministic demo suite.", "Execute live scripted Demos A, B, and C with instant reset-to-known-state."],
        ["<b>Inheritance, Polymorphism, Interfaces, Composition (20%)</b>", "<b>Four distinct hierarchies:</b> <code>Account</code>, <code>AbstractSpendingRule</code>, <code>AbstractCategorizationStrategy</code>, and <code>BudgetWiseException</code>. 5 interfaces, runtime strategy swaps.", "Walk through OOP Map (Sec 5) showing file/line numbers for each pillar."],
        ["<b>Testing & Edge Cases (15%)</b>", "Parameterized JUnit 5 suite testing leap years, rounding modes, negative inputs, and immutability.", "Run test suite live; explain a specific edge-case bug caught by a unit test."],
        ["<b>Extensibility & Code Quality (15%)</b>", "Open/Closed Principle proven by adding a new spending rule live in under 5 minutes; clean Javadoc.", "Live demonstration adding <code>WeekendSpendingRule</code> without editing services."]
    ]
    story.append(build_table(rubric_data[0], rubric_data[1:], [115, 275, 150]))

    story.append(PageBreak())

    # ==================== PAGE 2: SCOPE & DECISION LOG ====================
    story.append(Paragraph("2. Scope Control & 4-Tier Layered Architecture", h1_style))
    story.append(Paragraph(
        "<b>Strict Scope Boundary:</b> BudgetWise operates as a local, deterministic financial decision-support engine. "
        "It supports one user, multiple accounts, single base currency (USD/EUR), positive transaction amounts with explicit "
        "income/expense types, and monthly category budgets. It intentionally excludes banking APIs, multi-currency conversion, "
        "and opaque black-box machine learning. Instead, 'AI-assisted' behavior is delivered honestly and transparently as "
        "rule-based intelligent decision support, historical baseline comparison, and automated transaction pattern learning.",
        body_style
    ))
    story.append(Spacer(1, 3))

    arch_box = (
        "<b>Layer 1: Presentation (Console UI)</b> &mdash; <code>ConsoleMenu</code>, input parsers, deterministic demo runner (zero calculations)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&darr; (calls public service methods)<br/>"
        "<b>Layer 2: Application Services & Factory</b> &mdash; <code>TransactionService</code>, <code>BudgetService</code>, <code>SpendingAnalyzer</code>, "
        "<code>SavingsAdvisor</code>, wired via <code>BudgetWiseApplicationFactory</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&darr; (operates on domain entities & evaluates rules)<br/>"
        "<b>Layer 3: Domain Model & Strategy Interfaces</b> &mdash; <code>Account</code> (Checking/Credit), <code>Transaction</code>, <code>Budget</code>, "
        "<code>FinancialGoal</code>, Strategy/Rule contracts<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&darr; (delegates persistence)<br/>"
        "<b>Layer 4: Repositories & Data Source</b> &mdash; In-Memory Repositories + <code>FileTransactionRepository</code> (CSV) behind standard repository contracts"
    )
    arch_table = Table([[Paragraph(arch_box, callout_style)]], colWidths=[540])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Architectural Decisions Locked on Day 1 (Decision Log D1–D12)", h1_style))
    decisions = [
        ["ID", "Architectural Decision", "Design Rationale & OOP Justification"],
        ["<b>D1</b>", "<b>Category is an entity class</b> (id, name, isCustom), not an enum.", "Enums are fixed at compile time. The assignment mandates custom user categories at runtime."],
        ["<b>D2</b>", "<b>Budgets are scoped by Category + YearMonth</b> across accounts.", "Directly matches 'budgets by category and period'; removes unnecessary cross-account complexity."],
        ["<b>D3</b>", "<b>Monetary Math: BigDecimal strictly</b>, scale 2, RoundingMode.HALF_UP, compareTo.", "Floating-point (float/double) produces binary representation errors (e.g. 0.1 + 0.2 != 0.3). compareTo ignores scale difference."],
        ["<b>D4</b>", "<b>Account Domain Inheritance Hierarchy:</b> Abstract <code>Account</code> with <code>canWithdraw()</code>.", "<code>CheckingAccount</code> enforces zero-overdraft; <code>CreditAccount</code> supports credit limits and fees. Genuine business inheritance."],
        ["<b>D5</b>", "<b>Temporal Modeling:</b> <code>LocalDate</code> for transactions, <code>YearMonth</code> for budgets.", "Eliminates time-zone and clock-jitter bugs. Clean boundary testing for first and last days of the month."],
        ["<b>D6</b>", "<b>Strategies return Optional&lt;Category&gt;</b>.", "Clean functional idiom; strategies indicate 'no suggestion' without fabricating dummy entities."],
        ["<b>D7</b>", "<b>BudgetState & AlertSeverity as strict Java enums</b>.", "Ensures compile-time type safety; prevents magic strings in console UI and rules."],
        ["<b>D8</b>", "<b>BudgetPolicy holds threshold (default 80%)</b>; sole source of truth.", "Prevents threshold divergence between service status computation and alert generation."],
        ["<b>D9</b>", "<b>Goal month counting:</b> Current month counts; ceiling rounding for savings.", "<code>RoundingMode.CEILING</code> guarantees savings plan never underfunds a goal."],
        ["<b>D10</b>", "<b>Explicit Clock/Time injection into services and tests</b>.", "Guarantees 100% deterministic unit tests and reproducible grading demonstrations."],
        ["<b>D11</b>", "<b>Deep Immutability:</b> <code>Transaction</code>, <code>Budget</code>, <code>Category</code>, <code>Alert</code>.", "Prevents side effects; state can only change via validated service methods. Defensive copies via <code>List.copyOf</code>."],
        ["<b>D12</b>", "<b>Dual Repository Implementations (In-Memory + CSV File)</b>.", "Demonstrates structural polymorphism; validates Open/Closed Principle for storage."]
    ]
    story.append(build_table(decisions[0], decisions[1:], [25, 235, 280]))

    story.append(PageBreak())

    # ==================== PAGE 3: STUBS & OOP PILLARS ====================
    story.append(Paragraph("4. Responsibilities & Shared Contracts (Day 1 Compilable Stubs)", h1_style))
    story.append(Paragraph("To enable 4 developers to work in parallel without merge conflicts, these shared interfaces are committed on Day 1:", body_style))
    story.append(Spacer(1, 2))

    stubs_text = (
        "<b>// 1. Account Domain Base Class</b><br/>"
        "public abstract class Account {<br/>"
        "&nbsp;&nbsp;private final String id, name; private final BigDecimal openingBalance;<br/>"
        "&nbsp;&nbsp;public abstract boolean canWithdraw(BigDecimal amount, BigDecimal currentBalance);<br/>"
        "&nbsp;&nbsp;public abstract BigDecimal calculateAvailableFunds(BigDecimal currentBalance);<br/>"
        "}<br/>"
        "<b>// 2. Transaction Categorization Strategy Contract</b><br/>"
        "public interface TransactionCategorizationStrategy {<br/>"
        "&nbsp;&nbsp;Optional&lt;Category&gt; categorize(String description, List&lt;Transaction&gt; history);<br/>"
        "&nbsp;&nbsp;String getStrategyName();<br/>"
        "}<br/>"
        "<b>// 3. Spending Analysis Strategy Contract</b><br/>"
        "public interface SpendingAnalysisStrategy {<br/>"
        "&nbsp;&nbsp;SpendingSummary analyze(YearMonth month, List&lt;Transaction&gt; allTransactions);<br/>"
        "}<br/>"
        "<b>// 4. Spending Rule Contract & Template Base</b><br/>"
        "public interface SpendingRule {<br/>"
        "&nbsp;&nbsp;String name();<br/>"
        "&nbsp;&nbsp;List&lt;Alert&gt; evaluate(AnalysisContext context);<br/>"
        "}<br/>"
        "public abstract class AbstractSpendingRule implements SpendingRule {<br/>"
        "&nbsp;&nbsp;private final String name; private boolean enabled = true;<br/>"
        "&nbsp;&nbsp;public final List&lt;Alert&gt; evaluate(AnalysisContext context) {<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if (!enabled) return List.of();<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return doEvaluate(context); // Template Method Pattern<br/>"
        "&nbsp;&nbsp;}<br/>"
        "&nbsp;&nbsp;protected abstract List&lt;Alert&gt; doEvaluate(AnalysisContext context);<br/>"
        "}<br/>"
        "<b>// 5. Intelligent Savings Suggestion Rule Contract</b><br/>"
        "public interface SavingsSuggestionRule {<br/>"
        "&nbsp;&nbsp;List&lt;SavingsRecommendation&gt; suggest(AnalysisContext ctx, List&lt;FinancialGoal&gt; goals, YearMonth current);<br/>"
        "}<br/>"
        "<b>// 6. Generic Repository & Concrete Transaction Repository</b><br/>"
        "public interface TransactionRepository {<br/>"
        "&nbsp;&nbsp;void save(Transaction transaction);<br/>"
        "&nbsp;&nbsp;List&lt;Transaction&gt; findAll();<br/>"
        "&nbsp;&nbsp;List&lt;Transaction&gt; findByMonth(YearMonth month);<br/>"
        "&nbsp;&nbsp;List&lt;Transaction&gt; findByAccount(String accountId);<br/>"
        "}<br/>"
        "<b>// 7. Architectural Factory & Dependency Injection Wiring (Member 4 Ownership)</b><br/>"
        "public interface BudgetWiseApplicationFactory {<br/>"
        "&nbsp;&nbsp;TransactionService createTransactionService();<br/>"
        "&nbsp;&nbsp;BudgetService createBudgetService();<br/>"
        "&nbsp;&nbsp;SpendingAnalyzer createSpendingAnalyzer(SpendingAnalysisStrategy strategy);<br/>"
        "&nbsp;&nbsp;SavingsAdvisor createSavingsAdvisor();<br/>"
        "}"
    )
    stubs_table = Table([[Paragraph(stubs_text, code_style)]], colWidths=[540])
    stubs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.75, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(stubs_table)
    story.append(Spacer(1, 3))

    exc_text = (
        "<b>Domain Exception Hierarchy:</b> <code>BudgetWiseException</code> (base <code>RuntimeException</code>) &rarr; "
        "<code>ValidationException</code>, <code>InsufficientFundsException</code>, <code>DuplicateBudgetException</code>, <code>EntityNotFoundException</code>."
    )
    story.append(Paragraph(exc_text, body_style))
    story.append(Spacer(1, 4))

    # Section 5
    story.append(Paragraph("5. Making OOP Pillars Explicit & Defensible", h1_style))
    oop_map = [
        ["OOP Pillar", "Concrete Implementation in BudgetWise v3", "Oral Defense Justification"],
        ["<b>Inheritance 1: Domain Entities</b>", "<code>Account</code> (abstract base) extended by <code>CheckingAccount</code> and <code>CreditAccount</code>.", "Encapsulates shared identity/balance tracking while enforcing distinct withdrawal authorization policies."],
        ["<b>Inheritance 2: Rules (Template Method)</b>", "<code>AbstractSpendingRule</code> extended by <code>BudgetThresholdRule</code>, <code>LargeTransactionRule</code>, <code>AboveAverageRule</code>, <code>WeekendSpendingRule</code>.", "Eliminates boilerplate enable/disable checks across all rules. Template method guarantees disabled rules never fire."],
        ["<b>Inheritance 3: Strategy Helpers</b>", "<code>AbstractCategorizationStrategy</code> extended by <code>KeywordCategorizationStrategy</code> and <code>MerchantHistoryStrategy</code>.", "Guarantees unified text normalization (trim, lowercase, whitespace collapsing) across all text-matching algorithms."],
        ["<b>Inheritance 4: Exceptions</b>", "<code>BudgetWiseException</code> extended by 4 specialized domain exceptions.", "Allows clean multi-catch blocks; callers handle specific recovery or generic presentation."],
        ["<b>Polymorphism (Runtime Swapping)</b>", "1. <code>SpendingAnalyzer</code> loops over <code>List&lt;SpendingRule&gt;</code>.<br/>2. <code>TransactionService</code> invokes whichever categorizer is injected.<br/>3. Repositories swapped (In-Memory &harr; File) without changing services.", "The exact same method call executes radically different code at runtime depending on the injected object."],
        ["<b>Composition & Delegation</b>", "1. <code>SpendingAnalyzer</code> is composed of rules and a strategy.<br/>2. <code>SavingsAdvisor</code> is composed of suggestion rules.<br/>3. Services receive repositories via constructor injection.", "Promotes high cohesion and low coupling. Every component can be unit-tested in isolation using mock collaborators."],
        ["<b>Encapsulation & Immutability</b>", "Private final fields, no setters, defensive copying via <code>List.copyOf</code>, immutable value records (<code>Transaction</code>, <code>Budget</code>, <code>Alert</code>).", "Invalid state cannot exist. Once constructed, financial records cannot be tampered with by external classes."]
    ]
    story.append(build_table(oop_map[0], oop_map[1:], [110, 240, 190]))
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Academic Justification (Where We Refused to Force Inheritance):</b> "
        "A key sign of OOP maturity is knowing when <b>not</b> to use inheritance. We explicitly chose not to create "
        "<code>IncomeTransaction</code> and <code>ExpenseTransaction</code> subclasses because income and expense differ only by direction "
        "and category, not by behavior. A <code>TransactionType</code> enum with signed arithmetic multipliers represents this honestly. "
        "Adding empty subclasses with no unique behavior is an anti-pattern ('lazy class') that we avoid and defend in our report.",
        body_style
    ))

    story.append(PageBreak())

    # ==================== PAGE 4: BUSINESS RULES & WORKLOAD ====================
    story.append(Paragraph("6. Precise Business Rules & Enhanced 'AI-Assisted' Logic", h1_style))
    biz_rules_table = [
        ["Domain Area", "Exact Mathematical & Logical Specification", "Edge-Case Safeguard"],
        ["<b>Currency Math</b>", "<code>BigDecimal</code> scale 2, <code>RoundingMode.HALF_UP</code>. Comparison strictly via <code>compareTo() == 0</code>, never <code>equals()</code>.", "Rejects amounts with &gt;2 decimals. Balance = Opening + Income &minus; Expenses."],
        ["<b>Budget Utilization & State</b>", "Utilization % = <code>spent * 100 / limit</code>.<br/>State boundary evaluated by exact cross-multiplication:<br/>&bull; NORMAL: <code>spent * 100 &lt; limit * 80</code><br/>&bull; WARNING: <code>spent * 100 &ge; limit * 80 and spent &le; limit</code><br/>&bull; LIMIT_REACHED: <code>spent.compareTo(limit) == 0</code><br/>&bull; EXCEEDED: <code>spent.compareTo(limit) &gt; 0</code>", "Cross-multiplication prevents floating-point rounding from flipping state thresholds (e.g., limit of 0.03)."],
        ["<b>Categorization Precedence</b>", "Precedence: (1) Manual user override &rarr; (2) Injected Strategy &rarr; (3) Fallback to 'Uncategorized'.", "Manual entry always wins; strategy failure never crashes the transaction pipeline."],
        ["<b>Categorization Strategies</b>", "&bull; <b>Keyword:</b> Case-insensitive normalized substring search against configured map.<br/>&bull; <b>Merchant History:</b> Learns from past manual transactions; reuses most recent category for identical normalized merchant description.", "Tie-break rule: first configured keyword wins; empty merchant history returns <code>Optional.empty()</code> safely."],
        ["<b>Enhanced 'AI' Savings Advisor</b>", "Calculates multi-factor contextual recommendations:<br/>1. <b>Concentration Ratio:</b> Category expense as % of total monthly spending.<br/>2. <b>Spending Velocity:</b> Daily burn rate vs historical 3-month baseline.<br/>3. <b>Goal Timeline Impact:</b> Shows how trimming overspending advances the target date of active <code>FinancialGoal</code>s.", "Never produces vague text. Every recommendation includes exact dollar cut, percentage context, and goal linkage."]
    ]
    story.append(build_table(biz_rules_table[0], biz_rules_table[1:], [90, 275, 175]))
    story.append(Spacer(1, 4))

    # Section 7
    story.append(Paragraph("7. Balanced Workload Allocation & Oral Defense Armor", h1_style))
    team_data = [
        ["Member", "Core OOP Ownership (Primary Modules)", "Testing & Verification Responsibility", "Individual Defense Focal Point"],
        ["<b>Member 1</b>", "<b>Core Financial Domain & Storage:</b><br/><code>Account</code> hierarchy (<code>Checking</code>, <code>Credit</code>), <code>Transaction</code>, <code>TransactionType</code>, <code>Category</code>, <code>InMemoryTransactionRepository</code>, Exception hierarchy.", "Validation tests, balance calculation, immutability tests, account overdraft rules.", "Defends domain inheritance, defensive copying, and custom exception handling."],
        ["<b>Member 2</b>", "<b>Budgeting & Trend Analysis:</b><br/><code>Budget</code>, <code>BudgetPolicy</code>, <code>BudgetService</code>, <code>BudgetStatus</code>, <code>SpendingSummary</code>, both <code>SpendingAnalysisStrategy</code> implementations (Monthly vs Rolling).", "Threshold boundary tests, leap year handling, baseline computation with 0-3 months history.", "Defends the Strategy pattern for analysis and cross-multiplication threshold logic."],
        ["<b>Member 3</b>", "<b>Intelligence & Rules Engine:</b><br/><code>AbstractSpendingRule</code> hierarchy (Threshold, Large, AboveAverage), <code>SpendingAnalyzer</code>, <code>AbstractCategorizationStrategy</code> hierarchy, <code>SavingsAdvisor</code>.", "Rule triggering tests, disabled-rule safety, strategy switching, contextual advisor output.", "Defends the Template Method pattern, keyword/history categorization, and suggestion logic."],
        ["<b>Member 4</b>", "<b>Architecture, Persistence & Integration:</b><br/><code>BudgetWiseApplicationFactory</code> (dependency injection / wiring), <code>FileTransactionRepository</code> (CSV persistence), <code>ConsoleMenu</code>, demo runner.", "Clean-clone build, end-to-end integration scenarios A/B/C, CSV round-trip tests.", "Defends the Factory pattern, Dependency Inversion, and polymorphic file persistence."]
    ]
    story.append(build_table(team_data[0], team_data[1:], [55, 185, 150, 150]))
    story.append(Spacer(1, 3))

    defense_rehearsal = (
        "<b>Defense Readiness Protocols:</b><br/>"
        "&bull; <b>Cross-Module Walkthroughs (Nov 24 & Nov 29):</b> Each member spends 10 minutes explaining another member's code while the owner observes.<br/>"
        "&bull; <b>Mock Defense Rounds (Nov 29 & Nov 30):</b> The team uses the Section 13 Question Bank to grill each member under exam conditions.<br/>"
        "&bull; <b>Golden Rule:</b> Every single member must be capable of running all 3 live demos, adding a new rule from scratch, and explaining where polymorphism occurs."
    )
    story.append(Paragraph(defense_rehearsal, body_style))
    story.append(Spacer(1, 4))

    # Section 8
    story.append(Paragraph("8. Collaboration, Git & NetBeans Configuration", h1_style))
    collab_box = (
        "<b>Repository Layout:</b> Single shared GitHub repository. NetBeans + Maven structure:<br/>"
        "<code>pom.xml</code> | <code>src/main/java/com/budgetwise/{app, ui, model, service, strategy, rule, repository, exception}</code><br/>"
        "<code>src/test/java/com/budgetwise/...</code> | <code>docs/ (UML diagrams, report)</code> | <code>sample-data/ (CSV seeds)</code><br/>"
        "<b>Git Workflow:</b> <code>main</code> branch is always compilable. Short-lived feature branches (e.g. <code>feat/account-hierarchy</code>). "
        "Pull requests require at least one peer review. Definition of Done: compiles, Javadoc on public methods, 100% tests passing."
    )
    story.append(Paragraph(collab_box, body_style))

    story.append(PageBreak())

    # ==================== PAGE 5: SCHEDULE, TESTS & DEMOS ====================
    story.append(Paragraph("9. Dated Master Schedule (Nov 16 to Dec 1, 2026)", h1_style))
    schedule_data = [
        ["Date Window", "Phase Focus", "Key Deliverables & Milestones", "Exit Criteria (Verification)"],
        ["<b>Nov 16 &ndash; Nov 17</b>", "Contracts & Setup", "Agree on D1–D12; commit compilable interface stubs; draw UML v0; initialize Maven in NetBeans.", "All 4 members clone, build, and run green dummy test."],
        ["<b>Nov 18 &ndash; Nov 21</b>", "Core Domain & Repos", "Account hierarchy, transactions, in-memory & CSV repos, budget calculation, console skeleton.", "Thu Nov 19: First Integration Milestone (add expense, see balance)."],
        ["<b>Nov 22 &ndash; Nov 25</b>", "Strategies & Rules", "Both categorizers, both analyzers, spending rules, enhanced savings advisor; Module Rotation 1.", "Tue Nov 24: Demo B runs end-to-end; first cross-module review."],
        ["<b>Nov 26 &ndash; Nov 27</b>", "Integration & Polish", "Connect ConsoleMenu to Factory; test reset-demo-data; verify CSV save/load; complete test suite.", "<b>Fri Nov 27, 20:00: Hard Feature Freeze.</b> Only bug fixes & docs."],
        ["<b>Nov 28 &ndash; Nov 30</b>", "Verification & Report", "Final UML reconciliation against code; write project report; conduct 2 rounds of Mock Defenses.", "<b>Mon Nov 30: Final Submission on UVT platform</b> (24h early)."],
        ["<b>Dec 1 &ndash; Dec 3</b>", "Project Defense", "Individual oral defense examinations before the course grading panel.", "Flawless individual demonstrations and conceptual explanations."]
    ]
    story.append(build_table(schedule_data[0], schedule_data[1:], [80, 100, 220, 140]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("10. Comprehensive Unit & Integration Test Matrix", h1_style))
    test_matrix = [
        ["Testing Domain", "Target Component", "High-Priority Edge Cases & Boundary Conditions Tested"],
        ["<b>Financial Math</b>", "<code>Account</code>, <code>Transaction</code>", "Reject negative amounts; reject 3+ decimal places; compareTo equality (2.0 vs 2.00); zero balance handling; overdraft limit enforcement in <code>CreditAccount</code>."],
        ["<b>Budget Boundaries</b>", "<code>BudgetService</code>", "Spent exactly 80.00% (triggers WARNING); spent 79.99% (NORMAL); spent 100.00% (LIMIT_REACHED); spent 100.01% (EXCEEDED); small budget of 0.03."],
        ["<b>Temporal Boundaries</b>", "<code>SpendingSummary</code>", "Transactions on 1st day of month; last day of month; leap year (Feb 29, 2028); non-leap year (Feb 28, 2027); filtering out neighboring month transactions."],
        ["<b>Categorization</b>", "Strategies", "Case & whitespace normalization; keyword tie-breaks; merchant history exact match; empty merchant history; manual user override takes absolute precedence."],
        ["<b>Rules & Anomaly</b>", "<code>SpendingAnalyzer</code>", "Disabled rule produces zero alerts; exact multiplier boundary (e.g. 2.0x average); alert text verification contains exact calculated dollar values."],
        ["<b>Persistence</b>", "<code>FileTransactionRepository</code>", "CSV round-trip serialization/deserialization; missing file recovery; corrupted CSV line handling; parity with in-memory repository."],
        ["<b>Integration Scenario</b>", "Full Application", "The assignment's benchmark scenario: $300 Dining budget, $290 spent (WARNING), add $50 expense &rarr; $340 spent, EXCEEDED alert, and actionable advice."]
    ]
    story.append(build_table(test_matrix[0], test_matrix[1:], [90, 110, 340]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("11. Scripted Live Demonstration Flows (A, B, C)", h1_style))
    demo_box = (
        "<b>Demo A: Normal Lifecycle & Multi-Account Operations</b><br/>"
        "1. Initialize with deterministic demo dataset (Checking Account with $1,500, Credit Account with $500 limit).<br/>"
        "2. Record income ($2,000) and set a monthly 'Groceries' budget of $400.00.<br/>"
        "3. Add two grocery expenses totaling $160.00 &rarr; display status: $240.00 remaining, 40% utilization, state <code>NORMAL</code>.<br/><br/>"
        "<b>Demo B: The Assignment Scenario (Overspending, Contextual Alerts & Advice)</b><br/>"
        "1. Set 'Dining' budget of $300.00. Load existing dining expenses of $290.00 &rarr; display state <code>WARNING</code> (96.7%).<br/>"
        "2. Add a new $50.00 restaurant transaction &rarr; display state <code>EXCEEDED</code> ($340.00 spent, $40.00 over budget).<br/>"
        "3. Trigger Analysis & Advisor &rarr; generates <code>CRITICAL</code> alert and contextual savings advice: "
        "<i>'Dining represents 52% of this month's expenses. Trimming $40.00 returns you to limit and secures your $100/mo Emergency Fund goal.'</i><br/><br/>"
        "<b>Demo C: Extensibility & Runtime Polymorphism Showcase</b><br/>"
        "1. Categorize transaction 'Starbucks Coffee' using <code>KeywordCategorizationStrategy</code> &rarr; matches 'Dining'.<br/>"
        "2. Switch live to <code>MerchantHistoryStrategy</code> &rarr; automatically adapts based on previous manual entries.<br/>"
        "3. Switch analysis strategy from <code>MonthlyTotalAnalysis</code> to <code>RollingAverageAnalysis</code> &rarr; shows <code>AboveAverageRule</code> firing.<br/>"
        "4. <b>Live Extension:</b> Register <code>WeekendSpendingRule</code> into the engine live to prove the Open/Closed Principle."
    )
    story.append(Paragraph(demo_box, body_style))

    story.append(PageBreak())

    # ==================== PAGE 6: REPORT, DEFENSE CHEAT SHEET & CHECKLIST ====================
    story.append(Paragraph("12. UML Class Diagram & Final Report Checklist", h1_style))
    story.append(Paragraph(
        "<b>UML Diagram Standards:</b> Drawn in PlantUML with source maintained in <code>docs/budgetwise.puml</code>. "
        "Must feature: (1) Standard visibility markers (<code>+</code>, <code>-</code>, <code>#</code>), (2) Stereotypes "
        "<code>&lt;&lt;interface&gt;&gt;</code> and realization dashed arrows with closed hollow heads, (3) Generalization solid arrows "
        "for the 4 inheritance hierarchies, (4) Composition (filled diamonds) where lifecycle is owned (e.g. <code>SpendingAnalyzer</code> owns rules), "
        "and (5) Dependency dashed arrows from services to repositories and strategies. Checked line-by-line against code on Nov 28.<br/>"
        "<b>Report Structure (Target: 8–10 pages):</b> 1. Purpose & Honest AI Statement | 2. Requirements Mapping | "
        "3. Architecture & Decision Log (D1–D12) | 4. Responsibilities of Core Classes | 5. OOP Concepts with Source References | "
        "6. Business & Analysis Rules | 7. Test Strategy & Results | 8. Extensibility Walkthrough (Adding a new Strategy & Rule) | "
        "9. Limitations & Future Work | 10. Individual Team Contributions & Defense Sign-off.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("13. Oral Defense Cheat Sheet (Anticipated Professor Questions & Exact Answers)", h1_style))
    defense_qa = [
        ["Anticipated Grader Question", "Model Answer Demonstrating 100% Mastery"],
        ["<b>Why did you use inheritance for Account instead of a field?</b>", "Checking and Credit accounts have genuinely different business logic for withdrawal authorization. <code>CheckingAccount</code> rejects transactions that drop balance below zero, while <code>CreditAccount</code> evaluates against a credit limit and applies overdraft rules. This demonstrates behavioral polymorphism."],
        ["<b>Where is polymorphism demonstrated at runtime?</b>", "In three places: (1) <code>SpendingAnalyzer</code> iterates over <code>List&lt;SpendingRule&gt;</code> calling <code>evaluate()</code>, (2) <code>TransactionService</code> invokes whichever <code>TransactionCategorizationStrategy</code> was injected at runtime, and (3) Repositories can swap from In-Memory to CSV File without changing a line of service code."],
        ["<b>Why use BigDecimal instead of double? Why compareTo()?</b>", "Binary floating-point cannot accurately represent decimal fractions like 0.1, creating rounding errors in financial balances. We use <code>compareTo()</code> because <code>equals()</code> checks both value and scale (e.g., 2.0 != 2.00 in equals, but compareTo returns 0)."],
        ["<b>How does your design respect the Open/Closed Principle?</b>", "To add a new spending rule (e.g., <code>WeekendSpendingRule</code>) or a new categorization strategy, we simply implement the interface and register it in the <code>ApplicationFactory</code>. No existing service, repository, or UI code is modified."],
        ["<b>Why is the AI component described as rule-based?</b>", "To remain academically honest and transparent. Real-world financial systems avoid opaque black-box models for compliance. BudgetWise provides deterministic decision support: explainable rule engines, dynamic concentration ratios, and historical baseline deviations."],
        ["<b>How does Member 4's Factory pattern improve the code?</b>", "The <code>BudgetWiseApplicationFactory</code> centralizes dependency instantiation and wiring. Services depend strictly on interface abstractions, not concrete classes (Dependency Inversion Principle), allowing effortless testing with mocks and runtime strategy reconfiguration."]
    ]
    story.append(build_table(defense_qa[0], defense_qa[1:], [150, 390]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("14. Day 1 Immediate Action Checklist (Nov 16–17)", h1_style))
    checklist_box = (
        "&check; <b>Step 1:</b> Create GitHub repo <code>budgetwise-oop</code>, add <code>.gitignore</code> (Java/Maven/NetBeans), invite all 4 members.<br/>"
        "&check; <b>Step 2:</b> Initialize Maven project with JDK 21 and JUnit Jupiter 5.10.x dependencies in <code>pom.xml</code>.<br/>"
        "&check; <b>Step 3:</b> Commit the compilable Day 1 interface stubs from Section 4 and push to <code>main</code>.<br/>"
        "&check; <b>Step 4:</b> Verify that all 4 members can pull, build with <code>mvn clean compile</code>, and execute one passing dummy test.<br/>"
        "&check; <b>Step 5:</b> Create feature branches: <code>feat/member1-accounts</code>, <code>feat/member2-budgets</code>, <code>feat/member3-rules</code>, <code>feat/member4-factory-ui</code>.<br/>"
        "&check; <b>Step 6:</b> Book team calendar for Nov 19 (Integration Milestone 1), Nov 24 (Module Rotation 1), and Nov 29 (Mock Defense)."
    )
    story.append(Paragraph(checklist_box, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Action plan PDF generated successfully at: {output_path}")

if __name__ == '__main__':
    target_path = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\BudgetWise_Action_Plan_v3_Guaranteed_100.pdf"
    create_action_plan_pdf(target_path)
