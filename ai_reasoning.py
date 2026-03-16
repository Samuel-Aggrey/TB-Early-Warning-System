import pandas as pd

MIN_COHORT = 200   # minimum cohort size to include in analysis

def generate_surveillance_insights(df):

    insights = []

    # Ensure required columns exist
    required_cols = ["country", "newrel_coh"]
    for col in required_cols:
        if col not in df.columns:
            return ["Dataset missing required surveillance columns."]

    # Aggregate by country
    country_data = df.groupby("country").agg({
        "newrel_coh": "sum",
        "newrel_died": "sum" if "deaths" in df.columns else "sum"
    }).reset_index()

    # Apply cohort filter
    filtered = country_data[country_data["newrel_coh"] > MIN_COHORT]

    if filtered.empty:
        return ["No countries meet the minimum cohort threshold for analysis."]

    # Country with highest burden
    high_country = filtered.loc[filtered["newrel_coh"].idxmax()]

    insights.append(
        f"After applying a **minimum cohort threshold of {MIN_COHORT} cases**, "
        f"the country with the highest TB burden is **{high_country['country']}** "
        f"with **{int(high_country['newrel_coh']):,} reported cases**."
    )

    # Mortality analysis
    if "deaths" in df.columns:

        filtered["mortality_rate"] = (filtered["newrel_died"] / filtered["newrel_coh"]) * 100

        high_mortality = filtered[filtered["mortality_rate"] > 5]

        if not high_mortality.empty:
            countries = ", ".join(high_mortality["country"].tolist())

            insights.append(
                f"Countries with **mortality rates above 5%** among cohorts larger than "
                f"{MIN_COHORT} include: **{countries}**. "
                "This may indicate treatment gaps or delayed diagnosis."
            )

    # Trend analysis (if year column exists)
    if "year" in df.columns:

        yearly = df.groupby("year")["newrel_coh"].sum()

        if len(yearly) >= 2:
            if yearly.iloc[-1] > yearly.iloc[-2]:

                change = yearly.iloc[-1] - yearly.iloc[-2]

                insights.append(
                    f"Global TB cases increased by **{int(change):,} cases** "
                    "compared to the previous year, suggesting possible transmission acceleration."
                )

            else:
                insights.append(
                    "Recent surveillance data suggests **stable or declining TB incidence** globally."
                )

    insights.append(
        f"Note: Countries with **case cohorts below {MIN_COHORT} were excluded** "
        "to avoid statistical noise in surveillance reasoning."
    )

    return insights