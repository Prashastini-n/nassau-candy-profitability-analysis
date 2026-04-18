import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Profitability Intelligence",
    layout="wide"
)

st.title("Nassau Candy Profitability Intelligence Dashboard")
st.caption("Interactive analytics platform for product profitability and margin diagnostics.")

st.markdown("---")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv(r"data\cleaned_data.csv")

# Create calculated metrics
df["Margin"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")

division_filter = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

product_filter = st.sidebar.multiselect(
    "Select Product",
    df["Product Name"].unique(),
    default=df["Product Name"].unique()
)

margin_filter = st.sidebar.slider(
    "Minimum Margin %",
    0,
    100,
    0
)

# Margin Risk Threshold
margin_threshold = st.sidebar.slider(
    "Margin Risk Threshold (%)",
    min_value=0,
    max_value=50,
    value=15
)

filtered_df = df[
    (df["Division"].isin(division_filter)) &
    (df["Product Name"].isin(product_filter)) &
    (df["Margin"] >= margin_filter)
]

# ---------------------------------------------------
# NAVIGATION MENU
# ---------------------------------------------------

with st.sidebar:

    selected = option_menu(
        "Analytics Modules",
        [
            "Executive Overview",
            "Product Profitability",
            "Division Performance",
            "Cost Diagnostics",
            "Profit Concentration",
            "Division Distribution",
            "Margin Volatility",
            "Factory Distribution Map"
        ],
        icons=[
            "speedometer",
            "bar-chart",
            "building",
            "gear",
            "graph-up",
            "pie-chart",
            "activity",
            "geo-alt"
        ],
        menu_icon="cast",
        default_index=0
    )

# ---------------------------------------------------
# CHART STYLE FUNCTION
# ---------------------------------------------------

def style_chart(fig):

    fig.update_layout(
        template="plotly_white",
        title_font_size=20,
        title_x=0.02,
        margin=dict(l=20,r=20,t=40,b=20)
    )

    return fig


# ---------------------------------------------------
# EXECUTIVE OVERVIEW
# ---------------------------------------------------

if selected == "Executive Overview":

    st.subheader("Executive Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.0f}")
    col2.metric("Total Profit", f"${filtered_df['Gross Profit'].sum():,.0f}")
    col3.metric("Average Margin", f"{filtered_df['Margin'].mean():.2f}%")
    col4.metric("Total Products", filtered_df["Product Name"].nunique())

    style_metric_cards()


# ---------------------------------------------------
# PRODUCT PROFITABILITY
# ---------------------------------------------------

elif selected == "Product Profitability":

    st.subheader("Top Products by Profit")

    profit_rank = (
        filtered_df
        .groupby("Product Name")[["Sales","Gross Profit","Margin"]]
        .sum()
        .sort_values("Gross Profit",ascending=False)
        .reset_index()
    )

    fig = px.bar(
        profit_rank,
        x="Product Name",
        y="Gross Profit",
        color="Margin"
    )

    fig = style_chart(fig)

    st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# DIVISION PERFORMANCE
# ---------------------------------------------------

elif selected == "Division Performance":

    st.subheader("Division Revenue vs Profit")

    division_perf = (
        filtered_df
        .groupby("Division")[["Sales","Gross Profit"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        division_perf,
        x="Division",
        y=["Sales","Gross Profit"],
        barmode="group"
    )

    fig = style_chart(fig)

    st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# COST DIAGNOSTICS
# ---------------------------------------------------

elif selected == "Cost Diagnostics":

    st.subheader("Cost vs Sales Diagnostics")

    fig = px.scatter(
        filtered_df,
        x="Cost",
        y="Sales",
        size="Gross Profit",
        color="Division",
        hover_name="Product Name"
    )

    fig = style_chart(fig)

    st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# PROFIT CONCENTRATION
# ---------------------------------------------------

elif selected == "Profit Concentration":

    st.subheader("Profit Contribution (Pareto Analysis)")

    pareto = (
        filtered_df
        .groupby("Product Name")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    pareto_df = pareto.reset_index()

    pareto_df["Cumulative Profit"] = pareto_df["Gross Profit"].cumsum()
    pareto_df["Cumulative %"] = (
        100 * pareto_df["Cumulative Profit"] /
        pareto_df["Gross Profit"].sum()
    )

    fig = px.line(
        pareto_df,
        x="Product Name",
        y="Cumulative %"
    )

    fig = style_chart(fig)

    st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# DIVISION DISTRIBUTION
# ---------------------------------------------------

elif selected == "Division Distribution":

    st.subheader("Sales Distribution by Division")

    division_sales = (
        filtered_df
        .groupby("Division")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        division_sales,
        names="Division",
        values="Sales"
    )

    fig = style_chart(fig)

    st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# MARGIN VOLATILITY
# ---------------------------------------------------

elif selected == "Margin Volatility":

    st.subheader("Margin Volatility by Product")

    volatility = (
        filtered_df
        .groupby("Product Name")["Margin"]
        .std()
        .reset_index()
    )

    volatility.columns = ["Product Name","Margin Volatility"]

    fig = px.bar(
        volatility,
        x="Product Name",
        y="Margin Volatility",
        color="Margin Volatility"
    )

    fig = style_chart(fig)

    st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# FACTORY DISTRIBUTION MAP
# ---------------------------------------------------

elif selected == "Factory Distribution Map":

    st.write(
    "Manufacturing facilities supplying Nassau Candy are distributed across multiple geographic regions in the United States."
    )

    st.subheader("Factory Distribution Network")

    factory_data = pd.DataFrame({
        "Factory": [
            "Lot's O' Nuts",
            "Wicked Choccy's",
            "Sugar Shack",
            "Secret Factory",
            "The Other Factory"
        ],
        "Latitude": [
            32.881893,
            32.076176,
            48.11914,
            41.446333,
            35.1175
        ],
        "Longitude": [
            -111.768036,
            -81.088371,
            -96.18115,
            -90.565487,
            -89.971107
        ]
    })

    fig5 = px.scatter_mapbox(
        factory_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="Factory",
        zoom=3,
        height=500
    )

    fig5.update_traces(marker=dict(size=14, color="#2F5597"))

    fig5.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":40,"l":0,"b":0},
        title="Manufacturing Facilities Supplying Nassau Candy Distributor"
    )

    st.plotly_chart(fig5, use_container_width=True)
