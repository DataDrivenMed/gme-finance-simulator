"""
GME Finance Scenario Simulator
A decision tool for modeling financial and operational impacts
of Graduate Medical Education trainee movements and affiliation scenarios.
Built by Per Ram Paragi | Director, Accreditation & Strategic Planning
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# CONFIG & THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GME Finance Scenario Simulator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#1B2A4A",
    "accent": "#2E86AB",
    "success": "#2D936C",
    "warning": "#D4A843",
    "danger": "#C44536",
    "light_bg": "#F8F9FA",
    "text": "#333333",
    "muted": "#8C8C8C",
    "card_border": "#E8ECF0",
    "scenario_a": "#2E86AB",
    "scenario_b": "#D4A843",
    "baseline": "#8C8C8C",
}

st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['light_bg']};
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }}
    
    /* Header */
    .dashboard-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #2A3F6B 100%);
        color: white;
        padding: 1.8rem 2.2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }}
    .dashboard-header h1 {{
        font-size: 1.6rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.02em;
    }}
    .dashboard-header p {{
        font-size: 0.85rem;
        color: rgba(255,255,255,0.7);
        margin: 0;
    }}
    
    /* KPI Cards */
    .kpi-card {{
        background: white;
        border: 1px solid {COLORS['card_border']};
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .kpi-label {{
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {COLORS['muted']};
        margin-bottom: 0.3rem;
    }}
    .kpi-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORS['primary']};
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }}
    .kpi-delta {{
        font-size: 0.78rem;
        font-weight: 500;
    }}
    .kpi-delta.positive {{ color: {COLORS['success']}; }}
    .kpi-delta.negative {{ color: {COLORS['danger']}; }}
    .kpi-delta.neutral {{ color: {COLORS['muted']}; }}
    
    /* Section */
    .section-header {{
        font-size: 1.05rem;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 1.2rem 0 0.3rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid {COLORS['accent']};
        display: inline-block;
    }}
    .section-caption {{
        font-size: 0.8rem;
        color: {COLORS['muted']};
        margin-bottom: 1rem;
        font-style: italic;
    }}
    
    /* Chart cards */
    .chart-card {{
        background: white;
        border: 1px solid {COLORS['card_border']};
        border-radius: 10px;
        padding: 1.4rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }}
    .chart-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {COLORS['primary']};
        margin-bottom: 0.2rem;
    }}
    .chart-insight {{
        font-size: 0.78rem;
        color: {COLORS['muted']};
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }}
    
    /* Narrative */
    .narrative-box {{
        background: white;
        border-left: 4px solid {COLORS['accent']};
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.4rem;
        margin: 0.8rem 0;
        font-size: 0.85rem;
        color: {COLORS['text']};
        line-height: 1.6;
    }}
    .narrative-box.warning {{
        border-left-color: {COLORS['danger']};
    }}
    .narrative-box.positive {{
        border-left-color: {COLORS['success']};
    }}
    
    /* Scenario comparison table */
    .scenario-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }}
    .scenario-table th {{
        background: {COLORS['primary']};
        color: white;
        padding: 0.6rem 1rem;
        text-align: left;
        font-weight: 500;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .scenario-table td {{
        padding: 0.5rem 1rem;
        border-bottom: 1px solid {COLORS['card_border']};
        color: {COLORS['text']};
    }}
    .scenario-table tr:nth-child(even) {{
        background: {COLORS['light_bg']};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: white;
        border-right: 1px solid {COLORS['card_border']};
    }}
    [data-testid="stSidebar"] .stMarkdown h3 {{
        font-size: 0.9rem;
        color: {COLORS['primary']};
        margin-top: 1rem;
    }}
    
    /* Footer */
    .dashboard-footer {{
        text-align: center;
        font-size: 0.72rem;
        color: {COLORS['muted']};
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid {COLORS['card_border']};
    }}
    
    /* Hide extras */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GME FINANCIAL MODEL
# ─────────────────────────────────────────────

# Baseline parameters (realistic academic medical center)
BASELINE = {
    "total_residents": 650,
    "total_fellows": 120,
    "medicare_ime_per_fte": 112_000,       # IME payment per FTE resident
    "medicare_dme_per_fte": 38_000,        # DME payment per FTE
    "medicaid_gme_per_fte": 22_000,        # State Medicaid GME support
    "resident_salary_avg": 68_500,         # Average PGY salary
    "fellow_salary_avg": 78_200,
    "benefits_rate": 0.28,                 # Benefits as % of salary
    "overhead_per_trainee": 18_500,        # Admin, space, malpractice
    "teaching_cost_per_trainee": 42_000,   # Faculty teaching time, supervision
    "affiliated_sites": 6,
    "pct_at_primary": 0.62,               # % trainees at primary site
    "annual_case_volume_per_resident": 385, # Case volume contribution
    "revenue_per_case": 2_850,             # Average revenue per case/encounter
}


def calculate_scenario(params):
    """Calculate full financial model from scenario parameters."""
    
    total_trainees = params["residents"] + params["fellows"]
    
    # REVENUE
    ime_revenue = params["residents"] * params["ime_per_fte"]
    dme_revenue = params["residents"] * params["dme_per_fte"]
    medicaid_revenue = total_trainees * params["medicaid_per_fte"]
    
    # Clinical revenue from trainee case volume
    cases = params["residents"] * params["case_volume_per_resident"]
    clinical_revenue = cases * params["revenue_per_case"]
    
    total_revenue = ime_revenue + dme_revenue + medicaid_revenue + clinical_revenue
    
    # COSTS
    salary_cost = (params["residents"] * params["resident_salary"] +
                   params["fellows"] * params["fellow_salary"])
    benefits_cost = salary_cost * params["benefits_rate"]
    overhead_cost = total_trainees * params["overhead_per_trainee"]
    teaching_cost = total_trainees * params["teaching_cost_per_trainee"]
    
    total_cost = salary_cost + benefits_cost + overhead_cost + teaching_cost
    
    # NET
    net_position = total_revenue - total_cost
    
    # Per-trainee metrics
    revenue_per_trainee = total_revenue / total_trainees if total_trainees > 0 else 0
    cost_per_trainee = total_cost / total_trainees if total_trainees > 0 else 0
    
    # Site distribution
    trainees_primary = int(total_trainees * params["pct_primary"])
    trainees_affiliated = total_trainees - trainees_primary
    
    return {
        "total_trainees": total_trainees,
        "residents": params["residents"],
        "fellows": params["fellows"],
        "ime_revenue": ime_revenue,
        "dme_revenue": dme_revenue,
        "medicaid_revenue": medicaid_revenue,
        "clinical_revenue": clinical_revenue,
        "total_revenue": total_revenue,
        "salary_cost": salary_cost,
        "benefits_cost": benefits_cost,
        "overhead_cost": overhead_cost,
        "teaching_cost": teaching_cost,
        "total_cost": total_cost,
        "net_position": net_position,
        "revenue_per_trainee": revenue_per_trainee,
        "cost_per_trainee": cost_per_trainee,
        "cases": cases,
        "trainees_primary": trainees_primary,
        "trainees_affiliated": trainees_affiliated,
        "pct_primary": params["pct_primary"],
        "sites": params["sites"],
    }


# ─────────────────────────────────────────────
# SIDEBAR — SCENARIO CONTROLS
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown(f"""
    <div style="padding: 0.8rem 0;">
        <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['primary']};">
            Scenario Controls
        </div>
        <div style="font-size: 0.78rem; color: {COLORS['muted']}; margin-top: 0.2rem;">
            Adjust parameters to model different GME configurations
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Trainee Count
    st.markdown(f"### 👥 Trainee Volume")
    residents = st.slider(
        "Residents",
        min_value=400, max_value=900, value=BASELINE["total_residents"],
        step=10, help="Total resident FTEs across all programs"
    )
    fellows = st.slider(
        "Fellows",
        min_value=50, max_value=250, value=BASELINE["total_fellows"],
        step=10, help="Total fellow FTEs across all programs"
    )
    
    st.markdown(f"### 🏥 Site Distribution")
    pct_primary = st.slider(
        "% at Primary Site",
        min_value=30, max_value=90, value=int(BASELINE["pct_at_primary"] * 100),
        step=5, help="Percentage of trainees at primary teaching hospital",
        format="%d%%"
    ) / 100
    
    num_sites = st.slider(
        "Affiliated Sites",
        min_value=2, max_value=12, value=BASELINE["affiliated_sites"],
        step=1, help="Number of affiliated training sites"
    )
    
    st.markdown(f"### 💵 Payment Rates")
    ime_adjustment = st.slider(
        "IME Rate Adjustment",
        min_value=-30, max_value=30, value=0,
        step=5, format="%+d%%",
        help="Percentage change to Medicare IME per-FTE rate"
    )
    
    dme_adjustment = st.slider(
        "DME Rate Adjustment",
        min_value=-30, max_value=30, value=0,
        step=5, format="%+d%%",
        help="Percentage change to Medicare DME per-FTE rate"
    )
    
    medicaid_adjustment = st.slider(
        "Medicaid GME Adjustment",
        min_value=-50, max_value=100, value=0,
        step=10, format="%+d%%",
        help="Percentage change to state Medicaid GME support"
    )
    
    st.markdown(f"### 📊 Operational Parameters")
    case_volume_adj = st.slider(
        "Case Volume per Resident",
        min_value=300, max_value=500, value=BASELINE["annual_case_volume_per_resident"],
        step=10, help="Annual cases/encounters per resident"
    )
    
    salary_increase = st.slider(
        "Salary Increase",
        min_value=0, max_value=15, value=0,
        step=1, format="+%d%%",
        help="Across-the-board salary adjustment"
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.72rem; color: {COLORS['muted']}; line-height: 1.5;">
        <strong>Note:</strong> All figures use synthetic baseline parameters 
        modeled on a mid-size academic medical center. Adjust sliders to 
        explore "what if" scenarios.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CALCULATE SCENARIOS
# ─────────────────────────────────────────────

# Baseline
baseline_params = {
    "residents": BASELINE["total_residents"],
    "fellows": BASELINE["total_fellows"],
    "ime_per_fte": BASELINE["medicare_ime_per_fte"],
    "dme_per_fte": BASELINE["medicare_dme_per_fte"],
    "medicaid_per_fte": BASELINE["medicaid_gme_per_fte"],
    "resident_salary": BASELINE["resident_salary_avg"],
    "fellow_salary": BASELINE["fellow_salary_avg"],
    "benefits_rate": BASELINE["benefits_rate"],
    "overhead_per_trainee": BASELINE["overhead_per_trainee"],
    "teaching_cost_per_trainee": BASELINE["teaching_cost_per_trainee"],
    "pct_primary": BASELINE["pct_at_primary"],
    "sites": BASELINE["affiliated_sites"],
    "case_volume_per_resident": BASELINE["annual_case_volume_per_resident"],
    "revenue_per_case": BASELINE["revenue_per_case"],
}

# Scenario (from sliders)
scenario_params = {
    "residents": residents,
    "fellows": fellows,
    "ime_per_fte": BASELINE["medicare_ime_per_fte"] * (1 + ime_adjustment / 100),
    "dme_per_fte": BASELINE["medicare_dme_per_fte"] * (1 + dme_adjustment / 100),
    "medicaid_per_fte": BASELINE["medicaid_gme_per_fte"] * (1 + medicaid_adjustment / 100),
    "resident_salary": BASELINE["resident_salary_avg"] * (1 + salary_increase / 100),
    "fellow_salary": BASELINE["fellow_salary_avg"] * (1 + salary_increase / 100),
    "benefits_rate": BASELINE["benefits_rate"],
    "overhead_per_trainee": BASELINE["overhead_per_trainee"],
    "teaching_cost_per_trainee": BASELINE["teaching_cost_per_trainee"],
    "pct_primary": pct_primary,
    "sites": num_sites,
    "case_volume_per_resident": case_volume_adj,
    "revenue_per_case": BASELINE["revenue_per_case"],
}

base = calculate_scenario(baseline_params)
scen = calculate_scenario(scenario_params)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def fmt_millions(val):
    return f"${val / 1_000_000:.1f}M"

def fmt_currency(val):
    return f"${val:,.0f}"

def delta_str(scenario_val, baseline_val, fmt="millions"):
    diff = scenario_val - baseline_val
    if fmt == "millions":
        return f"{'▲' if diff >= 0 else '▼'} {fmt_millions(abs(diff))} vs. baseline"
    elif fmt == "currency":
        return f"{'▲' if diff >= 0 else '▼'} {fmt_currency(abs(diff))} vs. baseline"
    else:
        return f"{'▲' if diff >= 0 else '▼'} {abs(diff):,.0f} vs. baseline"

def delta_direction(scenario_val, baseline_val, invert=False):
    diff = scenario_val - baseline_val
    if diff == 0:
        return "neutral"
    if invert:
        return "negative" if diff > 0 else "positive"
    return "positive" if diff > 0 else "negative"

def kpi_card(label, value, delta=None, delta_dir="positive"):
    delta_html = ""
    if delta:
        arrow = "▲" if delta_dir == "positive" else "▼" if delta_dir == "negative" else "●"
        delta_html = f'<div class="kpi-delta {delta_dir}">{arrow} {delta}</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────

# Header
st.markdown(f"""
<div class="dashboard-header">
    <h1>GME Finance Scenario Simulator</h1>
    <p>Model financial and operational impacts of trainee movements and affiliation changes  ·  Synthetic demonstration data</p>
</div>
""", unsafe_allow_html=True)

# ── TOP-LINE KPIs ──
c1, c2, c3, c4, c5 = st.columns(5)

net_diff = scen["net_position"] - base["net_position"]
net_dir = delta_direction(scen["net_position"], base["net_position"])

with c1:
    st.markdown(kpi_card(
        "Total Trainees", f'{scen["total_trainees"]:,}',
        f'{scen["total_trainees"] - base["total_trainees"]:+,} vs. baseline',
        delta_direction(scen["total_trainees"], base["total_trainees"])
    ), unsafe_allow_html=True)

with c2:
    st.markdown(kpi_card(
        "Total Revenue", fmt_millions(scen["total_revenue"]),
        delta_str(scen["total_revenue"], base["total_revenue"]),
        delta_direction(scen["total_revenue"], base["total_revenue"])
    ), unsafe_allow_html=True)

with c3:
    st.markdown(kpi_card(
        "Total Cost", fmt_millions(scen["total_cost"]),
        delta_str(scen["total_cost"], base["total_cost"]),
        delta_direction(scen["total_cost"], base["total_cost"], invert=True)
    ), unsafe_allow_html=True)

with c4:
    net_color = "positive" if scen["net_position"] >= 0 else "negative"
    st.markdown(kpi_card(
        "Net Position", fmt_millions(scen["net_position"]),
        delta_str(scen["net_position"], base["net_position"]),
        net_dir
    ), unsafe_allow_html=True)

with c5:
    st.markdown(kpi_card(
        "Annual Cases", f'{scen["cases"]:,.0f}',
        f'{scen["cases"] - base["cases"]:+,.0f} vs. baseline',
        delta_direction(scen["cases"], base["cases"])
    ), unsafe_allow_html=True)

st.markdown("<div style='height: 0.8rem'></div>", unsafe_allow_html=True)

# ── REVENUE vs COST WATERFALL ──
st.markdown('<div class="section-header">Revenue & Cost Breakdown</div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">Decision focus: Where is the money coming from, and where is it going?</div>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Revenue Sources — Baseline vs. Scenario</div>', unsafe_allow_html=True)
    
    revenue_categories = ["Medicare IME", "Medicare DME", "Medicaid GME", "Clinical Revenue"]
    base_revenues = [base["ime_revenue"], base["dme_revenue"], base["medicaid_revenue"], base["clinical_revenue"]]
    scen_revenues = [scen["ime_revenue"], scen["dme_revenue"], scen["medicaid_revenue"], scen["clinical_revenue"]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Baseline", x=revenue_categories, y=[v/1e6 for v in base_revenues],
        marker_color=COLORS["baseline"],
        text=[f"${v/1e6:.1f}M" for v in base_revenues],
        textposition="outside", textfont=dict(size=9),
    ))
    fig.add_trace(go.Bar(
        name="Scenario", x=revenue_categories, y=[v/1e6 for v in scen_revenues],
        marker_color=COLORS["scenario_a"],
        text=[f"${v/1e6:.1f}M" for v in scen_revenues],
        textposition="outside", textfont=dict(size=9),
    ))
    fig.update_layout(
        barmode="group", height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10)),
        xaxis=dict(showgrid=False, showline=True, linecolor=COLORS["card_border"],
                   tickfont=dict(size=9, color=COLORS["muted"])),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
                   tickfont=dict(size=9, color=COLORS["muted"]),
                   tickprefix="$", ticksuffix="M"),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Cost Components — Baseline vs. Scenario</div>', unsafe_allow_html=True)
    
    cost_categories = ["Salaries", "Benefits", "Overhead", "Teaching"]
    base_costs = [base["salary_cost"], base["benefits_cost"], base["overhead_cost"], base["teaching_cost"]]
    scen_costs = [scen["salary_cost"], scen["benefits_cost"], scen["overhead_cost"], scen["teaching_cost"]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Baseline", x=cost_categories, y=[v/1e6 for v in base_costs],
        marker_color=COLORS["baseline"],
        text=[f"${v/1e6:.1f}M" for v in base_costs],
        textposition="outside", textfont=dict(size=9),
    ))
    fig.add_trace(go.Bar(
        name="Scenario", x=cost_categories, y=[v/1e6 for v in scen_costs],
        marker_color=COLORS["scenario_b"],
        text=[f"${v/1e6:.1f}M" for v in scen_costs],
        textposition="outside", textfont=dict(size=9),
    ))
    fig.update_layout(
        barmode="group", height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10)),
        xaxis=dict(showgrid=False, showline=True, linecolor=COLORS["card_border"],
                   tickfont=dict(size=9, color=COLORS["muted"])),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
                   tickfont=dict(size=9, color=COLORS["muted"]),
                   tickprefix="$", ticksuffix="M"),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── NET POSITION WATERFALL ──
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Net Financial Impact — What Changed</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-insight">Waterfall showing how each factor contributes to the shift from baseline to scenario net position.</div>', unsafe_allow_html=True)

