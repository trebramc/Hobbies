import streamlit as st
import pandas as pd
from PIL import Image
import io
from datetime import date

# -------------------------
# Initialize Session State
# -------------------------
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=[
        "Item Name","Series","Purchase Date","Purchase Price",
        "Resale Price","Status","Image","Selling Date"
    ])
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None
if "page" not in st.session_state:
    st.session_state.page = 0

ITEMS_PER_PAGE = 10

# -------------------------
# Function to display inventory
# -------------------------
def display_inventory():
    if st.session_state.inventory.empty:
        st.info("No items in inventory. Add items in the 'Add Item' tab.")
        return

    # --- Sorting / Filtering ---
    st.subheader("Filter / Sort Inventory")
    view_by = st.selectbox(
        "View by",
        ["Default", "Series", "Purchase Date (latest)", "Purchase Price", "Status"]
    )

    df_display = st.session_state.inventory.copy()

    if view_by == "Series":
        df_display = df_display.sort_values("Series")
    elif view_by == "Purchase Date (latest)":
        df_display = df_display.sort_values("Purchase Date", ascending=False)
    elif view_by == "Purchase Price":
        df_display = df_display.sort_values("Purchase Price", ascending=False)
    elif view_by == "Status":
        df_display = df_display.sort_values("Status")

    # --- Pagination ---
    total_pages = (len(df_display) - 1) // ITEMS_PER_PAGE + 1
    start_idx = st.session_state.page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    df_page = df_display.iloc[start_idx:end_idx]

    st.subheader(f"Minifigures (Page {st.session_state.page + 1} of {total_pages})")
    cols = st.columns(4)

    for i, (idx, row) in enumerate(df_page.iterrows()):
        with cols[i % 4]:
            # SELECT BUTTON (restore details)
            if st.button(row["Item Name"], key=f"select_{idx}", use_container_width=True):
                st.session_state.selected_item = idx

            # Image preview
            if row["Image"] is not None and not (isinstance(row["Image"], float) and pd.isna(row["Image"])):
                st.image(io.BytesIO(row["Image"]), width=120)
            else:
                st.caption("No Image")

            # REMOVE BUTTON
            if st.button("❌ Remove", key=f"remove_{idx}"):
                st.session_state.inventory = st.session_state.inventory.drop(idx).reset_index(drop=True)
                st.session_state.selected_item = None
                st.rerun()

    # --- Pagination Controls ---
    col_prev, col_next = st.columns(2)
    if col_prev.button("⬅ Previous") and st.session_state.page > 0:
        st.session_state.page -= 1
    if col_next.button("Next ➡") and st.session_state.page < total_pages - 1:
        st.session_state.page += 1

    # -------------------------
    # Selected Item Details
    # -------------------------
    if st.session_state.selected_item is not None:
        idx = st.session_state.selected_item
        if idx >= len(st.session_state.inventory):
            st.session_state.selected_item = None
            return
        item = st.session_state.inventory.loc[idx]

        st.divider()
        st.subheader(f"Details: {item['Item Name']}")

        # --- Editable Image ---
        st.subheader("🖼 Update Image")
        uploaded_image = st.file_uploader(
            "Upload or replace image",
            type=["png", "jpg", "jpeg"],
            key=f"image_upload_{idx}"
        )
        if uploaded_image is not None:
            img_bytes = uploaded_image.read()
            st.session_state.inventory.at[idx, "Image"] = img_bytes
            st.success("✅ Image updated successfully!")

        # Show current image
        if item["Image"] is not None and not (isinstance(item["Image"], float) and pd.isna(item["Image"])):
            st.image(Image.open(io.BytesIO(item["Image"])), width=220)
        else:
            st.caption("No image available")

        # --- Editable Series ---
        new_series = st.text_input(
            "Series",
            value=item["Series"],
            key=f"series_{idx}"
        )
        st.session_state.inventory.at[idx, "Series"] = new_series

        # --- Editable Purchase Date ---
        new_purchase_date = st.date_input(
            "Purchase Date",
            value=item["Purchase Date"],
            key=f"purchase_date_{idx}"
        )
        st.session_state.inventory.at[idx, "Purchase Date"] = new_purchase_date

        # --- Editable Purchase Price ---
        new_purchase_price = st.number_input(
            "Purchase Price",
            value=float(item["Purchase Price"]),
            step=0.01,
            key=f"purchase_price_{idx}"
        )
        st.session_state.inventory.at[idx, "Purchase Price"] = new_purchase_price

        # --- Editable Resale Price ---
        new_resale = st.number_input(
            "Resale Price",
            value=float(item["Resale Price"]),
            step=0.01,
            key=f"resale_{idx}"
        )
        st.session_state.inventory.at[idx, "Resale Price"] = new_resale

        # --- Editable Status ---
        new_status = st.selectbox(
            "Status",
            ["Available", "Sold"],
            index=0 if item["Status"] == "Available" else 1,
            key=f"status_{idx}"
        )
        if new_status != item["Status"]:
            st.session_state.inventory.at[idx, "Status"] = new_status
            if new_status == "Sold" and pd.isna(item["Selling Date"]):
                st.session_state.inventory.at[idx, "Selling Date"] = date.today()

        # --- Editable Selling Date ---
        current_selling_date = item["Selling Date"]
        default_selling_date = date.today() if pd.isna(current_selling_date) else current_selling_date

        new_selling_date = st.date_input(
            "Selling Date",
            value=default_selling_date,
            key=f"selling_date_{idx}"
        )
        st.session_state.inventory.at[idx, "Selling Date"] = new_selling_date
        st.write(f"**Selling Date:** {new_selling_date}")

