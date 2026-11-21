import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_uml_diagram(output_png, output_pdf):
    fig, ax = plt.subplots(figsize=(19, 13), dpi=200)
    ax.set_xlim(0, 190)
    ax.set_ylim(0, 130)
    ax.axis('off')

    # Color Palette
    BG_COLOR = "#F8FAFC"
    PKG_BORDER = "#94A3B8"
    C_NAVY = "#1E3A8A"
    C_BLUE = "#2563EB"
    C_TEAL = "#0D9488"
    C_EMERALD = "#047857"
    C_SLATE = "#475569"
    C_WHITE = "#FFFFFF"
    C_TEXT = "#0F172A"

    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # 1. Main Title Banner
    title_box = patches.FancyBboxPatch((4, 120), 182, 8, boxstyle="round,pad=0.5",
                                       fc=C_NAVY, ec=C_NAVY, lw=1.5)
    ax.add_patch(title_box)
    ax.text(7, 124.5, "BudgetWise — UML Class Diagram: Financial Entities & Analysis Components",
            fontsize=15, fontweight='bold', color=C_WHITE, va='center')
    ax.text(7, 121.5, "UVT OOP 2026 | Explicit OOP Concepts: Inheritance, Polymorphism, Interfaces, Composition & BigDecimal",
            fontsize=9.5, color="#93C5FD", va='center')

    # Helper function to draw UML class boxes
    def draw_class(x, y, w, h, title, stereo=None, fields=None, methods=None, header_color=C_NAVY):
        # Background box
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                                     fc=C_WHITE, ec=header_color, lw=1.2, zorder=2)
        ax.add_patch(box)
        # Header banner
        header_h = 3.2 if not stereo else 4.2
        header_patch = patches.Rectangle((x, y + h - header_h), w, header_h,
                                         fc=header_color, ec="none", zorder=3)
        ax.add_patch(header_patch)
        
        # Header text
        if stereo:
            ax.text(x + w/2, y + h - 1.4, f"<<{stereo}>>", fontsize=7.5,
                    color="#E2E8F0", style='italic', ha='center', va='center', zorder=4)
            ax.text(x + w/2, y + h - 3.0, title, fontsize=9.5,
                    color=C_WHITE, fontweight='bold', ha='center', va='center', zorder=4)
        else:
            ax.text(x + w/2, y + h - 1.6, title, fontsize=9.5,
                    color=C_WHITE, fontweight='bold', ha='center', va='center', zorder=4)

        # Content positions
        cur_y = y + h - header_h - 1.2
        if fields:
            for f in fields:
                ax.text(x + 1.2, cur_y, f, fontsize=7.2, color=C_TEXT, fontfamily='monospace', va='top', zorder=4)
                cur_y -= 1.6
            cur_y -= 0.5
            ax.plot([x, x + w], [cur_y, cur_y], color="#CBD5E1", lw=0.8, zorder=4)
            cur_y -= 1.0

        if methods:
            for m in methods:
                weight = 'bold' if '{abstract}' in m else 'normal'
                ax.text(x + 1.2, cur_y, m, fontsize=7.2, color=C_TEXT, fontfamily='monospace',
                        fontweight=weight, va='top', zorder=4)
                cur_y -= 1.6

    # =========================================================================
    # LEFT PACKAGE: com.budgetwise.model (Financial Entities)
    # =========================================================================
    pkg_left = patches.FancyBboxPatch((4, 6), 90, 111, boxstyle="round,pad=0.8",
                                     fc="#F1F5F9", ec=PKG_BORDER, lw=1.2, ls="--", zorder=1)
    ax.add_patch(pkg_left)
    ax.text(7, 114.5, "• PACKAGE: com.budgetwise.model (Financial Entities & Domain Hierarchy)",
            fontsize=10.5, fontweight='bold', color=C_NAVY)

    # 1. Account (Abstract)
    draw_class(6, 88, 41, 23, "Account", stereo="abstract",
               fields=["- id: String", "- name: String", "- openingBalance: BigDecimal"],
               methods=["# Account(id, name, openingBal)",
                        "+ {abstract} canWithdraw(amt, bal): boolean",
                        "+ {abstract} calculateAvailableFunds(bal): BD",
                        "+ getOpeningBalance(): BigDecimal"],
               header_color=C_NAVY)

    # 2. CheckingAccount
    draw_class(6, 68, 41, 14, "CheckingAccount",
               fields=["/* strict zero-overdraft balance floor */"],
               methods=["+ canWithdraw(amt, bal): boolean",
                        "+ calculateAvailableFunds(bal): BD"],
               header_color=C_BLUE)

    # 3. CreditAccount
    draw_class(6, 48, 41, 16, "CreditAccount",
               fields=["- creditLimit: BigDecimal"],
               methods=["+ canWithdraw(amt, bal): boolean",
                        "+ calculateAvailableFunds(bal): BD",
                        "+ getCreditLimit(): BigDecimal"],
               header_color=C_BLUE)

    # Account Generalization Arrows
    ax.annotate("", xy=(26, 88), xytext=(26, 82),
                arrowprops=dict(facecolor='white', edgecolor=C_NAVY, arrowstyle="-|>", lw=1.5), zorder=5)
    ax.plot([26, 26], [68, 82], color=C_NAVY, lw=1.5, zorder=5)
    
    ax.annotate("", xy=(36, 88), xytext=(36, 66),
                arrowprops=dict(facecolor='white', edgecolor=C_NAVY, arrowstyle="-|>", lw=1.5), zorder=5)
    ax.plot([36, 36], [64, 66], color=C_NAVY, lw=1.5, zorder=5)

    # 4. Category
    draw_class(51, 93, 40, 18, "Category",
               fields=["+ {static} UNCATEGORIZED: Category",
                       "- id: String, name: String", "- isCustom: boolean"],
               methods=["+ getId(): String, getName(): String",
                        "+ isCustom(): boolean",
                        "+ equals(o), hashCode()"],
               header_color=C_TEAL)

    # 5. Transaction
    draw_class(51, 62, 40, 27, "Transaction", stereo="immutable record",
               fields=["- id: String, accountId: String",
                       "- date: LocalDate, description: String",
                       "- amount: BigDecimal (scale 2)",
                       "- type: TransactionType",
                       "- category: Category"],
               methods=["+ getSignedAmount(): BigDecimal",
                        "+ getAmount(): BigDecimal",
                        "+ getType(): TransactionType",
                        "+ getCategory(): Category"],
               header_color=C_NAVY)

    # Association Transaction -> Category
    ax.annotate("", xy=(71, 93), xytext=(71, 89),
                arrowprops=dict(edgecolor=C_SLATE, arrowstyle="->", lw=1.2, ls="--"), zorder=5)
    ax.text(73, 90.5, "classified by", fontsize=7.5, color=C_SLATE)

    # 6. Budget
    draw_class(6, 24, 41, 20, "Budget", stereo="immutable",
               fields=["- category: Category",
                       "- month: YearMonth",
                       "- limit: BigDecimal (scale 2)"],
               methods=["+ getCategory(): Category",
                        "+ getMonth(): YearMonth",
                        "+ getLimit(): BigDecimal",
                        "+ equals(o), hashCode()"],
               header_color=C_NAVY)

    # 7. BudgetStatus
    draw_class(51, 35, 40, 23, "BudgetStatus", stereo="record",
               fields=["+ budget: Budget",
                       "+ spent, remaining: BigDecimal",
                       "+ utilizationPercentage: BigDecimal",
                       "+ state: BudgetState"],
               methods=["+ {static} compute(b, spent, pol): Status",
                        "  /* exact cross-multiplication: */",
                        "  /* spent*100 vs limit*threshold */"],
               header_color=C_TEAL)

    # BudgetStatus -> Budget
    ax.annotate("", xy=(47, 34), xytext=(51, 46),
                arrowprops=dict(edgecolor=C_SLATE, arrowstyle="->", lw=1.2, ls="--"), zorder=5)

    # 8. FinancialGoal
    draw_class(6, 8, 41, 14, "FinancialGoal",
               fields=["- targetAmount, savedAmount: BD", "- targetMonth: YearMonth"],
               methods=["+ addSavings(amt: BD): void",
                        "+ isCompleted(), isOverdue(curr)"],
               header_color=C_NAVY)

    # BudgetState & AlertSeverity Enums
    draw_class(51, 10, 19, 21, "BudgetState", stereo="enum",
               fields=["NORMAL (<80%)", "WARNING (80-100%)", "LIMIT_REACHED (100%)", "EXCEEDED (>100%)"],
               header_color=C_SLATE)

    draw_class(72, 10, 19, 21, "AlertSeverity", stereo="enum",
               fields=["INFO", "WARNING", "CRITICAL"],
               header_color=C_SLATE)

    # =========================================================================
    # RIGHT PACKAGE: com.budgetwise.{strategy, rule, service} (Analysis Components)
    # =========================================================================
    pkg_right = patches.FancyBboxPatch((96, 6), 90, 111, boxstyle="round,pad=0.8",
                                      fc="#F8FAFC", ec=C_TEAL, lw=1.2, ls="--", zorder=1)
    ax.add_patch(pkg_right)
    ax.text(99, 114.5, "• PACKAGES: strategy, rule, service (Intelligent Analysis & Decision Support)",
            fontsize=10.5, fontweight='bold', color=C_TEAL)

    # 9. SpendingAnalysisStrategy
    draw_class(98, 93, 40, 17, "SpendingAnalysisStrategy", stereo="interface",
               methods=["+ {abstract} analyze(month, txs): Summary",
                        "+ {abstract} getStrategyName(): String"],
               header_color=C_TEAL)

    # Implementations
    draw_class(98, 77, 19, 11, "MonthlyTotalStrategy",
               methods=["+ analyze(...) [1-month]"],
               header_color=C_EMERALD)
    draw_class(119, 77, 19, 11, "RollingAvgStrategy",
               methods=["+ analyze(...) [3-mo base]"],
               header_color=C_EMERALD)

    # Realization lines for Strategy
    ax.annotate("", xy=(108, 93), xytext=(108, 88),
                arrowprops=dict(facecolor='white', edgecolor=C_TEAL, arrowstyle="-|>", lw=1.2, ls="--"), zorder=5)
    ax.annotate("", xy=(128, 93), xytext=(128, 88),
                arrowprops=dict(facecolor='white', edgecolor=C_TEAL, arrowstyle="-|>", lw=1.2, ls="--"), zorder=5)

    # 10. SpendingAnalyzer
    draw_class(144, 93, 40, 18, "SpendingAnalyzer",
               fields=["- strategy: SpendingAnalysisStrategy",
                       "- rules: List<SpendingRule>"],
               methods=["+ addRule(rule: SpendingRule): void",
                        "+ setStrategy(s: AnalysisStrategy): void",
                        "+ analyzeMonth(m, statuses): List<Alert>"],
               header_color=C_NAVY)

    # Analyzer uses Strategy
    ax.annotate("", xy=(138, 101), xytext=(144, 101),
                arrowprops=dict(edgecolor=C_SLATE, arrowstyle="->", lw=1.2, ls="--"), zorder=5)

    # 11. SpendingRule (Interface)
    draw_class(144, 69, 40, 16, "SpendingRule", stereo="interface",
               methods=["+ {abstract} name(): String",
                        "+ {abstract} evaluate(ctx): List<Alert>",
                        "+ {abstract} isEnabled(), setEnabled(b)"],
               header_color=C_TEAL)

    # Analyzer *-- SpendingRule (Composition)
    ax.plot([164, 164], [93, 85], color=C_NAVY, lw=1.5, zorder=5)
    comp_diamond = patches.Polygon([[164, 93], [162.8, 91.5], [164, 90], [165.2, 91.5]],
                                   fc=C_NAVY, ec=C_NAVY, zorder=6)
    ax.add_patch(comp_diamond)

    # AbstractSpendingRule (Template Method)
    draw_class(144, 45, 40, 19, "AbstractSpendingRule", stereo="abstract template",
               fields=["- name: String", "- enabled: boolean"],
               methods=["+ evaluate(ctx): List<Alert> /* checks enabled */",
                        "# {abstract} doEvaluate(ctx): List<Alert>"],
               header_color=C_NAVY)

    # Realization line AbstractSpendingRule ..|> SpendingRule
    ax.annotate("", xy=(164, 69), xytext=(164, 64),
                arrowprops=dict(facecolor='white', edgecolor=C_TEAL, arrowstyle="-|>", lw=1.2, ls="--"), zorder=5)

    # Concrete Rules
    draw_class(98, 30, 27, 10, "BudgetThresholdRule",
               methods=["# doEvaluate() [WARN/EXC]"],
               header_color=C_BLUE)
    draw_class(127, 30, 27, 10, "LargeTransactionRule",
               methods=["# doEvaluate() [> $150]"],
               header_color=C_BLUE)
    draw_class(156, 30, 27, 10, "AboveAverageRule",
               methods=["# doEvaluate() [> 2.0x base]"],
               header_color=C_BLUE)

    # Rule Generalization lines
    ax.annotate("", xy=(164, 45), xytext=(164, 42),
                arrowprops=dict(facecolor='white', edgecolor=C_NAVY, arrowstyle="-|>", lw=1.5), zorder=5)
    ax.plot([111, 170], [42, 42], color=C_NAVY, lw=1.5, zorder=5)
    ax.plot([111, 111], [40, 42], color=C_NAVY, lw=1.5, zorder=5)
    ax.plot([140, 140], [40, 42], color=C_NAVY, lw=1.5, zorder=5)
    ax.plot([170, 170], [40, 42], color=C_NAVY, lw=1.5, zorder=5)

    # 12. SavingsAdvisor & GoalContributionRule
    draw_class(98, 10, 40, 16, "SavingsAdvisor",
               fields=["- rules: List<SavingsSuggestionRule>"],
               methods=["+ addRule(r: SavingsSuggestionRule): void",
                        "+ generateSuggestions(ctx, curr): List<Rec>",
                        "  /* multi-factor velocity & goal impact */"],
               header_color=C_NAVY)

    draw_class(144, 18, 40, 10, "SavingsSuggestionRule", stereo="interface",
               methods=["+ {abstract} suggest(ctx, goals, curr): List<Rec>"],
               header_color=C_TEAL)

    # SavingsAdvisor *-- SavingsSuggestionRule
    ax.plot([138, 144], [23, 23], color=C_NAVY, lw=1.5, zorder=5)
    comp_diamond2 = patches.Polygon([[138, 23], [139.5, 24.2], [141, 23], [139.5, 21.8]],
                                    fc=C_NAVY, ec=C_NAVY, zorder=6)
    ax.add_patch(comp_diamond2)

    draw_class(144, 8, 40, 8, "GoalContributionRule",
               methods=["+ suggest() [(target-saved)/months with CEILING]"],
               header_color=C_BLUE)
    ax.annotate("", xy=(164, 18), xytext=(164, 16),
                arrowprops=dict(facecolor='white', edgecolor=C_TEAL, arrowstyle="-|>", lw=1.2, ls="--"), zorder=5)

    # Cross-border collaboration arrows
    ax.annotate("", xy=(98, 50), xytext=(91, 50),
                arrowprops=dict(edgecolor=C_SLATE, arrowstyle="->", lw=1.5, ls="--"), zorder=5)
    ax.text(92, 51.5, "evaluates", fontsize=8, color=C_SLATE)

    # Legend at the bottom
    ax.plot([4, 186], [3.5, 3.5], color="#CBD5E1", lw=1)
    ax.text(6, 1.8, "UML Legend:", fontsize=9, fontweight='bold', color=C_NAVY)
    
    # Generalization
    ax.annotate("", xy=(30, 2), xytext=(22, 2),
                arrowprops=dict(facecolor='white', edgecolor=C_NAVY, arrowstyle="-|>", lw=1.5))
    ax.text(32, 1.8, "Generalization (Inheritance)", fontsize=8, color=C_TEXT)

    # Realization
    ax.annotate("", xy=(72, 2), xytext=(64, 2),
                arrowprops=dict(facecolor='white', edgecolor=C_TEAL, arrowstyle="-|>", lw=1.2, ls="--"))
    ax.text(74, 1.8, "Realization (Interface)", fontsize=8, color=C_TEXT)

    # Composition
    comp_leg = patches.Polygon([[114, 2], [115.5, 2.8], [117, 2], [115.5, 1.2]],
                               fc=C_NAVY, ec=C_NAVY, zorder=6)
    ax.add_patch(comp_leg)
    ax.plot([117, 122], [2, 2], color=C_NAVY, lw=1.5)
    ax.text(124, 1.8, "Composition (Owns Lifecycle)", fontsize=8, color=C_TEXT)

    # Dependency
    ax.annotate("", xy=(162, 2), xytext=(154, 2),
                arrowprops=dict(edgecolor=C_SLATE, arrowstyle="->", lw=1.2, ls="--"))
    ax.text(164, 1.8, "Association / Dependency", fontsize=8, color=C_TEXT)

    plt.tight_layout()
    plt.savefig(output_png, format='png', dpi=250, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.savefig(output_pdf, format='pdf', facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Generated High-Res PNG: {output_png}")
    print(f"Generated Vector PDF: {output_pdf}")

if __name__ == '__main__':
    base = r"C:\Users\dhaou\OneDrive\Desktop\OOP project\documentation"
    png_path = os.path.join(base, "BudgetWise_Financial_Entities_and_Analysis_UML.png")
    pdf_path = os.path.join(base, "BudgetWise_Financial_Entities_and_Analysis_UML.pdf")
    draw_uml_diagram(png_path, pdf_path)
