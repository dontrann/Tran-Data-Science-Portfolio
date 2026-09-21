import streamlit as st
import pandas as pd
from pathlib import Path

# -------------------------
# PAGE SETUP
# -------------------------

st.set_page_config(
    page_title="World Happiness Report",
    page_icon="🌎",
    layout="wide"
)

# Simple custom styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fffaf4;
    }

    h1, h2, h3 {
        font-family: Georgia, serif;
        color: #355070;
    }

    p, label, div {
        font-family: "Trebuchet MS", sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #f3e9dc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# TITLE AND DESCRIPTION
# -------------------------

st.title("🌎 World Happiness Report")

st.write(
    "This app explores the 2019 World Happiness Report. "
    "Use the filters in the sidebar to compare countries based on "
    "happiness, income, and other quality-of-life factors."
)

st.divider()

# -------------------------
# LOAD DATA
# -------------------------

data_path = Path(__file__).parent / "data" / "your_data.csv"
df = pd.read_csv(data_path)

# -------------------------
# SIDEBAR FILTERS
# -------------------------

st.sidebar.header("Explore the Data")

score_range = st.sidebar.slider(
    "Happiness Score",
    min_value=float(df["Score"].min()),
    max_value=float(df["Score"].max()),
    value=(
        float(df["Score"].min()),
        float(df["Score"].max())
    )
)

gdp_range = st.sidebar.slider(
    "GDP per Capita",
    min_value=float(df["GDP per capita"].min()),
    max_value=float(df["GDP per capita"].max()),
    value=(
        float(df["GDP per capita"].min()),
        float(df["GDP per capita"].max())
    )
)

countries = st.sidebar.multiselect(
    "Choose Countries",
    options=sorted(df["Country or region"].unique())
)

extra_filter = st.sidebar.selectbox(
    "Additional Filter",
    [
        "None",
        "Social support",
        "Healthy life expectancy",
        "Freedom to make life choices"
    ]
)

# -------------------------
# APPLY FILTERS
# -------------------------

filtered_df = df[
    (df["Score"] >= score_range[0]) &
    (df["Score"] <= score_range[1]) &
    (df["GDP per capita"] >= gdp_range[0]) &
    (df["GDP per capita"] <= gdp_range[1])
]

if countries:
    filtered_df = filtered_df[
        filtered_df["Country or region"].isin(countries)
    ]

# Optional extra filter
if extra_filter != "None":

    extra_range = st.sidebar.slider(
        f"{extra_filter} Range",
        min_value=float(df[extra_filter].min()),
        max_value=float(df[extra_filter].max()),
        value=(
            float(df[extra_filter].min()),
            float(df[extra_filter].max())
        )
    )

    filtered_df = filtered_df[
        (filtered_df[extra_filter] >= extra_range[0]) &
        (filtered_df[extra_filter] <= extra_range[1])
    ]

# -------------------------
# QUICK SUMMARY
# -------------------------

st.subheader("Quick Look")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Countries Shown",
        len(filtered_df)
    )

with col2:
    if len(filtered_df) > 0:
        st.metric(
            "Average Happiness Score",
            round(filtered_df["Score"].mean(), 2)
        )
    else:
        st.metric(
            "Average Happiness Score",
            "N/A"
        )

# -------------------------
# DATA TABLE
# -------------------------

st.subheader("Filtered Countries")

st.write(
    "Adjust the filters to see how different countries compare."
)

st.dataframe(
    filtered_df,
    use_container_width=True
)