waterfall_labels = [
    "Baseline Net",
    "IME Change", "DME Change", "Medicaid Change", "Clinical Rev Change",
    "Salary Change", "Benefits Change", "Overhead Change", "Teaching Change",
    "Scenario Net"
]
waterfall_values = [
    base["net_position"] / 1e6,
    (scen["ime_revenue"] - base["ime_revenue"]) / 1e6,
    (scen["dme_revenue"] - base["dme_revenue"]) / 1e6,
    (scen["medicaid_revenue"] - base["medicaid_revenue"]) / 1e6,
    (scen["clinical_revenue"] - base["clinical_revenue"]) / 1e6,
    -(scen["salary_cost"] - base["salary_cost"]) / 1e6,
    -(scen["benefits_cost"] - base["benefits_cost"]) / 1e6,
    -(scen["overhead_cost"] - base["overhead_cost"]) / 1e6,
    -(scen["teaching_cost"] - base["teaching_cost"]) / 1e6,
    scen["net_position"] / 1e6,
]
waterfall_measures = ["absolute"] + ["relative"] * 8 + ["total"]

fig = go.Figure(go.Waterfall(
    x=waterfall_labels,
    y=waterfall_values,
    measure=waterfall_measures,
    connector=dict(line=dict(color=COLORS["card_border"], width=1)),
    increasing=dict(marker=dict(color=COLORS["success"])),
    decreasing=dict(marker=dict(color=COLORS["danger"])),
    totals=dict(marker=dict(color=COLORS["primary"])),
    textposition="outside",
    text=[f"${v:+.1f}M" if m == "relative" else f"${v:.1f}M" for v, m in zip(waterfall_values, waterfall_measures)],
    textfont=dict(size=9),
))
fig.update_layout(
    height=300,
    margin=dict(l=10, r=10, t=10, b=10),
    plot_bgcolor="white", paper_bgcolor="white",
    xaxis=dict(showgrid=False, showline=True, linecolor=COLORS["card_border"],
               tickfont=dict(size=8, color=COLORS["muted"]), tickangle=-30),
    yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
               tickfont=dict(size=9, color=COLORS["muted"]),
               tickprefix="$", ticksuffix="M"),
    hoverlabel=dict(bgcolor="white", font_size=12),
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)


