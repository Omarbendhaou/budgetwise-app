import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

# Palette
C_PRIMARY = colors.HexColor("#1E3A8A")       # Deep Navy
C_SECONDARY = colors.HexColor("#0284C7")     # Ocean Blue
C_ACCENT = colors.HexColor("#0D9488")        # Deep Teal
C_TEXT = colors.HexColor("#1F2937")          # Charcoal
C_MUTED = colors.HexColor("#4B5563")         # Slate Muted
C_LIGHT_BG = colors.HexColor("#F8FAFC")      # Slate 50
C_ALT_ROW = colors.HexColor("#F1F5F9")       # Slate 100
C_BORDER = colors.HexColor("#CBD5E1")        # Slate 300
C_CALLOUT_BORDER = colors.HexColor("#2563EB")# Royal Blue
C_SUCCESS_BG = colors.HexColor("#ECFDF5")    # Mint
C_SUCCESS_BORDER = colors.HexColor("#10B981")# Emerald

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
            self.drawString(36, page_h - 22, getattr(self, 'doc_title_short', 'BudgetWise'))
            self.setFont("Helvetica", 7.5)
            self.setFillColor(C_MUTED)
            self.drawString(140, page_h - 22, "|   Individual Member Execution Playbook — UVT OOP 2026")
            
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(36, page_h - 25, page_w - 36, page_h - 25)

        # Footer (All pages)
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(36, 26, page_w - 36, 26)

        self.setFont("Helvetica", 7.0)
        self.setFillColor(C_MUTED)
        self.drawString(36, 16, "BudgetWise Project 4 | Submission: Dec 1, 2026 | Oral Defense: Dec 1-3, 2026")
        
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - 36, 16, page_str)
        self.restoreState()

def get_styles():
    styles = getSampleStyleSheet()
    return {
        'title': ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=17, leading=20, textColor=C_PRIMARY),
        'subtitle': ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12.5, textColor=C_SECONDARY),
        'meta': ParagraphStyle('DocMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=C_MUTED),
        'h1': ParagraphStyle('SectionH1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12.5, textColor=C_PRIMARY, spaceBefore=5, spaceAfter=2.5, keepWithNext=True),
        'h2': ParagraphStyle('SectionH2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=C_SECONDARY, spaceBefore=3.5, spaceAfter=1.5, keepWithNext=True),
        'body': ParagraphStyle('BodyDark', parent=styles['Normal'], fontName='Helvetica', fontSize=7.3, leading=9.6, textColor=C_TEXT),
        'callout': ParagraphStyle('CalloutText', parent=styles['Normal'], fontName='Helvetica', fontSize=7.3, leading=9.6, textColor=C_TEXT),
        'th': ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.white),
        'td': ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=6.6, leading=8.4, textColor=C_TEXT),
        'code': ParagraphStyle('CodeSnippet', parent=styles['Normal'], fontName='Courier', fontSize=6.3, leading=7.8, textColor=colors.HexColor("#0F172A"))
    }

def build_table(headers, data, col_widths, s):
    table_rows = []
    if headers:
        table_rows.append([Paragraph(h, s['th']) for h in headers])
    for row in data:
        formatted_row = []
        for item in row:
            if isinstance(item, str):
                formatted_row.append(Paragraph(item, s['td']))
            elif isinstance(item, Paragraph):
                formatted_row.append(item)
            else:
                formatted_row.append(item)
        table_rows.append(formatted_row)

    t = Table(table_rows, colWidths=col_widths, repeatRows=1 if headers else 0)
    t_style = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
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

