import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

# Professional Palette
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
            self.drawString(36, page_h - 22, "BudgetWise")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(C_MUTED)
            self.drawString(92, page_h - 22, "|   Teamwork & Engineering Execution Guide (Team of 4)")
            
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(36, page_h - 25, page_w - 36, page_h - 25)

        # Footer (All pages)
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(36, 26, page_w - 36, 26)

        self.setFont("Helvetica", 7.0)
        self.setFillColor(C_MUTED)
        self.drawString(36, 16, "UVT OOP Project 4 | BudgetWise Engineering Playbook | Submission: Dec 1, 2026")
        
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - 36, 16, page_str)
        self.restoreState()

def create_teamwork_guide_pdf(output_path):
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
        fontSize=18,
        leading=21,
        textColor=C_PRIMARY
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
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
        fontSize=10.2,
        leading=12.5,
        textColor=C_PRIMARY,
        spaceBefore=5,
        spaceAfter=2.5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=11,
        textColor=C_SECONDARY,
        spaceBefore=3.5,
        spaceAfter=1.5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.8,
        textColor=C_TEXT
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.8,
        textColor=C_TEXT
    )
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=8.8,
        textColor=colors.white
    )
    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.6,
        textColor=C_TEXT
    )
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.0,
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

    # ==================== PAGE 1: TITLE, STRATEGY, GIT SETUP & ROLES ====================
    story.append(Paragraph("BudgetWise: Teamwork & Execution Guide", title_style))
    story.append(Paragraph("Operational Playbook for a 4-Person Engineering Team", subtitle_style))
    story.append(Paragraph("<b>UVT Object-Oriented Programming (2026) | Java 21 LTS | NetBeans + Maven | Git Workflow</b><br/>"
                           "Target: 100% Grade | Submission Deadline: Dec 1, 2026 | Project Defense Window: Dec 1&ndash;3, 2026", meta_style))
    story.append(Spacer(1, 4))

    # Core Strategy Box
    core_strategy = (
        "<b>The Secret to 4-Person Success (Contract-First Parallel Coding):</b> "
        "Student teams usually fail when they code sequentially (e.g. Student 2 waits for Student 1 to finish accounts). "
        "In BudgetWise, <b>all 53 foundational contracts, interfaces, data models, and factory stubs are already committed on Day 1</b>. "
        "Because interfaces like <code>TransactionRepository</code>, <code>SpendingRule</code>, and <code>BudgetService</code> are fixed, "
        "<b>all 4 members can write code, run unit tests, and build features simultaneously without blocking each other.</b>"
    )
    strat_table = Table([[Paragraph(core_strategy, callout_style)]], colWidths=[540])
    strat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_CALLOUT_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(strat_table)
    story.append(Spacer(1, 4))

    # Step 1: Git Quickstart
    story.append(Paragraph("1. Shared Git Repository Setup (Immediate 30-Minute Kickoff)", h1_style))
    git_cmds = (
        "<b>// Step 1: Student 4 initializes and pushes the starter project to GitHub:</b><br/>"
        "cd \"c:\\Users\\dhaou\\OneDrive\\Desktop\\OOP project\"<br/>"
        "git init<br/>"
        "git add .<br/>"
        "git commit -m \"feat: initial BudgetWise v3 architecture and Day 1 contracts\"<br/>"
        "git branch -M main<br/>"
        "git remote add origin https://github.com/&lt;your-org-or-username&gt;/budgetwise-app.git<br/>"
        "git push -u origin main<br/><br/>"
        "<b>// Step 2: Students 1, 2, and 3 clone the repository onto their laptops:</b><br/>"
        "git clone https://github.com/&lt;your-org-or-username&gt;/budgetwise-app.git<br/>"
        "cd budgetwise-app<br/>"
        "<b>// Step 3: Every member verifies their environment compiles cleanly:</b><br/>"
        "mvn clean test    # Must output: BUILD SUCCESS with 2 passing tests"
    )
    git_table = Table([[Paragraph(git_cmds, code_style)]], colWidths=[540])
    git_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ('BOX', (0, 0), (-1, -1), 0.75, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    # style code text in white
    code_white = ParagraphStyle('CodeWhite', parent=code_style, textColor=colors.HexColor("#E2E8F0"))
    git_table = Table([[Paragraph(git_cmds, code_white)]], colWidths=[540])
    git_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5.5),
    ]))
    story.append(git_table)
    story.append(Spacer(1, 4))

    # Step 2: Role Matrix
    story.append(Paragraph("2. The 4 Engineering Tracks (File Ownership & Task Backlog)", h1_style))
    story.append(Paragraph("Each member owns an isolated set of classes. Nobody modifies another member's files without prior discussion.", body_style))
    story.append(Spacer(1, 2))

    roles_data = [
        ["Track / Member", "Git Feature Branch", "Source Files Owned in src/main/java/", "Concrete Tasks to Deliver"],
        ["<b>Member 1: Domain & Accounts</b>",
         "<code>feat/member1-domain</code>",
         "<code>com.budgetwise.model:</code><br/>&bull; Account (abstract)<br/>&bull; CheckingAccount<br/>&bull; CreditAccount<br/>&bull; Transaction, Category<br/>&bull; TransactionType<br/><code>com.budgetwise.repository:</code><br/>&bull; InMemoryTransactionRepo",
         "1. Refine <code>CreditAccount</code> with configurable credit limit and overdraft fee.<br/>"
         "2. Add strict constructor validations (reject negative balances, reject >2 decimal places).<br/>"
         "3. Write comprehensive unit tests in <code>AccountHierarchyTest</code> and <code>TransactionValidationTest</code>."],
        ["<b>Member 2: Budgeting & Trends</b>",
         "<code>feat/member2-budget</code>",
         "<code>com.budgetwise.model:</code><br/>&bull; Budget, BudgetPolicy<br/>&bull; BudgetStatus, BudgetState<br/>&bull; SpendingSummary<br/><code>com.budgetwise.service:</code><br/>&bull; BudgetService<br/><code>com.budgetwise.strategy:</code><br/>&bull; SpendingAnalysisStrategy<br/>&bull; MonthlyTotalAnalysis<br/>&bull; RollingAverageAnalysis",
         "1. Implement <code>RollingAverageAnalysisStrategy</code> calculating 3-month baseline averages per category.<br/>"
         "2. Validate exact cross-multiplication for budget states (NORMAL, WARNING, LIMIT_REACHED, EXCEEDED).<br/>"
         "3. Write unit tests covering threshold boundaries (exactly 80%, 100%, 100.01%) and leap-year month ends."],
        ["<b>Member 3: Rules & Intelligence</b>",
         "<code>feat/member3-rules</code>",
         "<code>com.budgetwise.rule:</code><br/>&bull; AbstractSpendingRule<br/>&bull; BudgetThresholdRule<br/>&bull; LargeTransactionRule<br/>&bull; AboveAverageRule<br/>&bull; GoalContributionRule<br/><code>com.budgetwise.service:</code><br/>&bull; SpendingAnalyzer<br/>&bull; SavingsAdvisor<br/><code>com.budgetwise.strategy:</code><br/>&bull; Categorization strategies",
         "1. Implement <code>LargeTransactionRule</code> (flags expenses > $150.00) and <code>AboveAverageRule</code> (spending > 2.0x baseline).<br/>"
         "2. Upgrade <code>SavingsAdvisor</code> to compute spending concentration ratios and link advice directly to <code>FinancialGoal</code> deadlines.<br/>"
         "3. Write unit tests proving disabled rules never fire and testing contextual advice generation."],
        ["<b>Member 4: Architecture & UI</b>",
         "<code>feat/member4-ui</code>",
         "<code>com.budgetwise.factory:</code><br/>&bull; ApplicationFactory<br/>&bull; DefaultAppFactory<br/><code>com.budgetwise.repository:</code><br/>&bull; FileTransactionRepo (CSV)<br/><code>com.budgetwise.ui:</code><br/>&bull; ConsoleMenu, Main",
         "1. Complete CSV serialization/deserialization in <code>FileTransactionRepository</code> with missing file recovery.<br/>"
         "2. Build interactive console CLI (1: Accounts, 2: Record Tx, 3: Budgets, 4: AI Advisor, 5: Run Demos).<br/>"
         "3. Script deterministic Demo Flows A and C, coordinate NetBeans build, and lead UML PlantUML diagram."]
    ]
    story.append(build_table(roles_data[0], roles_data[1:], [95, 95, 130, 220]))

    story.append(PageBreak())

    # ==================== PAGE 2: GIT WORKFLOW, PAIR REVIEWS & CALENDAR ====================
    story.append(Paragraph("3. Daily Git Workflow & Pull Request Protocol", h1_style))
    story.append(Paragraph(
        "To avoid merge conflicts and guarantee that <code>main</code> is always deployable and green, the team follows this strict cycle:",
        body_style
    ))
    story.append(Spacer(1, 3))

    git_cycle = (
        "<b>1. Start of day: Pull latest main into your branch</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>git checkout main && git pull origin main</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>git checkout &lt;your-branch&gt; && git merge main</code><br/>"
        "<b>2. Code your feature & write JUnit 5 unit tests in NetBeans</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Press <code>Alt + F6</code> in NetBeans or run <code>mvn test</code> in terminal. <b>Never commit code if tests fail.</b><br/>"
        "<b>3. Push your branch to GitHub</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>git add . && git commit -m \"feat(module): descriptive commit message\"</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>git push origin &lt;your-branch&gt;</code><br/>"
        "<b>4. Open a Pull Request (PR) on GitHub & assign your review partner</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;PR title must follow convention: <code>[Member X] Feature: Description of change</code>.<br/>"
        "<b>5. Partner reviews, pulls branch locally, tests, and merges into main</b>"
    )
    story.append(Paragraph(git_cycle, body_style))
    story.append(Spacer(1, 4))

    # Review Pairs Box
    story.append(Paragraph("The Peer Review 'Buddy System' (Defense Armor)", h2_style))
    pairs_box = (
        "&bull; <b>Pair Alpha: Member 1 &harr; Member 2:</b> Member 1 reviews Member 2's budget & analysis PRs; Member 2 reviews Member 1's domain PRs.<br/>"
        "&bull; <b>Pair Beta: Member 3 &harr; Member 4:</b> Member 3 reviews Member 4's factory & UI PRs; Member 4 reviews Member 3's rules & advisor PRs.<br/>"
        "&bull; <b>Why this matters for your grade:</b> In the oral defense, professors deliberately ask Member 1 questions about Member 2's code. "
        "Because every line was peer-reviewed, every member can explain their partner's classes with total confidence."
    )
    pairs_table = Table([[Paragraph(pairs_box, callout_style)]], colWidths=[540])
    pairs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_SUCCESS_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_SUCCESS_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(pairs_table)
    story.append(Spacer(1, 5))

    # Master Schedule Table
    story.append(Paragraph("4. Master Execution Calendar & Deliverable Milestones (Nov 16 &ndash; Dec 1)", h1_style))
    milestones_data = [
        ["Date Window", "Team Milestone", "Operational Target & Deliverables", "Exit Criteria (Verification Gate)"],
        ["<b>Mon Nov 16 &ndash; Tue Nov 17</b>",
         "<b>Project Kickoff & Contracts</b>",
         "1. Initialize GitHub repo; all 4 members clone and build.<br/>"
         "2. Review Decision Log D1–D12; commit compilable Day 1 stubs.<br/>"
         "3. Draw UML v0 diagram sketch in PlantUML.",
         "<code>mvn clean test</code> outputs BUILD SUCCESS on all 4 members' laptops."],
        ["<b>Wed Nov 18 &ndash; Sat Nov 21</b>",
         "<b>Core Domain & First Integration</b>",
         "1. Member 1 completes <code>Account</code> hierarchy and validation.<br/>"
         "2. Member 2 completes <code>BudgetService</code> and calculations.<br/>"
         "3. Member 4 connects Console to Factory.<br/>"
         "4. <b>Thu Nov 19: Integration Milestone 1.</b>",
         "<b>Live Test:</b> Add account, record expense, and verify balance via console and automated test."],
        ["<b>Sun Nov 22 &ndash; Wed Nov 25</b>",
         "<b>Intelligence & Module Rotation #1</b>",
         "1. Member 3 delivers all spending rules, analyzer, and advisor.<br/>"
         "2. Member 2 delivers <code>RollingAverageAnalysisStrategy</code>.<br/>"
         "3. <b>Tue Nov 24: Module Rotation #1.</b> Swap roles for 30 mins to practice oral defense.",
         "Demo B (the assignment scenario) runs end-to-end; peer walkthrough completed."],
        ["<b>Thu Nov 26 &ndash; Fri Nov 27</b>",
         "<b>Persistence & Feature Freeze</b>",
         "1. Member 4 finishes CSV persistence and full interactive menu.<br/>"
         "2. Script Demo A, B, and C with deterministic reset-demo-data.<br/>"
         "3. <b>Fri Nov 27, 20:00: Hard Feature Freeze.</b> Zero new features.",
         "Complete JUnit 5 suite runs green; all core requirements 1–6 verified functional."],
        ["<b>Sat Nov 28 &ndash; Mon Nov 30</b>",
         "<b>Verification, Report & Mock Defense</b>",
         "1. Reconcile PlantUML line-by-line with source code.<br/>"
         "2. Write 8–10 page report following Section 12 structure.<br/>"
         "3. Conduct 2 rounds of Mock Defenses (Sun Nov 29 & Mon Nov 30).<br/>"
         "4. <b>Mon Nov 30, 18:00: Final UVT Platform Submission.</b>",
         "Clean-clone build passes on fresh computer; report and ZIP submitted 24h early."],
        ["<b>Tue Dec 1 &ndash; Thu Dec 3</b>",
         "<b>Official Project Defense</b>",
         "Individual oral examination before the UVT course grading panel.",
         "Flawless individual demonstrations and answers to professor questions."]
    ]
    story.append(build_table(milestones_data[0], milestones_data[1:], [80, 105, 215, 140]))

    story.append(PageBreak())

    # ==================== PAGE 3: COMMUNICATION, PROTOCOLS & EMERGENCIES ====================
    story.append(Paragraph("5. Daily Communication & Standup Protocol", h1_style))
    story.append(Paragraph(
        "You do not need long, tiring meetings. You need a daily <b>5-minute asynchronous check-in</b> on WhatsApp or Discord:",
        body_style
    ))
    story.append(Spacer(1, 2))

    standup_box = (
        "<b>Every evening by 21:00, each member posts 3 bullet points:</b><br/>"
        "1. <b>Done today:</b> e.g., <i>'Finished CheckingAccount and wrote 4 unit tests for overdraft rejection.'</i><br/>"
        "2. <b>Doing tomorrow:</b> e.g., <i>'Writing CreditAccount credit-limit validation and fee calculation.'</i><br/>"
        "3. <b>Blockers:</b> e.g., <i>'None'</i> or <i>'Need Student 2 to clarify the return type of getBudgetStatus().'</i>"
    )
    story.append(Paragraph(standup_box, body_style))
    story.append(Spacer(1, 4))

    # Section 6: Golden Rules
    story.append(Paragraph("6. The 5 Golden Rules of Engineering Discipline", h1_style))
    rules_data = [
        ["Rule #", "Golden Rule Name", "Operational Mandate & Why It Protects Your Grade"],
        ["<b>Rule 1</b>", "<b>Interface Immutability</b>", "Never modify a shared interface in <code>com.budgetwise.strategy</code>, <code>rule</code>, or <code>repository</code> without a unanimous agreement from all 4 members. Changing an interface breaks other members' code."],
        ["<b>Rule 2</b>", "<b>Green Suite Mandatory</b>", "Never merge a Pull Request if any JUnit test fails or if there are compiler warnings. <code>main</code> must remain pristine at all times."],
        ["<b>Rule 3</b>", "<b>Javadoc on Public Methods</b>", "Every public class and public method must have a 2-line Javadoc explaining its responsibility and parameters. This directly satisfies the 15% code quality rubric."],
        ["<b>Rule 4</b>", "<b>No Magic Numbers</b>", "Never hardcode numbers like <code>80</code>, <code>150</code>, or <code>0.02</code> in service logic. Use named constants or inject them via <code>BudgetPolicy</code>."],
        ["<b>Rule 5</b>", "<b>Defensive Immutability</b>", "All domain entities (<code>Transaction</code>, <code>Budget</code>, <code>Alert</code>) must be immutable. Collection fields must return unmodifiable views using <code>List.copyOf</code> or <code>Collections.unmodifiableList</code>."]
    ]
    story.append(build_table(rules_data[0], rules_data[1:], [40, 120, 380]))
    story.append(Spacer(1, 5))

    # Section 7: Report Division
    story.append(Paragraph("7. Writing the Final Project Report (No Last-Minute Scramble)", h1_style))
    story.append(Paragraph("The report is 8–10 pages. Do not assign it to one person at the end. Divide sections by domain ownership:", body_style))
    story.append(Spacer(1, 2))

    report_data = [
        ["Report Section", "Primary Author", "Content to Document & Explain"],
        ["<b>Sec 1 & 2: Purpose & Requirements Mapping</b>", "<b>Member 4</b>", "Executive summary, honest AI decision-support statement, core requirements table."],
        ["<b>Sec 3: Architecture & Decision Log</b>", "<b>Member 4</b>", "4-tier architecture diagram, decision log D1–D12, and package organization."],
        ["<b>Sec 4 & 5: OOP Concepts & Code References</b>", "<b>Member 1 & 3</b>", "Deep explanation of the 4 inheritance hierarchies, polymorphism, and interfaces with exact line numbers."],
        ["<b>Sec 6: Business Rules & AI Logic</b>", "<b>Member 2 & 3</b>", "BigDecimal math, cross-multiplication threshold logic, contextual savings advisor calculations."],
        ["<b>Sec 7: Testing Strategy & Bug Found</b>", "<b>Member 1 & 2</b>", "Test counts, boundary test matrix, parameterized tests, and one concrete bug caught by a test."],
        ["<b>Sec 8: Extensibility Walkthrough</b>", "<b>Member 3</b>", "Code walkthrough showing how <code>WeekendSpendingRule</code> is added without modifying services."],
        ["<b>Sec 9 & 10: Team Contributions & Sign-Off</b>", "<b>All Members</b>", "Git commit statistics, peer review logs, and individual contribution statements."]
    ]
    story.append(build_table(report_data[0], report_data[1:], [115, 75, 350]))
    story.append(Spacer(1, 4))

    # Final Checklist Box
    story.append(Paragraph("8. Emergency Troubleshooting & Conflict Resolution", h1_style))
    trouble_box = (
        "&bull; <b>Git Merge Conflict:</b> Never force push (<code>git push -f</code>). If Git reports a conflict during a merge, hop on a screen share with your review partner and resolve it together.<br/>"
        "&bull; <b>A Team Member Falls Behind:</b> If someone is stuck for more than 24 hours, their review partner pair-programs with them that evening. Never leave a teammate isolated.<br/>"
        "&bull; <b>If Behind Schedule on Nov 25:</b> Cut stretch features from the bottom upward (Cut CSV export & GUI first). <b>Never cut tests, UML, or the two strategy pairs.</b>"
    )
    story.append(Paragraph(trouble_box, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Teamwork Guide PDF generated successfully at: {output_path}")

if __name__ == '__main__':
    target_path = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\BudgetWise_Teamwork_and_Execution_Guide.pdf"
    create_teamwork_guide_pdf(target_path)
