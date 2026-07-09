import streamlit as st
import pandas as pd
from datetime import date
import csv
import os
from io import StringIO

st.set_page_config(page_title="Finance Forms", layout="wide")

st.title("Finance Management Forms")

form_type = st.sidebar.selectbox(
    "Select Form",
    ["Cash Receipt Form", "LPO Form", "Expense Entry Form", "Budget Line Form"]
)

st.image("new.png")

# Database file name
DATABASE_FILE = "finance_records.csv"

# Generate fiscal year options from 2024 to 2030
fiscal_years = [str(year) for year in range(2024, 2031)]

# Function to initialize the database file with headers if it doesn't exist
def init_database():
    if not os.path.exists(DATABASE_FILE):
        # Create empty CSV with all possible columns
        df = pd.DataFrame(columns=[
            "Form_Type", "Date", "Description", "RV No", "LPO No", "PV No",
            "Fiscal Year", "Funding Source", "Cost Center", "Currency",
            "Amount", "Exchange Rate", "USD Amount", "Budget Line Item", "Timestamp"
        ])
        df.to_csv(DATABASE_FILE, index=False)

# Function to append data to CSV
def append_to_csv(data):
    # Convert data dictionary to DataFrame
    df_new = pd.DataFrame([data])
    
    # Append to existing CSV or create new one
    if os.path.exists(DATABASE_FILE):
        df_existing = pd.read_csv(DATABASE_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(DATABASE_FILE, index=False)
    else:
        df_new.to_csv(DATABASE_FILE, index=False)

# Function to convert data to CSV for download
def convert_to_csv(data):
    df = pd.DataFrame([data])
    return df.to_csv(index=False).encode('utf-8')

# Function to convert date objects to strings for JSON display
def prepare_data_for_display(data):
    # Create a copy of the data to avoid modifying the original
    display_data = data.copy()
    # Convert date object to string if present
    if 'Date' in display_data and isinstance(display_data['Date'], date):
        display_data['Date'] = display_data['Date'].strftime('%Y-%m-%d')
    return display_data

# Initialize database
init_database()

# Function to show view records button and display records
def show_view_records():
    if st.sidebar.button("📊 View All Records"):
        if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
            df = pd.read_csv(DATABASE_FILE)
            st.session_state.show_records = True
            st.session_state.records_df = df
        else:
            st.sidebar.warning("No records found in database")

# Add view records button to sidebar
show_view_records()

# Display records if requested
if st.session_state.get('show_records', False):
    st.header("📊 All Finance Records")
    st.dataframe(st.session_state.records_df)
    
    # Download all records as CSV
    csv_all = st.session_state.records_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download All Records as CSV",
        data=csv_all,
        file_name=f"all_finance_records_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    if st.button("Close Records"):
        st.session_state.show_records = False
        st.rerun()

# Initialize session state for storing submitted data
if 'submitted_data' not in st.session_state:
    st.session_state.submitted_data = None
if 'show_download' not in st.session_state:
    st.session_state.show_download = False

# -----------------------------
# CASH RECEIPT FORM
# -----------------------------
if form_type == "Cash Receipt Form":

    st.header("Cash Receipt Form")

    with st.form("cash_receipt_form"):
        trans_date = st.date_input("Date", value=date.today())
        description = st.text_area("Description")
        rv_no = st.text_input("RV No.")
        fiscal_year = st.selectbox("Fiscal Year", fiscal_years)
        funding_source = st.text_input("Funding Source")
        currency = st.selectbox("Currency", ["USD", "ZAR", "EUR", "GBP", "KES"])
        amount = st.number_input("Amount", min_value=0.0, value=0.0)
        exchange_rate = st.number_input("Exchange Rate", min_value=0.0001, value=1.0)
        usd_amount = amount / exchange_rate
        st.info(f"USD Amount: {usd_amount:,.2f}")
        
        submit = st.form_submit_button("Save")
        
        if submit:
            # Prepare data for database
            data = {
                "Form_Type": "Cash Receipt",
                "Date": trans_date.strftime('%Y-%m-%d'),  # Convert date to string
                "Description": description,
                "RV No": rv_no,
                "LPO No": "",
                "PV No": "",
                "Fiscal Year": fiscal_year,
                "Funding Source": funding_source,
                "Cost Center": "",
                "Currency": currency,
                "Amount": amount,
                "Exchange Rate": exchange_rate,
                "USD Amount": usd_amount,
                "Budget Line Item": "",
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Append to database
            append_to_csv(data)
            
            # Store data in session state for download
            st.session_state.submitted_data = data
            st.session_state.show_download = True
            
            st.success("Cash Receipt Saved to Database!")
            # Display data with properly formatted date
            st.json(prepare_data_for_display(data))
    
    # Show download button outside the form
    if st.session_state.show_download and st.session_state.submitted_data:
        csv_data = convert_to_csv(st.session_state.submitted_data)
        st.download_button(
            label="📥 Download this record as CSV",
            data=csv_data,
            file_name=f"cash_receipt_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_cash"
        )
        if st.button("Clear", key="clear_cash"):
            st.session_state.show_download = False
            st.session_state.submitted_data = None
            st.rerun()

# -----------------------------
# LPO FORM
# -----------------------------
elif form_type == "LPO Form":

    st.header("LPO Form")

    cost_centers = [
        "CG Office", "PSSPD", "TMD", "CMPA", "PED", "FID", "DCGTA OFFICE",
        "EDQARD", "ERMCD", "MISD", "TPSD", "NRARS", "EDAD", "OPR", "RMS",
        "D1-Office", "LTD"
    ]

    with st.form("lpo_form"):
        trans_date = st.date_input("Date")
        description = st.text_area("Description")
        lpo_no = st.text_input("LPO No.")
        cost_center = st.selectbox("Cost Center", cost_centers)
        fiscal_year = st.selectbox("Fiscal Year", fiscal_years)
        funding_source = st.text_input("Funding Source")
        amount = st.number_input("Amount", min_value=0.0, value=0.0)
        
        submit = st.form_submit_button("Save")
        
        if submit:
            # Prepare data for database
            data = {
                "Form_Type": "LPO",
                "Date": trans_date.strftime('%Y-%m-%d'),  # Convert date to string
                "Description": description,
                "RV No": "",
                "LPO No": lpo_no,
                "PV No": "",
                "Fiscal Year": fiscal_year,
                "Funding Source": funding_source,
                "Cost Center": cost_center,
                "Currency": "",
                "Amount": amount,
                "Exchange Rate": "",
                "USD Amount": "",
                "Budget Line Item": "",
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Append to database
            append_to_csv(data)
            
            # Store data in session state for download
            st.session_state.submitted_data = data
            st.session_state.show_download = True
            
            st.success("LPO Saved to Database!")
            # Display data with properly formatted date
            st.json(prepare_data_for_display(data))
    
    # Show download button outside the form
    if st.session_state.show_download and st.session_state.submitted_data:
        csv_data = convert_to_csv(st.session_state.submitted_data)
        st.download_button(
            label="📥 Download this record as CSV",
            data=csv_data,
            file_name=f"lpo_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_lpo"
        )
        if st.button("Clear", key="clear_lpo"):
            st.session_state.show_download = False
            st.session_state.submitted_data = None
            st.rerun()

# -----------------------------
# EXPENSE ENTRY FORM
# -----------------------------
elif form_type == "Expense Entry Form":

    st.header("Expense Entry Form")

    cost_centers = [
        "CG Office", "PSSPD", "TMD", "CMPA", "PED", "FID", "DCGTA OFFICE",
        "EDQARD", "ERMCD", "MISD", "TPSD", "NRARS", "EDAD", "OPR", "RMS",
        "D1-Office", "LTD"
    ]

    with st.form("expense_form"):
        trans_date = st.date_input("Date")
        description = st.text_area("Description")
        lpo_no = st.text_input("LPO No.")
        pv_no = st.text_input("PV No.")
        cost_center = st.selectbox("Cost Center", cost_centers)
        fiscal_year = st.selectbox("Fiscal Year", fiscal_years)
        funding_source = st.text_input("Funding Source")
        currency = st.selectbox("Currency", ["USD", "ZAR", "EUR", "GBP", "KES"])
        amount = st.number_input("Amount", min_value=0.0, value=0.0)
        exchange_rate = st.number_input("Exchange Rate", min_value=0.0001, value=1.0)
        usd_amount = amount / exchange_rate
        st.info(f"USD Amount: {usd_amount:,.2f}")
        
        submit = st.form_submit_button("Save")
        
        if submit:
            # Prepare data for database
            data = {
                "Form_Type": "Expense Entry",
                "Date": trans_date.strftime('%Y-%m-%d'),  # Convert date to string
                "Description": description,
                "RV No": "",
                "LPO No": lpo_no,
                "PV No": pv_no,
                "Fiscal Year": fiscal_year,
                "Funding Source": funding_source,
                "Cost Center": cost_center,
                "Currency": currency,
                "Amount": amount,
                "Exchange Rate": exchange_rate,
                "USD Amount": usd_amount,
                "Budget Line Item": "",
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Append to database
            append_to_csv(data)
            
            # Store data in session state for download
            st.session_state.submitted_data = data
            st.session_state.show_download = True
            
            st.success("Expense Entry Saved to Database!")
            # Display data with properly formatted date
            st.json(prepare_data_for_display(data))
    
    # Show download button outside the form
    if st.session_state.show_download and st.session_state.submitted_data:
        csv_data = convert_to_csv(st.session_state.submitted_data)
        st.download_button(
            label="📥 Download this record as CSV",
            data=csv_data,
            file_name=f"expense_entry_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_expense"
        )
        if st.button("Clear", key="clear_expense"):
            st.session_state.show_download = False
            st.session_state.submitted_data = None
            st.rerun()

# -----------------------------
# BUDGET LINE FORM
# -----------------------------
elif form_type == "Budget Line Form":

    st.header("Budget Line Form")

    # Budget Line Items dropdown options
    budget_line_items = [
        "Basic Salaries",
        "Over Time",
        "General Allowance",
        "Honorarium",
        "Foreign Means Of Travel",
        "Foreign Daily Subsistence Allowance",
        "Foreign Incidental Allowance",
        "Domestic Means of Travel",
        "Domestic Daily Subsistence Allowance",
        "Domestic Travel - Incidental Allowance",
        "Electricity",
        "Water And Sewage",
        "Telecommunication, Internet, Postage & Courier",
        "Scratch Cards",
        "Internet Provider Services",
        "Computer Supplies, Parts and Cabling",
        "Residential Property Rental/Allowance to staff",
        "Office Buildings Rental & Leases",
        "Other Rental & Lease",
        "Fuel & Lubricants (Utility) - Vehicles",
        "Fuel & Lubricants - Bikes",
        "Fuel & Lubricant - Generators",
        "Repair & Maint. - Civil",
        "Repair & Maint. - Vehicles",
        "Repairs & Maint. - Bikes",
        "Repairs & Maint. - Generators",
        "Repairs & Maint. - Of Equipment",
        "Repair & Maint. - ICT Equipment",
        "Cleaning Materials & Services"
    ]

    cost_centers = [
        "CG Office", "PSSPD", "TMD", "CMPA", "PED", "FID", "DCGTA OFFICE",
        "EDQARD", "ERMCD", "MISD", "TPSD", "NRARS", "EDAD", "OPR", "RMS",
        "D1-Office", "LTD"
    ]

    with st.form("budget_line_form"):
        trans_date = st.date_input("Date", value=date.today())
        description = st.text_area("Description/Justification")
        
        budget_line_item = st.selectbox(
            "Budget Line Item",
            budget_line_items
        )
        
        cost_center = st.selectbox(
            "Cost Center",
            cost_centers
        )
        
        fiscal_year = st.selectbox("Fiscal Year", fiscal_years)
        funding_source = st.text_input("Funding Source")
        
        col1, col2 = st.columns(2)
        
        with col1:
            currency = st.selectbox(
                "Currency",
                ["USD", "ZAR", "EUR", "GBP", "KES"],
                key="budget_currency"
            )
        
        with col2:
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=0.0,
                key="budget_amount"
            )
        
        exchange_rate = st.number_input(
            "Exchange Rate",
            min_value=0.0001,
            value=1.0,
            key="budget_exchange_rate"
        )
        
        usd_amount = amount / exchange_rate
        st.info(f"💰 USD Amount: {usd_amount:,.2f}")
        
        # Optional fields
        st.subheader("Optional Reference Information")
        col3, col4 = st.columns(2)
        
        with col3:
            reference_no = st.text_input("Reference No. (LPO/PV/RV)")
        
        with col4:
            reference_type = st.selectbox(
                "Reference Type",
                ["None", "LPO", "PV", "RV"]
            )
        
        submit = st.form_submit_button("Save Budget Line Item")
        
        if submit:
            # Prepare data for database
            data = {
                "Form_Type": "Budget Line",
                "Date": trans_date.strftime('%Y-%m-%d'),  # Convert date to string
                "Description": description,
                "RV No": reference_no if reference_type == "RV" else "",
                "LPO No": reference_no if reference_type == "LPO" else "",
                "PV No": reference_no if reference_type == "PV" else "",
                "Fiscal Year": fiscal_year,
                "Funding Source": funding_source,
                "Cost Center": cost_center,
                "Currency": currency,
                "Amount": amount,
                "Exchange Rate": exchange_rate,
                "USD Amount": usd_amount,
                "Budget Line Item": budget_line_item,
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Append to database
            append_to_csv(data)
            
            # Store data in session state for download
            st.session_state.submitted_data = data
            st.session_state.show_download = True
            
            st.success(f"Budget Line Item '{budget_line_item}' Saved to Database!")
            # Display data with properly formatted date
            st.json(prepare_data_for_display(data))
    
    # Show download button outside the form
    if st.session_state.show_download and st.session_state.submitted_data:
        csv_data = convert_to_csv(st.session_state.submitted_data)
        st.download_button(
            label="📥 Download this record as CSV",
            data=csv_data,
            file_name=f"budget_line_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_budget"
        )
        if st.button("Clear", key="clear_budget"):
            st.session_state.show_download = False
            st.session_state.submitted_data = None
            st.rerun()

# Display database statistics in sidebar
if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
    df_stats = pd.read_csv(DATABASE_FILE)
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Database Statistics")
    st.sidebar.metric("Total Records", len(df_stats))
    
    # Show breakdown by form type
    if "Form_Type" in df_stats.columns:
        form_counts = df_stats["Form_Type"].value_counts()
        st.sidebar.write("**Records by Type:**")
        for form_type_name, count in form_counts.items():
            st.sidebar.write(f"- {form_type_name}: {count}")
    
    # Show breakdown by fiscal year
    if "Fiscal Year" in df_stats.columns:
        fiscal_year_counts = df_stats["Fiscal Year"].value_counts().sort_index(ascending=False)
        if len(fiscal_year_counts) > 0:
            st.sidebar.write("**Records by Fiscal Year:**")
            for year, count in fiscal_year_counts.head(5).items():
                st.sidebar.write(f"- {year}: {count}")
    
    # Show budget line item breakdown if available
    if "Budget Line Item" in df_stats.columns:
        budget_items = df_stats[df_stats["Budget Line Item"] != ""]["Budget Line Item"].value_counts()
        if len(budget_items) > 0:
            st.sidebar.write("**Top Budget Lines:**")
            for item, count in budget_items.head(5).items():
                st.sidebar.write(f"- {item}: {count}")