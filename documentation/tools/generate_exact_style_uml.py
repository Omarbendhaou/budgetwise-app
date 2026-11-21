import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Colors matching the user's screenshot:
# Purple: #8A43A8 (User / AuthController)
# Blue:   #3498DB (AnalysisController / AnalysisSchema)
# Green:  #2ECC71 (Context Engine)
# Orange: #E67E22 (FlaskAPI / Python)
# Teal:   #16A085

COLOR_PURPLE = "#8A43A8"
COLOR_BLUE   = "#2980B9"
COLOR_GREEN  = "#27AE60"
COLOR_ORANGE = "#D35400"
COLOR_TEAL   = "#16A085"
COLOR_WHITE  = "#FFFFFF"
COLOR_TEXT   = "#2C3E50"
COLOR_LINE   = "#BDC3C7"

def draw_exact_style_diagram(output_png, output_svg, output_drawio):
    fig, ax = plt.subplots(figsize=(20, 14), dpi=220)
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 140)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Main Title
    ax.text(10, 134, "BudgetWise — UML Class Diagram (Financial Entities & Analysis Architecture)",
            fontsize=15, fontweight='bold', color="#2C3E50", ha='left')
    ax.text(10, 131, "UVT Object-Oriented Programming 2026 | Financial Entities & Analysis Components Specification",
            fontsize=9.5, color="#7F8C8D", ha='left')

    # Function to draw class box exactly matching user's image style:
    # Solid colored header bar, matching thin colored border, white body, dividing line
    def draw_uml_box(x, y, w, h, title, fields, methods, color):
        # Body box with matching colored border
        body_box = patches.Rectangle((x, y), w, h, fc=COLOR_WHITE, ec=color, lw=1.5, zorder=2)
        ax.add_patch(body_box)

        # Solid colored header bar
        header_h = 4.2
        header_box = patches.Rectangle((x, y + h - header_h), w, header_h, fc=color, ec=color, lw=1.5, zorder=3)
        ax.add_patch(header_box)

        # Centered white bold title
        ax.text(x + w / 2, y + h - (header_h / 2), title,
                fontsize=9.0, fontweight='bold', color=COLOR_WHITE, ha='center', va='center', zorder=4)

        # Fields (Attributes)
        cur_y = y + h - header_h - 1.4
        if fields:
            for f in fields:
                ax.text(x + 1.2, cur_y, f, fontsize=7.0, color=COLOR_TEXT, fontfamily='monospace', va='top', zorder=4)
                cur_y -= 1.6
            cur_y -= 0.4
            # Divider line
            ax.plot([x, x + w], [cur_y, cur_y], color=color, lw=1.0, zorder=4)
            cur_y -= 1.2

        # Methods (Operations)
        if methods:
            for m in methods:
                ax.text(x + 1.2, cur_y, m, fontsize=7.0, color=COLOR_TEXT, fontfamily='monospace', va='top', zorder=4)
                cur_y -= 1.6

    # =========================================================================
    # 1. FINANCIAL ENTITIES (LEFT & UPPER-MIDDLE)
    # =========================================================================

    # Account (Abstract) - Purple
    draw_uml_box(8, 96, 42, 30, "Account (Abstract)",
                 fields=["+ String id", "+ String name", "+ BigDecimal openingBalance"],
                 methods=["+ canWithdraw(amount, bal) : boolean",
                          "+ calculateAvailableFunds(bal) : BigDecimal",
                          "+ getOpeningBalance() : BigDecimal",
                          "+ getAccountType() : String"],
                 color=COLOR_PURPLE)

    # CheckingAccount - Purple
    draw_uml_box(8, 70, 42, 19, "CheckingAccount",
                 fields=["/* zero-overdraft balance floor */"],
                 methods=["+ canWithdraw(amount, bal) : boolean",
                          "+ calculateAvailableFunds(bal) : BigDecimal",
                          "+ getAccountType() : String"],
                 color=COLOR_PURPLE)

    # CreditAccount - Purple
    draw_uml_box(8, 44, 42, 21, "CreditAccount",
                 fields=["+ BigDecimal creditLimit"],
                 methods=["+ canWithdraw(amount, bal) : boolean",
                          "+ calculateAvailableFunds(bal) : BigDecimal",
                          "+ getCreditLimit() : BigDecimal",
                          "+ getAccountType() : String"],
                 color=COLOR_PURPLE)

    # Category - Teal
    draw_uml_box(56, 102, 38, 24, "Category (Domain Entity)",
                 fields=["+ String id", "+ String name", "+ boolean isCustom", "+ Category UNCATEGORIZED"],
                 methods=["+ getId() : String", "+ getName() : String", "+ isCustom() : boolean", "+ equals(obj) : boolean"],
                 color=COLOR_TEAL)

    # Transaction (Immutable) - Blue (like AnalysisSchema)
    draw_uml_box(56, 60, 40, 36, "Transaction (Immutable)",
                 fields=["+ String id", "+ String accountId", "+ LocalDate date",
                         "+ String description", "+ BigDecimal amount [scale 2]",
                         "+ TransactionType type", "+ Category category"],
                 methods=["+ getSignedAmount() : BigDecimal",
                          "+ getAmount() : BigDecimal",
                          "+ getType() : TransactionType",
                          "+ getCategory() : Category",
                          "+ equals(obj) : boolean"],
                 color=COLOR_BLUE)

    # Budget (Immutable) - Blue
    draw_uml_box(8, 14, 42, 24, "Budget (Entity)",
                 fields=["+ Category category", "+ YearMonth month", "+ BigDecimal limit [scale 2]"],
                 methods=["+ getCategory() : Category", "+ getMonth() : YearMonth",
                          "+ getLimit() : BigDecimal", "+ equals(obj) : boolean"],
                 color=COLOR_BLUE)

    # BudgetStatus - Blue
    draw_uml_box(56, 14, 40, 38, "BudgetStatus (Record)",
                 fields=["+ Budget budget", "+ BigDecimal spent", "+ BigDecimal remaining",
                         "+ BigDecimal utilizationPercentage", "+ BudgetState state"],
                 methods=["+ compute(b, spent, policy) : BudgetStatus",
                          "  /* exact cross-multiplication: */",
                          "  /* spent*100 vs limit*threshold */",
                          "+ getUtilizationPercentage() : BigDecimal",
                          "+ getState() : BudgetState"],
                 color=COLOR_BLUE)

    # FinancialGoal - Purple
    draw_uml_box(102, 14, 40, 24, "FinancialGoal",
                 fields=["+ String id", "+ String name", "+ BigDecimal targetAmount",
                         "+ BigDecimal savedAmount", "+ YearMonth targetMonth"],
                 methods=["+ addSavings(amount) : void", "+ isCompleted() : boolean",
                          "+ isOverdue(currentMonth) : boolean", "+ getRemainingAmount() : BigDecimal"],
                 color=COLOR_PURPLE)

    # =========================================================================
    # 2. ANALYSIS COMPONENTS & CONTROLLERS (CENTER & RIGHT)
    # =========================================================================

    # SpendingAnalyzer - Blue (Central Controller style, exactly like AnalysisController in screenshot!)
    draw_uml_box(102, 86, 44, 38, "SpendingAnalyzer (Controller)",
                 fields=["+ SpendingAnalysisStrategy strategy", "+ List<SpendingRule> rules"],
                 methods=["+ addRule(rule : SpendingRule) : void",
                          "+ setStrategy(s : AnalysisStrategy) : void",
                          "+ analyzeMonth(month, statuses) : List<Alert>",
                          "+ getRules() : List<SpendingRule>",
                          "+ getStrategy() : SpendingAnalysisStrategy"],
                 color=COLOR_BLUE)

    # Context / Strategy Engine - Green (exactly like Context Engine in screenshot!)
    draw_uml_box(152, 98, 42, 26, "Context Engine (Strategy)",
                 fields=["+ SpendingAnalysisStrategy (Interface)"],
                 methods=["+ analyze(month, txList) : SpendingSummary",
                          "+ MonthlyTotalStrategy : analyze()",
                          "+ RollingAverageStrategy : 3-mo baseline",
                          "+ getStrategyName() : String"],
                 color=COLOR_GREEN)

    # SpendingRule Engine - Orange (exactly like FlaskAPI / BERT in screenshot!)
    draw_uml_box(152, 48, 42, 42, "Rule Engine (SpendingRules)",
                 fields=["+ AbstractSpendingRule (Template Method)",
                         "+ String name", "+ boolean enabled"],
                 methods=["+ evaluate(context) : List<Alert>",
                          "# doEvaluate(context) : List<Alert>",
                          "+ BudgetThresholdRule : evaluate()",
                          "+ LargeTransactionRule : > $150",
                          "+ AboveAverageRule : > 2.0x base"],
                 color=COLOR_ORANGE)

    # SavingsAdvisor - Teal / Green (Intelligent Decision Support)
    draw_uml_box(148, 14, 46, 26, "SavingsAdvisor (AI Decision Support)",
                 fields=["+ List<SavingsSuggestionRule> rules"],
                 methods=["+ addRule(rule) : void",
                          "+ generateSuggestions(ctx, curr) : List<Rec>",
                          "+ GoalContributionRule : (target-saved)/months",
                          "+ computeConcentrationRatio() : BigDecimal"],
                 color=COLOR_TEAL)

    # =========================================================================
    # CONNECTING ARROWS & LABELS (matching user's screenshot style)
    # =========================================================================

    # Arrow helper
    def draw_connector(start_xy, end_xy, color, label=None, label_pos=None):
        ax.annotate("", xy=end_xy, xytext=start_xy,
                    arrowprops=dict(edgecolor=color, arrowstyle="->", lw=1.5, shrinkA=0, shrinkB=0), zorder=5)
        if label and label_pos:
            ax.text(label_pos[0], label_pos[1], label, fontsize=7.5, color=color,
                    fontweight='bold', backgroundcolor="#FFFFFF", zorder=6)

    # Account Inheritance (Checking & Credit -> Account)
    draw_connector((29, 70), (29, 96), COLOR_PURPLE, "extends", (24, 82))
    draw_connector((29, 65), (29, 70), COLOR_PURPLE)

    # Transaction -> Category
    draw_connector((75, 96), (75, 102), COLOR_TEAL, "classified by", (76, 98.5))

    # SpendingAnalyzer -> Context Engine (Green, just like in screenshot!)
    draw_connector((146, 110), (152, 110), COLOR_GREEN, "evaluates", (146.5, 111.5))

    # SpendingAnalyzer -> Rule Engine (Orange, just like in screenshot!)
    draw_connector((124, 86), (152, 70), COLOR_ORANGE, "applies rules", (132, 78))

    # SpendingAnalyzer -> BudgetStatus / Transactions (queries)
    draw_connector((102, 75), (96, 75), COLOR_BLUE, "queries", (97, 76))

    # BudgetStatus -> Budget
    draw_connector((56, 26), (50, 26), COLOR_BLUE, "evaluates", (50.5, 27))

    # SavingsAdvisor -> FinancialGoal
    draw_connector((148, 26), (142, 26), COLOR_TEAL, "links goals", (142.5, 27.5))

    # SpendingAnalyzer -> SavingsAdvisor
    draw_connector((124, 86), (148, 38), COLOR_TEAL, "triggers advice", (134, 56))

    plt.tight_layout()
    plt.savefig(output_png, format='png', dpi=220, bbox_inches='tight', facecolor='#FFFFFF')
    plt.savefig(output_svg, format='svg', bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"Generated Exact-Style PNG: {output_png}")
    print(f"Generated Exact-Style SVG: {output_svg}")

    # =========================================================================
    # GENERATE NATIVE DRAW.IO XML (.drawio)
    # =========================================================================
    drawio_xml = """<mxfile host="app.diagrams.net" modified="2026-11-16T16:15:00.000Z" agent="BudgetWise" version="24.0.0" type="device">
  <diagram id="budgetwise-uml" name="BudgetWise UML Class Diagram">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" background="#FFFFFF">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- Account (Abstract) -->
        <mxCell id="acc" value="&lt;b&gt;Account (Abstract)&lt;/b&gt;&lt;hr/&gt;+ String id&lt;br/&gt;+ String name&lt;br/&gt;+ BigDecimal openingBalance&lt;hr/&gt;+ canWithdraw(amount, bal) : boolean&lt;br/&gt;+ calculateAvailableFunds(bal) : BigDecimal&lt;br/&gt;+ getOpeningBalance() : BigDecimal" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#8A43A8;fontColor=#ffffff;strokeColor=#8A43A8;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="60" y="80" width="280" height="190" as="geometry"/>
        </mxCell>

        <!-- CheckingAccount -->
        <mxCell id="chk" value="&lt;b&gt;CheckingAccount&lt;/b&gt;&lt;hr/&gt;/* zero-overdraft balance floor */&lt;hr/&gt;+ canWithdraw(amount, bal) : boolean&lt;br/&gt;+ calculateAvailableFunds(bal) : BigDecimal" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#8A43A8;fontColor=#ffffff;strokeColor=#8A43A8;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="60" y="320" width="280" height="120" as="geometry"/>
        </mxCell>

        <!-- CreditAccount -->
        <mxCell id="crd" value="&lt;b&gt;CreditAccount&lt;/b&gt;&lt;hr/&gt;+ BigDecimal creditLimit&lt;hr/&gt;+ canWithdraw(amount, bal) : boolean&lt;br/&gt;+ calculateAvailableFunds(bal) : BigDecimal&lt;br/&gt;+ getCreditLimit() : BigDecimal" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#8A43A8;fontColor=#ffffff;strokeColor=#8A43A8;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="60" y="480" width="280" height="130" as="geometry"/>
        </mxCell>

        <!-- Category -->
        <mxCell id="cat" value="&lt;b&gt;Category (Domain Entity)&lt;/b&gt;&lt;hr/&gt;+ String id&lt;br/&gt;+ String name&lt;br/&gt;+ boolean isCustom&lt;br/&gt;+ Category UNCATEGORIZED&lt;hr/&gt;+ getId() : String&lt;br/&gt;+ getName() : String&lt;br/&gt;+ isCustom() : boolean" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#16A085;fontColor=#ffffff;strokeColor=#16A085;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="400" y="80" width="260" height="160" as="geometry"/>
        </mxCell>

        <!-- Transaction -->
        <mxCell id="tx" value="&lt;b&gt;Transaction (Immutable)&lt;/b&gt;&lt;hr/&gt;+ String id&lt;br/&gt;+ String accountId&lt;br/&gt;+ LocalDate date&lt;br/&gt;+ String description&lt;br/&gt;+ BigDecimal amount [scale 2]&lt;br/&gt;+ TransactionType type&lt;br/&gt;+ Category category&lt;hr/&gt;+ getSignedAmount() : BigDecimal&lt;br/&gt;+ getAmount() : BigDecimal&lt;br/&gt;+ getType() : TransactionType" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#2980B9;fontColor=#ffffff;strokeColor=#2980B9;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="400" y="280" width="260" height="230" as="geometry"/>
        </mxCell>

        <!-- Budget -->
        <mxCell id="bdg" value="&lt;b&gt;Budget (Entity)&lt;/b&gt;&lt;hr/&gt;+ Category category&lt;br/&gt;+ YearMonth month&lt;br/&gt;+ BigDecimal limit [scale 2]&lt;hr/&gt;+ getCategory() : Category&lt;br/&gt;+ getMonth() : YearMonth&lt;br/&gt;+ getLimit() : BigDecimal" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#2980B9;fontColor=#ffffff;strokeColor=#2980B9;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="60" y="660" width="280" height="150" as="geometry"/>
        </mxCell>

        <!-- BudgetStatus -->
        <mxCell id="bds" value="&lt;b&gt;BudgetStatus (Record)&lt;/b&gt;&lt;hr/&gt;+ Budget budget&lt;br/&gt;+ BigDecimal spent&lt;br/&gt;+ BigDecimal remaining&lt;br/&gt;+ BigDecimal utilizationPercentage&lt;br/&gt;+ BudgetState state&lt;hr/&gt;+ compute(budget, spent, policy) : BudgetStatus&lt;br/&gt;/* exact cross-multiplication: spent*100 vs limit*thresh */" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#2980B9;fontColor=#ffffff;strokeColor=#2980B9;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="400" y="560" width="280" height="190" as="geometry"/>
        </mxCell>

        <!-- SpendingAnalyzer (Controller) -->
        <mxCell id="ana" value="&lt;b&gt;SpendingAnalyzer (Controller)&lt;/b&gt;&lt;hr/&gt;+ SpendingAnalysisStrategy strategy&lt;br/&gt;+ List&amp;lt;SpendingRule&amp;gt; rules&lt;hr/&gt;+ addRule(rule : SpendingRule) : void&lt;br/&gt;+ setStrategy(s : AnalysisStrategy) : void&lt;br/&gt;+ analyzeMonth(month, statuses) : List&amp;lt;Alert&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#2980B9;fontColor=#ffffff;strokeColor=#2980B9;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="740" y="180" width="280" height="180" as="geometry"/>
        </mxCell>

        <!-- Context Engine (Strategy) -->
        <mxCell id="ctx" value="&lt;b&gt;Context Engine (Strategy)&lt;/b&gt;&lt;hr/&gt;+ SpendingAnalysisStrategy (Interface)&lt;hr/&gt;+ analyze(month, txList) : SpendingSummary&lt;br/&gt;+ MonthlyTotalStrategy : analyze()&lt;br/&gt;+ RollingAverageStrategy : 3-mo baseline" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#27AE60;fontColor=#ffffff;strokeColor=#27AE60;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="1100" y="100" width="280" height="140" as="geometry"/>
        </mxCell>

        <!-- Rule Engine (SpendingRules) -->
        <mxCell id="rul" value="&lt;b&gt;Rule Engine (SpendingRules)&lt;/b&gt;&lt;hr/&gt;+ AbstractSpendingRule (Template Method)&lt;br/&gt;+ String name&lt;br/&gt;+ boolean enabled&lt;hr/&gt;+ evaluate(context) : List&amp;lt;Alert&amp;gt;&lt;br/&gt;# doEvaluate(context) : List&amp;lt;Alert&amp;gt;&lt;br/&gt;+ BudgetThresholdRule : evaluate()&lt;br/&gt;+ LargeTransactionRule : &amp;gt; $150&lt;br/&gt;+ AboveAverageRule : &amp;gt; 2.0x baseline" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#D35400;fontColor=#ffffff;strokeColor=#D35400;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="1100" y="300" width="280" height="210" as="geometry"/>
        </mxCell>

        <!-- SavingsAdvisor -->
        <mxCell id="adv" value="&lt;b&gt;SavingsAdvisor (AI Decision Support)&lt;/b&gt;&lt;hr/&gt;+ List&amp;lt;SavingsSuggestionRule&amp;gt; rules&lt;hr/&gt;+ addRule(rule) : void&lt;br/&gt;+ generateSuggestions(ctx, curr) : List&amp;lt;Rec&amp;gt;&lt;br/&gt;+ GoalContributionRule : (target-saved)/months" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#16A085;fontColor=#ffffff;strokeColor=#16A085;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="1100" y="580" width="280" height="150" as="geometry"/>
        </mxCell>

        <!-- FinancialGoal -->
        <mxCell id="gol" value="&lt;b&gt;FinancialGoal&lt;/b&gt;&lt;hr/&gt;+ String id&lt;br/&gt;+ String name&lt;br/&gt;+ BigDecimal targetAmount&lt;br/&gt;+ BigDecimal savedAmount&lt;br/&gt;+ YearMonth targetMonth&lt;hr/&gt;+ addSavings(amount) : void&lt;br/&gt;+ isCompleted() : boolean&lt;br/&gt;+ getRemainingAmount() : BigDecimal" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#8A43A8;fontColor=#ffffff;strokeColor=#8A43A8;rounded=0;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="740" y="580" width="260" height="170" as="geometry"/>
        </mxCell>

        <!-- Connectors -->
        <mxCell id="e1" value="evaluates" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#27AE60;strokeWidth=2;fontColor=#27AE60;fontStyle=1;" edge="1" parent="1" source="ana" target="ctx">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e2" value="applies rules" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D35400;strokeWidth=2;fontColor=#D35400;fontStyle=1;" edge="1" parent="1" source="ana" target="rul">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e3" value="queries" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2980B9;strokeWidth=2;fontColor=#2980B9;fontStyle=1;" edge="1" parent="1" source="ana" target="tx">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e4" value="triggers advice" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#16A085;strokeWidth=2;fontColor=#16A085;fontStyle=1;" edge="1" parent="1" source="ana" target="adv">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e5" value="links goals" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#16A085;strokeWidth=2;fontColor=#16A085;fontStyle=1;" edge="1" parent="1" source="adv" target="gol">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e6" value="classified by" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#16A085;strokeWidth=2;fontColor=#16A085;fontStyle=1;" edge="1" parent="1" source="tx" target="cat">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e7" value="extends" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#8A43A8;strokeWidth=2;fontColor=#8A43A8;fontStyle=1;" edge="1" parent="1" source="chk" target="acc">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e8" value="extends" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#8A43A8;strokeWidth=2;fontColor=#8A43A8;fontStyle=1;" edge="1" parent="1" source="crd" target="acc">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e9" value="evaluates" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2980B9;strokeWidth=2;fontColor=#2980B9;fontStyle=1;" edge="1" parent="1" source="bds" target="bdg">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(output_drawio, "w", encoding="utf-8") as f:
        f.write(drawio_xml)
    print(f"Generated Native Draw.io XML: {output_drawio}")

if __name__ == '__main__':
    base_dir = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\documentation"
    png_out = os.path.join(base_dir, "BudgetWise_UML_Exact_Style.png")
    svg_out = os.path.join(base_dir, "BudgetWise_UML_Exact_Style.svg")
    drawio_out = os.path.join(base_dir, "BudgetWise_UML_Diagram.drawio")
    draw_exact_style_diagram(png_out, svg_out, drawio_out)
