import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Global TB Early Warning Surveillance", layout="wide", page_icon= "tb_logo_final.png")


# --- 2. DATA LOADING & PIPELINE ---
@st.cache_data
def load_data():
    df = pd.read_csv('TB_outcomes_2025-12-13.csv')

    # Filter: Only consider significant cohorts to prevent statistical noise/false alarms
    df = df[df['newrel_coh'] > 200].copy()

    # Calculate Rates
    df['mortality_rate'] = (df['newrel_died'] / df['newrel_coh']) * 100
    df['failure_rate'] = (df['newrel_fail'] / df['newrel_coh']) * 100

    return df


df = load_data()

# --- 3. UI POLISH ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    .stApp { background-color: transparent; }
    /* Increase body font size */
    body, .stApp{
        font-size: 30px; /*adjust this value as needed */
    }
    .content-box {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 30px;
        padding: 25px;
        background-color: rgba(128, 128, 128, 0.05);
        margin-bottom: 25px;
    }
    .section-header {
        font-size: 50px;
        font-weight: 700;
        color: #2C3E50;
        padding-bottom: 8px;
        border-bottom: 3px solid #2E86C1;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    .social-link { font-size: 32px; margin-right: 20px; text-decoration: none; transition: 0.3s; }
    .social-link:hover { opacity: 0.7; transform: scale(1.1); }
    .fa-linkedin { color: #0077b5; }
    .fa-envelope { color: #ea4335; }

    /* Author Page Styling */
    .author-card {
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, rgba(46, 134, 193, 0.1), rgba(0,0,0,0));
        border: 1px solid rgba(46, 134, 193, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)




# Create 3 columns to center the content horizontally
import base64

# Function to convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Load your logo
binary_logo = get_base64_image("tb_logo_final.png")

# Use a ratio that gives the header plenty of room on the left
col1, col2 = st.columns([4, 1])

with col1:
    if binary_logo:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-start;">
                <img src="data:image/png;base64,{binary_logo}" width="70">
                <h1 style="margin-left: 15px; margin-top: 0; margin-bottom: 0; line-height: 1.2; font-size: 2.5rem;">
                    Global TB Early Warning Surveillance
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Logo file not found. Check the file path!")

st.divider()




# --- 5. PAGE: AUTHOR PROFILE (Integrated from CV) ---
def author_page():
    st.markdown("<h2 class='section-header'>Researcher Identity</h2>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.image("grad portrait.jpg", use_container_width=True)
        st.markdown("""
        <div class='author-card' style='text-align: center;'>
            <h3 style='margin-bottom: 0;'>Samuel Aggrey</h3>
            <p style='color: #2E86C1;'><b>Independent Researcher</b></p>
            <hr>
            <a href="https://www.linkedin.com/in/samuel-a-7ab884a9/" class="social-link"><i class="fa-brands fa-linkedin"></i></a>
            <a href="mailto:aggreyfynnsamuel@gmail.com" class="social-link"><i class="fa-solid fa-envelope"></i></a>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        ### Professional Summary
        Independent Researcher and Data Scientist with a **BSc in Biological Sciences (First Class Honors)** from KNUST. 
        Specializing in infectious disease surveillance, host-pathogen interactions, and clinical data modeling.

        **Core Expertise:**
        * **Physiology & Immunology:** Experienced Teaching Assistant at KNUST School of Medical Sciences.
        * **Data Science:** Advanced Python implementation for epidemiological surveillance and predictive health risk modeling.
        * **Clinical Research:** Background in laboratory diagnostics and biosafety experimental design.
        """)

        with st.form("reviewer_form"):
            st.subheader("Reviewer Feedback")

            name = st.text_input("Name")
            observation = st.text_area("Observations")

            submit = st.form_submit_button("Send to Samuel")

            if submit:
                st.success("Thank you for your feedback!")

# --- 6. NAVIGATION ---
with st.sidebar:
    st.image("tb_logo_final.png", use_container_width=True)
    page = st.sidebar.radio("Navigation", ["WHO Strategy", "Sentinel Analysis", "AI Surveillance", "Author Profile", "Future Projection (coming soon)"])
    st.divider()
    st.caption("Trial Version Early Warning System")



if page == "WHO Strategy":
    col1, col2 = st.columns([2.5, 2])
    with col2:
        st.markdown("<h2 class='section-header'>WHO End TB Strategy</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class='content-box'>
        <h4>Global Mission: End TB Epidemic by 2030</h4>
        <p>The <b>End TB Strategy</b> targets a world free of TB, focusing on:</p>
        <ul>
            <li><b>90% Reduction</b> in TB deaths.</li>
            <li><b>80% Reduction</b> in TB incidence rate.</li>
            <li><b>Zero</b> TB-affected families facing catastrophic costs.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        trend = df.groupby('year').apply(
            lambda x: (x['c_new_tsr'] * x['newrel_coh']).sum() / x['newrel_coh'].sum()).reset_index()
        trend.columns = ['year', 'tsr']
        fig = px.line(trend, x='year', y='tsr', title="Treatment Success")
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    col1, col2 = st.columns([1.7,3])
    with col2:
        latest_year = df["year"].max()
        # 1. Use Streamlit for the title (cleaner and more consistent)
        st.markdown("### Global Mortality Rate Heatmap")

        # 2. Remove the 'title' argument from px.choropleth
        fig_map = px.choropleth(
            df[df['year'] == latest_year],
            locations="iso3",
            color="mortality_rate"
        )

        # 3. Tighten the margins and move the map higher
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),  # Sets top margin to 0
            height=400,  # Optional: controls the height of the chart container
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )

        st.plotly_chart(fig_map, use_container_width=True)


    # --- SECTION 1: ACHIEVEMENTS ---
    with col1:
        st.markdown("### <i class='fa-solid fa-award'></i> Strategic Achievements", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background-color: rgba(46, 134, 193, 0.1); padding: 20px; border-radius: 15px; border-left: 5px solid #2ECC71; margin-bottom: 20px;'>
            <h4 style='margin-top:0; color:#2E86C1;'>WHO End TB Milestone</h4>
            <ul style='font-size: 0.95rem; padding-left: 20px;'>
                <li><b>75M+ Lives Saved:</b> Estimated impact of global TB interventions between 2000–2022.</li>
                <li><b>7.5M Notifications:</b> Record-high case detection in 2022, signaling a strong post-pandemic recovery.</li>
                <li><b>Regimen Breakthrough:</b> Global scale-up of the <b>BPaLM regimen</b> (6-month all-oral) for drug-resistant cases.</li>
            </ul>
            <small><i>Ref: WHO Global Tuberculosis Report 2024</i></small>
        </div>
        """, unsafe_allow_html=True)

    # --- SECTION 2: LIMITATIONS & 2026 CONTEXT ---
    st.markdown("### <i class='fa-solid fa-circle-exclamation'></i> Surveillance Constraints",
                    unsafe_allow_html=True)

    with st.expander("Why is data limited to 2022?"):
            st.markdown("""
                <div style='font-size: 0.9rem; line-height: 1.5;'>
                As of <b>2026</b>, verified outcomes for the 2023-2025 cohorts are pending for the following reasons:
                <br><br>
                <b>1. Treatment Duration:</b> Successful outcomes (TSR) can only be confirmed after a patient completes a 6–18 month regimen.
                <br><br>
                <b>2. Verification Cycle:</b> WHO requires an 18–24 month lag to audit and validate national data globally.
                <br><br>
                <b>3. The 'Missing Millions':</b> A gap remains between cases notified on this map and the true global incidence.
                <br><br>
                <b>4. Heterogeneity:</b> High national success rates often mask sub-national 'hotspots' or specific MDR-TB failures.
            </div>
            """, unsafe_allow_html=True)

    # --- SECTION 3: 2026 STATUS INDICATOR ---
    st.info(
            "**Current Status (March 2026):** National systems are presently finalizing the 2024 outcome data. This dashboard will update as WHO audits are released.")


elif page == "AI Surveillance":
    from ai_reasoning import generate_surveillance_insights

    st.markdown(
        '<h2 class="section-header">AI Surveillance Reasoning</h2>',
        unsafe_allow_html=True
    )

    insights = generate_surveillance_insights(df)

    for insight in insights:
        st.info(insight)




elif page == "Sentinel Analysis":
    st.markdown("<p class='header-style'>Sentinel Country Performance</p>", unsafe_allow_html=True)

    country = st.selectbox("Search Sentinel Country", sorted(df['country'].unique()))
    c_data = df[df['country'] == country].sort_values('year')

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(c_data, x='year', y=['mortality_rate', 'failure_rate'], title=f"Outcomes: {country}")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Historical Outcome Data Overview")
        st.dataframe(c_data[['year', 'newrel_coh', 'mortality_rate', 'failure_rate', 'c_new_tsr']],
                     use_container_width=True)

elif page == "Author Profile":
    author_page()


elif page == "Projected Future Risks":
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    import numpy as np


    # Use @st.cache_data so the model doesn't re-run every time you click a button
    @st.cache_data
    def get_tb_early_warning_data():
        # FIX: Added .csv extension and added error handling for file existence
        try:
            df = pd.read_csv("TB_outcomes_2025-12-13.csv")
        except FileNotFoundError:
            st.error("Dataset not found. Please ensure 'TB_outcomes_2025-12-13.csv' is in the project folder.")
            return pd.DataFrame(), pd.DataFrame()

        # 1. Clean and Label Pandemic Years
        data = df[['country', 'year', 'newrel_coh']].dropna()
        data['is_covid'] = data['year'].apply(lambda x: 1 if x in [2020, 2021] else 0)
        base_year = data['year'].min()
        data['year_idx'] = data['year'] - base_year

        alerts = []
        projections = []

        for country, c_data in data.groupby('country'):
            c_data = c_data.sort_values('year')
            if len(c_data) < 7: continue

            try:
                # 2. Fit Poisson with COVID Dampening
                model = smf.glm(formula='newrel_coh ~ year_idx + is_covid',
                                data=c_data, family=sm.families.Poisson()).fit()

                # 3. Calculate Dispersion (The "Quasi" Adjustment)
                # This handles 'noisy' data unique to each country
                dispersion = max(1, model.pearson_chi2 / model.df_resid)

                # 4. Check for Alerts in latest data (2023)
                curr_row = c_data[c_data['year'] == 2023].copy()
                if not curr_row.empty:
                    curr_row['is_covid'] = 0
                    pred = model.get_prediction(curr_row).summary_frame()

                    # Widen interval by dispersion factor
                    mean_val = pred['mean'].values[0]
                    adj_se = pred['mean_se'].values[0] * np.sqrt(dispersion)
                    threshold = mean_val + (1.96 * adj_se)

                    if curr_row['newrel_coh'].values[0] > threshold:
                        alerts.append({
                            'country': country,
                            'observed': int(curr_row['newrel_coh'].values[0]),
                            'limit': int(round(threshold)),
                            'severity': round((curr_row['newrel_coh'].values[0] / threshold), 2)
                        })

                # 5. Build Future Projection (2024-2030)
                future = pd.DataFrame({'year': range(2024, 2031)})
                future['year_idx'] = future['year'] - base_year
                future['is_covid'] = 0
                f_preds = model.get_prediction(future).summary_frame()

                for i, year in enumerate(range(2024, 2031)):
                    m = f_preds['mean'].iloc[i]
                    u = m + (1.96 * f_preds['mean_se'].iloc[i] * np.sqrt(dispersion))
                    projections.append({
                        'country': country,
                        'year': year,
                        'projected': int(round(m)),
                        'upper_limit': int(round(u))
                    })
            except:
                continue

        return pd.DataFrame(alerts), pd.DataFrame(projections)


    # UI Logic
    st.header("🌍 TB Early Warning & Future Projections")

    with st.spinner("Analyzing country trends..."):
        final_alerts, final_projections = get_tb_early_warning_data()

    if not final_alerts.empty:
        st.subheader("🚩 Active Alerts (2023 Surge)")
        st.dataframe(final_alerts.sort_values('severity', ascending=False))

        # Add a selection box to view specific country projections
        selected_country = st.selectbox("Select a country to view 2030 risks:", final_projections['country'].unique())
        country_df = final_projections[final_projections['country'] == selected_country]
        st.line_chart(country_df.set_index('year')[['projected', 'upper_limit']])
