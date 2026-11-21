import os
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Color Palette matching preferred academic style
COLOR_PURPLE = "#8A43A8"  # Domain Entities (Account, Checking, Credit, FinancialGoal)
COLOR_BLUE   = "#2980B9"  # Transactions, Budgets, SpendingAnalyzer
COLOR_GREEN  = "#27AE60"  # Strategy Pattern
COLOR_ORANGE = "#D35400"  # Rule Engine (Anomaly Rules)
COLOR_TEAL   = "#16A085"  # Category & AI Savings Advisor
COLOR_GRAY   = "#546E7A"  # Storage & Utilities
COLOR_WHITE  = "#FFFFFF"
COLOR_TEXT   = "#2C3E50"

def generate_clean_student_uml(base_dir):
    drawio_path = os.path.join(base_dir, "BudgetWise_UML_Diagram.drawio")
    png_path = os.path.join(base_dir, "BudgetWise_UML_Exact_Style.png")
    svg_path = os.path.join(base_dir, "BudgetWise_UML_Exact_Style.svg")
    puml_path = os.path.join(base_dir, "budgetwise.puml")

    # =========================================================================
    # 1. DRAW.IO XML GENERATION (14 CLEAN STUDENT CLASSES)
    # =========================================================================
    classes = [
        # --- COLUMN 1: ACCOUNTS & STORAGE (Member 1) ---
        {
            "id": "acc", "title": "Account (Abstract)",
            "x": 50, "y": 50, "w": 380, "h": 180, "color": COLOR_PURPLE,
            "fields": "+ String id&#xa;+ String name&#xa;# BigDecimal balance", "f_h": 60,
            "methods": "+ deposit(amount : BigDecimal) : void&#xa;+ {abstract} canWithdraw(amt) : boolean&#xa;+ {abstract} withdraw(amt) : void&#xa;+ {abstract} getAccountType() : String", "m_h": 90
        },
        {
            "id": "chk", "title": "CheckingAccount",
            "x": 50, "y": 280, "w": 180, "h": 140, "color": COLOR_PURPLE,
            "fields": "/* strict zero floor */", "f_h": 36,
            "methods": "+ canWithdraw(amt) : boolean&#xa;+ withdraw(amt) : void&#xa;+ getAccountType() : String", "m_h": 72
        },
        {
            "id": "crd", "title": "CreditAccount",
            "x": 250, "y": 280, "w": 180, "h": 150, "color": COLOR_PURPLE,
            "fields": "- BigDecimal creditLimit", "f_h": 36,
            "methods": "+ canWithdraw(amt) : boolean&#xa;+ withdraw(amt) : void&#xa;+ getCreditLimit() : BigDecimal&#xa;+ getAccountType() : String", "m_h": 84
        },
        {
            "id": "csv", "title": "CsvStorage (Utility)",
            "x": 50, "y": 520, "w": 380, "h": 130, "color": COLOR_GRAY,
            "fields": "/* reads &amp; writes CSV data */", "f_h": 34,
            "methods": "+ {static} loadTransactions(file) : List&lt;Transaction&gt;&#xa;+ {static} saveTransactions(file, list) : void", "m_h": 64
        },

        # --- COLUMN 2: DATA & BUDGET MODEL (Member 1 & 2) ---
        {
            "id": "cat", "title": "Category (Enum)",
            "x": 480, "y": 50, "w": 340, "h": 140, "color": COLOR_TEAL,
            "fields": "FOOD, HOUSING, TRANSPORTATION&#xa;ENTERTAINMENT, HEALTHCARE&#xa;UTILITIES, OTHER", "f_h": 68,
            "methods": "/* standard enum literals */", "m_h": 40
        },
        {
            "id": "tx", "title": "Transaction (Immutable)",
            "x": 480, "y": 250, "w": 340, "h": 220, "color": COLOR_BLUE,
            "fields": "- String id, accountId&#xa;- LocalDate date&#xa;- String description&#xa;- BigDecimal amount [scale 2]&#xa;- Type type (INCOME / EXPENSE)&#xa;- Category category", "f_h": 110,
            "methods": "+ getId() : String&#xa;+ getAmount() : BigDecimal&#xa;+ getType() : Type&#xa;+ getCategory() : Category", "m_h": 78
        },
        {
            "id": "bdg", "title": "Budget (Entity)",
            "x": 480, "y": 520, "w": 340, "h": 160, "color": COLOR_BLUE,
            "fields": "- Category category&#xa;- YearMonth month&#xa;- BigDecimal limit [scale 2]", "f_h": 60,
            "methods": "+ calculateUsagePercentage(spent) : double&#xa;+ getCategory() : Category&#xa;+ getLimit() : BigDecimal", "m_h": 68
        },

        # --- COLUMN 3: SERVICES & CONTROLLERS (Member 2 & 3 & 4) ---
        {
            "id": "ana", "title": "SpendingAnalyzer (Controller)",
            "x": 880, "y": 250, "w": 360, "h": 190, "color": COLOR_BLUE,
            "fields": "- SpendingStrategy strategy&#xa;- List&lt;SpendingRule&gt; rules", "f_h": 46,
            "methods": "+ setStrategy(s : SpendingStrategy) : void&#xa;+ addRule(rule : SpendingRule) : void&#xa;+ calculateSpending(m, cat, txList) : BigDecimal&#xa;+ runAnalysis(m, txList, budgets) : List&lt;Alert&gt;", "m_h": 112
        },
        {
            "id": "adv", "title": "SavingsAdvisor (AI Decision Engine)",
            "x": 880, "y": 520, "w": 360, "h": 150, "color": COLOR_TEAL,
            "fields": "/* analyzes discretionary spending */", "f_h": 34,
            "methods": "+ generateAdvice(goal, month, txList) : List&lt;String&gt;&#xa;/* pace: (target-saved)/monthsRemaining */&#xa;/* suggests 25% cut on top category */", "m_h": 84
        },

        # --- COLUMN 4: STRATEGY & RULES & GOALS (Member 2 & 3) ---
        {
            "id": "str", "title": "SpendingStrategy (Interface)",
            "x": 1300, "y": 50, "w": 360, "h": 140, "color": COLOR_GREEN,
            "fields": "/* Strategy Design Pattern */", "f_h": 34,
            "methods": "+ calculateSpending(month, cat, txList) : BigDecimal&#xa;+ MonthlyTotalStrategy : calendar month&#xa;+ RollingAverageStrategy : 3-mo baseline", "m_h": 74
        },
        {
            "id": "rul", "title": "SpendingRule (Interface)",
            "x": 1300, "y": 250, "w": 360, "h": 160, "color": COLOR_ORANGE,
            "fields": "/* Anomaly Detection Rule Engine */", "f_h": 34,
            "methods": "+ evaluate(tx, allTxs, budget) : Alert&#xa;+ BudgetThresholdRule : &gt;= 80% / 100%&#xa;+ LargePurchaseRule : &gt; $150.00", "m_h": 94
        },
        {
            "id": "gol", "title": "FinancialGoal",
            "x": 1300, "y": 520, "w": 360, "h": 170, "color": COLOR_PURPLE,
            "fields": "- String name&#xa;- BigDecimal targetAmount&#xa;- BigDecimal savedAmount&#xa;- YearMonth targetMonth", "f_h": 76,
            "methods": "+ addSavings(amount) : void&#xa;+ getRemainingAmount() : BigDecimal&#xa;+ calculateMonthlySavingsPace(currentMonth) : BigDecimal&#xa;+ getProgressPercentage() : double", "m_h": 62
        }
    ]

    edges = [
        # Checking -> Account: straight UP
        {"id": "e_chk_acc", "val": "extends", "src": "chk", "tgt": "acc", "color": COLOR_PURPLE,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.25;entryY=1;entryDx=0;entryDy=0;", "pts": []},
        # Credit -> Account: straight UP
        {"id": "e_crd_acc", "val": "extends", "src": "crd", "tgt": "acc", "color": COLOR_PURPLE,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.75;entryY=1;entryDx=0;entryDy=0;", "pts": []},
        # Transaction -> Category: straight UP
        {"id": "e_tx_cat", "val": "classified by", "src": "tx", "tgt": "cat", "color": COLOR_TEAL,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.5;entryY=1;entryDx=0;entryDy=0;", "pts": []},
        # Budget -> Category: straight UP
        {"id": "e_bdg_cat", "val": "targets", "src": "bdg", "tgt": "tx", "color": COLOR_BLUE,
         "exit": "exitX=0.5;exitY=0;exitDx=0;exitDy=0;", "entry": "entryX=0.5;entryY=1;entryDx=0;entryDy=0;", "pts": []},
        # SpendingAnalyzer -> Transaction: straight LEFT
        {"id": "e_ana_tx", "val": "queries", "src": "ana", "tgt": "tx", "color": COLOR_BLUE,
         "exit": "exitX=0;exitY=0.5;exitDx=0;exitDy=0;", "entry": "entryX=1;entryY=0.5;entryDx=0;entryDy=0;", "pts": []},
        # SpendingAnalyzer -> SpendingStrategy: straight RIGHT-UP
        {"id": "e_ana_str", "val": "uses strategy", "src": "ana", "tgt": "str", "color": COLOR_GREEN,
         "exit": "exitX=1;exitY=0.2;exitDx=0;exitDy=0;", "entry": "entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
         "pts": [(1270, 288), (1270, 120)]},
        # SpendingAnalyzer -> SpendingRule: straight RIGHT
        {"id": "e_ana_rul", "val": "evaluates rules", "src": "ana", "tgt": "rul", "color": COLOR_ORANGE,
         "exit": "exitX=1;exitY=0.6;exitDx=0;exitDy=0;", "entry": "entryX=0;entryY=0.5;entryDx=0;entryDy=0;", "pts": []},
        # SpendingAnalyzer -> SavingsAdvisor: straight DOWN
        {"id": "e_ana_adv", "val": "triggers advice", "src": "ana", "tgt": "adv", "color": COLOR_TEAL,
         "exit": "exitX=0.5;exitY=1;exitDx=0;exitDy=0;", "entry": "entryX=0.5;entryY=0;entryDx=0;entryDy=0;", "pts": []},
        # SavingsAdvisor -> FinancialGoal: straight RIGHT
        {"id": "e_adv_gol", "val": "evaluates goal", "src": "adv", "tgt": "gol", "color": COLOR_PURPLE,
         "exit": "exitX=1;exitY=0.5;exitDx=0;exitDy=0;", "entry": "entryX=0;entryY=0.5;entryDx=0;entryDy=0;", "pts": []}
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<mxfile host="app.diagrams.net" modified="2026-11-21T12:00:00.000Z" agent="BudgetWise" version="24.0.0" type="device">',
           '  <diagram id="budgetwise-student-diagram" name="BudgetWise Clean UML Class Diagram">',
           '    <mxGraphModel dx="1750" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1750" pageHeight="1100" background="#FFFFFF">',
           '      <root>',
           '        <mxCell id="0"/>',
           '        <mxCell id="1" parent="0"/>']

    for c in classes:
        cid, title = c["id"], c["title"]
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        col = c["color"]
        fields, methods = c["fields"], c["methods"]
        fh, mh = c["f_h"], c["m_h"]

        xml.append(f'        <mxCell id="{cid}" value="{title}" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor={col};fontColor=#ffffff;strokeColor={col};rounded=0;fontSize=12;shadow=1;" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>')
        xml.append('        </mxCell>')

        xml.append(f'        <mxCell id="{cid}_fields" value="{fields}" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=top;spacingLeft=10;spacingRight=10;spacingTop=6;spacingBottom=4;overflow=visible;whiteSpace=nowrap;html=1;fontSize=11;fontColor=#2C3E50;fontFamily=monospace;" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="28" width="{w}" height="{fh}" as="geometry"/>')
        xml.append('        </mxCell>')

        xml.append(f'        <mxCell id="{cid}_line" value="" style="line;strokeWidth=1.2;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=0;spacingRight=0;rotatable=0;strokeColor={col};html=1;" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="{28+fh}" width="{w}" height="8" as="geometry"/>')
        xml.append('        </mxCell>')

        xml.append(f'        <mxCell id="{cid}_methods" value="{methods}" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=top;spacingLeft=10;spacingRight=10;spacingTop=6;spacingBottom=6;overflow=visible;whiteSpace=nowrap;html=1;fontSize=11;fontColor=#2C3E50;fontFamily=monospace;" vertex="1" parent="{cid}">')
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
    print(f"Generated Clean Student Draw.io XML: {drawio_path}")

    # =========================================================================
    # 2. GENERATE HIGH-RES PNG & SVG (MATPLOTLIB)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(24, 14), dpi=220)
    ax.set_xlim(0, 240)
    ax.set_ylim(0, 140)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title & Subtitle Banner
    ax.text(8, 134, "BudgetWise — Clean UML Class Diagram (Student Architecture Specification)",
            fontsize=16, fontweight='bold', color="#2C3E50", ha='left')
    ax.text(8, 131, "UVT Object-Oriented Programming 2026 | Project 4 | 14 Core Classes | Zero Crossings & Full Text Visibility",
            fontsize=10, color="#7F8C8D", ha='left')

    def draw_box(x, y, w, h, title, fields, methods, color):
        body = patches.Rectangle((x, y), w, h, fc=COLOR_WHITE, ec=color, lw=1.8, zorder=2)
        ax.add_patch(body)
        hh = 4.2
        header = patches.Rectangle((x, y + h - hh), w, hh, fc=color, ec=color, lw=1.8, zorder=3)
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
    # Col 1: x = 8..56 (w=48), Checking w=23, Credit w=23
    # Col 2: x = 66..112 (w=46)
    # Col 3: x = 122..172 (w=50)
    # Col 4: x = 182..232 (w=50)

    # --- Col 1: Accounts & Storage ---
    draw_box(8, 96, 48, 28, "Account (Abstract)",
             ["+ String id, name", "# BigDecimal balance"],
             ["+ deposit(amount) : void", "+ {abstract} canWithdraw(amt) : bool", "+ {abstract} withdraw(amt) : void", "+ {abstract} getAccountType() : String"],
             COLOR_PURPLE)

    draw_box(8, 64, 23, 24, "CheckingAccount",
             ["/* zero-overdraft */"],
             ["+ canWithdraw() : bool", "+ withdraw(amt) : void", "+ getAccountType() : String"],
             COLOR_PURPLE)

    draw_box(33, 64, 23, 24, "CreditAccount",
             ["- BigDecimal creditLimit"],
             ["+ canWithdraw() : bool", "+ withdraw(amt) : void", "+ getCreditLimit() : BD", "+ getAccountType() : String"],
             COLOR_PURPLE)

    draw_box(8, 28, 48, 24, "CsvStorage (Utility)",
             ["/* reads &amp; writes CSV */"],
             ["+ {static} loadTransactions(file) : List", "+ {static} saveTransactions(file, list) : void"],
             COLOR_GRAY)

    # --- Col 2: Data Model ---
    draw_box(66, 98, 46, 26, "Category (Enum)",
             ["FOOD, HOUSING, TRANSPORT", "ENTERTAINMENT, HEALTHCARE", "UTILITIES, OTHER"],
             ["/* standard enum literals */"],
             COLOR_TEAL)

    draw_box(66, 56, 46, 34, "Transaction (Immutable)",
             ["- String id, accountId", "- LocalDate date, description", "- BigDecimal amount [scale 2]", "- Type type (INCOME/EXPENSE)", "- Category category"],
             ["+ getId() : String", "+ getAmount() : BigDecimal", "+ getType() : Type", "+ getCategory() : Category"],
             COLOR_BLUE)

    draw_box(66, 22, 46, 26, "Budget (Entity)",
             ["- Category category", "- YearMonth month", "- BigDecimal limit [scale 2]"],
             ["+ calculateUsagePercentage(spent) : double", "+ getCategory() : Category", "+ getLimit() : BigDecimal"],
             COLOR_BLUE)

    # --- Col 3: Controllers & Services ---
    draw_box(122, 60, 50, 32, "SpendingAnalyzer (Controller)",
             ["- SpendingStrategy strategy", "- List<SpendingRule> rules"],
             ["+ setStrategy(s : SpendingStrategy) : void", "+ addRule(rule : SpendingRule) : void", "+ calculateSpending(m, cat, txs) : BD", "+ runAnalysis(m, txs, budgets) : List"],
             COLOR_BLUE)

    draw_box(122, 22, 50, 26, "SavingsAdvisor (AI Decision Support)",
             ["/* analyzes discretionary spending */"],
             ["+ generateAdvice(goal, month, txs) : List", "/* required pace: (target-saved)/months */", "/* suggests 25% cut on top category */"],
             COLOR_TEAL)

    # --- Col 4: Strategy, Rules & Goals ---
    draw_box(182, 98, 50, 26, "SpendingStrategy (Interface)",
             ["/* Strategy Design Pattern */"],
             ["+ calculateSpending(m, cat, txs) : BD", "+ MonthlyTotalStrategy : calendar total", "+ RollingAverageStrategy : 3-mo average"],
             COLOR_GREEN)

    draw_box(182, 58, 50, 30, "SpendingRule (Interface)",
             ["/* Anomaly Detection Rule Engine */"],
             ["+ evaluate(tx, allTxs, budget) : Alert", "+ BudgetThresholdRule : >= 80% / 100%", "+ LargePurchaseRule : > $150.00"],
             COLOR_ORANGE)

    draw_box(182, 18, 50, 30, "FinancialGoal",
             ["- String name", "- BigDecimal targetAmount, savedAmount", "- YearMonth targetMonth"],
             ["+ addSavings(amount) : void", "+ getRemainingAmount() : BigDecimal", "+ calculateMonthlySavingsPace() : BigDecimal", "+ getProgressPercentage() : double"],
             COLOR_PURPLE)

    # Connectors
    def draw_arrow(start_xy, end_xy, color, label=None, label_pos=None):
        ax.annotate("", xy=end_xy, xytext=start_xy,
                    arrowprops=dict(edgecolor=color, arrowstyle="-|>", lw=1.8, shrinkA=0, shrinkB=0), zorder=5)
        if label and label_pos:
            ax.text(label_pos[0], label_pos[1], label, fontsize=8.0, color=color,
                    fontweight='bold', backgroundcolor="#FFFFFF", zorder=6, ha='center', va='center',
                    bbox=dict(boxstyle="square,pad=0.2", fc="#FFFFFF", ec="none"))

    # Col 1: Checking & Credit straight UP into Account
    draw_arrow((19, 88), (19, 96), COLOR_PURPLE, "extends", (19, 92))
    draw_arrow((44, 88), (44, 96), COLOR_PURPLE, "extends", (44, 92))

    # Col 2: Transaction UP to Category, Budget UP to Transaction
    draw_arrow((89, 90), (89, 98), COLOR_TEAL, "classified by", (89, 94))
    draw_arrow((89, 48), (89, 56), COLOR_BLUE, "targets", (89, 52))

    # Col 3 to Col 2: SpendingAnalyzer straight LEFT to Transaction
    draw_arrow((122, 72), (112, 72), COLOR_BLUE, "queries", (117, 74.5))

    # Col 3 to Col 4 (Top): SpendingAnalyzer orthogonal to SpendingStrategy
    ax.plot([172, 177, 177], [84, 84, 111], color=COLOR_GREEN, lw=1.8, zorder=5)
    draw_arrow((177, 111), (182, 111), COLOR_GREEN, "uses strategy", (177, 98))

    # Col 3 to Col 4 (Middle): SpendingAnalyzer straight RIGHT to SpendingRule
    draw_arrow((172, 72), (182, 72), COLOR_ORANGE, "applies rules", (177, 74.5))

    # Col 3: SpendingAnalyzer straight DOWN to SavingsAdvisor
    draw_arrow((147, 60), (147, 48), COLOR_TEAL, "triggers advice", (147, 54))

    # Col 3 to Col 4 (Bottom): SavingsAdvisor straight RIGHT to FinancialGoal
    draw_arrow((172, 35), (182, 35), COLOR_PURPLE, "evaluates goal", (177, 37.5))

    plt.tight_layout()
    plt.savefig(png_path, format='png', dpi=220, bbox_inches='tight', facecolor='#FFFFFF')
    plt.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"Generated Clean Student PNG: {png_path}")
    print(f"Generated Clean Student SVG: {svg_path}")

    # =========================================================================
    # 3. GENERATE PLANTUML FILE (.puml)
    # =========================================================================
    puml = [
        "@startuml budgetwise_clean",
        "skinparam classAttributeIconSize false",
        "skinparam roundcorner 8",
        "skinparam linetype ortho",
        "",
        "package \"com.budgetwise.model\" {",
        "    abstract class Account {",
        "        - String id",
        "        - String name",
        "        # BigDecimal balance",
        "        + deposit(BigDecimal amount) : void",
        "        + {abstract} canWithdraw(BigDecimal amount) : boolean",
        "        + {abstract} withdraw(BigDecimal amount) : void",
        "        + {abstract} getAccountType() : String",
        "    }",
        "    class CheckingAccount extends Account {",
        "        + canWithdraw(amount) : boolean",
        "        + withdraw(amount) : void",
        "        + getAccountType() : String",
        "    }",
        "    class CreditAccount extends Account {",
        "        - BigDecimal creditLimit",
        "        + canWithdraw(amount) : boolean",
        "        + withdraw(amount) : void",
        "        + getCreditLimit() : BigDecimal",
        "        + getAccountType() : String",
        "    }",
        "    enum Category {",
        "        FOOD",
        "        HOUSING",
        "        TRANSPORTATION",
        "        ENTERTAINMENT",
        "        HEALTHCARE",
        "        UTILITIES",
        "        OTHER",
        "    }",
        "    class Transaction {",
        "        - String id",
        "        - String accountId",
        "        - LocalDate date",
        "        - String description",
        "        - BigDecimal amount",
        "        - Type type",
        "        - Category category",
        "    }",
        "    class Budget {",
        "        - Category category",
        "        - YearMonth month",
        "        - BigDecimal limit",
        "        + calculateUsagePercentage(BigDecimal spent) : double",
        "    }",
        "    class FinancialGoal {",
        "        - String name",
        "        - BigDecimal targetAmount",
        "        - BigDecimal savedAmount",
        "        - YearMonth targetMonth",
        "        + addSavings(amount) : void",
        "        + calculateMonthlySavingsPace(currentMonth) : BigDecimal",
        "    }",
        "    class Alert {",
        "        - String ruleName",
        "        - String message",
        "        - Severity severity",
        "    }",
        "}",
        "",
        "package \"com.budgetwise.strategy\" {",
        "    interface SpendingStrategy {",
        "        + calculateSpending(month, category, transactions) : BigDecimal",
        "        + getStrategyName() : String",
        "    }",
        "    class MonthlyTotalStrategy implements SpendingStrategy",
        "    class RollingAverageStrategy implements SpendingStrategy",
        "}",
        "",
        "package \"com.budgetwise.rule\" {",
        "    interface SpendingRule {",
        "        + evaluate(transaction, allTransactions, budget) : Alert",
        "        + getRuleName() : String",
        "    }",
        "    class BudgetThresholdRule implements SpendingRule",
        "    class LargePurchaseRule implements SpendingRule",
        "}",
        "",
        "package \"com.budgetwise.service\" {",
        "    class SpendingAnalyzer {",
        "        - SpendingStrategy strategy",
        "        - List<SpendingRule> rules",
        "        + setStrategy(SpendingStrategy strategy) : void",
        "        + calculateSpending(month, category, transactions) : BigDecimal",
        "        + runAnalysis(month, transactions, budgets) : List<Alert>",
        "    }",
        "    class SavingsAdvisor {",
        "        + generateAdvice(goal, month, transactions) : List<String>",
        "    }",
        "}",
        "",
        "package \"com.budgetwise.storage\" {",
        "    class CsvStorage {",
        "        + {static} loadTransactions(File file) : List<Transaction>",
        "        + {static} saveTransactions(File file, List<Transaction> list) : void",
        "    }",
        "}",
        "",
        "Transaction --> Category : classified by",
        "Budget --> Category : targets",
        "SpendingAnalyzer --> Transaction : queries",
        "SpendingAnalyzer --> SpendingStrategy : uses strategy",
        "SpendingAnalyzer --> SpendingRule : evaluates rules",
        "SpendingAnalyzer --> SavingsAdvisor : triggers advice",
        "SavingsAdvisor --> FinancialGoal : evaluates goal",
        "@enduml"
    ]

    with open(puml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(puml))
    print(f"Generated Clean Student PlantUML: {puml_path}")

if __name__ == '__main__':
    base_dir = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\documentation"
    generate_clean_student_uml(base_dir)
