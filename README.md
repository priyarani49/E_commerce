# E-Commerce Sales Analytics Dashboard

Interactive Streamlit dashboard built with **Matplotlib and Seaborn** for visualizations.

## Features
- KPI cards: Total Sales, Total Profit, Total Orders, Quantity Sold, Average Order Value and Profit Margin
- Sidebar filters for date, region, category, sub-category, customer segment, payment method, ship mode, order status and state
- Overview charts for category performance, monthly sales and regional performance
- Custom chart builder with Bar, Line, Pie, Histogram, Scatter, Area, Box and Heatmap
- Choose multiple chart types and configure fields separately
- Filtered data explorer, statistical summary, data quality report and CSV export
- Light theme

## Run the app

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run:

   ```bash
   streamlit run app.py
   ```

The included `Ecommerce_Sales_Dataset.xlsx` loads automatically. You can also upload an Excel or CSV file from the sidebar.

## Notes
- Built-in KPI and overview sections use the supplied dataset's column names.
- The custom chart builder uses the columns in the uploaded dataset.
- Visualizations are rendered using Matplotlib and Seaborn (not Plotly).