# -------------------------
# Tabs
# -------------------------
st.title("LEGO Minifigure Inventory Manager")
tab1, tab2, tab3 = st.tabs(["🧱Inventory Tracker", "➕Add Item", "📊 Analytics"])

# =========================
# TAB 2: Add Item
# =========================
with tab2:
    st.header("➕ Add Item")

    # --- Initialize session state for inputs if not already ---
    for key in ["name_input", "series_input", "purchase_date_input",
                "purchase_price_input", "resale_price_input", "status_input", "image_input"]:
        if key not in st.session_state:
            if key == "status_input":
                st.session_state[key] = "Available"
            elif key == "purchase_date_input":
                st.session_state[key] = date.today()
            elif key in ["purchase_price_input", "resale_price_input"]:
                st.session_state[key] = 0.0
            else:
                st.session_state[key] = ""

    # --- Manual Add Form ---
    with st.form("add_item_form"):
        st.session_state.name_input = st.text_input("Item Name", value=st.session_state.name_input)
        st.session_state.series_input = st.text_input("Series", value=st.session_state.series_input)
        st.session_state.purchase_date_input = st.date_input("Purchase Date", value=st.session_state.purchase_date_input)
        st.session_state.purchase_price_input = st.number_input(
            "Purchase Price", min_value=0.0, step=0.01, value=st.session_state.purchase_price_input
        )
        st.session_state.resale_price_input = st.number_input(
            "Resale Price", min_value=0.0, step=0.01, value=st.session_state.resale_price_input
        )
        st.session_state.status_input = st.selectbox(
            "Status", ["Available", "Sold"], index=0 if st.session_state.status_input=="Available" else 1
        )
        st.session_state.image_input = st.file_uploader("Upload Thumbnail Image", type=["png","jpg","jpeg"], key="img_uploader")

        submitted = st.form_submit_button("Add Item")

        if submitted:
            img_bytes = st.session_state.image_input.read() if st.session_state.image_input else None
            selling_date = date.today() if st.session_state.status_input=="Sold" else pd.NA

            new_row = {
                "Item Name": st.session_state.name_input,
                "Series": st.session_state.series_input,
                "Purchase Date": st.session_state.purchase_date_input,
                "Purchase Price": st.session_state.purchase_price_input,
                "Resale Price": st.session_state.resale_price_input,
                "Status": st.session_state.status_input,
                "Image": img_bytes,
                "Selling Date": selling_date
            }

            # Append to inventory
            st.session_state.inventory = pd.concat(
                [st.session_state.inventory, pd.DataFrame([new_row])],
                ignore_index=True
            )

            # --- SUCCESS MESSAGE ---
            st.success(f"✅ '{st.session_state.name_input}' added to inventory!")

            # --- RESET INPUTS ---
            st.session_state.name_input = ""
            st.session_state.series_input = ""
            st.session_state.purchase_date_input = date.today()
            st.session_state.purchase_price_input = 0.0
            st.session_state.resale_price_input = 0.0
            st.session_state.status_input = "Available"
            st.session_state.image_input = None
            
    # =========================
    # BULK UPLOAD (INSIDE TAB 2)
    # =========================
    st.divider()
    st.subheader("📂 Bulk Upload (CSV – No Images)")

    st.caption(
        """
        **Required CSV columns:**
        - Item Name
        - Series
        - Purchase Date (YYYY-MM-DD)
        - Purchase Price
        - Resale Price
        - Status (Available / Sold)
        """
    )

    csv_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        key="bulk_csv"
    )

    if csv_file is not None:
        try:
            df_csv = pd.read_csv(csv_file)

            required_cols = [
                "Item Name",
                "Series",
                "Purchase Date",
                "Purchase Price",
                "Resale Price",
                "Status"
            ]

            missing = [c for c in required_cols if c not in df_csv.columns]
            if missing:
                st.error(f"Missing columns: {', '.join(missing)}")
            else:
                df_csv["Purchase Date"] = pd.to_datetime(df_csv["Purchase Date"]).dt.date
                df_csv["Status"] = df_csv["Status"].str.title()

                df_csv["Selling Date"] = df_csv["Status"].apply(
                    lambda x: date.today() if x == "Sold" else pd.NA
                )

                df_csv["Image"] = None

                df_csv = df_csv[
                    [
                        "Item Name",
                        "Series",
                        "Purchase Date",
                        "Purchase Price",
                        "Resale Price",
                        "Status",
                        "Image",
                        "Selling Date"
                    ]
                ]

                if st.button("✅ Confirm Bulk Add"):
                    st.session_state.inventory = pd.concat(
                        [st.session_state.inventory, df_csv],
                        ignore_index=True
                    )

                    st.success(f"📦 {len(df_csv)} items added successfully!")

                    # ✅ Reset file uploader safely
                    st.rerun()  # use st.rerun() instead of experimental_rerun

        except Exception as e:
            st.error(f"Error reading file: {e}")


