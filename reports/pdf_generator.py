import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from workflows.state import FinanceState
from reports.charts import (
    generate_category_pie_chart,
    generate_monthly_trend_chart,
    generate_budget_variance_chart,
    generate_portfolio_allocation_chart,
)
from reports.insights import (
    build_executive_summary,
    build_recommendation_summary,
    build_investment_insight,
)
from config.settings import settings


def _build_variance_table(variance: dict) -> Table:
    data = [["Category", "Planned", "Actual", "Variance %", "Status"]]
    for category, v in variance.items():
        status = "Overspent" if v["overspent"] else "On Track"
        data.append([
            category, f"₹{v['planned']:.2f}", f"₹{v['actual']:.2f}",
            f"{v['variance_percent']}%", status
        ])

    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]))
    return table


def generate_pdf_report(state: FinanceState, user_id: int) -> str:
    """
    Assembles all agent outputs into a single, professional PDF report:
    summary, charts, tables, and recommendations.
    """
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    chart_dir = os.path.join(settings.OUTPUT_DIR, f"charts_{user_id}")
    os.makedirs(chart_dir, exist_ok=True)

    file_name = f"financial_report_{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(settings.OUTPUT_DIR, file_name)

    doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=20)
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    elements = []

    # --- Title ---
    elements.append(Paragraph("Personal Financial Report", title_style))
    elements.append(Paragraph(f"Generated on {datetime.utcnow().strftime('%d %b %Y')}", body_style))
    elements.append(Spacer(1, 0.5 * cm))

    # --- Executive Summary ---
    elements.append(Paragraph("Executive Summary", heading_style))
    elements.append(Paragraph(build_executive_summary(state), body_style))
    elements.append(Spacer(1, 0.5 * cm))

    # --- Expense Breakdown ---
    expense_analysis = state.get("expense_analysis", {})
    if expense_analysis:
        elements.append(Paragraph("Expense Breakdown", heading_style))
        pie_path = generate_category_pie_chart(expense_analysis.get("category_distribution", {}), chart_dir)
        if pie_path:
            elements.append(Image(pie_path, width=10 * cm, height=10 * cm))

        trend_path = generate_monthly_trend_chart(expense_analysis.get("monthly_trend", {}), chart_dir)
        if trend_path:
            elements.append(Image(trend_path, width=14 * cm, height=7 * cm))
        elements.append(Spacer(1, 0.5 * cm))

    # --- Budget Performance ---
    budget_analysis = state.get("budget_analysis", {})
    if budget_analysis:
        elements.append(Paragraph("Budget Performance", heading_style))
        elements.append(_build_variance_table(budget_analysis.get("variance", {})))
        elements.append(Spacer(1, 0.3 * cm))

        variance_chart = generate_budget_variance_chart(budget_analysis.get("variance", {}), chart_dir)
        if variance_chart:
            elements.append(Image(variance_chart, width=14 * cm, height=7 * cm))
        elements.append(Spacer(1, 0.5 * cm))

    # --- Investment Analysis ---
    investment_analysis = state.get("investment_analysis") or {}
    if investment_analysis:
        elements.append(Paragraph("Investment Analysis", heading_style))
        elements.append(Paragraph(build_investment_insight(investment_analysis), body_style))

        portfolio_chart = generate_portfolio_allocation_chart(
            investment_analysis.get("sector_allocation", {}), chart_dir
        )
        if portfolio_chart:
            elements.append(Image(portfolio_chart, width=10 * cm, height=10 * cm))
        elements.append(Spacer(1, 0.5 * cm))

    # --- Subscription Review ---
    subscription_analysis = state.get("subscription_analysis") or {}
    if subscription_analysis:
        elements.append(Paragraph("Subscription Review", heading_style))
        elements.append(Paragraph(
            f"Active subscriptions: {subscription_analysis.get('active_count', 0)}. "
            f"Estimated annual cost: ₹{subscription_analysis.get('total_estimated_annual_cost', 0):,.2f}.",
            body_style
        ))
        elements.append(Spacer(1, 0.5 * cm))

    # --- Recommendations ---
    recommendations = state.get("recommendations", [])
    elements.append(Paragraph("Recommendations", heading_style))
    elements.append(Paragraph(build_recommendation_summary(recommendations).replace("\n", "<br/>"), body_style))
    elements.append(Spacer(1, 0.5 * cm))

    # --- Financial Health Score ---
    health_score = budget_analysis.get("financial_health_score", "N/A")
    elements.append(Paragraph("Financial Health Score", heading_style))
    elements.append(Paragraph(f"<b>{health_score} / 100</b>", body_style))

    doc.build(elements)
    return file_path


def generate_report_node(state: FinanceState) -> FinanceState:
    """
    LangGraph node wrapper — generates the final PDF report and
    stores its path in shared state.
    """
    user_id = state.get("user_id", 0)
    report_path = generate_pdf_report(state, user_id)
    state["report_path"] = report_path
    return state