# ==============================================================================
# 1. MEMBER 1 PDF
# ==============================================================================
def generate_member1_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=30)
    s = get_styles()
    story = []

    story.append(Paragraph("BudgetWise: Member 1 Playbook", s['title']))
    story.append(Paragraph("Core Domain Entities, Account Hierarchy & In-Memory Storage", s['subtitle']))
    story.append(Paragraph("<b>Git Branch:</b> <code>feat/member1-domain</code> | <b>Review Partner:</b> Member 2 (Pair Alpha) | <b>Deadline:</b> Dec 1, 2026", s['meta']))
    story.append(Spacer(1, 4))

    box = (
        "<b>Your Executive Role:</b> You are the <b>Financial Domain Modeler & Storage Specialist</b>. "
        "You own the fundamental entities of the application (<code>Account</code>, <code>Transaction</code>, <code>Category</code>) "
        "and the <code>InMemoryTransactionRepository</code>. Your biggest architectural contribution to the group's 100% grade "
        "is the <b>Account Domain Inheritance Hierarchy</b>, which demonstrates genuine behavioral polymorphism in withdrawal validation."
    )
    t_box = Table([[Paragraph(box, s['callout'])]], colWidths=[540])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_CALLOUT_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Files You Own & What to Build in Each", s['h1']))
    files_data = [
        ["Class / Interface File", "Package", "Your Concrete Responsibilities & Tasks"],
        ["<code>Account.java</code> (abstract)", "<code>com.budgetwise.model</code>", "Defines shared account state (id, name, openingBalance) and abstract methods <code>canWithdraw()</code> and <code>calculateAvailableFunds()</code>."],
        ["<code>CheckingAccount.java</code>", "<code>com.budgetwise.model</code>", "Implements strict zero-floor withdrawal validation. Rejects transactions dropping balance below zero."],
        ["<code>CreditAccount.java</code>", "<code>com.budgetwise.model</code>", "Implements credit limit logic. Validates withdrawals up to <code>openingBalance + creditLimit</code>. Tracks overdraft status."],
        ["<code>Transaction.java</code>", "<code>com.budgetwise.model</code>", "Enforces deep immutability, scale-2 <code>BigDecimal</code> amounts, positive values, and signed arithmetic via <code>TransactionType</code>."],
        ["<code>Category.java</code>", "<code>com.budgetwise.model</code>", "Supports custom categories created at runtime; implements <code>equals()</code>/<code>hashCode()</code> and holds static <code>UNCATEGORIZED</code>."],
        ["<code>InMemoryTransactionRepo</code>", "<code>com.budgetwise.repository</code>", "Thread-safe repository using <code>ConcurrentHashMap</code> for storage; filters by account and YearMonth."],
        ["<code>BudgetWiseException</code> suite", "<code>com.budgetwise.exception</code>", "Creates base unchecked exception and specialized domain subclasses (<code>ValidationException</code>, <code>InsufficientFundsException</code>)."]
    ]
    story.append(build_table(files_data[0], files_data[1:], [130, 110, 300], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2. Step-by-Step Execution Roadmap (Sprint by Sprint)", s['h1']))
    roadmap = [
        ["Phase / Date", "Sprint Target", "Deliverables & Verification Steps"],
        ["<b>Sprint 1 (Nov 16&ndash;19)</b>", "<b>Domain Validation & Setup</b>", "1. Clone repo, checkout <code>feat/member1-domain</code>.<br/>2. Add strict constructor validations (reject negative amounts, reject >2 decimal places).<br/>3. <b>Milestone 1 (Thu Nov 19):</b> Verify account creation and transaction recording run end-to-end."],
        ["<b>Sprint 2 (Nov 20&ndash;24)</b>", "<b>Overdraft Rules & Storage</b>", "1. Refine <code>CreditAccount</code> with configurable credit limit and fee deduction.<br/>2. Optimize <code>InMemoryTransactionRepository</code> with fast month-indexed lookups.<br/>3. Review Member 2's budget PRs; participate in <b>Module Rotation #1 (Tue Nov 24)</b>."],
        ["<b>Sprint 3 (Nov 25&ndash;27)</b>", "<b>Unit Testing & Hardening</b>", "1. Write parameterized tests for amounts, rounding, and negative inputs.<br/>2. Reach 100% green test suite before <b>Feature Freeze (Fri Nov 27, 20:00)</b>."],
        ["<b>Final (Nov 28&ndash;30)</b>", "<b>Report & Defense Rehearsal</b>", "1. Write Report Section 4 & 5 (Domain entities and exception hierarchy).<br/>2. Rehearse oral defense questions with Member 2."]
    ]
    story.append(build_table(roadmap[0], roadmap[1:], [90, 110, 340], s))

    story.append(PageBreak())

    story.append(Paragraph("3. Unit Tests You Must Write to Guarantee 15% Test Marks", s['h1']))
    story.append(Paragraph("You own <code>AccountHierarchyTest.java</code> and <code>TransactionValidationTest.java</code>. Implement these exact cases:", s['body']))
    story.append(Spacer(1, 2))

    tests_data = [
        ["Test Case Method Name", "Scenario Tested", "Expected Assertion"],
        ["<code>shouldRejectWithdrawalWhenCheckingBalanceZero()</code>", "Withdraw 10.00 from CheckingAccount with 0.00 balance.", "<code>canWithdraw()</code> returns <code>false</code>."],
        ["<code>shouldAllowOverdraftUpToCreditLimit()</code>", "Withdraw 450.00 from CreditAccount with 0.00 balance and 500.00 limit.", "<code>canWithdraw()</code> returns <code>true</code>."],
        ["<code>shouldRejectOverdraftBeyondCreditLimit()</code>", "Withdraw 500.01 from CreditAccount with 0.00 balance and 500.00 limit.", "<code>canWithdraw()</code> returns <code>false</code>."],
        ["<code>shouldRejectAmountWithThreeDecimals()</code>", "Create Transaction with amount <code>new BigDecimal(\"10.555\")</code>.", "Throws <code>ValidationException</code>."],
        ["<code>shouldRejectNegativeOpeningBalance()</code>", "Create CheckingAccount with opening balance -50.00.", "Throws <code>ValidationException</code>."],
        ["<code>shouldGuaranteeTransactionImmutability()</code>", "Verify Transaction has zero setter methods and fields are final.", "Reflection / compiler verification."]
    ]
    story.append(build_table(tests_data[0], tests_data[1:], [165, 235, 140], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4. Oral Defense Armor: Anticipated Professor Questions & Exact Answers", s['h1']))
    qa_data = [
        ["Professor Question", "Your Model Answer (Demonstrating 100% Mastery)"],
        ["<b>Why did you use inheritance for Account instead of a field or enum?</b>",
         "<i>'Professor, CheckingAccount and CreditAccount have fundamentally different business logic for withdrawal authorization. CheckingAccount enforces a strict zero-floor balance, while CreditAccount calculates available funds against a credit limit. By defining an abstract canWithdraw() method in Account, TransactionService can polymorphically authorize withdrawals without any if/else type checks.'</i>"],
        ["<b>Why is Transaction immutable?</b>",
         "<i>'Financial records must be tamper-proof once recorded. By making Transaction final with private final fields and no setters, we guarantee that no service or UI bug can alter transaction dates, amounts, or categories after creation.'</i>"],
        ["<b>Why didn't you create IncomeTransaction and ExpenseTransaction subclasses?</b>",
         "<i>'Because income and expense differ only in algebraic sign and categorization, not in behavior. Creating empty subclasses without unique methods is an OOP anti-pattern ('lazy class'). We modeled direction cleanly using a TransactionType enum with a signed multiplier.'</i>"]
    ]
    story.append(build_table(qa_data[0], qa_data[1:], [145, 395], s))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Member 1 PDF generated: {output_path}")

# ==============================================================================
# 2. MEMBER 2 PDF
# ==============================================================================
def generate_member2_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=30)
    s = get_styles()
    story = []

    story.append(Paragraph("BudgetWise: Member 2 Playbook", s['title']))
    story.append(Paragraph("Budgeting, Trend Analysis Strategies & Mathematical Precision", s['subtitle']))
    story.append(Paragraph("<b>Git Branch:</b> <code>feat/member2-budget</code> | <b>Review Partner:</b> Member 1 (Pair Alpha) | <b>Deadline:</b> Dec 1, 2026", s['meta']))
    story.append(Spacer(1, 4))

    box = (
        "<b>Your Executive Role:</b> You are the <b>Financial Analytics & Budget Engine Specialist</b>. "
        "You own the budget lifecycle (<code>Budget</code>, <code>BudgetService</code>, <code>BudgetStatus</code>), "
        "the <b>Strategy Pattern for Trend Analysis</b> (<code>SpendingAnalysisStrategy</code>), and mathematical boundary safety. "
        "Your biggest architectural contribution to the group's 100% grade is ensuring that financial math has **zero rounding errors** "
        "using `BigDecimal` and exact cross-multiplication for budget state transitions."
    )
    t_box = Table([[Paragraph(box, s['callout'])]], colWidths=[540])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_CALLOUT_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Files You Own & What to Build in Each", s['h1']))
    files_data = [
        ["Class / Interface File", "Package", "Your Concrete Responsibilities & Tasks"],
        ["<code>Budget.java</code>", "<code>com.budgetwise.model</code>", "Immutable entity scoped by Category + YearMonth with strictly positive limit."],
        ["<code>BudgetPolicy.java</code>", "<code>com.budgetwise.model</code>", "Single source of truth for the warning threshold (default 80.00%); prevents policy drift."],
        ["<code>BudgetStatus.java</code>", "<code>com.budgetwise.model</code>", "Computes spent, remaining, utilization %, and states (NORMAL, WARNING, LIMIT_REACHED, EXCEEDED) via exact cross-multiplication."],
        ["<code>BudgetService.java</code>", "<code>com.budgetwise.service</code>", "Manages budget creation (rejecting duplicates via <code>DuplicateBudgetException</code>) and monthly aggregations."],
        ["<code>SpendingAnalysisStrategy</code>", "<code>com.budgetwise.strategy</code>", "Strategy interface contract for generating <code>SpendingSummary</code> objects from transaction history."],
        ["<code>MonthlyTotalAnalysis</code>", "<code>com.budgetwise.strategy</code>", "Computes current month category totals and total expenses."],
        ["<code>RollingAverageAnalysis</code>", "<code>com.budgetwise.strategy</code>", "Calculates historical baseline averages per category across up to 3 prior calendar months."]
    ]
    story.append(build_table(files_data[0], files_data[1:], [130, 110, 300], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2. Step-by-Step Execution Roadmap (Sprint by Sprint)", s['h1']))
    roadmap = [
        ["Phase / Date", "Sprint Target", "Deliverables & Verification Steps"],
        ["<b>Sprint 1 (Nov 16&ndash;19)</b>", "<b>Budget Math & Service Setup</b>", "1. Clone repo, checkout <code>feat/member2-budget</code>.<br/>2. Implement <code>BudgetStatus.compute()</code> using exact cross-multiplication: <code>spent * 100 vs limit * threshold</code>.<br/>3. Verify duplicate budget prevention in <code>BudgetService</code>."],
        ["<b>Sprint 2 (Nov 20&ndash;24)</b>", "<b>Rolling Average Strategy</b>", "1. Implement <code>RollingAverageAnalysisStrategy</code> scanning previous 1 to 3 months.<br/>2. Review Member 1's domain PRs; lead <b>Module Rotation #1 (Tue Nov 24)</b>."],
        ["<b>Sprint 3 (Nov 25&ndash;27)</b>", "<b>Edge Case Testing</b>", "1. Test leap-year transactions (Feb 29, 2028), small budget limits (0.03), and 80.00% boundaries.<br/>2. Lock features before <b>Feature Freeze (Fri Nov 27, 20:00)</b>."],
        ["<b>Final (Nov 28&ndash;30)</b>", "<b>Report & Defense Rehearsal</b>", "1. Write Report Section 6 (Business logic math) and Section 7 (Testing strategy).<br/>2. Rehearse defense questions with Member 1."]
    ]
    story.append(build_table(roadmap[0], roadmap[1:], [90, 110, 340], s))

    story.append(PageBreak())

    story.append(Paragraph("3. Unit Tests You Must Write to Guarantee 15% Test Marks", s['h1']))
    story.append(Paragraph("You own <code>BudgetThresholdTest.java</code> and <code>SpendingAnalysisStrategyTest.java</code>. Implement these exact cases:", s['body']))
    story.append(Spacer(1, 2))

    tests_data = [
        ["Test Case Method Name", "Scenario Tested", "Expected Assertion"],
        ["<code>shouldBeNormalWhenUnderWarningThreshold()</code>", "Spent 239.99 on 300.00 limit (79.99% used).", "State is <code>BudgetState.NORMAL</code>."],
        ["<code>shouldBeWarningWhenAtExactEightyPercent()</code>", "Spent exactly 240.00 on 300.00 limit (80.00% used).", "State is <code>BudgetState.WARNING</code>."],
        ["<code>shouldBeLimitReachedWhenAtExactHundred()</code>", "Spent exactly 300.00 on 300.00 limit (100.00% used).", "State is <code>BudgetState.LIMIT_REACHED</code>."],
        ["<code>shouldBeExceededWhenOneCentOverLimit()</code>", "Spent 300.01 on 300.00 limit.", "State is <code>BudgetState.EXCEEDED</code>."],
        ["<code>shouldRejectDuplicateBudgetInSameMonth()</code>", "Create two Dining budgets in 2026-11.", "Throws <code>DuplicateBudgetException</code>."],
        ["<code>shouldComputeRollingAverageAcrossThreeMonths()</code>", "Dining expenses of 100, 200, 300 in Aug, Sep, Oct.", "Baseline average for Nov is exactly 200.00."]
    ]
    story.append(build_table(tests_data[0], tests_data[1:], [165, 235, 140], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4. Oral Defense Armor: Anticipated Professor Questions & Exact Answers", s['h1']))
    qa_data = [
        ["Professor Question", "Your Model Answer (Demonstrating 100% Mastery)"],
        ["<b>Why did you use cross-multiplication instead of dividing spent by limit?</b>",
         "<i>'In floating-point and even BigDecimal division, dividing spent by limit can produce repeating decimals (e.g., 1/3 = 0.333...) requiring rounding. If a user sets a small limit like 0.03, rounding can erroneously flip a boundary. By comparing spent * 100 directly against limit * warningThreshold using compareTo(), we guarantee exact integer comparisons with zero rounding errors.'</i>"],
        ["<b>How does SpendingAnalysisStrategy demonstrate the Strategy Pattern?</b>",
         "<i>'SpendingAnalyzer depends exclusively on the SpendingAnalysisStrategy interface. At runtime, we can inject MonthlyTotalAnalysisStrategy or RollingAverageAnalysisStrategy without altering a single line of SpendingAnalyzer. This strictly follows the Open/Closed Principle.'</i>"],
        ["<b>How does your rolling average handle a brand new user with no history?</b>",
         "<i>'If a user has 0 prior months of data, the strategy returns an empty baseline map. AboveAverageRule checks if a baseline exists before evaluating, ensuring no false alerts are produced for new accounts.'</i>"]
    ]
    story.append(build_table(qa_data[0], qa_data[1:], [145, 395], s))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Member 2 PDF generated: {output_path}")

# ==============================================================================
# 3. MEMBER 3 PDF
# ==============================================================================
def generate_member3_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=30)
    s = get_styles()
    story = []

    story.append(Paragraph("BudgetWise: Member 3 Playbook", s['title']))
    story.append(Paragraph("Rules Engine, Template Method & Intelligent Savings Advisor", s['subtitle']))
    story.append(Paragraph("<b>Git Branch:</b> <code>feat/member3-rules</code> | <b>Review Partner:</b> Member 4 (Pair Beta) | <b>Deadline:</b> Dec 1, 2026", s['meta']))
    story.append(Spacer(1, 4))

    box = (
        "<b>Your Executive Role:</b> You are the <b>Decision Support Architect & Pattern Recognition Lead</b>. "
        "You own the rule evaluation engine (<code>SpendingAnalyzer</code>, <code>AbstractSpendingRule</code> hierarchy), "
        "the categorization algorithms (<code>KeywordCategorizationStrategy</code>, <code>MerchantHistoryStrategy</code>), "
        "and the <b>Intelligent Savings Advisor</b> (<code>SavingsAdvisor</code>). "
        "Your biggest architectural contribution is the <b>Template Method Pattern</b> for spending rules and the contextual advice engine."
    )
    t_box = Table([[Paragraph(box, s['callout'])]], colWidths=[540])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_CALLOUT_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Files You Own & What to Build in Each", s['h1']))
    files_data = [
        ["Class / Interface File", "Package", "Your Concrete Responsibilities & Tasks"],
        ["<code>AbstractSpendingRule.java</code>", "<code>com.budgetwise.rule</code>", "Applies Template Method pattern: <code>evaluate()</code> checks <code>isEnabled()</code> before calling abstract <code>doEvaluate()</code>."],
        ["<code>BudgetThresholdRule.java</code>", "<code>com.budgetwise.rule</code>", "Fires CRITICAL alerts when budget is EXCEEDED and WARNING alerts when in WARNING state."],
        ["<code>LargeTransactionRule.java</code>", "<code>com.budgetwise.rule</code>", "Flags individual expense transactions exceeding configured threshold (default $150.00)."],
        ["<code>AboveAverageRule.java</code>", "<code>com.budgetwise.rule</code>", "Flags categories whose monthly spend exceeds 2.0x their historical 3-month baseline."],
        ["<code>SavingsAdvisor.java</code>", "<code>com.budgetwise.service</code>", "Runs savings suggestion rules; calculates category expense ratios and goal deadline milestones."],
        ["<code>GoalContributionRule.java</code>", "<code>com.budgetwise.rule</code>", "Calculates required monthly savings: <code>(target - saved) / remainingMonths</code> with CEILING rounding."],
        ["<code>MerchantHistoryStrategy</code>", "<code>com.budgetwise.strategy</code>", "Adaptive categorization strategy that inspects user's past manual entries to infer categories."]
    ]
    story.append(build_table(files_data[0], files_data[1:], [130, 110, 300], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2. Step-by-Step Execution Roadmap (Sprint by Sprint)", s['h1']))
    roadmap = [
        ["Phase / Date", "Sprint Target", "Deliverables & Verification Steps"],
        ["<b>Sprint 1 (Nov 16&ndash;19)</b>", "<b>Template Method & Core Rules</b>", "1. Clone repo, checkout <code>feat/member3-rules</code>.<br/>2. Implement <code>LargeTransactionRule</code> and <code>AboveAverageRule</code> extending <code>AbstractSpendingRule</code>.<br/>3. Verify template method guarantees disabled rules return empty alert lists."],
        ["<b>Sprint 2 (Nov 20&ndash;24)</b>", "<b>Adaptive AI & Savings Advisor</b>", "1. Implement <code>MerchantHistoryStrategy</code> with normalized string matching.<br/>2. Upgrade <code>SavingsAdvisor</code> with multi-factor advice.<br/>3. Review Member 4's factory PRs; participate in <b>Module Rotation #1 (Tue Nov 24)</b>."],
        ["<b>Sprint 3 (Nov 25&ndash;27)</b>", "<b>Live Extension Preparation</b>", "1. Prepare <code>WeekendSpendingRule.java</code> to demonstrate the Open/Closed Principle live.<br/>2. Lock features before <b>Feature Freeze (Fri Nov 27, 20:00)</b>."],
        ["<b>Final (Nov 28&ndash;30)</b>", "<b>Report & Defense Rehearsal</b>", "1. Write Report Section 5 (Rule polymorphism) and Section 8 (Extensibility walkthrough).<br/>2. Rehearse live rule addition with Member 4."]
    ]
    story.append(build_table(roadmap[0], roadmap[1:], [90, 110, 340], s))

    story.append(PageBreak())

    story.append(Paragraph("3. Unit Tests You Must Write to Guarantee 15% Test Marks", s['h1']))
    story.append(Paragraph("You own <code>SpendingRuleTest.java</code> and <code>CategorizationStrategyTest.java</code>. Implement these exact cases:", s['body']))
    story.append(Spacer(1, 2))

    tests_data = [
        ["Test Case Method Name", "Scenario Tested", "Expected Assertion"],
        ["<code>shouldReturnNoAlertsWhenRuleIsDisabled()</code>", "Run evaluate on disabled BudgetThresholdRule with exceeded budget.", "Alert list is empty (guaranteed by base class)."],
        ["<code>shouldFireAlertWhenTransactionExceedsLimit()</code>", "Expense of 220.00 against 150.00 LargeTransaction limit.", "Alert generated with severity WARNING."],
        ["<code>shouldFireAboveAverageWhenSpendDoublesBaseline()</code>", "Dining spend 180.00 against 75.00 baseline (2.4x).", "Alert generated stating 2.4x baseline ratio."],
        ["<code>shouldCategorizeFromMerchantHistory()</code>", "Prior transaction 'Starbucks' categorized as Dining; new Starbucks tx.", "MerchantHistoryStrategy returns Dining category."],
        ["<code>shouldCalculateCeilingGoalContribution()</code>", "Goal remaining 100.00 with 3 months remaining.", "Required monthly saving is 33.34 (not 33.33)."],
        ["<code>shouldHandleWhitespaceAndCaseInNormalization()</code>", "Categorize '   sTaRbUcKs   cOfFeE   '.", "Correctly matches normalized keyword 'starbucks'."]
    ]
    story.append(build_table(tests_data[0], tests_data[1:], [165, 235, 140], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4. Oral Defense Armor: Anticipated Professor Questions & Exact Answers", s['h1']))
    qa_data = [
        ["Professor Question", "Your Model Answer (Demonstrating 100% Mastery)"],
        ["<b>Where is the Template Method pattern used and why?</b>",
         "<i>'In AbstractSpendingRule. The evaluate() method is final and contains invariant logic: checking if the rule is enabled. If enabled, it calls the abstract doEvaluate() method implemented by subclasses like BudgetThresholdRule. This eliminates code duplication across all rules and guarantees a disabled rule can never fire.'</i>"],
        ["<b>How does your categorization strategy learn without machine learning?</b>",
         "<i>'MerchantHistoryStrategy implements adaptive rule-based learning. It inspects the user\'s past transaction history, normalizes merchant descriptions, and automatically reuses the most recent category the user assigned. This provides genuine adaptive behavior while remaining 100% transparent and deterministic.'</i>"],
        ["<b>Can you prove the Open/Closed Principle right now?</b>",
         "<i>'Yes, Professor. Watch me add WeekendSpendingRule in 2 minutes: I create the class extending AbstractSpendingRule, implement doEvaluate(), and register it in the ApplicationFactory. Notice that SpendingAnalyzer, BudgetService, and the UI require zero modifications.'</i>"]
    ]
    story.append(build_table(qa_data[0], qa_data[1:], [145, 395], s))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Member 3 PDF generated: {output_path}")

# ==============================================================================
# 4. MEMBER 4 PDF
# ==============================================================================
def generate_member4_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=30)
    s = get_styles()
    story = []

    story.append(Paragraph("BudgetWise: Member 4 Playbook", s['title']))
    story.append(Paragraph("Architecture, Factory Pattern, CSV Persistence & Interactive UI", s['subtitle']))
    story.append(Paragraph("<b>Git Branch:</b> <code>feat/member4-ui</code> | <b>Review Partner:</b> Member 3 (Pair Beta) | <b>Deadline:</b> Dec 1, 2026", s['meta']))
    story.append(Spacer(1, 4))

    box = (
        "<b>Your Executive Role:</b> You are the <b>System Architect, Persistence Engineer & Integration Lead</b>. "
        "You own the **Factory Pattern & Dependency Injection** (<code>BudgetWiseApplicationFactory</code>), "
        "the **Storage Polymorphism** (<code>FileTransactionRepository</code> CSV engine), "
        "and the presentation layer (<code>ConsoleMenu</code>, <code>Main</code>). "
        "You coordinate Git releases, lead the PlantUML class diagram, and ensure the entire application runs seamlessly."
    )
    t_box = Table([[Paragraph(box, s['callout'])]], colWidths=[540])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_CALLOUT_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Files You Own & What to Build in Each", s['h1']))
    files_data = [
        ["Class / Interface File", "Package", "Your Concrete Responsibilities & Tasks"],
        ["<code>ApplicationFactory.java</code>", "<code>com.budgetwise.factory</code>", "Contract defining service instantiation, dependency wiring, and runtime strategy swapping."],
        ["<code>DefaultAppFactory.java</code>", "<code>com.budgetwise.factory</code>", "Instantiates in-memory/file repositories, registers default categories, and injects dependencies via constructors."],
        ["<code>FileTransactionRepo.java</code>", "<code>com.budgetwise.repository</code>", "CSV persistence engine with auto file creation, corrupted line recovery, and in-memory caching."],
        ["<code>ConsoleMenu.java</code>", "<code>com.budgetwise.ui</code>", "Interactive console CLI with text menus, input validation, and scripted Demos A, B, and C."],
        ["<code>Main.java</code>", "<code>com.budgetwise.ui</code>", "Application entry point; instantiates Factory and starts ConsoleMenu."],
        ["<code>pom.xml</code> & Git", "Project Root", "Coordinates Maven configuration, JUnit 5 dependencies, and manages pull request releases."],
        ["<code>docs/budgetwise.puml</code>", "Documentation", "Draws and synchronizes the official PlantUML class diagram line-by-line with source code."]
    ]
    story.append(build_table(files_data[0], files_data[1:], [130, 110, 300], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2. Step-by-Step Execution Roadmap (Sprint by Sprint)", s['h1']))
    roadmap = [
        ["Phase / Date", "Sprint Target", "Deliverables & Verification Steps"],
        ["<b>Sprint 1 (Nov 16&ndash;19)</b>", "<b>Git Setup & CSV Persistence</b>", "1. Initialize Git and push starter repo to GitHub; invite teammates.<br/>2. Complete CSV reading/writing in <code>FileTransactionRepository</code>.<br/>3. <b>Milestone 1 (Thu Nov 19):</b> Verify clean clone and build across all 4 machines."],
        ["<b>Sprint 2 (Nov 20&ndash;24)</b>", "<b>Interactive CLI & Demos</b>", "1. Build full interactive console menu loop with Scanner input handling.<br/>2. Script Demo A, B, and C with deterministic demo data reset.<br/>3. Review Member 3's rules PRs; participate in <b>Module Rotation #1 (Tue Nov 24)</b>."],
        ["<b>Sprint 3 (Nov 25&ndash;27)</b>", "<b>Integration Tests & Freeze</b>", "1. Write <code>IntegrationScenarioTest.java</code> testing the full application pipeline.<br/>2. Enforce <b>Feature Freeze on Fri Nov 27 at 20:00</b>."],
        ["<b>Final (Nov 28&ndash;30)</b>", "<b>UML, Report & Packaging</b>", "1. Finalize PlantUML diagram; author Report Sections 1, 2, 3.<br/>2. Assemble submission ZIP package and submit on UVT platform (Mon Nov 30)."]
    ]
    story.append(build_table(roadmap[0], roadmap[1:], [90, 110, 340], s))

    story.append(PageBreak())

    story.append(Paragraph("3. Unit Tests You Must Write to Guarantee 15% Test Marks", s['h1']))
    story.append(Paragraph("You own <code>FileTransactionRepositoryTest.java</code> and <code>IntegrationScenarioTest.java</code>. Implement these exact cases:", s['body']))
    story.append(Spacer(1, 2))

    tests_data = [
        ["Test Case Method Name", "Scenario Tested", "Expected Assertion"],
        ["<code>shouldSaveAndReloadTransactionsFromCsv()</code>", "Save 3 transactions to CSV; instantiate new repo pointing to same file.", "All 3 transactions reloaded with exact fields."],
        ["<code>shouldCreateFileIfDoesNotExist()</code>", "Initialize FileTransactionRepository pointing to non-existent path.", "File created automatically without crashing."],
        ["<code>shouldRunEndToEndAssignmentScenario()</code>", "Simulate full assignment scenario: $300 Dining budget, $290 spent, add $50.", "Alert EXCEEDED and advice generated without console."],
        ["<code>shouldSwapStrategiesAtRuntimeViaFactory()</code>", "Switch from MonthlyTotalAnalysis to RollingAverageAnalysis.", "Analyzer updates baseline without modifying service code."],
        ["<code>shouldRejectInvalidMenuInputs()</code>", "Pass invalid menu choices (e.g. 'abc' or '99') to ConsoleMenu.", "Handles error gracefully without crashing application."]
    ]
    story.append(build_table(tests_data[0], tests_data[1:], [165, 235, 140], s))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4. Oral Defense Armor: Anticipated Professor Questions & Exact Answers", s['h1']))
    qa_data = [
        ["Professor Question", "Your Model Answer (Demonstrating 100% Mastery)"],
        ["<b>How does your Factory pattern implement the Dependency Inversion Principle?</b>",
         "<i>'BudgetWiseApplicationFactory decouples high-level services from concrete low-level implementations. Notice that TransactionService only depends on the TransactionRepository interface. DefaultApplicationFactory handles the instantiation and injection. This allows us to swap in-memory storage with CSV storage or mock repositories for unit testing effortlessly.'</i>"],
        ["<b>How does FileTransactionRepository demonstrate storage polymorphism?</b>",
         "<i>'Both InMemoryTransactionRepository and FileTransactionRepository implement the TransactionRepository interface. The service layer does not care where data is stored. We can switch from RAM to disk storage by injecting a different object into the constructor, proving the Open/Closed Principle.'</i>"],
        ["<b>How does ConsoleMenu maintain strict Separation of Concerns?</b>",
         "<i>'ConsoleMenu is strictly a presentation layer. It never computes budget utilization, never filters dates, and never decides alert thresholds. It merely captures user input, delegates to application services, and receives immutable result objects (BudgetStatus, Alert) for display.'</i>"]
    ]
    story.append(build_table(qa_data[0], qa_data[1:], [145, 395], s))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Member 4 PDF generated: {output_path}")

# Run generation
if __name__ == '__main__':
    base_dir = r"C:\Users\dhaou\OneDrive\Desktop\OOP project"
    generate_member1_pdf(os.path.join(base_dir, "BudgetWise_Member1_Domain_and_Storage_Guide.pdf"))
    generate_member2_pdf(os.path.join(base_dir, "BudgetWise_Member2_Budgets_and_Analysis_Guide.pdf"))
    generate_member3_pdf(os.path.join(base_dir, "BudgetWise_Member3_Rules_and_Advisor_Guide.pdf"))
    generate_member4_pdf(os.path.join(base_dir, "BudgetWise_Member4_Architecture_and_UI_Guide.pdf"))
    print("\nAll 4 member guide PDFs generated successfully!")