# =========================
# TAB 1: Inventory Tracker
# Display inventory AFTER any add
# =========================
with tab1:
    st.header("🧱 Inventory Tracker")
    display_inventory()

# =========================
# TAB 3: Analytics
# =========================
with tab3:
    st.header("📊 Inventory Analytics")

    df = st.session_state.inventory.copy()

    if df.empty:
        st.info("No data yet. Add items to see analytics.")
        st.stop()

    # -------------------------
    # SPLIT DATA
    # -------------------------
    sold_df = df[df["Status"] == "Sold"].copy()
    available_df = df[df["Status"] == "Available"].copy()

    # -------------------------
    # SUMMARY METRICS
    # -------------------------
    total_sales = sold_df["Resale Price"].sum()
    total_expenses = df["Purchase Price"].sum()
    unrealized_sales = available_df["Resale Price"].sum()
    unrealized_profit = unrealized_sales - available_df["Purchase Price"].sum()

    # Total Percent Gain (including unrealized gains)
    total_percent_gain = ((total_sales + unrealized_sales - total_expenses) / total_expenses * 100) if total_expenses > 0 else 0.0

    # -------------------------
    # ROW 1: Total Sales / Expenses / Percent Gain
    # -------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"₱{total_sales:,.2f}")
    col2.metric("📉 Total Expenses", f"₱{total_expenses:,.2f}")
    col3.metric("📈 Total Percent Gain", f"{total_percent_gain:.2f}%")

    # -------------------------
    # ROW 2: Unrealized Sales / Unrealized Profit
    # -------------------------
    col4, col5 = st.columns(2)
    col4.metric("📦 Unrealized Sales", f"₱{unrealized_sales:,.2f}")
    col5.metric("⏳ Unrealized Profit", f"₱{unrealized_profit:,.2f}")

    st.divider()

    # -------------------------
    # TOP PERFORMING SERIES (ROI)
    # -------------------------
    st.subheader("🏆 Top Performing Series (by % Gain)")

    if sold_df.empty:
        st.warning("No sold items yet.")
    else:
        sold_df["Profit"] = sold_df["Resale Price"] - sold_df["Purchase Price"]

        series_roi = (
            sold_df
            .groupby("Series")
            .agg(
                Total_Cost=("Purchase Price", "sum"),
                Total_Profit=("Profit", "sum")
            )
            .reset_index()
        )

        series_roi["Percent Gain (%)"] = (series_roi["Total_Profit"] / series_roi["Total_Cost"] * 100)
        series_roi = series_roi.sort_values("Percent Gain (%)", ascending=False)

        st.dataframe(
            series_roi.style.format({
                "Total_Cost": "₱{:,.2f}",
                "Total_Profit": "₱{:,.2f}",
                "Percent Gain (%)": "{:.2f}%"
            }),
            use_container_width=True
        )

        st.bar_chart(series_roi.set_index("Series")["Percent Gain (%)"])

    st.divider()

    # -------------------------
    # TOP PERFORMING MINIFIGURES (ROI)
    # -------------------------
    st.subheader("🥇 Top Performing Minifigures (by % Gain)")

    if not sold_df.empty:
        sold_df["Percent Gain (%)"] = ((sold_df["Resale Price"] - sold_df["Purchase Price"]) / sold_df["Purchase Price"] * 100)

        top_figs = (
            sold_df
            .sort_values("Percent Gain (%)", ascending=False)
            [["Item Name", "Series", "Purchase Price", "Resale Price", "Percent Gain (%)"]]
            .head(10)
        )

        st.dataframe(
            top_figs.style.format({
                "Purchase Price": "₱{:,.2f}",
                "Resale Price": "₱{:,.2f}",
                "Percent Gain (%)": "{:.2f}%"
            }),
            use_container_width=True
        )

    st.divider()

    # -------------------------
    # WORST PERFORMING MINIFIGURES (ROI)
    # -------------------------
    st.subheader("📉 Worst Performing Minifigures (by % Gain)")

    if not sold_df.empty:
        # Already has Percent Gain (%) calculated
        worst_figs = (
            sold_df
            .sort_values("Percent Gain (%)", ascending=True)  # lowest (negative) first
            [["Item Name", "Series", "Purchase Price", "Resale Price", "Percent Gain (%)"]]
            .head(10)
        )

        st.dataframe(
            worst_figs.style.format({
                "Purchase Price": "₱{:,.2f}",
                "Resale Price": "₱{:,.2f}",
                "Percent Gain (%)": "{:.2f}%"
            }),
            use_container_width=True
        )
    else:
        st.info("No sold items yet to evaluate worst performers.")

    st.divider()

    # -------------------------
    # CASH FLOW OVER TIME
    # -------------------------
    st.subheader("💸 Cash Flow Over Time")

    cash_out = df[["Purchase Date", "Purchase Price"]].copy()
    cash_out["Amount"] = -cash_out["Purchase Price"]
    cash_out.rename(columns={"Purchase Date": "Date"}, inplace=True)

    cash_in = sold_df[["Selling Date", "Resale Price"]].copy()
    cash_in.rename(columns={"Selling Date": "Date", "Resale Price": "Amount"}, inplace=True)

    cashflow_df = pd.concat([cash_out[["Date", "Amount"]], cash_in])
    cashflow_df["Date"] = pd.to_datetime(cashflow_df["Date"])
    cashflow_df = cashflow_df.sort_values("Date")
    cashflow_df["Cumulative Cash Flow"] = cashflow_df["Amount"].cumsum()

    st.line_chart(cashflow_df.set_index("Date")["Cumulative Cash Flow"])

    st.divider()

    # -------------------------
    # SALES DISTRIBUTION (WHERE MONEY COMES FROM)
    # -------------------------
    st.subheader("📊 Sales Distribution by Series")

    if not sold_df.empty:
        sales_by_series = sold_df.groupby("Series")["Resale Price"].sum()

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.pie(
            sales_by_series,
            labels=sales_by_series.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Revenue Share by Series")
        ax.axis("equal")
        st.pyplot(fig)

    st.divider()

    # -------------------------
    # UNSOLD INVENTORY EXPOSURE
    # -------------------------
    st.subheader("📦 Unsold Inventory Exposure by Series")

    if not available_df.empty:
        unsold_value = (
            available_df
            .groupby("Series")["Resale Price"]
            .sum()
            .sort_values(ascending=False)
        )

        # --- Clean NaNs and remove zero values ---
        unsold_value = unsold_value.dropna()
        unsold_value = unsold_value[unsold_value > 0]

        if unsold_value.empty:
            st.info("No unsold inventory data available for pie chart.")
        else:
            fig, ax = plt.subplots()
            ax.pie(
                unsold_value,
                labels=unsold_value.index,
                autopct="%1.1f%%",
                startangle=90
            )
            ax.set_title("Capital Tied Up in Unsold Inventory")
            ax.axis("equal")
            st.pyplot(fig)
    else:
        st.info("No unsold items in inventory.")
    # -------------------------
    # LOW LIQUIDITY INVENTORY
    # -------------------------
    st.subheader("⏳ Low Liquidity Inventory (Items Held > 1 Year)")

    if not available_df.empty:
        today = pd.to_datetime(date.today())
        available_df["Days in Inventory"] = (today - pd.to_datetime(available_df["Purchase Date"])).dt.days

        # Threshold: items held more than 365 days (1 year)
        low_liquidity_df = available_df[available_df["Days in Inventory"] > 365].copy()

        if low_liquidity_df.empty:
            st.info("No low liquidity items (all items sold or held ≤ 1 year).")
        else:
            st.dataframe(
                low_liquidity_df[["Item Name", "Series", "Purchase Date", "Purchase Price", "Days in Inventory"]]
                .sort_values("Days in Inventory", ascending=False),
                use_container_width=True
            )
    # -------------------------
    # AVAILABLE MINIFIGURES BY SERIES
    # -------------------------
    st.subheader("📦 Available Minifigures by Series")

    if not available_df.empty:
        # Group available items by Series
        series_groups = available_df.groupby("Series")

        for series, group in series_groups:
            st.markdown(f"**Series: {series}**")
            # Display item names and purchase dates
            st.write(
                group[["Item Name", "Purchase Date", "Purchase Price", "Resale Price"]]
                .sort_values("Purchase Date")
                .reset_index(drop=True)
            )
    else:
        st.info("No available minifigures at the moment.")

