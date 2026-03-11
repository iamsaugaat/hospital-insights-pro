import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hospital Insights Pro",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# DARK MODE COLOR PALETTE
# ─────────────────────────────────────────────────────────────
BG = "#0E1117"
BG_CARD = "#1A1D23"
BG_CARD_ALT = "#21252B"
TEXT = "#E8EAED"
TEXT_MUTED = "#9AA0A6"
ACCENT = "#4FC3F7"
ACCENT_GREEN = "#66BB6A"
ACCENT_RED = "#EF5350"
ACCENT_AMBER = "#FFA726"
BORDER = "#2D3139"
PLOTLY_BG = "#1A1D23"
PLOTLY_GRID = "#2D3139"
PLOTLY_TEXT = "#9AA0A6"
GAUGE_BAR = "#E8EAED"
SHADOW = "0 2px 12px rgba(0,0,0,0.3)"
INSIGHT_BG_GOOD = "rgba(102,187,106,0.08)"
INSIGHT_BORDER_GOOD = "rgba(102,187,106,0.3)"
INSIGHT_BG_BAD = "rgba(239,83,80,0.08)"
INSIGHT_BORDER_BAD = "rgba(239,83,80,0.3)"
INSIGHT_BG_NEUTRAL = "rgba(79,195,247,0.06)"
INSIGHT_BORDER_NEUTRAL = "rgba(79,195,247,0.25)"

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stApp"] {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}
[data-testid="stHeader"] {{ background-color: {BG} !important; }}
[data-testid="stSidebar"] {{ display: none !important; }}
.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1320px !important;
}}

[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stRadio"] label {{
    color: {TEXT_MUTED} !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    margin-bottom: 2px !important;
}}
[data-testid="stSelectbox"] > div > div {{
    background-color: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
    font-size: 0.9rem !important;
}}
[data-testid="stSelectbox"] svg {{ fill: {TEXT_MUTED} !important; }}
div[data-baseweb="select"] > div {{
    background-color: {BG_CARD} !important;
    border-color: {BORDER} !important;
}}
div[data-baseweb="select"] span {{ color: {TEXT} !important; }}

[data-testid="stTabs"] button {{
    background-color: {BG_CARD_ALT} !important;
    color: {TEXT_MUTED} !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.2rem !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    margin-right: 6px !important;
    transition: all 0.15s ease;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
    background-color: {ACCENT} !important;
    color: {BG} !important;
    font-weight: 600 !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-border"],
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{ display: none !important; }}

[data-testid="stMetric"] {{
    background: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: {SHADOW};
}}
[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED} !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    font-weight: 500 !important;
}}
[data-testid="stMetricValue"] {{
    color: {TEXT} !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.8rem !important; }}

[data-testid="stSlider"] > div > div > div > div {{ background-color: {ACCENT} !important; }}

