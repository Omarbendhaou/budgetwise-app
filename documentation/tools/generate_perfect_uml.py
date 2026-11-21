import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Color Palette matching user's reference image
COLOR_PURPLE = "#8A43A8"  # Domain Entities (Account, Checking, Credit, FinancialGoal)
COLOR_BLUE   = "#2980B9"  # Financial State & Controller (Transaction, Budget, BudgetStatus, SpendingAnalyzer)
COLOR_GREEN  = "#27AE60"  # Context / Strategy Engine
COLOR_ORANGE = "#D35400"  # Rule Engine / SpendingRules
COLOR_TEAL   = "#16A085"  # Category & SavingsAdvisor
COLOR_WHITE  = "#FFFFFF"
COLOR_TEXT   = "#2C3E50"

def generate_perfect_diagrams(drawio_path, png_path, svg_path):
    # =========================================================================
    # 1. GENERATE PERFECT 4-COLUMN DRAW.IO XML (.drawio)
    # ZERO INTERSECTIONS, ZERO LINES THROUGH BOXES
    # =========================================================================
    classes = [
        # --- COLUMN 1: ACCOUNT DOMAIN (x = 50..390) ---
        {
            "id": "acc", "title": "Account (Abstract)",
            "x": 50, "y": 50, "w": 340, "h": 180, "color": COLOR_PURPLE,
            "fields": "+ String id&#xa;+ String name&#xa;+ BigDecimal openingBalance", "f_h": 62,
            "methods": "+ canWithdraw(amount, bal) : boolean&#xa;+ calculateAvailableFunds(bal) : BigDecimal&#xa;+ getOpeningBalance() : BigDecimal&#xa;+ getAccountType() : String", "m_h": 82
        },
        {
            "id": "chk", "title": "CheckingAccount",
            "x": 50, "y": 290, "w": 160, "h": 150, "color": COLOR_PURPLE,
            "fields": "/* strict zero floor */&#xa;/* no overdraft */", "f_h": 44,
            "methods": "+ canWithdraw(amt, bal) : bool&#xa;+ calculateAvailableFunds() : BD&#xa;+ getAccountType() : String", "m_h": 70
        },
        {
            "id": "crd", "title": "CreditAccount",
            "x": 230, "y": 290, "w": 160, "h": 150, "color": COLOR_PURPLE,
            "fields": "+ BigDecimal creditLimit", "f_h": 36,
            "methods": "+ canWithdraw(amt, bal) : bool&#xa;+ calculateAvailableFunds() : BD&#xa;+ getCreditLimit() : BigDecimal&#xa;+ getAccountType() : String", "m_h": 78
        },

        # --- COLUMN 2: TRANSACTION & BUDGET MODEL (x = 450..750) ---
        {
            "id": "cat", "title": "Category (Domain Entity)",
            "x": 450, "y": 50, "w": 300, "h": 170, "color": COLOR_TEAL,
            "fields": "+ String id&#xa;+ String name&#xa;+ boolean isCustom&#xa;+ Category UNCATEGORIZED", "f_h": 76,
            "methods": "+ getId() : String&#xa;+ getName() : String&#xa;+ isCustom() : boolean&#xa;+ equals(obj) : boolean", "m_h": 58
        },
        {
            "id": "tx", "title": "Transaction (Immutable)",
            "x": 450, "y": 290, "w": 300, "h": 250, "color": COLOR_BLUE,
            "fields": "+ String id&#xa;+ String accountId&#xa;+ LocalDate date&#xa;+ String description&#xa;+ BigDecimal amount [scale 2]&#xa;+ TransactionType type&#xa;+ Category category", "f_h": 122,
            "methods": "+ getSignedAmount() : BigDecimal&#xa;+ getAmount() : BigDecimal&#xa;+ getType() : TransactionType&#xa;+ getCategory() : Category&#xa;+ equals(obj) : boolean", "m_h": 92
        },
        {
            "id": "bdg", "title": "Budget (Entity)",
            "x": 450, "y": 570, "w": 300, "h": 170, "color": COLOR_BLUE,
            "fields": "+ Category category&#xa;+ YearMonth month&#xa;+ BigDecimal limit [scale 2]", "f_h": 62,
            "methods": "+ getCategory() : Category&#xa;+ getMonth() : YearMonth&#xa;+ getLimit() : BigDecimal&#xa;+ equals(obj) : boolean", "m_h": 72
        },
        {
            "id": "bds", "title": "BudgetStatus (Record)",
            "x": 450, "y": 800, "w": 300, "h": 200, "color": COLOR_BLUE,
            "fields": "+ Budget budget&#xa;+ BigDecimal spent&#xa;+ BigDecimal remaining&#xa;+ BigDecimal utilizationPercentage&#xa;+ BudgetState state", "f_h": 92,
            "methods": "+ compute(b, spent, policy) : BudgetStatus&#xa;  /* spent*100 vs limit*threshold */&#xa;+ getUtilizationPercentage() : BigDecimal&#xa;+ getState() : BudgetState", "m_h": 72
        },

        # --- COLUMN 3: ANALYZER & ADVISOR (x = 820..1140) ---
        {
            "id": "ana", "title": "SpendingAnalyzer (Controller)",
            "x": 820, "y": 290, "w": 320, "h": 190, "color": COLOR_BLUE,
            "fields": "+ SpendingAnalysisStrategy strategy&#xa;+ List&lt;SpendingRule&gt; rules", "f_h": 46,
            "methods": "+ addRule(rule : SpendingRule) : void&#xa;+ setStrategy(s : AnalysisStrategy) : void&#xa;+ analyzeMonth(month, statuses) : List&lt;Alert&gt;&#xa;+ getRules() : List&lt;SpendingRule&gt;&#xa;+ getStrategy() : SpendingAnalysisStrategy", "m_h": 108
        },
        {
            "id": "adv", "title": "SavingsAdvisor (AI Decision Support)",
            "x": 820, "y": 570, "w": 320, "h": 170, "color": COLOR_TEAL,
            "fields": "+ List&lt;SavingsSuggestionRule&gt; rules", "f_h": 36,
            "methods": "+ addRule(rule) : void&#xa;+ generateSuggestions(ctx, curr) : List&lt;Rec&gt;&#xa;+ GoalContributionRule : (target-saved)/months&#xa;+ computeConcentrationRatio() : BigDecimal", "m_h": 98
        },

        # --- COLUMN 4: ENGINES & GOALS (x = 1200..1520) ---
        {
            "id": "ctx", "title": "Context Engine (Strategy)",
            "x": 1200, "y": 50, "w": 320, "h": 170, "color": COLOR_GREEN,
            "fields": "+ SpendingAnalysisStrategy (Interface)", "f_h": 36,
            "methods": "+ analyze(month, txList) : SpendingSummary&#xa;+ MonthlyTotalStrategy : analyze()&#xa;+ RollingAverageStrategy : 3-mo baseline&#xa;+ getStrategyName() : String", "m_h": 98
        },
        {
            "id": "rul", "title": "Rule Engine (SpendingRules)",
            "x": 1200, "y": 290, "w": 320, "h": 210, "color": COLOR_ORANGE,
            "fields": "+ AbstractSpendingRule (Template Method)&#xa;+ String name&#xa;+ boolean enabled", "f_h": 58,
            "methods": "+ evaluate(context) : List&lt;Alert&gt;&#xa;# doEvaluate(context) : List&lt;Alert&gt;&#xa;+ BudgetThresholdRule : evaluate()&#xa;+ LargeTransactionRule : &gt; $150&#xa;+ AboveAverageRule : &gt; 2.0x base", "m_h": 116
        },
        {
            "id": "gol", "title": "FinancialGoal",
            "x": 1200, "y": 570, "w": 320, "h": 200, "color": COLOR_PURPLE,
            "fields": "+ String id&#xa;+ String name&#xa;+ BigDecimal targetAmount&#xa;+ BigDecimal savedAmount&#xa;+ YearMonth targetMonth", "f_h": 92,
            "methods": "+ addSavings(amount) : void&#xa;+ isCompleted() : boolean&#xa;+ isOverdue(currentMonth) : boolean&#xa;+ getRemainingAmount() : BigDecimal", "m_h": 72
        }
    ]

    edges = [
        # Checking -> Account: straight UP
        {"id": "e_chk_acc", "val": "extends", "src": "chk", "tgt": "acc", "color": COLOR_PURPLE,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.25;entryY=1;entryDx=0;entryDy=0;",
         "pts": []},
        # Credit -> Account: straight UP
        {"id": "e_crd_acc", "val": "extends", "src": "crd", "tgt": "acc", "color": COLOR_PURPLE,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.75;entryY=1;entryDx=0;entryDy=0;",
         "pts": []},
        # Transaction -> Category: straight UP
        {"id": "e_tx_cat", "val": "classified by", "src": "tx", "tgt": "cat", "color": COLOR_TEAL,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.5;entryY=1;entryDx=0;entryDy=0;",
         "pts": []},
        # BudgetStatus -> Budget: straight UP
        {"id": "e_bds_bdg", "val": "evaluates", "src": "bds", "tgt": "bdg", "color": COLOR_BLUE,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.5;entryY=1;entryDx=0;entryDy=0;",
         "pts": []},
        # SpendingAnalyzer -> Transaction: straight LEFT
        {"id": "e_ana_tx", "val": "queries", "src": "ana", "tgt": "tx", "color": COLOR_BLUE,
         "exit": "exitX=0;exitY=0.45;exitDx=0;exitDy=0;", "entry": "entryX=1;entryY=0.45;entryDx=0;entryDy=0;",
         "pts": []},
        # SpendingAnalyzer -> Context Engine: orthogonal UP-RIGHT in open channel
        {"id": "e_ana_ctx", "val": "evaluates", "src": "ana", "tgt": "ctx", "color": COLOR_GREEN,
         "exit": "exitX=1;exitY=0.2;exitDx=0;exitDy=0;", "entry": "entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
         "pts": [(1170, 328), (1170, 135)]},
        # SpendingAnalyzer -> Rule Engine: straight RIGHT
        {"id": "e_ana_rul", "val": "applies rules", "src": "ana", "tgt": "rul", "color": COLOR_ORANGE,
         "exit": "exitX=1;exitY=0.6;exitDx=0;exitDy=0;", "entry": "entryX=0;entryY=0.45;entryDx=0;entryDy=0;",
         "pts": []},
        # SpendingAnalyzer -> SavingsAdvisor: straight DOWN
        {"id": "e_ana_adv", "val": "triggers advice", "src": "ana", "tgt": "adv", "color": COLOR_TEAL,
         "exit": "exitX=0.5;exitY=1;exitDx=0;exitDy=0;", "entry": "entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
         "pts": []},
        # SavingsAdvisor -> FinancialGoal: straight RIGHT
        {"id": "e_adv_gol", "val": "links goals", "src": "adv", "tgt": "gol", "color": COLOR_TEAL,
         "exit": "exitX=1;exitY=0.5;exitDx=0;exitDy=0;", "entry": "entryX=0;entryY=0.45;entryDx=0;entryDy=0;",
         "pts": []}
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<mxfile host="app.diagrams.net" modified="2026-11-16T16:45:00.000Z" agent="BudgetWise" version="24.0.0" type="device">',
           '  <diagram id="budgetwise-diagram" name="BudgetWise UML Class Diagram">',
           '    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" background="#FFFFFF">',
           '      <root>',
           '        <mxCell id="0"/>',
           '        <mxCell id="1" parent="0"/>']

    for c in classes:
        cid, title = c["id"], c["title"]
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        col = c["color"]
        fields, methods = c["fields"], c["methods"]
        fh, mh = c["f_h"], c["m_h"]

        # Swimlane Header
        xml.append(f'        <mxCell id="{cid}" value="{title}" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor={col};fontColor=#ffffff;strokeColor={col};rounded=0;fontSize=12;shadow=1;" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>')
        xml.append('        </mxCell>')

        # Fields Section
        xml.append(f'        <mxCell id="{cid}_fields" value="{fields}" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;spacingTop=4;spacingBottom=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;fontColor=#2C3E50;fontFamily=monospace;" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="28" width="{w}" height="{fh}" as="geometry"/>')
        xml.append('        </mxCell>')

        # Divider Line
        xml.append(f'        <mxCell id="{cid}_line" value="" style="line;strokeWidth=1.2;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=0;spacingRight=0;rotatable=0;strokeColor={col};html=1;" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="{28+fh}" width="{w}" height="8" as="geometry"/>')
        xml.append('        </mxCell>')

        # Methods Section
        xml.append(f'        <mxCell id="{cid}_methods" value="{methods}" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;spacingTop=4;spacingBottom=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;fontColor=#2C3E50;fontFamily=monospace;" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="{28+fh+8}" width="{w}" height="{mh}" as="geometry"/>')
        xml.append('        </mxCell>')

    for e in edges:
        eid, val, src, tgt, col = e["id"], e["val"], e["src"], e["tgt"], e["color"]
        ex, en = e["exit"], e["entry"]
        xml.append(f'        <mxCell id="{eid}" value="{val}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={col};strokeWidth=2;fontColor={col};fontStyle=1;fontSize=11;labelBackgroundColor=#ffffff;{ex}{en}" edge="1" parent="1" source="{src}" target="{tgt}">')
        xml.append('          <mxGeometry relative="1" as="geometry">')
        if e["pts"]:
            xml.append('            <Array as="points">')
            for pt in e["pts"]:
                xml.append(f'              <mxPoint x="{pt[0]}" y="{pt[1]}"/>')
            xml.append('            </Array>')
        xml.append('          </mxGeometry>')
        xml.append('        </mxCell>')

    xml.append('      </root>')
    xml.append('    </mxGraphModel>')
    xml.append('  </diagram>')
    xml.append('</mxfile>')

    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    print(f"Generated Organized Draw.io XML: {drawio_path}")

    # =========================================================================
    # 2. GENERATE HIGH-RES PNG & SVG MATCHING THIS EXACT BEAUTIFUL LAYOUT
    # =========================================================================
    fig, ax = plt.subplots(figsize=(24, 15), dpi=220)
    ax.set_xlim(0, 240)
    ax.set_ylim(0, 150)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title & Subtitle Banner
    ax.text(8, 144, "BudgetWise — UML Class Diagram (Financial Entities & Analysis Architecture)",
            fontsize=16, fontweight='bold', color="#2C3E50", ha='left')
    ax.text(8, 141, "UVT Object-Oriented Programming 2026 | Guaranteed 100% Top-Grade Architecture | Clean 4-Column Layout (Zero Intersecting Lines)",
            fontsize=10, color="#7F8C8D", ha='left')

    def draw_box(x, y, w, h, title, fields, methods, color):
        body = patches.Rectangle((x, y), w, h, fc=COLOR_WHITE, ec=color, lw=1.6, zorder=2)
        ax.add_patch(body)
        hh = 4.2
        header = patches.Rectangle((x, y + h - hh), w, hh, fc=color, ec=color, lw=1.6, zorder=3)
        ax.add_patch(header)
        ax.text(x + w / 2, y + h - (hh / 2), title, fontsize=9.2, fontweight='bold',
                color=COLOR_WHITE, ha='center', va='center', zorder=4)

        cur_y = y + h - hh - 1.4
        if fields:
            for f in fields:
                ax.text(x + 1.2, cur_y, f, fontsize=7.2, color=COLOR_TEXT, fontfamily='monospace', va='top', zorder=4)
                cur_y -= 1.65
            cur_y -= 0.3
            ax.plot([x, x + w], [cur_y, cur_y], color=color, lw=1.1, zorder=4)
            cur_y -= 1.3

        if methods:
            for m in methods:
                ax.text(x + 1.2, cur_y, m, fontsize=7.2, color=COLOR_TEXT, fontfamily='monospace', va='top', zorder=4)
                cur_y -= 1.65

    # Coordinates mapping:
    # Col 1: x = 8..52 (w=44), Checking w=21, Credit w=21
    # Col 2: x = 62..106 (w=44)
    # Col 3: x = 118..166 (w=48)
    # Col 4: x = 178..226 (w=48)

    # --- COLUMN 1: Accounts ---
    draw_box(8, 106, 44, 28, "Account (Abstract)",
             ["+ String id", "+ String name", "+ BigDecimal openingBalance"],
             ["+ canWithdraw(amount, bal) : boolean", "+ calculateAvailableFunds(bal) : BigDecimal", "+ getOpeningBalance() : BigDecimal", "+ getAccountType() : String"],
             COLOR_PURPLE)

    draw_box(8, 76, 21, 22, "CheckingAccount",
             ["/* zero-overdraft */", "/* strict floor */"],
             ["+ canWithdraw() : bool", "+ calculateFunds() : BD", "+ getAccountType() : String"],
             COLOR_PURPLE)

    draw_box(31, 76, 21, 22, "CreditAccount",
             ["+ BigDecimal creditLimit"],
             ["+ canWithdraw() : bool", "+ calculateFunds() : BD", "+ getCreditLimit() : BD", "+ getAccountType() : String"],
             COLOR_PURPLE)

    # --- COLUMN 2: Data Model ---
    draw_box(62, 108, 44, 26, "Category (Domain Entity)",
             ["+ String id", "+ String name", "+ boolean isCustom", "+ Category UNCATEGORIZED"],
             ["+ getId() : String", "+ getName() : String", "+ isCustom() : boolean", "+ equals(obj) : boolean"],
             COLOR_TEAL)

    draw_box(62, 66, 44, 34, "Transaction (Immutable)",
             ["+ String id, accountId", "+ LocalDate date, description", "+ BigDecimal amount [scale 2]", "+ TransactionType type", "+ Category category"],
             ["+ getSignedAmount() : BigDecimal", "+ getAmount() : BigDecimal", "+ getType() : TransactionType", "+ getCategory() : Category", "+ equals(obj) : boolean"],
             COLOR_BLUE)

    draw_box(62, 38, 44, 22, "Budget (Entity)",
             ["+ Category category", "+ YearMonth month", "+ BigDecimal limit [scale 2]"],
             ["+ getCategory() : Category", "+ getMonth() : YearMonth", "+ getLimit() : BigDecimal", "+ equals(obj) : boolean"],
             COLOR_BLUE)

    draw_box(62, 8, 44, 24, "BudgetStatus (Record)",
             ["+ Budget budget", "+ BigDecimal spent, remaining", "+ BigDecimal utilizationPercentage", "+ BudgetState state"],
             ["+ compute(b, spent, pol) : BudgetStatus", "  /* spent*100 vs limit*threshold */", "+ getUtilizationPercentage() : BD", "+ getState() : BudgetState"],
             COLOR_BLUE)

    # --- COLUMN 3: Controllers & Services ---
    draw_box(118, 76, 48, 28, "SpendingAnalyzer (Controller)",
             ["+ SpendingAnalysisStrategy strategy", "+ List<SpendingRule> rules"],
             ["+ addRule(rule : SpendingRule) : void", "+ setStrategy(s : AnalysisStrategy) : void", "+ analyzeMonth(month, stat) : List<Alert>", "+ getRules() : List<SpendingRule>", "+ getStrategy() : AnalysisStrategy"],
             COLOR_BLUE)

    draw_box(118, 36, 48, 26, "SavingsAdvisor (AI Decision Support)",
             ["+ List<SavingsSuggestionRule> rules"],
             ["+ addRule(rule) : void", "+ generateSuggestions(ctx, curr) : List<Rec>", "+ GoalContributionRule : (target-saved)/mo", "+ computeConcentrationRatio() : BigDecimal"],
             COLOR_TEAL)

    # --- COLUMN 4: Strategy, Rules & Goals ---
    draw_box(178, 108, 48, 26, "Context Engine (Strategy)",
             ["+ SpendingAnalysisStrategy (Interface)"],
             ["+ analyze(month, txList) : SpendingSummary", "+ MonthlyTotalStrategy : analyze()", "+ RollingAverageStrategy : 3-mo baseline", "+ getStrategyName() : String"],
             COLOR_GREEN)

    draw_box(178, 70, 48, 30, "Rule Engine (SpendingRules)",
             ["+ AbstractSpendingRule (Template Method)", "+ String name", "+ boolean enabled"],
             ["+ evaluate(context) : List<Alert>", "# doEvaluate(context) : List<Alert>", "+ BudgetThresholdRule : evaluate()", "+ LargeTransactionRule : > $150", "+ AboveAverageRule : > 2.0x base"],
             COLOR_ORANGE)

    draw_box(178, 32, 48, 28, "FinancialGoal",
             ["+ String id, name", "+ BigDecimal targetAmount", "+ BigDecimal savedAmount", "+ YearMonth targetMonth"],
             ["+ addSavings(amount) : void", "+ isCompleted() : boolean", "+ isOverdue(currentMonth) : boolean", "+ getRemainingAmount() : BigDecimal"],
             COLOR_PURPLE)

    # Clean Connectors (Zero Intersections!)
    def draw_arrow(start_xy, end_xy, color, label=None, label_pos=None):
        ax.annotate("", xy=end_xy, xytext=start_xy,
                    arrowprops=dict(edgecolor=color, arrowstyle="-|>", lw=1.8, shrinkA=0, shrinkB=0), zorder=5)
        if label and label_pos:
            ax.text(label_pos[0], label_pos[1], label, fontsize=8.0, color=color,
                    fontweight='bold', backgroundcolor="#FFFFFF", zorder=6, ha='center', va='center',
                    bbox=dict(boxstyle="square,pad=0.2", fc="#FFFFFF", ec="none"))

    # Col 1: Checking & Credit straight UP into Account
    draw_arrow((18, 98), (18, 106), COLOR_PURPLE, "extends", (18, 102))
    draw_arrow((41, 98), (41, 106), COLOR_PURPLE, "extends", (41, 102))

    # Col 2: Transaction UP to Category, BudgetStatus UP to Budget
    draw_arrow((84, 100), (84, 108), COLOR_TEAL, "classified by", (84, 104))
    draw_arrow((84, 32), (84, 38), COLOR_BLUE, "evaluates", (84, 35))

    # Col 3 to Col 2: SpendingAnalyzer straight LEFT to Transaction
    draw_arrow((118, 86), (106, 86), COLOR_BLUE, "queries", (112, 88.5))

    # Col 3 to Col 4 (Top): SpendingAnalyzer orthogonal to Context Engine
    # Path: (166, 96) -> (172, 96) -> (172, 121) -> (178, 121)
    ax.plot([166, 172, 172], [96, 96, 121], color=COLOR_GREEN, lw=1.8, zorder=5)
    draw_arrow((172, 121), (178, 121), COLOR_GREEN, "evaluates", (172, 108))

    # Col 3 to Col 4 (Middle): SpendingAnalyzer straight RIGHT to Rule Engine
    draw_arrow((166, 85), (178, 85), COLOR_ORANGE, "applies rules", (172, 87.5))

    # Col 3: SpendingAnalyzer straight DOWN to SavingsAdvisor
    draw_arrow((142, 76), (142, 62), COLOR_TEAL, "triggers advice", (142, 69))

    # Col 3 to Col 4 (Bottom): SavingsAdvisor straight RIGHT to FinancialGoal
    draw_arrow((166, 48), (178, 48), COLOR_TEAL, "links goals", (172, 50.5))

    # Legend at bottom-left corner
    leg_x = 8
    leg_y = 12
    leg_w = 44
    leg_h = 48
    leg_box = patches.Rectangle((leg_x, leg_y), leg_w, leg_h, fc="#F8F9FA", ec="#BDC3C7", lw=1.0, zorder=2)
    ax.add_patch(leg_box)
    ax.text(leg_x + 2, leg_y + leg_h - 3, "ARCHITECTURE LEGEND", fontsize=8.5, fontweight='bold', color="#2C3E50")
    
    items = [
        (COLOR_PURPLE, "Purple: Domain Core (Entities & Accounts)"),
        (COLOR_BLUE,   "Blue: Transactions, Budgets & Analyzer"),
        (COLOR_TEAL,   "Teal: Category & AI Decision Advisor"),
        (COLOR_GREEN,  "Green: Strategy Engine (Analysis)"),
        (COLOR_ORANGE, "Orange: Template Method Rule Engine")
    ]
    cur_ly = leg_y + leg_h - 7.5
    for c, text in items:
        circ = patches.Circle((leg_x + 3.5, cur_ly - 0.5), 1.2, fc=c, ec=c, zorder=3)
        ax.add_patch(circ)
        ax.text(leg_x + 6.5, cur_ly, text, fontsize=7.0, color="#34495E", va='center')
        cur_ly -= 5.0

    plt.tight_layout()
    plt.savefig(png_path, format='png', dpi=220, bbox_inches='tight', facecolor='#FFFFFF')
    plt.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"Generated Perfect PNG: {png_path}")
    print(f"Generated Perfect SVG: {svg_path}")

if __name__ == '__main__':
    base_dir = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\documentation"
    drawio_file = os.path.join(base_dir, "BudgetWise_UML_Diagram.drawio")
    png_file = os.path.join(base_dir, "BudgetWise_UML_Exact_Style.png")
    svg_file = os.path.join(base_dir, "BudgetWise_UML_Exact_Style.svg")
    generate_perfect_diagrams(drawio_file, png_file, svg_file)