# ── DYNAMIC NARRATIVE ──
net_change = scen["net_position"] - base["net_position"]
narrative_class = "positive" if net_change >= 0 else "warning"

# Identify biggest driver
revenue_changes = {
    "IME rate adjustment": scen["ime_revenue"] - base["ime_revenue"],
    "DME rate adjustment": scen["dme_revenue"] - base["dme_revenue"],
    "Medicaid GME changes": scen["medicaid_revenue"] - base["medicaid_revenue"],
    "clinical volume shifts": scen["clinical_revenue"] - base["clinical_revenue"],
}
cost_changes = {
    "salary adjustments": scen["salary_cost"] - base["salary_cost"],
    "benefits": scen["benefits_cost"] - base["benefits_cost"],
    "overhead": scen["overhead_cost"] - base["overhead_cost"],
    "teaching costs": scen["teaching_cost"] - base["teaching_cost"],
}

biggest_rev_driver = max(revenue_changes.items(), key=lambda x: abs(x[1]))
biggest_cost_driver = max(cost_changes.items(), key=lambda x: abs(x[1]))

if net_change >= 0:
    direction_text = f"improves the net position by {fmt_millions(abs(net_change))}"
else:
    direction_text = f"reduces the net position by {fmt_millions(abs(net_change))}"

