# # dashboard.py

# import streamlit as st
# import pandas as pd
# import altair as alt
# import mysql.connector
# import configparser
# import traceback

# # --- Load MySQL Config from config.ini ---
# config = configparser.ConfigParser()
# config.read('config.ini')

# db_config = {
#     'host': config.get('mysql', 'host'),
#     'port': config.getint('mysql', 'port'),
#     'user': config.get('mysql', 'user'),
#     'password': config.get('mysql', 'password'),
#     'database': config.get('mysql', 'database')
# }

# # --- Streamlit Setup ---
# st.set_page_config(page_title="Global Healthcare Dashboard", layout="wide")

# # --- Custom Styling ---
# st.markdown("""
#     <style>
#         .main { background-color: #f8f9fa; }
#         .stButton>button { background-color: #4CAF50; color: white; }
#         .stSlider > div > div { padding-top: 10px; }
#         .block-container { padding: 2rem 1rem; }
#         h1, h2, h3 { color: #0a5275; }
#     </style>
# """, unsafe_allow_html=True)

# st.title("Global Healthcare Data Dashboard")
# st.markdown("Visualize COVID-19 cases and vaccination trends for selected countries.")
# st.markdown("---")

# # --- Sidebar Filters ---
# st.sidebar.header("Filter Options")

# country_list = ["India", "USA", "Brazil", "Germany"]
# country = st.sidebar.selectbox("Country", country_list)
# metric_type = st.sidebar.radio("Metric Type", ["Cases", "Vaccinations"])
# n_days = st.sidebar.slider("Last N Days", min_value=5, max_value=60, value=14)
# st.sidebar.markdown("---")
# st.sidebar.subheader("Visualization Type")
# chart_type = st.sidebar.selectbox("Chart", ["Line Chart", "Bar Chart", "Area Chart"])

# # --- Determine Metric and Query ---
# if metric_type == "Cases":
#     metric = st.sidebar.selectbox("Case Metric", [
#         "total_cases", "new_cases", "total_deaths", "new_deaths"
#     ])
#     query = f"""
#         SELECT report_date, {metric}
#         FROM daily_cases
#         WHERE country_name = %s
#         ORDER BY report_date DESC
#         LIMIT %s
#     """
# else:
#     metric = st.sidebar.selectbox("Vaccination Metric", [
#         "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"
#     ])
#     query = f"""
#         SELECT report_date, {metric}
#         FROM vaccination_data
#         WHERE country_name = %s
#         ORDER BY report_date DESC
#         LIMIT %s
#     """

# # --- Execute Query ---
# try:
#     st.info("Connecting to the database...")
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     cursor.execute(query, (country, n_days))
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     st.success("Data loaded successfully.")
# except Exception as e:
#     st.error("Error occurred while fetching data:")
#     st.code(traceback.format_exc())
#     st.stop()

# # --- Handle Empty Result ---
# if not rows:
#     st.warning("No data available for the selected options.")
#     st.stop()

# # --- Create DataFrame ---
# df = pd.DataFrame(rows, columns=["Date", metric])
# df["Date"] = pd.to_datetime(df["Date"])
# df = df.sort_values("Date")

# # --- Summary Metrics ---
# col1, col2, col3 = st.columns(3)
# col1.metric("Start Date", df["Date"].min().strftime('%Y-%m-%d'))
# col2.metric("End Date", df["Date"].max().strftime('%Y-%m-%d'))
# col3.metric(f"Avg {metric.replace('_', ' ').title()}", f"{df[metric].mean():,.2f}")

# # --- Chart Section ---
# st.subheader(f"{metric.replace('_', ' ').title()} in {country}")

# if chart_type == "Line Chart":
#     chart = alt.Chart(df).mark_line(point=True).encode(
#         x=alt.X("Date:T", title="Date"),
#         y=alt.Y(f"{metric}:Q", title=metric.replace('_', ' ').title()),
#         tooltip=["Date", metric]
#     )
# elif chart_type == "Bar Chart":
#     chart = alt.Chart(df).mark_bar().encode(
#         x=alt.X("Date:T", title="Date"),
#         y=alt.Y(f"{metric}:Q", title=metric.replace('_', ' ').title()),
#         tooltip=["Date", metric]
#     )
# elif chart_type == "Area Chart":
#     chart = alt.Chart(df).mark_area(opacity=0.5).encode(
#         x=alt.X("Date:T", title="Date"),
#         y=alt.Y(f"{metric}:Q", title=metric.replace('_', ' ').title()),
#         tooltip=["Date", metric]
#     )

# st.altair_chart(chart.properties(width="container", height=400), use_container_width=True)

# # --- Raw Data ---
# with st.expander("View Raw Data"):
#     st.dataframe(df.style.format({metric: '{:,.0f}'}), use_container_width=True)

# # --- CSV Download ---
# st.download_button("Download CSV", data=df.to_csv(index=False), file_name="healthcare_data.csv", mime="text/csv")







import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import mysql.connector
import configparser
import traceback

# --- Load MySQL Config from config.ini ---
config = configparser.ConfigParser()
config.read('config.ini')

