import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# LIGHT THEME AND PROFESSIONAL STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #f6f8fc; color: #172033; }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e7ebf2;
    }
    .block-container { padding-top: 1.7rem; max-width: 1500px; }
    h1, h2, h3 { color: #172033; }
    .subtitle { color: #64748b; font-size: 0.98rem; margin-top: -10px; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e7ebf2;
        padding: 17px; border-radius: 13px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }
    div[data-testid="stMetricLabel"] { color: #64748b; font-weight: 600; }
    div[data-testid="stMetricValue"] { color: #172033; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# Use a consistent Seaborn style for all charts
sns.set_theme(style="whitegrid", context="notebook")

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def money(value):
    return f"₹{value:,.0f}"

def load_data(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
    else:
        file_path = Path(__file__).parent / "Ecommerce_Sales_Dataset.xlsx"
        if not file_path.exists():
            return None
        data = pd.read_excel(file_path)

    for column in ["Order Date", "Ship Date"]:
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], errors="coerce")
    return data

def prepare_chart_data(data, x_field, y_field, aggregation):
    """Group data for charts such as bar, line, area and pie."""
    if aggregation == "Count" or y_field is None:
        result = data.groupby(x_field, dropna=False).size().reset_index(name="Count")
        return result, "Count"

    if aggregation == "Average":
        result = data.groupby(x_field, dropna=False)[y_field].mean().reset_index()
    elif aggregation == "Minimum":
        result = data.groupby(x_field, dropna=False)[y_field].min().reset_index()
    elif aggregation == "Maximum":
        result = data.groupby(x_field, dropna=False)[y_field].max().reset_index()
    else:
        result = data.groupby(x_field, dropna=False)[y_field].sum().reset_index()

    return result, y_field

def make_chart(data, chart_type, x_field, y_field, aggregation,
               group_field, chart_title):
    """Create one Matplotlib/Seaborn chart and return its figure."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    plot_data = data.copy()

    if chart_type in ["Bar", "Line", "Area", "Pie"]:
        chart_data, value_field = prepare_chart_data(
            plot_data, x_field, y_field, aggregation
        )

        if chart_type == "Bar":
            sns.barplot(
                data=chart_data, x=x_field, y=value_field,
                hue=x_field if group_field == x_field else (
                    group_field if group_field in chart_data.columns else None
                ),
                ax=ax, palette="Blues", legend=False
            )
            ax.tick_params(axis="x", rotation=25)

        elif chart_type == "Line":
            sns.lineplot(
                data=chart_data, x=x_field, y=value_field,
                marker="o", color="#2878B5", ax=ax
            )
            ax.tick_params(axis="x", rotation=25)

        elif chart_type == "Area":
            # Matplotlib area chart
            x_values = range(len(chart_data))
            ax.fill_between(
                x_values, chart_data[value_field],
                color="#8DBCE6", alpha=0.55
            )
            ax.plot(x_values, chart_data[value_field],
                    color="#2878B5", marker="o")
            ax.set_xticks(list(x_values))
            ax.set_xticklabels(chart_data[x_field].astype(str), rotation=25, ha="right")

        elif chart_type == "Pie":
            pie_data = chart_data[chart_data[value_field] > 0]
            if pie_data.empty:
                ax.text(0.5, 0.5, "No positive values to display",
                        ha="center", va="center")
            else:
                ax.pie(
                    pie_data[value_field],
                    labels=pie_data[x_field].astype(str),
                    autopct="%1.1f%%",
                    startangle=90,
                    wedgeprops={"edgecolor": "white", "linewidth": 1}
                )
                ax.axis("equal")

    elif chart_type == "Histogram":
        sns.histplot(
            data=plot_data, x=x_field,
            bins=25, kde=True, color="#4C91C6", ax=ax
        )

    elif chart_type == "Scatter":
        if not y_field:
            raise ValueError("Select a numeric Y-axis field for a scatter plot.")
        sns.scatterplot(
            data=plot_data, x=x_field, y=y_field,
            hue=group_field if group_field and group_field != "None" else None,
            alpha=0.75, ax=ax
        )

    elif chart_type == "Box":
        if y_field:
            sns.boxplot(
                data=plot_data, x=x_field, y=y_field,
                hue=group_field if group_field and group_field != "None" else None,
                ax=ax
            )
        else:
            sns.boxplot(data=plot_data, y=x_field, color="#8DBCE6", ax=ax)

    elif chart_type == "Heatmap":
        if not y_field:
            raise ValueError("Select a numeric Y-axis field for a heatmap.")
        if not group_field or group_field == "None":
            raise ValueError("Choose a grouping field for the heatmap.")
        heat_data = plot_data.pivot_table(
            index=x_field, columns=group_field,
            values=y_field, aggfunc="mean", observed=False
        )
        sns.heatmap(
            heat_data, annot=True, fmt=".1f",
            cmap="Blues", linewidths=0.5, ax=ax
        )

    ax.set_title(chart_title, fontsize=15, fontweight="bold", pad=15)
    if chart_type not in ["Pie", "Heatmap"]:
        ax.set_xlabel(x_field, fontsize=11)
        if chart_type in ["Bar", "Line", "Area"]:
            ax.set_ylabel(value_field, fontsize=11)
        elif chart_type == "Histogram":
            ax.set_ylabel("Number of records", fontsize=11)
        elif y_field:
            ax.set_ylabel(y_field, fontsize=11)

    fig.tight_layout()
    return fig

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📊 E-Commerce Sales Analytics")
st.markdown(
    '<p class="subtitle">Explore sales, profit, customers and order performance '
    'through interactive filters and visual reports.</p>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------
with st.sidebar:
    st.header("Dashboard Controls")
    st.caption("Upload your own Excel or CSV file, or use the included sales dataset.")
    uploaded_file = st.file_uploader(
        "Upload sales dataset",
        type=["xlsx", "xls", "csv"]
    )

try:
    df = load_data(uploaded_file)
except Exception as error:
    st.error(f"Unable to read the file: {error}")
    st.stop()

if df is None:
    st.info(
        "Upload an Excel/CSV file in the sidebar, or place "
        "`Ecommerce_Sales_Dataset.xlsx` in the same folder as app.py."
    )
    st.stop()

if df.empty:
    st.error("The uploaded dataset is empty.")
    st.stop()

all_columns = df.columns.tolist()
numeric_columns = df.select_dtypes(include="number").columns.tolist()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
with st.sidebar:
    st.divider()
    st.subheader("Filter Your Data")
    filtered = df.copy()

    if "Order Date" in df.columns and df["Order Date"].notna().any():
        min_date = df["Order Date"].min().date()
        max_date = df["Order Date"].max().date()
        selected_dates = st.date_input(
            "Order date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
            filtered = filtered[
                filtered["Order Date"].dt.date.between(start_date, end_date)
            ]

    filter_fields = [
        "Region", "Category", "Sub-Category", "Customer Segment",
        "Payment Method", "Ship Mode", "Order Status", "State"
    ]

    for field in filter_fields:
        if field in filtered.columns:
            choices = sorted(filtered[field].dropna().astype(str).unique().tolist())
            selected_values = st.multiselect(
                field, choices, default=choices, key=f"filter_{field}"
            )
            if selected_values:
                filtered = filtered[filtered[field].astype(str).isin(selected_values)]
            else:
                filtered = filtered.iloc[0:0]

    st.divider()
    st.caption(f"Showing {len(filtered):,} of {len(df):,} records")

if filtered.empty:
    st.warning("No records match the selected filters. Change your filters and try again.")
    st.stop()

# ---------------------------------------------------------
# KEY PERFORMANCE INDICATORS
# ---------------------------------------------------------
sales_col = "Sales (INR)" if "Sales (INR)" in filtered.columns else None
profit_col = "Profit (INR)" if "Profit (INR)" in filtered.columns else None
quantity_col = "Quantity" if "Quantity" in filtered.columns else None
order_col = "Order ID" if "Order ID" in filtered.columns else None

total_sales = filtered[sales_col].sum() if sales_col else 0
total_profit = filtered[profit_col].sum() if profit_col else 0
total_quantity = filtered[quantity_col].sum() if quantity_col else 0
total_orders = filtered[order_col].nunique() if order_col else len(filtered)
average_order_value = total_sales / total_orders if total_orders else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

st.subheader("Key Performance Indicators")
st.caption("These values automatically update when you change the sidebar filters.")

k1, k2, k3 = st.columns(3)
k4, k5, k6 = st.columns(3)

k1.metric("Total Sales", money(total_sales))
k2.metric("Total Profit", money(total_profit))
k3.metric("Total Orders", f"{total_orders:,}")
k4.metric("Quantity Sold", f"{total_quantity:,.0f}")
k5.metric("Average Order Value", money(average_order_value))
k6.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# ---------------------------------------------------------
# SALES OVERVIEW CHARTS
# ---------------------------------------------------------
st.subheader("Sales Overview")
tab1, tab2, tab3 = st.tabs(
    ["Category Performance", "Monthly Sales Trend", "Regional Performance"]
)

with tab1:
    if "Category" in filtered.columns and sales_col:
        category_data = filtered.groupby("Category", as_index=False)[sales_col].sum()
        fig, ax = plt.subplots(figsize=(9, 4.8))
        sns.barplot(data=category_data, x="Category", y=sales_col,
                    color="#5B9BD5", ax=ax)
        ax.set_title("Total Sales by Category", fontsize=15, fontweight="bold")
        ax.set_xlabel("Product Category")
        ax.set_ylabel("Sales (INR)")
        ax.tick_params(axis="x", rotation=15)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("Category and Sales columns are required for this chart.")

with tab2:
    if "Order Date" in filtered.columns and sales_col:
        monthly = filtered.dropna(subset=["Order Date"]).copy()
        monthly["Month"] = monthly["Order Date"].dt.to_period("M").astype(str)
        monthly_data = monthly.groupby("Month", as_index=False)[sales_col].sum()
        fig, ax = plt.subplots(figsize=(9, 4.8))
        sns.lineplot(data=monthly_data, x="Month", y=sales_col,
                     marker="o", color="#2878B5", linewidth=2.5, ax=ax)
        ax.set_title("Monthly Sales Trend", fontsize=15, fontweight="bold")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales (INR)")
        ax.tick_params(axis="x", rotation=35)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("Order Date and Sales columns are required for this chart.")

with tab3:
    if "Region" in filtered.columns and sales_col:
        region_data = filtered.groupby("Region", as_index=False)[sales_col].sum()
        fig, ax = plt.subplots(figsize=(9, 4.8))
        sns.barplot(data=region_data, x="Region", y=sales_col,
                    color="#76B7A5", ax=ax)
        ax.set_title("Total Sales by Region", fontsize=15, fontweight="bold")
        ax.set_xlabel("Region")
        ax.set_ylabel("Sales (INR)")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("Region and Sales columns are required for this chart.")

st.divider()

# ---------------------------------------------------------
# CUSTOM VISUALIZATION BUILDER
# ---------------------------------------------------------
st.subheader("Custom Visualization Builder")
st.caption(
    "Select multiple chart types, choose the fields and aggregation, "
    "then create your own charts."
)

chart_types = [
    "Bar", "Line", "Pie", "Histogram",
    "Scatter", "Area", "Box", "Heatmap"
]
selected_chart_types = st.multiselect(
    "1. Select one or more chart types",
    chart_types,
    default=["Bar", "Line"]
)

if selected_chart_types:
    for chart_type in selected_chart_types:
        with st.expander(f"Configure {chart_type} chart", expanded=(chart_type == selected_chart_types[0])):
            col1, col2, col3 = st.columns(3)

            default_x = "Order Date" if "Order Date" in all_columns else all_columns[0]
            with col1:
                x_field = st.selectbox(
                    "X-axis / Category",
                    all_columns,
                    index=all_columns.index(default_x),
                    key=f"x_{chart_type}"
                )

            with col2:
                y_options = ["Count of records"] + numeric_columns
                default_y = sales_col if sales_col else (
                    numeric_columns[0] if numeric_columns else "Count of records"
                )
                y_choice = st.selectbox(
                    "Y-axis / Numeric value",
                    y_options,
                    index=y_options.index(default_y),
                    key=f"y_{chart_type}"
                )
                y_field = None if y_choice == "Count of records" else y_choice

            with col3:
                group_options = ["None"] + all_columns
                group_field = st.selectbox(
                    "Color / Group / Heatmap columns",
                    group_options,
                    key=f"group_{chart_type}"
                )
                if group_field == "None":
                    group_field = None

            aggregation = st.selectbox(
                "Aggregation",
                ["Sum", "Average", "Count", "Minimum", "Maximum"],
                key=f"aggregation_{chart_type}",
                disabled=chart_type in ["Histogram", "Scatter", "Box", "Heatmap"]
            )

            default_title = f"{chart_type} chart - {y_field or 'Record Count'} by {x_field}"
            chart_title = st.text_input(
                "Chart title", value=default_title, key=f"title_{chart_type}"
            )

            if st.button(f"Generate {chart_type} chart", key=f"generate_{chart_type}"):
                try:
                    if chart_type in ["Scatter", "Heatmap"] and y_field is None:
                        st.error(f"{chart_type} requires a numeric Y-axis field.")
                    elif chart_type == "Heatmap" and group_field is None:
                        st.error("For a heatmap, select a field for the heatmap columns.")
                    else:
                        fig = make_chart(
                            filtered, chart_type, x_field, y_field,
                            aggregation, group_field, chart_title
                        )
                        st.pyplot(fig, use_container_width=True)
                        plt.close(fig)
                except Exception as error:
                    st.error(f"Could not generate this chart: {error}")
else:
    st.info("Choose at least one chart type to configure a visualization.")

st.divider()

# ---------------------------------------------------------
# DATA EXPLORER
# ---------------------------------------------------------
st.subheader("Data Explorer")
data_tab1, data_tab2, data_tab3 = st.tabs(
    ["Filtered Data", "Statistical Summary", "Data Quality"]
)

with data_tab1:
    st.dataframe(filtered, use_container_width=True, height=350)
    csv_file = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_file,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

with data_tab2:
    if numeric_columns:
        st.dataframe(filtered[numeric_columns].describe().T, use_container_width=True)
    else:
        st.info("No numeric columns are available.")

with data_tab3:
    quality_report = pd.DataFrame({
        "Column": filtered.columns,
        "Missing Values": filtered.isnull().sum().values,
        "Missing (%)": (filtered.isnull().mean().values * 100).round(2),
        "Data Type": filtered.dtypes.astype(str).values
    })
    st.dataframe(quality_report, use_container_width=True, hide_index=True)

st.caption("Built with Python, Streamlit, Pandas, Matplotlib and Seaborn.")