st.markdown(f"""
<div class="narrative-box {narrative_class}">
    <strong>What this means:</strong> This scenario {direction_text} compared to baseline. 
    The largest revenue factor is <strong>{biggest_rev_driver[0]}</strong> 
    ({'+' if biggest_rev_driver[1] >= 0 else ''}{fmt_millions(biggest_rev_driver[1])}), 
    and the largest cost driver is <strong>{biggest_cost_driver[0]}</strong> 
    ({'+' if biggest_cost_driver[1] >= 0 else ''}{fmt_millions(biggest_cost_driver[1])}).
    {'The scenario is financially sustainable.' if scen['net_position'] >= 0 else '<strong>Warning:</strong> The scenario results in a net deficit that requires offsetting strategies.'}
</div>
""", unsafe_allow_html=True)


# ── SITE DISTRIBUTION ──
st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Site Distribution & Sensitivity</div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">Decision focus: How does the trainee footprint shift, and what happens if key rates change?</div>', unsafe_allow_html=True)

col_site, col_sens = st.columns(2)

with col_site:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Trainee Distribution by Site Type</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-insight">{scen["trainees_primary"]} trainees at primary site, {scen["trainees_affiliated"]} across {scen["sites"]} affiliated sites ({scen["trainees_affiliated"] // max(scen["sites"], 1)} avg per site).</div>', unsafe_allow_html=True)

    fig = go.Figure()
    site_labels = ["Baseline", "Scenario"]
    primary_vals = [base["trainees_primary"], scen["trainees_primary"]]
    affiliated_vals = [base["trainees_affiliated"], scen["trainees_affiliated"]]
    
    fig.add_trace(go.Bar(name="Primary Site", x=site_labels, y=primary_vals,
                         marker_color=COLORS["accent"],
                         text=primary_vals, textposition="inside", textfont=dict(size=12, color="white")))
    fig.add_trace(go.Bar(name="Affiliated Sites", x=site_labels, y=affiliated_vals,
                         marker_color=COLORS["warning"],
                         text=affiliated_vals, textposition="inside", textfont=dict(size=12, color="white")))
    fig.update_layout(
        barmode="stack", height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        xaxis=dict(showgrid=False, showline=False, tickfont=dict(size=11, color=COLORS["text"])),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
                   tickfont=dict(size=9, color=COLORS["muted"])),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_sens:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Sensitivity: Net Position by IME Rate Change</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-insight">Shows how the current scenario\'s net position shifts with IME rate changes from −30% to +30%.</div>', unsafe_allow_html=True)

    ime_range = list(range(-30, 35, 5))
    net_positions = []
    for adj in ime_range:
        test_params = scenario_params.copy()
        test_params["ime_per_fte"] = BASELINE["medicare_ime_per_fte"] * (1 + adj / 100)
        result = calculate_scenario(test_params)
        net_positions.append(result["net_position"] / 1e6)

    fig = go.Figure()
    colors_line = [COLORS["danger"] if v < 0 else COLORS["success"] for v in net_positions]
    fig.add_trace(go.Scatter(
        x=[f"{v:+d}%" for v in ime_range],
        y=net_positions,
        mode="lines+markers",
        line=dict(color=COLORS["accent"], width=2.5),
        marker=dict(size=7, color=COLORS["accent"]),
        hovertemplate="IME %{x}: $%{y:.1f}M<extra></extra>",
    ))
    fig.add_hline(y=0, line_dash="dot", line_color=COLORS["danger"],
                  annotation_text="Break-even", annotation_position="bottom right",
                  annotation_font_size=9, annotation_font_color=COLORS["danger"])
    
    # Highlight current scenario
    current_idx = ime_range.index(ime_adjustment) if ime_adjustment in ime_range else None
    if current_idx is not None:
        fig.add_trace(go.Scatter(
            x=[f"{ime_adjustment:+d}%"],
            y=[net_positions[current_idx]],
            mode="markers",
            marker=dict(size=14, color=COLORS["primary"], symbol="diamond"),
            name="Current",
            showlegend=True,
        ))
    
    fig.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        xaxis=dict(showgrid=False, showline=True, linecolor=COLORS["card_border"],
                   tickfont=dict(size=9, color=COLORS["muted"]),
                   title=dict(text="IME Rate Change", font=dict(size=9, color=COLORS["muted"]))),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
                   tickfont=dict(size=9, color=COLORS["muted"]),
                   tickprefix="$", ticksuffix="M"),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ── COMPARISON TABLE ──