db_config = {
    'host': config.get('mysql', 'host'),
    'port': config.getint('mysql', 'port'),
    'user': config.get('mysql', 'user'),
    'password': config.get('mysql', 'password'),
    'database': config.get('mysql', 'database')
}

# --- Streamlit Setup ---
st.set_page_config(page_title="Global Healthcare Dashboard", layout="wide")
st.title("🌍 Global Healthcare Data Dashboard")
st.markdown("Visualize COVID-19 case and vaccination trends globally.")
st.markdown("---")

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")
country_list = [
    "Australia", "Brazil", "Canada", "China", "France",
    "Germany", "India", "Japan", "Russia", "South Korea", "UK", "USA"
]
selected_countries = st.sidebar.multiselect("Select Countries", country_list, default=["India"])

metric_type = st.sidebar.radio("Metric Type", ["Cases", "Vaccinations"])
n_days = st.sidebar.slider("Last N Days", min_value=5, max_value=60, value=14)

chart_type = st.sidebar.selectbox("Chart", ["Line Chart", "Bar Chart", "Area Chart"])
show_cumulative = st.sidebar.checkbox("Show Cumulative Map (for cases only)", value=True)

# --- Metric Selection ---
if metric_type == "Cases":
    table = "daily_cases"
    metric_column = st.sidebar.selectbox("Case Metric", ["total_cases", "new_cases", "total_deaths", "new_deaths"])
else:
    table = "vaccination_data"
    metric_column = st.sidebar.selectbox("Vaccination Metric", ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"])

# --- Fetch Data ---
def fetch_data(country, table, metric):
    query = f"""
        SELECT report_date, {metric}
        FROM {table}
        WHERE country_name = %s
        ORDER BY report_date DESC
        LIMIT %s
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, (country, n_days))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        df = pd.DataFrame(rows, columns=["Date", metric])
        df["Date"] = pd.to_datetime(df["Date"])
        df["Country"] = country
        return df.sort_values("Date")
    except Exception:
        st.error("❌ Database error while fetching data.")
        st.code(traceback.format_exc())
        return pd.DataFrame()

# --- Load and Combine Data ---
all_data = []
for country in selected_countries:
    df = fetch_data(country, table, metric_column)
    if not df.empty:
        all_data.append(df)

if not all_data:
    st.warning("No data available for selected filters.")
    st.stop()

final_df = pd.concat(all_data)

# --- Visualization ---
st.subheader(f"📊 {metric_column.replace('_', ' ').title()} Over Time")
if chart_type == "Line Chart":
    chart = alt.Chart(final_df).mark_line(point=True).encode(
        x="Date:T",
        y=alt.Y(metric_column, title=metric_column.replace("_", " ").title()),
        color="Country:N",
        tooltip=["Date", metric_column, "Country"]
    )
elif chart_type == "Bar Chart":
    chart = alt.Chart(final_df).mark_bar().encode(
        x="Date:T",
        y=metric_column,
        color="Country:N",
        tooltip=["Date", metric_column, "Country"]
    )
elif chart_type == "Area Chart":
    chart = alt.Chart(final_df).mark_area(opacity=0.5).encode(
        x="Date:T",
        y=metric_column,
        color="Country:N",
        tooltip=["Date", metric_column, "Country"]
    )
st.altair_chart(chart.properties(width="container", height=400), use_container_width=True)

# --- Choropleth Map ---
if metric_type == "Cases" and show_cumulative:
    st.subheader("🗺️ Global Cumulative Summary Map")
    try:
        format_strings = ','.join(['%s'] * len(selected_countries))
        query = f"""
            SELECT country_name, MAX({metric_column}) as total
            FROM {table}
            WHERE country_name IN ({format_strings})
            GROUP BY country_name
        """
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, selected_countries)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        map_df = pd.DataFrame(result, columns=["Country", "Total"])
        map_df["ISO"] = map_df["Country"].map({
            "Australia": "AUS", "Brazil": "BRA", "Canada": "CAN", "China": "CHN", "France": "FRA",
            "Germany": "DEU", "India": "IND", "Japan": "JPN", "Russia": "RUS",
            "South Korea": "KOR", "UK": "GBR", "USA": "USA"
        })

        fig = px.choropleth(map_df, locations="ISO", color="Total", hover_name="Country",
                            color_continuous_scale="Blues", locationmode="ISO-3")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Failed to load summary map.")
        st.code(traceback.format_exc())

# --- Summary Stats ---
st.subheader("📋 Summary Statistics")
summary = final_df.groupby("Country")[metric_column].agg(["min", "max", "mean"]).reset_index()

# Convert to numeric (safe conversion)
for col in ["min", "max", "mean"]:
    summary[col] = pd.to_numeric(summary[col], errors="coerce")

# Display
st.dataframe(summary.style.format({"min": "{:.2f}", "max": "{:.2f}", "mean": "{:.2f}"}))

# --- Download Button ---
st.download_button("📥 Download CSV", data=final_df.to_csv(index=False), file_name="healthcare_dashboard.csv", mime="text/csv")

# --- Raw Data Table ---
with st.expander("🔍 View Raw Data"):
    st.dataframe(final_df)
