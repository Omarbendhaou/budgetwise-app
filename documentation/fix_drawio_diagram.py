import os

def generate_perfect_drawio(output_path):
    # Colors:
    # Purple: #8A43A8
    # Blue:   #2980B9
    # Green:  #27AE60
    # Orange: #D35400
    # Teal:   #16A085

    classes = [
        {
            "id": "acc",
            "title": "Account (Abstract)",
            "x": 60, "y": 80, "w": 300, "h": 200,
            "color": "#8A43A8",
            "fields": "+ String id&#xa;+ String name&#xa;+ BigDecimal openingBalance",
            "f_h": 60,
            "methods": "+ canWithdraw(amount, bal) : boolean&#xa;+ calculateAvailableFunds(bal) : BigDecimal&#xa;+ getOpeningBalance() : BigDecimal&#xa;+ getAccountType() : String",
            "m_h": 104
        },
        {
            "id": "chk",
            "title": "CheckingAccount",
            "x": 60, "y": 330, "w": 300, "h": 140,
            "color": "#8A43A8",
            "fields": "/* strict zero-overdraft balance floor */",
            "f_h": 34,
            "methods": "+ canWithdraw(amount, bal) : boolean&#xa;+ calculateAvailableFunds(bal) : BigDecimal&#xa;+ getAccountType() : String",
            "m_h": 70
        },
        {
            "id": "crd",
            "title": "CreditAccount",
            "x": 60, "y": 520, "w": 300, "h": 160,
            "color": "#8A43A8",
            "fields": "+ BigDecimal creditLimit",
            "f_h": 34,
            "methods": "+ canWithdraw(amount, bal) : boolean&#xa;+ calculateAvailableFunds(bal) : BigDecimal&#xa;+ getCreditLimit() : BigDecimal&#xa;+ getAccountType() : String",
            "m_h": 90
        },
        {
            "id": "cat",
            "title": "Category (Domain Entity)",
            "x": 420, "y": 80, "w": 280, "h": 170,
            "color": "#16A085",
            "fields": "+ String id&#xa;+ String name&#xa;+ boolean isCustom&#xa;+ Category UNCATEGORIZED",
            "f_h": 74,
            "methods": "+ getId() : String&#xa;+ getName() : String&#xa;+ isCustom() : boolean&#xa;+ equals(obj) : boolean",
            "m_h": 60
        },
        {
            "id": "tx",
            "title": "Transaction (Immutable)",
            "x": 420, "y": 290, "w": 280, "h": 250,
            "color": "#2980B9",
            "fields": "+ String id&#xa;+ String accountId&#xa;+ LocalDate date&#xa;+ String description&#xa;+ BigDecimal amount [scale 2]&#xa;+ TransactionType type&#xa;+ Category category",
            "f_h": 116,
            "methods": "+ getSignedAmount() : BigDecimal&#xa;+ getAmount() : BigDecimal&#xa;+ getType() : TransactionType&#xa;+ getCategory() : Category&#xa;+ equals(obj) : boolean",
            "m_h": 98
        },
        {
            "id": "bdg",
            "title": "Budget (Entity)",
            "x": 60, "y": 730, "w": 300, "h": 160,
            "color": "#2980B9",
            "fields": "+ Category category&#xa;+ YearMonth month&#xa;+ BigDecimal limit [scale 2]",
            "f_h": 56,
            "methods": "+ getCategory() : Category&#xa;+ getMonth() : YearMonth&#xa;+ getLimit() : BigDecimal&#xa;+ equals(obj) : boolean",
            "m_h": 68
        },
        {
            "id": "bds",
            "title": "BudgetStatus (Record)",
            "x": 420, "y": 590, "w": 280, "h": 220,
            "color": "#2980B9",
            "fields": "+ Budget budget&#xa;+ BigDecimal spent&#xa;+ BigDecimal remaining&#xa;+ BigDecimal utilizationPercentage&#xa;+ BudgetState state",
            "f_h": 86,
            "methods": "+ compute(b, spent, policy) : BudgetStatus&#xa;  /* exact cross-multiplication: */&#xa;  /* spent*100 vs limit*threshold */&#xa;+ getUtilizationPercentage() : BigDecimal&#xa;+ getState() : BudgetState",
            "m_h": 98
        },
        {
            "id": "ana",
            "title": "SpendingAnalyzer (Controller)",
            "x": 760, "y": 180, "w": 320, "h": 190,
            "color": "#2980B9",
            "fields": "+ SpendingAnalysisStrategy strategy&#xa;+ List&lt;SpendingRule&gt; rules",
            "f_h": 46,
            "methods": "+ addRule(rule : SpendingRule) : void&#xa;+ setStrategy(s : AnalysisStrategy) : void&#xa;+ analyzeMonth(month, statuses) : List&lt;Alert&gt;&#xa;+ getRules() : List&lt;SpendingRule&gt;&#xa;+ getStrategy() : SpendingAnalysisStrategy",
            "m_h": 108
        },
        {
            "id": "ctx",
            "title": "Context Engine (Strategy)",
            "x": 1140, "y": 80, "w": 300, "h": 160,
            "color": "#27AE60",
            "fields": "+ SpendingAnalysisStrategy (Interface)",
            "f_h": 34,
            "methods": "+ analyze(month, txList) : SpendingSummary&#xa;+ MonthlyTotalStrategy : analyze()&#xa;+ RollingAverageStrategy : 3-mo baseline&#xa;+ getStrategyName() : String",
            "m_h": 90
        },
        {
            "id": "rul",
            "title": "Rule Engine (SpendingRules)",
            "x": 1140, "y": 280, "w": 300, "h": 230,
            "color": "#D35400",
            "fields": "+ AbstractSpendingRule (Template Method)&#xa;+ String name&#xa;+ boolean enabled",
            "f_h": 56,
            "methods": "+ evaluate(context) : List&lt;Alert&gt;&#xa;# doEvaluate(context) : List&lt;Alert&gt;&#xa;+ BudgetThresholdRule : evaluate()&#xa;+ LargeTransactionRule : &gt; $150&#xa;+ AboveAverageRule : &gt; 2.0x base",
            "m_h": 138
        },
        {
            "id": "adv",
            "title": "SavingsAdvisor (AI Decision Support)",
            "x": 1140, "y": 560, "w": 300, "h": 170,
            "color": "#16A085",
            "fields": "+ List&lt;SavingsSuggestionRule&gt; rules",
            "f_h": 34,
            "methods": "+ addRule(rule) : void&#xa;+ generateSuggestions(ctx, curr) : List&lt;Rec&gt;&#xa;+ GoalContributionRule : (target-saved)/months&#xa;+ computeConcentrationRatio() : BigDecimal",
            "m_h": 100
        },
        {
            "id": "gol",
            "title": "FinancialGoal",
            "x": 760, "y": 590, "w": 300, "h": 180,
            "color": "#8A43A8",
            "fields": "+ String id&#xa;+ String name&#xa;+ BigDecimal targetAmount&#xa;+ BigDecimal savedAmount&#xa;+ YearMonth targetMonth",
            "f_h": 86,
            "methods": "+ addSavings(amount) : void&#xa;+ isCompleted() : boolean&#xa;+ isOverdue(currentMonth) : boolean&#xa;+ getRemainingAmount() : BigDecimal",
            "m_h": 58
        }
    ]

    edges = [
        {"id": "e_chk_acc", "val": "extends", "src": "chk", "tgt": "acc", "color": "#8A43A8"},
        {"id": "e_crd_acc", "val": "extends", "src": "crd", "tgt": "acc", "color": "#8A43A8"},
        {"id": "e_tx_cat", "val": "classified by", "src": "tx", "tgt": "cat", "color": "#16A085"},
        {"id": "e_ana_ctx", "val": "evaluates", "src": "ana", "tgt": "ctx", "color": "#27AE60"},
        {"id": "e_ana_rul", "val": "applies rules", "src": "ana", "tgt": "rul", "color": "#D35400"},
        {"id": "e_ana_tx", "val": "queries", "src": "ana", "tgt": "tx", "color": "#2980B9"},
        {"id": "e_ana_adv", "val": "triggers advice", "src": "ana", "tgt": "adv", "color": "#16A085"},
        {"id": "e_adv_gol", "val": "links goals", "src": "adv", "tgt": "gol", "color": "#16A085"},
        {"id": "e_bds_bdg", "val": "evaluates", "src": "bds", "tgt": "bdg", "color": "#2980B9"}
    ]

    xml = ['<mxfile host="app.diagrams.net" modified="2026-11-16T16:25:00.000Z" agent="BudgetWise" version="24.0.0" type="device">',
           '  <diagram id="budgetwise-diagram" name="BudgetWise UML Class Diagram">',
           '    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" background="#FFFFFF">',
           '      <root>',
           '        <mxCell id="0"/>',
           '        <mxCell id="1" parent="0"/>']

    for c in classes:
        cid = c["id"]
        title = c["title"]
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        col = c["color"]
        fields = c["fields"]
        methods = c["methods"]
        fh = c["f_h"]
        mh = c["m_h"]

        # Container swimlane (Header only!)
        xml.append(f'        <mxCell id="{cid}" value="{title}" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor={col};fontColor=#ffffff;strokeColor={col};rounded=0;fontSize=12;shadow=1;" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>')
        xml.append('        </mxCell>')

        # Attributes child cell
        xml.append(f'        <mxCell id="{cid}_fields" value="{fields}" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;fontColor=#2C3E50;fontFamily=monospace;" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="28" width="{w}" height="{fh}" as="geometry"/>')
        xml.append('        </mxCell>')

        # Divider line
        xml.append(f'        <mxCell id="{cid}_line" value="" style="line;strokeWidth=1.2;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=0;spacingRight=0;rotatable=0;strokeColor={col};" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="{28+fh}" width="{w}" height="8" as="geometry"/>')
        xml.append('        </mxCell>')

        # Methods child cell
        xml.append(f'        <mxCell id="{cid}_methods" value="{methods}" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;fontColor=#2C3E50;fontFamily=monospace;" vertex="1" parent="{cid}">')
        xml.append(f'          <mxGeometry y="{28+fh+8}" width="{w}" height="{mh}" as="geometry"/>')
        xml.append('        </mxCell>')

    # Add edges
    for e in edges:
        eid = e["id"]
        val = e["val"]
        src = e["src"]
        tgt = e["tgt"]
        col = e["color"]
        xml.append(f'        <mxCell id="{eid}" value="{val}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={col};strokeWidth=2;fontColor={col};fontStyle=1;fontSize=11;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="{src}" target="{tgt}">')
        xml.append('          <mxGeometry relative="1" as="geometry"/>')
        xml.append('        </mxCell>')

    xml.append('      </root>')
    xml.append('    </mxGraphModel>')
    xml.append('  </diagram>')
    xml.append('</mxfile>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    print(f"Fixed Draw.io XML generated at: {output_path}")

if __name__ == '__main__':
    target = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\documentation\BudgetWise_UML_Diagram.drawio"
    generate_perfect_drawio(target)