st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Full Scenario Comparison</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-insight">Side-by-side view of all financial and operational metrics.</div>', unsafe_allow_html=True)

comparison_data = {
    "Metric": [
        "Total Residents", "Total Fellows", "Total Trainees",
        "", 
        "Medicare IME Revenue", "Medicare DME Revenue",
        "Medicaid GME Revenue", "Clinical Revenue", "Total Revenue",
        "",
        "Salary Cost", "Benefits Cost", "Overhead Cost",
        "Teaching Cost", "Total Cost",
        "",
        "Net Position", "Revenue per Trainee", "Cost per Trainee",
        "",
        "Trainees at Primary", "Trainees at Affiliated",
        "Annual Case Volume",
    ],
    "Baseline": [
        f'{base["residents"]:,}', f'{base["fellows"]:,}', f'{base["total_trainees"]:,}',
        "",
        fmt_millions(base["ime_revenue"]), fmt_millions(base["dme_revenue"]),
        fmt_millions(base["medicaid_revenue"]), fmt_millions(base["clinical_revenue"]),
        fmt_millions(base["total_revenue"]),
        "",
        fmt_millions(base["salary_cost"]), fmt_millions(base["benefits_cost"]),
        fmt_millions(base["overhead_cost"]), fmt_millions(base["teaching_cost"]),
        fmt_millions(base["total_cost"]),
        "",
        fmt_millions(base["net_position"]), fmt_currency(base["revenue_per_trainee"]),
        fmt_currency(base["cost_per_trainee"]),
        "",
        f'{base["trainees_primary"]:,}', f'{base["trainees_affiliated"]:,}',
        f'{base["cases"]:,.0f}',
    ],
    "Scenario": [
        f'{scen["residents"]:,}', f'{scen["fellows"]:,}', f'{scen["total_trainees"]:,}',
        "",
        fmt_millions(scen["ime_revenue"]), fmt_millions(scen["dme_revenue"]),
        fmt_millions(scen["medicaid_revenue"]), fmt_millions(scen["clinical_revenue"]),
        fmt_millions(scen["total_revenue"]),
        "",
        fmt_millions(scen["salary_cost"]), fmt_millions(scen["benefits_cost"]),
        fmt_millions(scen["overhead_cost"]), fmt_millions(scen["teaching_cost"]),
        fmt_millions(scen["total_cost"]),
        "",
        fmt_millions(scen["net_position"]), fmt_currency(scen["revenue_per_trainee"]),
        fmt_currency(scen["cost_per_trainee"]),
        "",
        f'{scen["trainees_primary"]:,}', f'{scen["trainees_affiliated"]:,}',
        f'{scen["cases"]:,.0f}',
    ],
}

df_compare = pd.DataFrame(comparison_data)

# Build HTML table
table_html = '<table class="scenario-table"><thead><tr>'
for col in df_compare.columns:
    table_html += f'<th>{col}</th>'
table_html += '</tr></thead><tbody>'

for _, row in df_compare.iterrows():
    if row["Metric"] == "":
        table_html += '<tr><td colspan="3" style="height: 0.3rem; border: none;"></td></tr>'
    else:
        bold = row["Metric"] in ["Total Revenue", "Total Cost", "Net Position", "Total Trainees"]
        style = 'font-weight: 600;' if bold else ''
        table_html += '<tr>'
        for val in row:
            table_html += f'<td style="{style}">{val}</td>'
        table_html += '</tr>'

table_html += '</tbody></table>'
st.markdown(table_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ──
from datetime import datetime
st.markdown(f"""
<div class="dashboard-footer">
    GME Finance Scenario Simulator  ·  Demonstration with synthetic parameters<br>
    Built by Per Ram Paragi  ·  Director, Accreditation & Strategic Planning  ·  {datetime.now().year}
</div>
""", unsafe_allow_html=True)
