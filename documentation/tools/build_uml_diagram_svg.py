import os
import sys

# Generate a high-resolution, perfectly-styled SVG UML diagram
def generate_uml_svg(output_path):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="100%" style="background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <!-- Arrowhead markers -->
    <!-- Inheritance: closed hollow triangle -->
    <marker id="inheritance" markerWidth="14" markerHeight="14" refX="14" refY="7" orient="auto">
      <polygon points="0 0, 14 7, 0 14" fill="#FFFFFF" stroke="#1E3A8A" stroke-width="1.5"/>
    </marker>
    <!-- Realization: dashed with closed hollow triangle -->
    <marker id="realization" markerWidth="14" markerHeight="14" refX="14" refY="7" orient="auto">
      <polygon points="0 0, 14 7, 0 14" fill="#FFFFFF" stroke="#0D9488" stroke-width="1.5"/>
    </marker>
    <!-- Dependency / Association arrow -->
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#4B5563"/>
    </marker>
    <!-- Composition: filled diamond -->
    <marker id="composition" markerWidth="16" markerHeight="10" refX="0" refY="5" orient="auto">
      <polygon points="0 5, 8 0, 16 5, 8 10" fill="#1E3A8A" stroke="#1E3A8A" stroke-width="1"/>
    </marker>

    <!-- Drop shadow -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <style>
    .pkg-title { font-size: 16px; font-weight: bold; fill: #1E3A8A; letter-spacing: 0.5px; }
    .class-header { font-size: 12px; font-weight: bold; fill: #FFFFFF; }
    .class-stereo { font-size: 10px; font-style: italic; fill: #E2E8F0; }
    .member-text { font-size: 11px; fill: #1F2937; font-family: 'Consolas', 'Courier New', monospace; }
    .method-text { font-size: 11px; fill: #0F172A; font-family: 'Consolas', 'Courier New', monospace; }
    .divider { stroke: #CBD5E1; stroke-width: 1; }
    .box-border { stroke-width: 1.5; filter: url(#shadow); rx: 6; ry: 6; }
    .rel-line { stroke: #1E3A8A; stroke-width: 1.5; fill: none; }
    .rel-dash { stroke: #0D9488; stroke-width: 1.5; stroke-dasharray: 5,4; fill: none; }
    .rel-assoc { stroke: #64748B; stroke-width: 1.2; stroke-dasharray: 4,3; fill: none; }
    .label { font-size: 10px; fill: #475569; font-weight: 500; }
  </style>

  <!-- Title Banner -->
  <rect x="30" y="20" width="1540" height="60" rx="8" fill="#1E3A8A" filter="url(#shadow)"/>
  <text x="50" y="48" font-size="20" font-weight="bold" fill="#FFFFFF">BudgetWise &mdash; UML Class Diagram: Financial Entities &amp; Analysis Components</text>
  <text x="50" y="68" font-size="12" fill="#93C5FD">UVT OOP 2026 | Strict OOP Principles: Inheritance, Polymorphism, Interfaces, Composition, Immutability &amp; BigDecimal</text>

  <!-- ========================================================================= -->
  <!-- LEFT ZONE: FINANCIAL ENTITIES PACKAGE (com.budgetwise.model)               -->
  <!-- ========================================================================= -->
  <rect x="30" y="95" width="760" height="980" rx="10" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="50" y="125" class="pkg-title">&bull; PACKAGE: com.budgetwise.model (Financial Entities &amp; Domain Model)</text>

  <!-- 1. Abstract Account -->
  <g id="class-Account">
    <rect x="50" y="145" width="330" height="150" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 50 145 h 330 v 35 h -330 z" fill="#1E3A8A" rx="6" ry="6"/>
    <rect x="50" y="170" width="330" height="10" fill="#1E3A8A"/>
    <text x="215" y="159" text-anchor="middle" class="class-stereo">&lt;&lt;abstract&gt;&gt;</text>
    <text x="215" y="173" text-anchor="middle" class="class-header">Account</text>
    
    <text x="60" y="195" class="member-text">- id: String</text>
    <text x="60" y="210" class="member-text">- name: String</text>
    <text x="60" y="225" class="member-text">- openingBalance: BigDecimal</text>
    <line x1="50" y1="233" x2="380" y2="233" class="divider"/>
    <text x="60" y="248" class="method-text">+ {abstract} canWithdraw(amt, bal): boolean</text>
    <text x="60" y="263" class="method-text">+ {abstract} calculateAvailableFunds(bal): BigDecimal</text>
    <text x="60" y="278" class="method-text">+ getOpeningBalance(): BigDecimal</text>
  </g>

  <!-- 2. CheckingAccount -->
  <g id="class-CheckingAccount">
    <rect x="50" y="340" width="330" height="90" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 50 340 h 330 v 26 h -330 z" fill="#2563EB" rx="6" ry="6"/>
    <rect x="50" y="360" width="330" height="6" fill="#2563EB"/>
    <text x="215" y="358" text-anchor="middle" class="class-header">CheckingAccount</text>
    
    <text x="60" y="380" class="member-text">/* zero overdraft limit enforced */</text>
    <line x1="50" y1="388" x2="380" y2="388" class="divider"/>
    <text x="60" y="403" class="method-text">+ canWithdraw(amt, bal): boolean</text>
    <text x="60" y="418" class="method-text">+ calculateAvailableFunds(bal): BigDecimal</text>
  </g>

  <!-- 3. CreditAccount -->
  <g id="class-CreditAccount">
    <rect x="50" y="465" width="330" height="110" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 50 465 h 330 v 26 h -330 z" fill="#2563EB" rx="6" ry="6"/>
    <rect x="50" y="485" width="330" height="6" fill="#2563EB"/>
    <text x="215" y="483" text-anchor="middle" class="class-header">CreditAccount</text>
    
    <text x="60" y="505" class="member-text">- creditLimit: BigDecimal</text>
    <line x1="50" y1="513" x2="380" y2="513" class="divider"/>
    <text x="60" y="528" class="method-text">+ canWithdraw(amt, bal): boolean</text>
    <text x="60" y="543" class="method-text">+ calculateAvailableFunds(bal): BigDecimal</text>
    <text x="60" y="558" class="method-text">+ getCreditLimit(): BigDecimal</text>
  </g>

  <!-- Account Inheritance Arrows -->
  <path d="M 150 340 V 295" class="rel-line" marker-end="url(#inheritance)"/>
  <path d="M 270 465 V 315 H 250 V 295" class="rel-line" marker-end="url(#inheritance)"/>

  <!-- 4. Category -->
  <g id="class-Category">
    <rect x="420" y="145" width="350" height="120" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 420 145 h 350 v 26 h -350 z" fill="#0D9488" rx="6" ry="6"/>
    <rect x="420" y="165" width="350" height="6" fill="#0D9488"/>
    <text x="595" y="163" text-anchor="middle" class="class-header">Category</text>
    
    <text x="430" y="185" class="member-text">+ {static} UNCATEGORIZED: Category</text>
    <text x="430" y="200" class="member-text">- id: String, name: String, isCustom: boolean</text>
    <line x1="420" y1="208" x2="770" y2="208" class="divider"/>
    <text x="430" y="223" class="method-text">+ getId(): String, getName(): String</text>
    <text x="430" y="238" class="method-text">+ equals(o: Object): boolean, hashCode(): int</text>
  </g>

  <!-- 5. Transaction -->
  <g id="class-Transaction">
    <rect x="420" y="300" width="350" height="190" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 420 300 h 350 v 35 h -350 z" fill="#1E3A8A" rx="6" ry="6"/>
    <rect x="420" y="325" width="350" height="10" fill="#1E3A8A"/>
    <text x="595" y="314" text-anchor="middle" class="class-stereo">&lt;&lt;immutable record&gt;&gt;</text>
    <text x="595" y="328" text-anchor="middle" class="class-header">Transaction</text>
    
    <text x="430" y="350" class="member-text">- id: String, accountId: String</text>
    <text x="430" y="365" class="member-text">- date: LocalDate, description: String</text>
    <text x="430" y="380" class="member-text">- amount: BigDecimal (scale 2)</text>
    <text x="430" y="395" class="member-text">- type: TransactionType</text>
    <text x="430" y="410" class="member-text">- category: Category</text>
    <line x1="420" y1="418" x2="770" y2="418" class="divider"/>
    <text x="430" y="433" class="method-text">+ getSignedAmount(): BigDecimal</text>
    <text x="430" y="448" class="method-text">+ getAmount(): BigDecimal, getType(): Type</text>
    <text x="430" y="463" class="method-text">+ equals(o), hashCode(), toString()</text>
  </g>

  <!-- Transaction Associations -->
  <path d="M 595 300 V 265" class="rel-assoc" marker-end="url(#arrow)"/>
  <text x="605" y="285" class="label">classified by (1)</text>

  <!-- 6. Budget & BudgetPolicy -->
  <g id="class-Budget">
    <rect x="50" y="615" width="330" height="140" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 50 615 h 330 v 35 h -330 z" fill="#1E3A8A" rx="6" ry="6"/>
    <rect x="50" y="640" width="330" height="10" fill="#1E3A8A"/>
    <text x="215" y="629" text-anchor="middle" class="class-stereo">&lt;&lt;immutable&gt;&gt;</text>
    <text x="215" y="643" text-anchor="middle" class="class-header">Budget</text>
    
    <text x="60" y="665" class="member-text">- category: Category</text>
    <text x="60" y="680" class="member-text">- month: YearMonth</text>
    <text x="60" y="695" class="member-text">- limit: BigDecimal (scale 2)</text>
    <line x1="50" y1="703" x2="380" y2="703" class="divider"/>
    <text x="60" y="718" class="method-text">+ getCategory(): Category, getMonth(): YM</text>
    <text x="60" y="733" class="method-text">+ getLimit(): BigDecimal</text>
  </g>

  <!-- 7. BudgetStatus -->
  <g id="class-BudgetStatus">
    <rect x="420" y="520" width="350" height="165" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 420 520 h 350 v 35 h -350 z" fill="#0D9488" rx="6" ry="6"/>
    <rect x="420" y="545" width="350" height="10" fill="#0D9488"/>
    <text x="595" y="534" text-anchor="middle" class="class-stereo">&lt;&lt;record&gt;&gt;</text>
    <text x="595" y="548" text-anchor="middle" class="class-header">BudgetStatus</text>
    
    <text x="430" y="570" class="member-text">+ budget: Budget</text>
    <text x="430" y="585" class="member-text">+ spent: BigDecimal, remaining: BigDecimal</text>
    <text x="430" y="600" class="member-text">+ utilizationPercentage: BigDecimal</text>
    <text x="430" y="615" class="member-text">+ state: BudgetState (NORMAL/WARN/EXCEEDED)</text>
    <line x1="420" y1="623" x2="770" y2="623" class="divider"/>
    <text x="430" y="638" class="method-text">+ {static} compute(b, spent, policy): BudgetStatus</text>
    <text x="430" y="653" class="method-text">  /* exact cross-multiplication: spent*100 vs lim*thresh */</text>
  </g>

  <!-- Budget to Category & Status to Budget -->
  <path d="M 380 670 H 400 V 210 H 420" class="rel-assoc" marker-end="url(#arrow)"/>
  <text x="390" y="200" class="label">scopes</text>
  <path d="M 420 620 H 380" class="rel-assoc" marker-end="url(#arrow)"/>

  <!-- 8. FinancialGoal -->
  <g id="class-FinancialGoal">
    <rect x="50" y="795" width="330" height="150" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 50 795 h 330 v 26 h -330 z" fill="#1E3A8A" rx="6" ry="6"/>
    <rect x="50" y="815" width="330" height="6" fill="#1E3A8A"/>
    <text x="215" y="813" text-anchor="middle" class="class-header">FinancialGoal</text>
    
    <text x="60" y="835" class="member-text">- id: String, name: String</text>
    <text x="60" y="850" class="member-text">- targetAmount, savedAmount: BigDecimal</text>
    <text x="60" y="865" class="member-text">- targetMonth: YearMonth</text>
    <line x1="50" y1="873" x2="380" y2="873" class="divider"/>
    <text x="60" y="888" class="method-text">+ addSavings(amt: BigDecimal): void</text>
    <text x="60" y="903" class="method-text">+ isCompleted(): boolean, isOverdue(curr): boolean</text>
    <text x="60" y="918" class="method-text">+ getRemainingAmount(): BigDecimal</text>
  </g>

  <!-- Enums at bottom left -->
  <g id="class-Enums">
    <rect x="420" y="720" width="165" height="120" class="box-border" fill="#FFFFFF" stroke="#64748B"/>
    <path d="M 420 720 h 165 v 24 h -165 z" fill="#64748B" rx="6" ry="6"/>
    <text x="502" y="736" text-anchor="middle" class="class-header">&lt;&lt;enum&gt;&gt; BudgetState</text>
    <text x="430" y="760" class="member-text">NORMAL (&lt;80%)</text>
    <text x="430" y="775" class="member-text">WARNING (80-100%)</text>
    <text x="430" y="790" class="member-text">LIMIT_REACHED (100%)</text>
    <text x="430" y="805" class="member-text">EXCEEDED (&gt;100%)</text>

    <rect x="605" y="720" width="165" height="120" class="box-border" fill="#FFFFFF" stroke="#64748B"/>
    <path d="M 605 720 h 165 v 24 h -165 z" fill="#64748B" rx="6" ry="6"/>
    <text x="687" y="736" text-anchor="middle" class="class-header">&lt;&lt;enum&gt;&gt; AlertSeverity</text>
    <text x="615" y="765" class="member-text">INFO</text>
    <text x="615" y="785" class="member-text">WARNING</text>
    <text x="615" y="805" class="member-text">CRITICAL</text>
  </g>

  <!-- ========================================================================= -->
  <!-- RIGHT ZONE: ANALYSIS COMPONENTS (com.budgetwise.{strategy, rule, service}) -->
  <!-- ========================================================================= -->
  <rect x="810" y="95" width="760" height="980" rx="10" fill="#F8FAFC" stroke="#0D9488" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="830" y="125" class="pkg-title">&bull; PACKAGES: strategy, rule, service (Intelligent Analysis &amp; Decision Support)</text>

  <!-- 9. SpendingAnalysisStrategy Interface & Implementations -->
  <g id="class-AnalysisStrategy">
    <rect x="830" y="145" width="340" height="100" class="box-border" fill="#FFFFFF" stroke="#0D9488"/>
    <path d="M 830 145 h 340 v 35 h -340 z" fill="#0D9488" rx="6" ry="6"/>
    <rect x="830" y="170" width="340" height="10" fill="#0D9488"/>
    <text x="1000" y="159" text-anchor="middle" class="class-stereo">&lt;&lt;interface&gt;&gt;</text>
    <text x="1000" y="173" text-anchor="middle" class="class-header">SpendingAnalysisStrategy</text>
    
    <text x="840" y="198" class="method-text">+ {abstract} analyze(month, txs): SpendingSummary</text>
    <text x="840" y="215" class="method-text">+ {abstract} getStrategyName(): String</text>
  </g>

  <g id="class-MonthlyStrategy">
    <rect x="830" y="280" width="160" height="60" class="box-border" fill="#FFFFFF" stroke="#0D9488"/>
    <path d="M 830 280 h 160 v 22 h -160 z" fill="#047857" rx="6" ry="6"/>
    <text x="910" y="295" text-anchor="middle" class="class-header">MonthlyTotalStrategy</text>
    <text x="840" y="320" class="method-text">+ analyze(...) [this month]</text>
  </g>

  <g id="class-RollingStrategy">
    <rect x="1010" y="280" width="160" height="60" class="box-border" fill="#FFFFFF" stroke="#0D9488"/>
    <path d="M 1010 280 h 160 v 22 h -160 z" fill="#047857" rx="6" ry="6"/>
    <text x="1090" y="295" text-anchor="middle" class="class-header">RollingAverageStrategy</text>
    <text x="1020" y="320" class="method-text">+ analyze(...) [3-mo base]</text>
  </g>

  <path d="M 910 280 V 245" class="rel-dash" marker-end="url(#realization)"/>
  <path d="M 1090 280 V 245" class="rel-dash" marker-end="url(#realization)"/>

  <!-- 10. SpendingAnalyzer Service -->
  <g id="class-SpendingAnalyzer">
    <rect x="1200" y="145" width="350" height="135" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 1200 145 h 350 v 26 h -350 z" fill="#1E3A8A" rx="6" ry="6"/>
    <rect x="1200" y="165" width="350" height="6" fill="#1E3A8A"/>
    <text x="1375" y="163" text-anchor="middle" class="class-header">SpendingAnalyzer</text>
    
    <text x="1210" y="185" class="member-text">- strategy: SpendingAnalysisStrategy</text>
    <text x="1210" y="200" class="member-text">- rules: List&lt;SpendingRule&gt;</text>
    <line x1="1200" y1="208" x2="1550" y2="208" class="divider"/>
    <text x="1210" y="223" class="method-text">+ addRule(rule: SpendingRule): void</text>
    <text x="1210" y="238" class="method-text">+ setStrategy(s: SpendingAnalysisStrategy): void</text>
    <text x="1210" y="253" class="method-text">+ analyzeMonth(m, statuses): List&lt;Alert&gt;</text>
  </g>

  <!-- SpendingAnalyzer delegates to Strategy and composes Rules -->
  <path d="M 1200 195 H 1170" class="rel-assoc" marker-end="url(#arrow)"/>
  <text x="1175" y="185" class="label">uses</text>

  <!-- 11. SpendingRule Hierarchy (Template Method) -->
  <g id="class-SpendingRuleInterface">
    <rect x="1200" y="320" width="350" height="85" class="box-border" fill="#FFFFFF" stroke="#0D9488"/>
    <path d="M 1200 320 h 350 v 30 h -350 z" fill="#0D9488" rx="6" ry="6"/>
    <rect x="1200" y="345" width="350" height="5" fill="#0D9488"/>
    <text x="1375" y="334" text-anchor="middle" class="class-stereo">&lt;&lt;interface&gt;&gt;</text>
    <text x="1375" y="347" text-anchor="middle" class="class-header">SpendingRule</text>
    
    <text x="1210" y="370" class="method-text">+ {abstract} name(): String</text>
    <text x="1210" y="385" class="method-text">+ {abstract} evaluate(ctx: AnalysisContext): List&lt;Alert&gt;</text>
  </g>

  <!-- Composition line Analyzer *-- Rule -->
  <path d="M 1375 280 V 320" class="rel-line" marker-start="url(#composition)"/>

  <!-- AbstractSpendingRule -->
  <g id="class-AbstractSpendingRule">
    <rect x="1200" y="440" width="350" height="110" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 1200 440 h 350 v 35 h -350 z" fill="#1E3A8A" rx="6" ry="6"/>
    <rect x="1200" y="465" width="350" height="10" fill="#1E3A8A"/>
    <text x="1375" y="454" text-anchor="middle" class="class-stereo">&lt;&lt;abstract template&gt;&gt;</text>
    <text x="1375" y="468" text-anchor="middle" class="class-header">AbstractSpendingRule</text>
    
    <text x="1210" y="490" class="member-text">- name: String, enabled: boolean</text>
    <line x1="1200" y1="498" x2="1550" y2="498" class="divider"/>
    <text x="1210" y="513" class="method-text">+ evaluate(ctx): List&lt;Alert&gt; /* checks enabled */</text>
    <text x="1210" y="528" class="method-text"># {abstract} doEvaluate(ctx): List&lt;Alert&gt;</text>
  </g>

  <path d="M 1375 440 V 405" class="rel-dash" marker-end="url(#realization)"/>

  <!-- Concrete Rules -->
  <g id="class-ConcreteRules">
    <rect x="830" y="585" width="220" height="65" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 830 585 h 220 v 22 h -220 z" fill="#2563EB" rx="6" ry="6"/>
    <text x="940" y="600" text-anchor="middle" class="class-header">BudgetThresholdRule</text>
    <text x="840" y="625" class="method-text"># doEvaluate(ctx) [WARNING/EXCEEDED]</text>

    <rect x="1070" y="585" width="230" height="65" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 1070 585 h 230 v 22 h -230 z" fill="#2563EB" rx="6" ry="6"/>
    <text x="1185" y="600" text-anchor="middle" class="class-header">LargeTransactionRule</text>
    <text x="1080" y="625" class="method-text"># doEvaluate(ctx) [expense &gt; $150]</text>

    <rect x="1320" y="585" width="230" height="65" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 1320 585 h 230 v 22 h -230 z" fill="#2563EB" rx="6" ry="6"/>
    <text x="1435" y="600" text-anchor="middle" class="class-header">AboveAverageRule</text>
    <text x="1330" y="625" class="method-text"># doEvaluate(ctx) [spend &gt; 2.0x base]</text>
  </g>

  <path d="M 940 585 V 565 H 1375 V 550" class="rel-line" marker-end="url(#inheritance)"/>
  <path d="M 1185 585 V 565" class="rel-line"/>
  <path d="M 1435 585 V 565" class="rel-line"/>

  <!-- 12. SavingsAdvisor & GoalContributionRule -->
  <g id="class-SavingsAdvisor">
    <rect x="830" y="690" width="340" height="120" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 830 690 h 340 v 26 h -340 z" fill="#1E3A8A" rx="6" ry="6"/>
    <rect x="830" y="710" width="340" height="6" fill="#1E3A8A"/>
    <text x="1000" y="708" text-anchor="middle" class="class-header">SavingsAdvisor</text>
    
    <text x="840" y="730" class="member-text">- rules: List&lt;SavingsSuggestionRule&gt;</text>
    <line x1="830" y1="738" x2="1170" y2="738" class="divider"/>
    <text x="840" y="753" class="method-text">+ addRule(r: SavingsSuggestionRule): void</text>
    <text x="840" y="768" class="method-text">+ generateSuggestions(ctx, curr): List&lt;Rec&gt;</text>
    <text x="840" y="783" class="method-text">  /* computes velocity, ratios &amp; goal slippage */</text>
  </g>

  <g id="class-SavingsRule">
    <rect x="1200" y="690" width="350" height="60" class="box-border" fill="#FFFFFF" stroke="#0D9488"/>
    <path d="M 1200 690 h 350 v 24 h -350 z" fill="#0D9488" rx="6" ry="6"/>
    <text x="1375" y="706" text-anchor="middle" class="class-header">&lt;&lt;interface&gt;&gt; SavingsSuggestionRule</text>
    <text x="1210" y="730" class="method-text">+ {abstract} suggest(ctx, goals, curr): List&lt;Rec&gt;</text>
  </g>

  <!-- Advisor composes rule -->
  <path d="M 1170 720 H 1200" class="rel-line" marker-start="url(#composition)"/>

  <g id="class-GoalContributionRule">
    <rect x="1200" y="780" width="350" height="60" class="box-border" fill="#FFFFFF" stroke="#1E3A8A"/>
    <path d="M 1200 780 h 350 v 22 h -350 z" fill="#2563EB" rx="6" ry="6"/>
    <text x="1375" y="795" text-anchor="middle" class="class-header">GoalContributionRule</text>
    <text x="1210" y="820" class="method-text">+ suggest(...) [(target-saved)/months with CEILING]</text>
  </g>

  <path d="M 1375 780 V 750" class="rel-dash" marker-end="url(#realization)"/>

  <!-- Output Records -->
  <g id="class-OutputRecords">
    <rect x="830" y="845" width="340" height="110" class="box-border" fill="#FFFFFF" stroke="#64748B"/>
    <path d="M 830 845 h 340 v 24 h -340 z" fill="#64748B" rx="6" ry="6"/>
    <text x="1000" y="861" text-anchor="middle" class="class-header">&lt;&lt;record&gt;&gt; Alert</text>
    <text x="840" y="885" class="member-text">+ severity: AlertSeverity, ruleName: String</text>
    <text x="840" y="900" class="member-text">+ message: String, triggerAmount: BigDecimal</text>
    <text x="840" y="915" class="member-text">+ basisExplanation: String</text>
    <text x="840" y="930" class="member-text">+ toString(): formatted audit alert</text>

    <rect x="1200" y="860" width="350" height="110" class="box-border" fill="#FFFFFF" stroke="#64748B"/>
    <path d="M 1200 860 h 350 v 24 h -350 z" fill="#64748B" rx="6" ry="6"/>
    <text x="1375" y="876" text-anchor="middle" class="class-header">&lt;&lt;record&gt;&gt; SavingsRecommendation</text>
    <text x="1210" y="900" class="member-text">+ headline: String, detailedRationale: String</text>
    <text x="1210" y="915" class="member-text">+ recommendedCut: BigDecimal</text>
    <text x="1210" y="930" class="member-text">+ impactedGoal: Optional&lt;FinancialGoal&gt;</text>
    <text x="1210" y="945" class="member-text">+ priority: RecommendationPriority</text>
  </g>

  <!-- Cross-Package Collaboration Links (Entities & Analysis) -->
  <path d="M 770 590 H 830" class="rel-assoc" marker-end="url(#arrow)"/>
  <text x="778" y="582" class="label">evaluates</text>

  <path d="M 380 870 H 810 V 870 H 830" class="rel-assoc" marker-end="url(#arrow)"/>
  <text x="400" y="862" class="label">tracks goals</text>

  <!-- Legend -->
  <g id="legend" transform="translate(30, 1085)">
    <text x="20" y="0" font-size="11" font-weight="bold" fill="#1E3A8A">UML Legend:</text>
    <line x1="100" y1="-4" x2="140" y2="-4" stroke="#1E3A8A" stroke-width="1.5" marker-end="url(#inheritance)"/>
    <text x="145" y="0" font-size="10" fill="#334155">Generalization (Inheritance)</text>

    <line x1="310" y1="-4" x2="350" y2="-4" stroke="#0D9488" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#realization)"/>
    <text x="355" y="0" font-size="10" fill="#334155">Realization (Interface)</text>

    <line x1="510" y1="-4" x2="550" y2="-4" stroke="#1E3A8A" stroke-width="1.5" marker-start="url(#composition)"/>
    <text x="555" y="0" font-size="10" fill="#334155">Composition (Owns Lifecycle)</text>

    <line x1="730" y1="-4" x2="770" y2="-4" stroke="#64748B" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#arrow)"/>
    <text x="775" y="0" font-size="10" fill="#334155">Association / Dependency</text>
  </g>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated Vector SVG diagram at: {output_path}")

if __name__ == '__main__':
    target = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\documentation\BudgetWise_Financial_Entities_and_Analysis_UML.svg"
    generate_uml_svg(target)