[data-testid="stExpander"] {{
    background-color: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}
[data-testid="stExpander"] summary {{ color: {TEXT} !important; font-weight: 500 !important; }}
[data-testid="stExpander"] p {{ color: {TEXT_MUTED} !important; }}

hr {{ border-color: {BORDER} !important; opacity: 0.5 !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}

[data-testid="stPlotlyChart"] {{ border-radius: 12px; overflow: hidden; }}

::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}

[data-testid="stRadio"] > div {{ gap: 0.5rem; }}
[data-testid="stRadio"] label[data-baseweb="radio"] {{
    background: {BG_CARD_ALT} !important;
    border-radius: 6px !important;
    padding: 0.35rem 0.8rem !important;
    font-size: 0.85rem !important;
    text-transform: none !important;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────
# DATA PIPELINE
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_data():
    df_general = pd.read_csv("Hospital_General_Information.csv", low_memory=False)
    df_visits = pd.read_csv("Unplanned_Hospital_Visits-Hospital.csv", low_memory=False)

    df_general.columns = df_general.columns.str.strip()
    df_visits.columns = df_visits.columns.str.strip()

    df_readmission = df_visits[df_visits["Measure ID"] == "Hybrid_HWR"].copy()
    df_readmission["Score"] = pd.to_numeric(df_readmission["Score"], errors="coerce")

    df_merged = pd.merge(
        df_general[["Facility ID", "Facility Name", "State", "City/Town",
                     "Hospital overall rating", "Hospital Type", "Hospital Ownership"]],
        df_readmission[["Facility ID", "Score"]],
        on="Facility ID",
        how="inner",
    )

    df_merged.rename(columns={
        "Hospital overall rating": "CMS Rating",
        "Score": "Readmission Rate (%)",
    }, inplace=True)

    NATIONAL_AVG = 15.0
    df_merged["Above Threshold"] = df_merged["Readmission Rate (%)"] > NATIONAL_AVG

    np.random.seed(42)
    penalty_vals = np.where(
        df_merged["Above Threshold"],
        (df_merged["Readmission Rate (%)"] - NATIONAL_AVG) * 150000
        + np.random.randint(50000, 200000, len(df_merged)),
        0,
    )
    df_merged["Est. Penalty ($)"] = np.round(penalty_vals, 0)
    df_merged = df_merged.dropna(subset=["Readmission Rate (%)"])
    return df_merged


df = load_data()
NATIONAL_AVG = 15.0


# ─────────────────────────────────────────────────────────────
# HELPER — safe plotly layout builder (prevents duplicate kwarg errors)
# ─────────────────────────────────────────────────────────────
def make_layout(**overrides):
    """Build a Plotly layout dict. Overrides take precedence over defaults."""
    base = dict(
        paper_bgcolor=PLOTLY_BG,
        plot_bgcolor=PLOTLY_BG,
        font=dict(family="DM Sans, sans-serif", color=PLOTLY_TEXT, size=12),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    if "xaxis" not in overrides:
        base["xaxis"] = dict(gridcolor=PLOTLY_GRID, zeroline=False)
    if "yaxis" not in overrides:
        base["yaxis"] = dict(gridcolor=PLOTLY_GRID, zeroline=False)
    base.update(overrides)
    return base


def generate_insights(name, rate, penalty, state_avg, state_rank, state_total):
    insights = []
    gap = round(rate - NATIONAL_AVG, 2)
    if gap > 1:
        insights.append(
            f"{name} readmits {abs(gap)}% more patients than the national average. "
            "More patients are returning within 30 days, which can lead to Medicare payment cuts.")
    elif gap > 0:
        insights.append(
            f"{name} is slightly above average by {abs(gap)}%. "
            "A small improvement could move it into the safe zone and avoid penalties.")
    else:
        insights.append(
            f"{name} is {abs(gap)}% below the national average — a strong result. "
            "Readmissions are low, protecting both revenue and patient care quality.")

    pct = round((state_rank / state_total) * 100)
    if pct <= 25:
        insights.append(f"Ranked #{state_rank} of {state_total} in the state (top 25%) — one of the best.")
    elif pct <= 50:
        insights.append(f"Ranked #{state_rank} of {state_total} — above the midpoint, with room to reach the top tier.")
    else:
        insights.append(f"Ranked #{state_rank} of {state_total} — most peers are doing better on readmissions.")

    if penalty > 0:
        insights.append(f"Estimated annual penalty: ${penalty:,.0f}. Even a small improvement could save a large portion.")
    else:
        insights.append("No penalty expected — the hospital is avoiding CMS fines. Keep it up.")
    return insights


def generate_recommendations(rate, penalty, state_avg, cms_rating):
    recs = []
    gap = rate - NATIONAL_AVG
    if gap > 0:
        recs.append("Call or visit every discharged patient within 48 hours — this alone can cut readmissions by 2–3%.")
    if rate > state_avg:
        recs.append("Study what top hospitals in the state do differently, especially around discharge planning.")
    if penalty > 0:
        recovery = min(penalty, penalty * (1.0 / max(gap, 0.1)))
        recs.append(f"Reducing readmissions by just 1% could save roughly ${recovery:,.0f}/year in avoided penalties.")
    try:
        if int(cms_rating) <= 2:
            recs.append("CMS star rating is low — improving safety and satisfaction alongside readmissions will help.")
    except (ValueError, TypeError):
        pass
    return recs[:3]


def state_summary(state_data, selected_state):
    total = len(state_data)
    avg_rate = state_data["Readmission Rate (%)"].mean()
    above = int((state_data["Readmission Rate (%)"] > NATIONAL_AVG).sum())
    below = total - above
    total_penalty = state_data["Est. Penalty ($)"].sum()
    return dict(
        total=total, avg_rate=round(avg_rate, 2), above=above, below=below,
        pct_safe=round((below / total) * 100) if total else 0,
        total_penalty=total_penalty,
        best=state_data.nsmallest(5, "Readmission Rate (%)"),
        worst=state_data.nlargest(5, "Readmission Rate (%)"),
    )


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.2rem;">
        <div style="width:38px;height:38px;border-radius:10px;
            background:linear-gradient(135deg,{ACCENT},{ACCENT_GREEN});
            display:flex;align-items:center;justify-content:center;
            font-size:1.1rem;color:#fff;font-weight:700;">H</div>
        <div>
            <span style="font-size:1.25rem;font-weight:700;color:{TEXT};letter-spacing:-0.02em;">Hospital Insights Pro</span><br/>
            <span style="font-size:0.78rem;color:{TEXT_MUTED};letter-spacing:0.02em;">Strategic Readmission Analytics for U.S. Hospitals</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HORIZONTAL FILTERS
# ─────────────────────────────────────────────────────────────
f1, f2, f3 = st.columns([1.5, 3, 3])

with f1:
    states = sorted(df["State"].dropna().unique())
    default_idx = states.index("TX") if "TX" in states else 0
    selected_state = st.selectbox("State", states, index=default_idx)

state_data = df[df["State"] == selected_state].copy()

with f2:
    hospitals = sorted(state_data["Facility Name"].dropna().unique())
    selected_hospital = st.selectbox("Hospital", hospitals, index=0)

hosp = state_data[state_data["Facility Name"] == selected_hospital].iloc[0]
rate = float(hosp["Readmission Rate (%)"])
penalty = float(hosp["Est. Penalty ($)"])
s_avg = state_data["Readmission Rate (%)"].mean()

sorted_state = state_data.sort_values("Readmission Rate (%)").reset_index(drop=True)
s_rank = int(sorted_state[sorted_state["Facility Name"] == selected_hospital].index[0]) + 1
s_total = len(sorted_state)

with f3:
    st.markdown(
        f"""<div style="padding:0.6rem 1rem;margin-top:1.35rem;border-radius:10px;
            background:{BG_CARD};border:1px solid {BORDER};display:flex;gap:1.6rem;align-items:center;box-shadow:{SHADOW};">
            <div><span style="color:{TEXT_MUTED};font-size:0.72rem;text-transform:uppercase;letter-spacing:0.04em;">Location</span><br/>
                <span style="color:{TEXT};font-size:0.92rem;font-weight:600;">{hosp['City/Town']}, {selected_state}</span></div>
            <div style="width:1px;height:28px;background:{BORDER};"></div>
            <div><span style="color:{TEXT_MUTED};font-size:0.72rem;text-transform:uppercase;letter-spacing:0.04em;">CMS Rating</span><br/>
                <span style="color:{TEXT};font-size:0.92rem;font-weight:600;">{hosp['CMS Rating']} / 5</span></div>
            <div style="width:1px;height:28px;background:{BORDER};"></div>
            <div><span style="color:{TEXT_MUTED};font-size:0.72rem;text-transform:uppercase;letter-spacing:0.04em;">Type</span><br/>
                <span style="color:{TEXT};font-size:0.92rem;font-weight:600;">{hosp.get('Hospital Type','N/A')}</span></div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# STATE SNAPSHOT
# ─────────────────────────────────────────────────────────────
ss = state_summary(state_data, selected_state)

st.markdown(
    f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1.2rem 1.6rem;margin-bottom:0.8rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.8rem;">
            <div style="font-weight:600;font-size:1rem;color:{ACCENT};">{selected_state} State Snapshot</div>
            <div style="display:flex;gap:2rem;flex-wrap:wrap;">
                <div style="text-align:center;"><div style="font-size:1.3rem;font-weight:700;color:{TEXT};">{ss['total']}</div>
                    <div style="font-size:0.7rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.04em;">Hospitals</div></div>
                <div style="text-align:center;"><div style="font-size:1.3rem;font-weight:700;color:{TEXT};">{ss['avg_rate']}%</div>
                    <div style="font-size:0.7rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.04em;">Avg Rate</div></div>
                <div style="text-align:center;"><div style="font-size:1.3rem;font-weight:700;color:{ACCENT_GREEN};">{ss['pct_safe']}%</div>
                    <div style="font-size:0.7rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.04em;">Below Threshold</div></div>
                <div style="text-align:center;"><div style="font-size:1.3rem;font-weight:700;color:{ACCENT_RED};">{ss['above']}</div>
                    <div style="font-size:0.7rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.04em;">At Risk</div></div>
                <div style="text-align:center;"><div style="font-size:1.3rem;font-weight:700;color:{ACCENT_AMBER};">${ss['total_penalty']/1e6:.1f}M</div>
                    <div style="font-size:0.7rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.04em;">Total Est. Penalties</div></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# Best & Worst side by side
c_best, c_worst = st.columns(2)

with c_best:
    rows_html = ""
    for i, (_, r) in enumerate(ss["best"].iterrows()):
        sep = f"border-top:1px solid {BORDER};" if i > 0 else ""
        rows_html += f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:0.45rem 0;{sep}">
            <div style="font-size:0.84rem;color:{TEXT};max-width:75%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{i+1}. {r['Facility Name']}</div>
            <div style="font-size:0.84rem;font-weight:600;color:{ACCENT_GREEN};">{r['Readmission Rate (%)']:.1f}%</div></div>"""
    st.markdown(f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem 1.2rem;">
        <div style="font-weight:600;font-size:0.85rem;color:{ACCENT_GREEN};margin-bottom:0.6rem;text-transform:uppercase;letter-spacing:0.04em;">Top 5 — Lowest Readmission Rates</div>
        {rows_html}</div>""", unsafe_allow_html=True)

with c_worst:
    rows_html = ""
    for i, (_, r) in enumerate(ss["worst"].iterrows()):
        sep = f"border-top:1px solid {BORDER};" if i > 0 else ""
        rows_html += f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:0.45rem 0;{sep}">
            <div style="font-size:0.84rem;color:{TEXT};max-width:75%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{i+1}. {r['Facility Name']}</div>
            <div style="font-size:0.84rem;font-weight:600;color:{ACCENT_RED};">{r['Readmission Rate (%)']:.1f}%</div></div>"""
    st.markdown(f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem 1.2rem;">
        <div style="font-weight:600;font-size:0.85rem;color:{ACCENT_RED};margin-bottom:0.6rem;text-transform:uppercase;letter-spacing:0.04em;">Bottom 5 — Highest Readmission Rates</div>
        {rows_html}</div>""", unsafe_allow_html=True)

# State insight
svn = round(ss["avg_rate"] - NATIONAL_AVG, 2)
if svn > 0.5:
    si_text = f"{selected_state} averages {ss['avg_rate']}%, which is {abs(svn)}% above the national threshold. {ss['above']} hospitals face penalty risk, totaling an estimated ${ss['total_penalty']/1e6:.1f}M in exposure."
    si_bg, si_border = INSIGHT_BG_BAD, INSIGHT_BORDER_BAD
elif svn > 0:
    si_text = f"{selected_state} is near the national average at {ss['avg_rate']}%. {ss['pct_safe']}% of hospitals are safe, but {ss['above']} still face risk."
    si_bg, si_border = INSIGHT_BG_NEUTRAL, INSIGHT_BORDER_NEUTRAL
else:
    si_text = f"{selected_state} outperforms the national average at {ss['avg_rate']}%. {ss['pct_safe']}% of hospitals are below the penalty threshold."
    si_bg, si_border = INSIGHT_BG_GOOD, INSIGHT_BORDER_GOOD

st.markdown(f"""<div style="background:{si_bg};border:1px solid {si_border};border-radius:10px;padding:0.9rem 1.2rem;margin-top:0.6rem;margin-bottom:0.4rem;">
    <div style="font-size:0.88rem;color:{TEXT};line-height:1.6;">{si_text}</div></div>""", unsafe_allow_html=True)

st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Executive Summary", "Deep Dive", "Financial Simulator"])

# ======================== TAB 1 ========================
with tab1:
    k1, k2, k3, k4 = st.columns(4)
    gn = round(rate - NATIONAL_AVG, 2)
    gs = round(rate - s_avg, 2)
    k1.metric("Readmission Rate", f"{rate}%", f"{gn:+.2f}% vs National", delta_color="inverse")
    k2.metric("State Average", f"{round(s_avg, 2)}%", f"{gs:+.2f}% vs Peers", delta_color="inverse")
    k3.metric("State Rank", f"#{s_rank} of {s_total}", "Lower is better")
    if penalty > 0:
        k4.metric("Est. Annual Penalty", f"${penalty:,.0f}", "At Risk", delta_color="inverse")
    else:
        k4.metric("Est. Annual Penalty", "$0", "Safe")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Simple explainer
    st.markdown(f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:1rem;">
        <div style="font-weight:600;font-size:0.9rem;color:{ACCENT};margin-bottom:0.5rem;">What does this mean?</div>
        <div style="font-size:0.88rem;color:{TEXT};line-height:1.7;">
            When a patient leaves the hospital and has to come back within 30 days, it counts as a <strong>readmission</strong>.
            The government tracks this for every hospital. If the rate is too high (above 15%), <strong>Medicare reduces
            the hospital's payments</strong>. The maximum cut is 3% of all Medicare revenue. This tool helps hospitals
            understand where they stand and how much money they could save by improving.
        </div></div>""", unsafe_allow_html=True)

    # Insights
    insights = generate_insights(selected_hospital, rate, penalty, s_avg, s_rank, s_total)
    is_good = rate <= NATIONAL_AVG
    ins_bg = INSIGHT_BG_GOOD if is_good else INSIGHT_BG_BAD
    ins_border = INSIGHT_BORDER_GOOD if is_good else INSIGHT_BORDER_BAD
    ins_color = ACCENT_GREEN if is_good else ACCENT_RED
    ins_title = "Good Standing — Key Takeaways" if is_good else "Needs Attention — Key Takeaways"

    st.markdown(f"""<div style="background:{ins_bg};border:1px solid {ins_border};border-radius:12px;padding:1.4rem 1.6rem;margin-bottom:1rem;">
        <div style="font-weight:600;font-size:1rem;color:{ins_color};margin-bottom:0.8rem;">{ins_title}</div>
        <ol style="margin:0;padding-left:1.2rem;color:{TEXT};line-height:1.75;font-size:0.9rem;">
            <li style="margin-bottom:0.4rem;">{insights[0]}</li>
            <li style="margin-bottom:0.4rem;">{insights[1]}</li>
            <li>{insights[2]}</li>
        </ol></div>""", unsafe_allow_html=True)

    # Recommendations
    recs = generate_recommendations(rate, penalty, s_avg, hosp["CMS Rating"])
    if recs:
        st.markdown(f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1.4rem 1.6rem;">
            <div style="font-weight:600;font-size:1rem;color:{ACCENT};margin-bottom:0.8rem;">Recommended Next Steps</div>
            <ol style="margin:0;padding-left:1.2rem;color:{TEXT};line-height:1.75;font-size:0.9rem;">
                {''.join(f'<li style="margin-bottom:0.4rem;">{r}</li>' for r in recs)}
            </ol></div>""", unsafe_allow_html=True)


# ======================== TAB 2 ========================
with tab2:
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    cg, ch = st.columns(2)

    with cg:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=rate,
            number=dict(suffix="%", font=dict(size=42, color=TEXT)),
            title=dict(text="Readmission Severity Index", font=dict(size=14, color=TEXT_MUTED)),
            gauge=dict(
                axis=dict(range=[10, 20], tickcolor=PLOTLY_TEXT, tickfont=dict(color=PLOTLY_TEXT)),
                bar=dict(color=GAUGE_BAR), bgcolor=PLOTLY_BG, borderwidth=0,
                steps=[
                    dict(range=[10, 14], color="rgba(102,187,106,0.25)"),
                    dict(range=[14, 15], color="rgba(255,167,38,0.25)"),
                    dict(range=[15, 17], color="rgba(255,167,38,0.35)"),
                    dict(range=[17, 20], color="rgba(239,83,80,0.35)"),
                ],
                threshold=dict(line=dict(color=ACCENT_RED, width=3), thickness=0.8, value=NATIONAL_AVG),
            ),
        ))
        fig_gauge.update_layout(**make_layout(height=340))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"""<div style="font-size:0.8rem;color:{TEXT_MUTED};text-align:center;margin-top:-0.5rem;">
            Green = safe &nbsp;|&nbsp; Yellow = watch zone &nbsp;|&nbsp; Red = high risk &nbsp;|&nbsp; Red line = 15% threshold</div>""", unsafe_allow_html=True)

    with ch:
        fig_hist = px.histogram(state_data, x="Readmission Rate (%)", nbins=25, color_discrete_sequence=[ACCENT])
        fig_hist.add_vline(x=rate, line_dash="dash", line_color=ACCENT_RED,
                           annotation_text="This Hospital", annotation_font_color=ACCENT_RED)
        fig_hist.update_layout(**make_layout(
            height=340, bargap=0.06,
            title=dict(text=f"Readmission Distribution — {selected_state}", font=dict(size=14, color=TEXT_MUTED)),
            xaxis=dict(gridcolor=PLOTLY_GRID, zeroline=False, title="Readmission Rate (%)"),
            yaxis=dict(gridcolor=PLOTLY_GRID, zeroline=False, title="Number of Hospitals"),
        ))
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown(f"""<div style="font-size:0.8rem;color:{TEXT_MUTED};text-align:center;margin-top:-0.5rem;">
            Each bar = how many hospitals fall in that range. Red dashed line = <strong>{selected_hospital}</strong>.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    view_opt = st.radio("Show facilities with:", ["Highest Readmission Rates", "Lowest Readmission Rates"], horizontal=True)

    if view_opt == "Highest Readmission Rates":
        cd = state_data.nlargest(15, "Readmission Rate (%)").sort_values("Readmission Rate (%)", ascending=True)
        bcolors = [ACCENT_RED if v > NATIONAL_AVG else ACCENT_GREEN for v in cd["Readmission Rate (%)"]]
    else:
        cd = state_data.nsmallest(15, "Readmission Rate (%)").sort_values("Readmission Rate (%)", ascending=True)
        bcolors = [ACCENT_GREEN if v <= NATIONAL_AVG else ACCENT_RED for v in cd["Readmission Rate (%)"]]

    fig_bar = go.Figure(go.Bar(
        y=cd["Facility Name"], x=cd["Readmission Rate (%)"], orientation="h",
        marker_color=bcolors,
        text=[f"{v:.1f}%" for v in cd["Readmission Rate (%)"]],
        textposition="outside", textfont=dict(color=TEXT_MUTED, size=11),
    ))
    fig_bar.add_vline(x=NATIONAL_AVG, line_dash="dot", line_color=TEXT_MUTED,
                      annotation_text="National Avg (15%)", annotation_font_color=TEXT_MUTED)
    fig_bar.update_layout(**make_layout(
        height=max(420, len(cd) * 34), showlegend=False,
        title=dict(text=f"Top 15 — {view_opt} in {selected_state}", font=dict(size=14, color=TEXT_MUTED)),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11, color=TEXT), zeroline=False),
        xaxis=dict(gridcolor=PLOTLY_GRID, title="Readmission Rate (%)", zeroline=False),
    ))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Scatter
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    scat = state_data.copy()
    scat["CMS Numeric"] = pd.to_numeric(scat["CMS Rating"], errors="coerce")
    scat = scat.dropna(subset=["CMS Numeric"])
    scat["Selected"] = scat["Facility Name"] == selected_hospital

    fig_sc = px.scatter(scat, x="CMS Numeric", y="Readmission Rate (%)", color="Selected",
                        color_discrete_map={True: ACCENT_RED, False: "rgba(79,195,247,0.4)"},
                        hover_data=["Facility Name"])
    fig_sc.update_traces(marker=dict(size=7, line=dict(width=0)))
    fig_sc.update_layout(**make_layout(
        height=380, showlegend=False,
        title=dict(text="CMS Star Rating vs Readmission Rate", font=dict(size=14, color=TEXT_MUTED)),
        xaxis=dict(title="CMS Star Rating", gridcolor=PLOTLY_GRID, dtick=1, zeroline=False),
        yaxis=dict(title="Readmission Rate (%)", gridcolor=PLOTLY_GRID, zeroline=False),
    ))
    fig_sc.add_hline(y=NATIONAL_AVG, line_dash="dot", line_color=TEXT_MUTED,
                     annotation_text="National Avg", annotation_font_color=TEXT_MUTED)
    st.plotly_chart(fig_sc, use_container_width=True)
    st.markdown(f"""<div style="font-size:0.8rem;color:{TEXT_MUTED};margin-top:-0.5rem;">
        Higher star rating + lower readmission = best. Upper-left corner = most at-risk hospitals. Red dot = <strong>{selected_hospital}</strong>.</div>""", unsafe_allow_html=True)


# ======================== TAB 3 ========================
with tab3:
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    st.markdown(f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:1rem;">
        <div style="font-weight:600;font-size:0.9rem;color:{ACCENT};margin-bottom:0.5rem;">How does this work?</div>
        <div style="font-size:0.88rem;color:{TEXT};line-height:1.7;">
            When a hospital's readmission rate is above 15%, Medicare cuts its payments. The higher the rate,
            the bigger the cut — up to 3% of all Medicare revenue. Use the slider below to see how much money
            this hospital could save by lowering its readmission rate.
        </div></div>""", unsafe_allow_html=True)

    if penalty > 0:
        gap = rate - NATIONAL_AVG

        st.markdown(f"""<div style="background:{INSIGHT_BG_BAD};border:1px solid {INSIGHT_BORDER_BAD};
            border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:1rem;">
            <div style="font-size:0.88rem;color:{TEXT};line-height:1.6;">
                <strong>{selected_hospital}</strong> is <strong>{round(gap, 2)}%</strong> above the safe zone,
                resulting in an estimated <strong>${penalty:,.0f}</strong> annual penalty.
            </div></div>""", unsafe_allow_html=True)

        reduction = st.slider("How much could readmissions be reduced? (%)",
                              min_value=0.0, max_value=round(gap + 0.5, 1),
                              value=min(1.0, round(gap, 1)), step=0.1)

        new_rate = round(rate - reduction, 2)
        sav_pct = min(reduction / gap, 1.0) if gap > 0 else 0
        savings = round(penalty * sav_pct, 0)

        m1, m2, m3 = st.columns(3)
        m1.metric("Current Rate", f"{rate}%")
        m2.metric("Projected Rate", f"{new_rate}%")
        m3.metric("Projected Savings", f"${savings:,.0f}")

        steps = np.arange(0, reduction + 0.05, 0.1)
        savs = [round(min(s / gap, 1.0) * penalty, 0) if gap > 0 else 0 for s in steps]

        fig_ln = go.Figure(go.Scatter(
            x=steps, y=savs, mode="lines+markers",
            line=dict(color=ACCENT, width=2.5), marker=dict(size=6, color=ACCENT),
            fill="tozeroy", fillcolor="rgba(79,195,247,0.08)",
        ))
        fig_ln.update_layout(**make_layout(
            height=360,
            title=dict(text="Savings Trajectory", font=dict(size=14, color=TEXT_MUTED)),
            xaxis=dict(title="Readmission Rate Reduction (%)", gridcolor=PLOTLY_GRID, zeroline=False),
            yaxis=dict(title="Estimated Savings ($)", gridcolor=PLOTLY_GRID, zeroline=False),
        ))
        st.plotly_chart(fig_ln, use_container_width=True)

        below_msg = "The hospital would drop below the threshold and avoid penalties entirely." if new_rate <= NATIONAL_AVG else "Further reductions would bring it closer to the safe zone."
        st.markdown(f"""<div style="background:{INSIGHT_BG_GOOD};border:1px solid {INSIGHT_BORDER_GOOD};
            border-radius:12px;padding:1.2rem 1.4rem;">
            <div style="color:{TEXT};font-size:0.9rem;line-height:1.65;">
                If <strong>{selected_hospital}</strong> reduces readmissions by <strong>{reduction}%</strong>,
                the new rate would be <strong>{new_rate}%</strong>. This could save approximately
                <strong>${savings:,.0f}</strong> per year in avoided Medicare penalties. {below_msg}
            </div></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="background:{INSIGHT_BG_GOOD};border:1px solid {INSIGHT_BORDER_GOOD};
            border-radius:12px;padding:1.8rem 2rem;text-align:center;">
            <div style="font-size:1.4rem;font-weight:600;color:{ACCENT_GREEN};margin-bottom:0.5rem;">No Penalty Risk</div>
            <div style="color:{TEXT};font-size:0.95rem;line-height:1.6;">
                <strong>{selected_hospital}</strong> is below the national threshold. No CMS penalty at this time. Great work.
            </div></div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DATA TABLE
# ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

with st.expander(f"View All {s_total} Hospitals in {selected_state}"):
    disp = (state_data[["Facility Name", "City/Town", "CMS Rating", "Readmission Rate (%)", "Est. Penalty ($)", "Hospital Type"]]
            .sort_values("Readmission Rate (%)").reset_index(drop=True))
    disp.index = disp.index + 1
    st.dataframe(disp, use_container_width=True, height=420)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown(f"""<div style="border-top:1px solid {BORDER};padding:1.2rem 0 0.5rem 0;
    display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:1rem;">
    <div style="font-size:0.78rem;color:{TEXT_MUTED};line-height:1.7;">
        <strong style="color:{TEXT};">Data Sources</strong><br/>
        <a href="https://data.cms.gov/provider-data/dataset/xubh-q36u" target="_blank" style="color:{ACCENT};text-decoration:none;">Hospital General Information</a>
        &nbsp;&middot;&nbsp;
        <a href="https://data.cms.gov/provider-data/dataset/632h-zaca" target="_blank" style="color:{ACCENT};text-decoration:none;">Unplanned Hospital Visits — Hospital</a><br/>
        Published by the Centers for Medicare &amp; Medicaid Services (CMS) Provider Data Catalog.
    </div>
    <div style="font-size:0.78rem;color:{TEXT_MUTED};text-align:right;line-height:1.7;">
        <strong style="color:{TEXT};">Hospital Insights Pro</strong><br/>
        Built by Saugat Pyakuryal<br/>
        For informational purposes only. Not medical or financial advice.
    </div></div>""", unsafe_allow_html=True)