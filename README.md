# Global TB Early Warning Surveillance System

An interactive infectious disease surveillance dashboard designed to monitor global tuberculosis (TB) treatment outcomes and detect potential early warning signals of epidemiological risk.

The system analyzes WHO tuberculosis treatment outcome datasets and provides real-time visualizations, country-level performance monitoring, and statistical alerts for unusual case surges.

Live Dashboard  
https://tbearlywarning.streamlit.app

---

## Project Overview

Tuberculosis remains one of the world's most persistent infectious diseases. Monitoring treatment outcomes and case trends across countries is essential for detecting emerging risks and evaluating the effectiveness of global TB control programs.

This project was developed as a digital surveillance prototype that integrates epidemiological data analysis with an interactive dashboard. It allows researchers and public health observers to explore TB treatment outcomes across countries and identify potential warning signals in surveillance data.

The application combines data processing, statistical modelling, and visualization to create an accessible monitoring platform for global TB control trends.

---

## Key Features

### Global Surveillance Dashboard
Visualizes treatment success trends and mortality patterns across countries using interactive charts.

### Country Sentinel Analysis
Users can select individual countries to evaluate historical treatment outcomes and cohort performance.

### Global Mortality Heatmap
Displays country-level mortality rates geographically to highlight regions with higher TB burden.

### AI Surveillance Reasoning
An automated reasoning module generates contextual insights from surveillance data to assist interpretation.

### Statistical Early Warning System
A Poisson regression model analyzes longitudinal case data to detect unusual increases in TB cohorts and generate alert signals.

### Future Risk Projections
The system estimates projected case trends up to 2030 using statistical modeling and uncertainty intervals.

---

## Data Source

The dashboard uses tuberculosis treatment outcome data derived from the global tuberculosis database maintained by the World Health Organization.

Data include national treatment cohort outcomes such as:

- New and relapse treatment cohorts
- Treatment success rates
- Mortality outcomes
- Treatment failures
- Country-level surveillance indicators

To reduce statistical noise, the system filters cohorts with fewer than 200 cases before analysis.

---

## Methods

### Data Processing

The pipeline performs several preprocessing steps:

- Filtering small cohorts (<200 cases)
- Calculating derived metrics such as:
  - Mortality rate
  - Treatment failure rate
- Aggregating trends by country and year

### Epidemiological Indicators

Two key surveillance indicators are derived:

Mortality Rate  
(newrel_died / newrel_coh) × 100

Failure Rate  
(newrel_fail / newrel_coh) × 100

These indicators help identify potential weaknesses in TB treatment programs.

### Statistical Alert System

The early warning module uses a Poisson generalized linear model to detect unusual increases in reported TB cohorts.

Model features include:

- Time trend modeling
- COVID-19 adjustment for pandemic years (2020–2021)
- Dispersion correction for noisy epidemiological data
- Statistical thresholds for surge detection

Countries exceeding expected case levels trigger a surveillance alert.

### Future Projection Model

The system generates projections for TB cohorts between 2024 and 2030 based on fitted Poisson models and uncertainty intervals.

These projections are intended for exploratory surveillance analysis rather than official epidemiological forecasting.

---

## Dashboard Pages

WHO Strategy  
Overview of the WHO End TB strategy and global treatment success trends.

Sentinel Analysis  
Country-level analysis of treatment outcomes and historical cohort performance.

AI Surveillance  
Automated interpretation of epidemiological patterns using rule-based reasoning.

Author Profile  
Research background and project context.

Future Projection (Early Warning System)  
Statistical alert detection and projections for potential future case surges.

---

## Technology Stack

Python

Streamlit – interactive web application framework

Pandas – data processing

Plotly – interactive visualization

NumPy – numerical computation

Statsmodels – statistical modeling

Font Awesome – interface icons

---

## Installation

Clone the repository:
