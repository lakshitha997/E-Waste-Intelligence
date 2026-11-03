import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="E-Waste Intelligence Dashboard",
    page_icon="♻️",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/ewaste_cleaned.csv")

df = load_data()

# Dashboard title
st.title("E-Waste Generation and Recycling Intelligence")
st.caption("Global E-Waste Analysis | 2022")

st.markdown("---")

# Key metrics
total_ewaste = df["ewaste_generated_million_kg_2022"].sum()

available_data = df.dropna(
    subset=["ewaste_documented_collected_million_kg_2022"]
)

total_collected = available_data[
    "ewaste_documented_collected_million_kg_2022"
].sum()

overall_rate = (total_collected / total_ewaste) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total E-Waste", f"{total_ewaste:,.0f} million kg")
col2.metric("Documented Collection", f"{total_collected:,.0f} million kg")
col3.metric("Collection Rate", f"{overall_rate:.2f}%")
col4.metric("Countries Analyzed", len(df))

st.markdown("---")
# Region Filter
st.markdown("---")
st.subheader("Filter by Region")

regions = ["All Regions"] + sorted(df["region"].dropna().unique())

selected_region = st.selectbox(
    "Choose a Region",
    regions
)

if selected_region == "All Regions":
    filtered_df = df.copy()
else:
    filtered_df = df[df["region"] == selected_region]

st.write(f"Countries in selection: {len(filtered_df)}")

# Top 10 countries
st.subheader("Top 10 E-Waste Generating Countries")

top_10 = filtered_df.nlargest(
    10, "ewaste_generated_million_kg_2022"
).sort_values("ewaste_generated_million_kg_2022")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top_10["country"],
    top_10["ewaste_generated_million_kg_2022"]
)
ax.set_xlabel("E-Waste Generated (Million kg)")
ax.set_ylabel("Country")
ax.set_title("Top 10 E-Waste Generators")
st.pyplot(fig)
plt.close(fig)

# Top recycling rates
st.subheader("Top 10 Documented Collection Rates")

recycling_data = filtered_df.dropna(
    subset=["recycling_rate_percent"]
)

top_recycling = recycling_data.nlargest(
    10, "recycling_rate_percent"
).sort_values("recycling_rate_percent")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top_recycling["country"],
    top_recycling["recycling_rate_percent"]
)
ax.set_xlabel("Documented Collection Rate (%)")
ax.set_ylabel("Country")
ax.set_title("Top 10 Documented Collection Rates")
st.pyplot(fig)
plt.close(fig)

# Country search
st.subheader("Explore Individual Countries")

selected_country = st.selectbox(
    "Select a country",
    sorted(df["country"].dropna().unique())
)

country_data = df[df["country"] == selected_country]

st.dataframe(
    country_data[
        [
            "country",
            "ewaste_generated_million_kg_2022",
            "ewaste_generated_kg_per_capita_2022",
            "ewaste_documented_collected_million_kg_2022",
            "recycling_rate_percent",
            "validation_status"
        ]
    ],
    width="stretch",
    hide_index=True
)

# Country Comparison
st.markdown("---")
st.subheader("Compare Two Countries")

country_list = sorted(df["country"].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    country1 = st.selectbox(
        "Select First Country",
        country_list,
        index=country_list.index("India"),
        key="country1"
    )

with col2:
    country2 = st.selectbox(
        "Select Second Country",
        country_list,
        index=country_list.index("China"),
        key="country2"
    )

comparison_df = df[
    df["country"].isin([country1, country2])
][
    [
        "country",
        "ewaste_generated_million_kg_2022",
        "ewaste_generated_kg_per_capita_2022",
        "recycling_rate_percent"
    ]
]

st.dataframe(
    comparison_df,
    width="stretch",
    hide_index=True
)
st.subheader("Download Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Cleaned E-Waste Dataset",
    data=csv,
    file_name="ewaste_cleaned.csv",
    mime="text/csv"
)

# Data table
with st.expander("View Complete Dataset"):
    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

st.markdown("---")
st.caption(
    "Source: Global E-waste Monitor 2024 | Data year: 2022. "
    "Collection figures represent documented collection, "
    "not necessarily verified final recycling."
)
