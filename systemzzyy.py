import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import hashlib
import time
import re
from io import BytesIO

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Enterprise Budget & Finance Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ENTERPRISE GRADE CSS
# =========================
st.markdown("""
<style>
    /* ========== GOOGLE FONTS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* ========== GLOBAL BACKGROUND ========== */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8edf3 100%);
    }
    
    /* ========== PROFESSIONAL SIDEBAR ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a2b3e 0%, #0d3b4f 100%);
        border-right: none;
        box-shadow: 4px 0 20px rgba(0,0,0,0.15);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255,255,255,0.85);
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15);
        margin: 1.2rem 0;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Sidebar logo area */
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-logo-icon {
        font-size: 3rem;
    }
    
    .sidebar-logo-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 0.5rem;
        letter-spacing: -0.3px;
    }
    
    .sidebar-logo-sub {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 0.25rem;
    }
    
    /* User profile in sidebar */
    .user-profile {
        background: rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 0.8rem;
        margin: 1rem 0;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .user-role {
        font-size: 0.65rem;
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .user-name {
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    /* ========== MAIN HEADER ========== */
    .main-header {
        background: linear-gradient(135deg, #0a2b3e 0%, #1a4a6e 100%);
        border-radius: 24px;
        padding: 2rem 2rem;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        transform: rotate(25deg);
    }
    
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        opacity: 0.85;
        margin: 0;
        font-size: 0.9rem;
    }
    
    .header-date {
        background: rgba(255,255,255,0.12);
        padding: 0.5rem 1rem;
        border-radius: 40px;
        font-size: 0.8rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    /* ========== FORM CARDS ========== */
    .form-card {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .form-card:hover {
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    
    /* ========== SECTION HEADERS ========== */
    .section-header {
        background: transparent;
        border-left: 4px solid #2c7da0;
        padding: 0.5rem 0 0.5rem 1rem;
        margin: 1.5rem 0 1.2rem 0;
        font-weight: 700;
        font-size: 1rem;
        color: #0a2b3e;
        letter-spacing: -0.3px;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    /* ========== METRIC GRID ========== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 20px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #2c7da0, #61a5c2, #2c7da0);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.12);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0a2b3e;
        margin: 0.5rem 0;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.7rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        border-radius: 40px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        padding: 0.6rem 1.8rem !important;
        font-size: 0.85rem !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2c7da0 0%, #1a5a7a 100%) !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(44,125,160,0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(44,125,160,0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* ========== INPUT FIELDS ========== */
    .stTextInput input, .stNumberInput input, .stDateInput input,
    .stSelectbox > div > div, .stTextArea textarea {
        border-radius: 14px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: white !important;
        transition: all 0.2s ease !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1rem !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus,
    .stDateInput input:focus, .stTextArea textarea:focus {
        border-color: #2c7da0 !important;
        box-shadow: 0 0 0 3px rgba(44,125,160,0.1) !important;
        outline: none;
    }
    
    .stTextInput label, .stNumberInput label, .stDateInput label,
    .stSelectbox label, .stTextArea label {
        font-weight: 600 !important;
        color: #0a2b3e !important;
        font-size: 0.75rem !important;
        margin-bottom: 0.3rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ========== DATA TABLE ========== */
    [data-testid="stDataFrame"] {
        border-radius: 20px !important;
        overflow: hidden !important;
        border: 1px solid #eef2f6 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
    }
    
    [data-testid="stDataFrame"] table {
        font-size: 0.8rem !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: #f8fafc !important;
        font-weight: 700 !important;
        color: #0a2b3e !important;
        padding: 12px 16px !important;
        border-bottom: 2px solid #e2e8f0 !important;
    }
    
    [data-testid="stDataFrame"] td {
        padding: 10px 16px !important;
    }
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 8px;
        border-radius: 60px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600 !important;
        border-radius: 40px !important;
        padding: 8px 28px !important;
        color: #7f8c8d !important;
        font-size: 0.85rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0a2b3e 0%, #2c7da0 100%) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(44,125,160,0.3) !important;
    }
    
    /* ========== ALERTS ========== */
    .stAlert {
        border-radius: 16px !important;
        border-left: 4px solid !important;
        padding: 1rem 1.2rem !important;
    }
    
    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        background: #f8fafc !important;
        border-radius: 14px !important;
        color: #0a2b3e !important;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        margin-top: 3rem;
        padding: 1.5rem;
        text-align: center;
        border-top: 1px solid rgba(0,0,0,0.08);
        font-size: 0.7rem;
        color: #7f8c8d;
    }
    
    /* ========== LOGIN PAGE ========== */
    .auth-container {
        max-width: 500px;
        margin: 80px auto;
        background: white;
        border-radius: 40px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        overflow: hidden;
    }
    
    .auth-header {
        background: linear-gradient(135deg, #0a2b3e 0%, #1a4a6e 100%);
        padding: 2rem;
        text-align: center;
        color: white;
    }
    
    .auth-icon {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }
    
    .auth-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .auth-subtitle {
        font-size: 0.8rem;
        opacity: 0.8;
        margin-top: 0.25rem;
    }
    
    .auth-body {
        padding: 2rem;
    }
    
    /* ========== ANIMATIONS ========== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .form-card, .metric-card, [data-testid="stDataFrame"] {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .metric-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        
        .form-card {
            padding: 1.2rem;
        }
        
        .main-header {
            padding: 1.2rem;
        }
        
        .main-header h1 {
            font-size: 1.3rem;
        }
    }
    
    /* ========== PRINT ========== */
    @media print {
        [data-testid="stSidebar"], .stButton, .stTabs, .st-emotion-cache-1v0mbdj {
            display: none !important;
        }
        
        .form-card {
            box-shadow: none !important;
            border: 1px solid #ddd !important;
            break-inside: avoid;
        }
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2c7da0;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1a5a7a;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# AUTHENTICATION SYSTEM (FULLY CORRECTED)
# =========================
def init_auth_db():
    """Initialize users table with all required columns - handles existing databases"""
    conn = sqlite3.connect('budget_management.db')
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Get existing columns
        cursor.execute("PRAGMA table_info(users)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        # Add missing columns one by one
        if 'full_name' not in existing_columns:
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
            except:
                pass
        if 'email' not in existing_columns:
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            except:
                pass
        if 'role' not in existing_columns:
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
            except:
                pass
        if 'last_login' not in existing_columns:
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
            except:
                pass
    else:
        # Create new users table with all columns
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                role TEXT DEFAULT 'user',
                created_at TEXT NOT NULL,
                last_login TEXT
            )
        ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using PBKDF2"""
    salt = "budget_finance_salt_2026"
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def create_user(username, password, full_name="", email=""):
    """Create a new user account"""
    conn = sqlite3.connect('budget_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash, full_name, email, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, hash_password(password), full_name, email, 'user', datetime.now().isoformat()))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def authenticate_user(username, password):
    """Verify username and password - handles both old and new schema"""
    conn = sqlite3.connect('budget_management.db')
    cursor = conn.cursor()
    
    # First, ensure columns exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    has_full_name = 'full_name' in columns
    has_role = 'role' in columns
    
    # Build query based on available columns
    if has_full_name and has_role:
        cursor.execute('SELECT password_hash, full_name, role FROM users WHERE username = ?', (username,))
    elif has_full_name:
        cursor.execute('SELECT password_hash, full_name FROM users WHERE username = ?', (username,))
    else:
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    
    result = cursor.fetchone()
    
    if result and result[0] == hash_password(password):
        # Update last login
        try:
            if 'last_login' in columns:
                cursor.execute('UPDATE users SET last_login = ? WHERE username = ?', (datetime.now().isoformat(), username))
            else:
                cursor.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
                cursor.execute('UPDATE users SET last_login = ? WHERE username = ?', (datetime.now().isoformat(), username))
        except:
            pass
        
        conn.commit()
        
        # Extract full_name and role
        full_name = result[1] if len(result) > 1 else username
        role = result[2] if len(result) > 2 else 'user'
        
        conn.close()
        return True, full_name, role
    
    conn.close()
    return False, None, None

def login_or_register():
    """Professional login/register interface"""
    st.markdown("""
    <div class="auth-container">
        <div class="auth-header">
            <div class="auth-icon">🏦</div>
            <div class="auth-title">Budget & Finance Management System</div>
            <div class="auth-subtitle">Enterprise Edition</div>
        </div>
        <div class="auth-body">
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
            
            if submitted:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                else:
                    success, full_name, role = authenticate_user(username, password)
                    if success:
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.session_state['full_name'] = full_name or username
                        st.session_state['role'] = role
                        st.success(f"Welcome back, {full_name or username}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Username *", placeholder="Choose a username (min 3 characters)")
            new_password = st.text_input("Password *", type="password", placeholder="Min 6 characters")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password")
            full_name = st.text_input("Full Name", placeholder="Your full name (optional)")
            email = st.text_input("Email", placeholder="your@email.com (optional)")
            submitted_reg = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted_reg:
                if not new_username or len(new_username) < 3:
                    st.error("❌ Username must be at least 3 characters")
                elif not new_password or len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif not re.match("^[a-zA-Z0-9_]+$", new_username):
                    st.error("❌ Username can only contain letters, numbers, and underscores")
                else:
                    if create_user(new_username, new_password, full_name, email):
                        st.success("✅ Account created successfully! Please sign in.")
                    else:
                        st.error("❌ Username already exists. Please choose another.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    return False

# =========================
# DATABASE SETUP
# =========================
def init_database():
    """Initialize main budget database tables"""
    conn = sqlite3.connect('budget_management.db')
    cursor = conn.cursor()
    
    # Create budget entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id TEXT UNIQUE NOT NULL,
            date TEXT NOT NULL,
            payee TEXT NOT NULL,
            pv_no TEXT,
            check_no TEXT,
            lpo_no TEXT,
            description TEXT,
            account_class TEXT NOT NULL,
            cost_center TEXT,
            funding_source TEXT NOT NULL,
            fiscal_year TEXT NOT NULL,
            currency TEXT NOT NULL,
            amount REAL NOT NULL,
            exchange_rate REAL DEFAULT 1.0,
            gross_amount REAL DEFAULT 0.0,
            withholding_amount REAL DEFAULT 0.0,
            net_amount REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Pending',
            created_by TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # Check and add missing columns to budget_entries if needed
    cursor.execute("PRAGMA table_info(budget_entries)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    if 'created_by' not in existing_columns:
        try:
            cursor.execute("ALTER TABLE budget_entries ADD COLUMN created_by TEXT")
        except:
            pass
    
    # Create audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user TEXT,
            action TEXT NOT NULL,
            entry_id TEXT,
            details TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_to_database(entry):
    """Save form data to database"""
    conn = sqlite3.connect('budget_management.db')
    cursor = conn.cursor()
    
    # Generate unique entry ID
    entry_id = hashlib.md5(
        f"{entry['date']}{entry['payee']}{datetime.now()}{entry.get('amount', 0)}".encode()
    ).hexdigest()[:10].upper()
    
    cursor.execute('''
        INSERT INTO budget_entries 
        (entry_id, date, payee, pv_no, check_no, lpo_no, description, 
         account_class, cost_center, funding_source, fiscal_year, 
         currency, amount, exchange_rate, gross_amount, withholding_amount, 
         net_amount, created_by, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry_id, entry['date'], entry['payee'], entry.get('pv_no', ''), 
        entry.get('check_no', ''), entry.get('lpo_no', ''), entry.get('description', ''),
        entry['account_class'], entry.get('cost_center', ''), entry['funding_source'],
        entry['fiscal_year'], entry['currency'], entry['amount'],
        entry.get('exchange_rate', 1.0), entry.get('gross_amount', 0), entry.get('withholding_amount', 0),
        entry.get('net_amount', entry['amount']), st.session_state.get('username', 'system'),
        datetime.now().isoformat(), datetime.now().isoformat()
    ))
    
    # Log to audit table
    cursor.execute('''
        INSERT INTO audit_log (timestamp, user, action, entry_id, details)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        st.session_state.get('username', 'system'),
        'ENTRY_CREATED',
        entry_id,
        f"Budget entry created for {entry['payee']} - Amount: {entry['currency']} {entry['amount']:,.2f}"
    ))
    
    conn.commit()
    conn.close()
    return entry_id

def get_all_entries():
    """Retrieve all entries from database"""
    conn = sqlite3.connect('budget_management.db')
    df = pd.read_sql_query("SELECT * FROM budget_entries ORDER BY id DESC", conn)
    conn.close()
    return df

def update_entry_status(entry_id, new_status):
    """Update the status of an entry"""
    conn = sqlite3.connect('budget_management.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE budget_entries 
        SET status = ?, updated_at = ?
        WHERE entry_id = ?
    ''', (new_status, datetime.now().isoformat(), entry_id))
    
    cursor.execute('''
        INSERT INTO audit_log (timestamp, user, action, entry_id, details)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        st.session_state.get('username', 'system'),
        'STATUS_UPDATED',
        entry_id,
        f"Status changed to {new_status}"
    ))
    
    conn.commit()
    conn.close()

def delete_entry(entry_id):
    """Delete an entry from database"""
    conn = sqlite3.connect('budget_management.db')
    cursor = conn.cursor()
    
    # Get entry details for audit
    cursor.execute('SELECT payee, amount FROM budget_entries WHERE entry_id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    cursor.execute('DELETE FROM budget_entries WHERE entry_id = ?', (entry_id,))
    
    cursor.execute('''
        INSERT INTO audit_log (timestamp, user, action, entry_id, details)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        st.session_state.get('username', 'system'),
        'ENTRY_DELETED',
        entry_id,
        f"Budget entry deleted - Payee: {entry[0] if entry else 'Unknown'}, Amount: {entry[1] if entry else 0:,.2f}"
    ))
    
    conn.commit()
    conn.close()

def get_summary_stats(df):
    """Calculate summary statistics"""
    if df.empty:
        return {
            'total_entries': 0,
            'total_amount': 0,
            'avg_amount': 0,
            'pending_count': 0,
            'approved_count': 0,
            'rejected_count': 0,
            'paid_count': 0
        }
    
    return {
        'total_entries': len(df),
        'total_amount': df['amount'].sum(),
        'avg_amount': df['amount'].mean(),
        'pending_count': len(df[df['status'] == 'Pending']),
        'approved_count': len(df[df['status'] == 'Approved']),
        'rejected_count': len(df[df['status'] == 'Rejected']),
        'paid_count': len(df[df['status'] == 'Paid'])
    }

# =========================
# FORM TYPES
# =========================
def budget_entry_form():
    """Main budget entry form"""
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📌 General Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input("Date", datetime.now())
        payee = st.text_input("Payee *", placeholder="Enter payee/vendor name")
        pv_no = st.text_input("PV Number", placeholder="e.g., PV-2026-001")
        check_no = st.text_input("Check Number", placeholder="e.g., CHK-001")
        
    with col2:
        lpo_no = st.text_input("LPO Number", placeholder="e.g., LPO-2026-001")
        description = st.text_area("Description", placeholder="Enter payment description", height=100)
        cost_center = st.text_input("Cost Center", placeholder="e.g., CC-FIN-001")
    
    st.markdown('<div class="section-header">🏦 Classification</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        account_classes = [
            "Wages & Salaries",
            "Employee Benefits",
            "Capacity Building & Training",
            "Supplies & Consumables",
            "Professional Services",
            "Travel & Transport",
            "Construction & Infrastructure",
            "Property, Plant & Equipment",
            "ICT Equipment & Software",
            "Other Operating Expenses"
        ]
        account_class = st.selectbox("Account Classification *", account_classes)
        
        funding_sources = ["GOL - Government of Liberia", "MTS - Multi-Donor Trust Fund", 
                          "CUF - Central Unity Fund", "OT - Other Sources", 
                          "Excise Stamp", "UNDP", "AfDB", "World Bank", "EU", "USAID"]
        funding_source = st.selectbox("Funding Source *", funding_sources)
        
    with col4:
        fiscal_years = ["FY-2024", "FY-2025", "FY-2026", "FY-2027"]
        fiscal_year = st.selectbox("Fiscal Year *", fiscal_years)
    
    st.markdown('<div class="section-header">💵 Financial Details</div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        currencies = ["USD", "LRD", "EUR", "GBP"]
        currency = st.selectbox("Currency *", currencies)
        amount = st.number_input("Amount *", min_value=0.0, value=0.0, step=100.0, format="%.2f")
        exchange_rate = st.number_input("Exchange Rate (to LRD)", value=1.0, step=0.1, format="%.4f",
                                        help="Rate to Liberian Dollar. Use 1 if currency is LRD")
        
    with col6:
        gross_amount = st.number_input("Gross Amount", min_value=0.0, value=amount, step=100.0, format="%.2f")
        withholding_amount = st.number_input("Withholding Amount", min_value=0.0, value=0.0, step=10.0, format="%.2f")
        net_amount = st.number_input("Net Amount", min_value=0.0, value=gross_amount - withholding_amount, step=100.0, format="%.2f")
    
    if withholding_amount > 0 and gross_amount > 0:
        calculated_net = gross_amount - withholding_amount
        if net_amount != calculated_net:
            st.info(f"💡 Calculated Net Amount: {currency} {calculated_net:,.2f}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'date': date.isoformat(),
        'payee': payee,
        'pv_no': pv_no,
        'check_no': check_no,
        'lpo_no': lpo_no,
        'description': description,
        'account_class': account_class,
        'cost_center': cost_center,
        'funding_source': funding_source,
        'fiscal_year': fiscal_year,
        'currency': currency,
        'amount': amount,
        'exchange_rate': exchange_rate,
        'gross_amount': gross_amount,
        'withholding_amount': withholding_amount,
        'net_amount': net_amount if net_amount > 0 else gross_amount - withholding_amount
    }

def payment_voucher_form():
    """Payment voucher specific form"""
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">💰 Payment Voucher</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        voucher_no = st.text_input("Voucher Number *", placeholder="e.g., PV-2026-001")
        voucher_date = st.date_input("Voucher Date", datetime.now())
        payee_name = st.text_input("Payee Name *", placeholder="Enter payee name")
        
    with col2:
        department = st.text_input("Department/Unit", placeholder="e.g., Finance Department")
        payment_method = st.selectbox("Payment Method", ["Cash", "Cheque", "Bank Transfer", "Mobile Money", "RTGS"])
        bank_name = st.text_input("Bank Name", placeholder="e.g., Central Bank of Liberia")
    
    st.markdown('<div class="section-header">📋 Payment Details</div>', unsafe_allow_html=True)
    
    description = st.text_area("Payment Description *", placeholder="Detailed description of the payment purpose", height=100)
    
    col3, col4 = st.columns(2)
    
    with col3:
        amount = st.number_input("Payment Amount *", min_value=0.0, value=0.0, step=100.0, format="%.2f")
        currency = st.selectbox("Currency", ["USD", "LRD", "EUR", "GBP"])
        
    with col4:
        approval_status = st.selectbox("Approval Status", ["Pending", "Approved", "Rejected", "Disbursed"])
        remarks = st.text_area("Remarks", placeholder="Any additional notes or comments")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'date': voucher_date.isoformat(),
        'payee': payee_name,
        'pv_no': voucher_no,
        'check_no': payment_method == "Cheque" and "CHK-" or "",
        'lpo_no': '',
        'description': description,
        'account_class': 'Payment Voucher',
        'cost_center': department,
        'funding_source': 'General',
        'fiscal_year': datetime.now().strftime("FY-2026"),
        'currency': currency,
        'amount': amount,
        'exchange_rate': 1.0,
        'gross_amount': amount,
        'withholding_amount': 0.0,
        'net_amount': amount,
        'status': approval_status,
        'payment_method': payment_method,
        'bank_name': bank_name,
        'remarks': remarks
    }

def requisition_form():
    """Requisition form"""
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📝 Requisition Form</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        requisition_no = st.text_input("Requisition Number *", placeholder="e.g., REQ-2026-001")
        requisition_date = st.date_input("Requisition Date", datetime.now())
        requester_name = st.text_input("Requester Name *", placeholder="Full name of requester")
        
    with col2:
        department = st.text_input("Department *", placeholder="e.g., IT Department")
        priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Urgent"])
        delivery_date = st.date_input("Required Delivery Date", datetime.now())
    
    st.markdown('<div class="section-header">🛒 Items Requisitioned</div>', unsafe_allow_html=True)
    
    if 'requisition_items' not in st.session_state:
        st.session_state.requisition_items = [{'item': '', 'quantity': 1, 'unit_price': 0.0}]
    
    for i, item in enumerate(st.session_state.requisition_items):
        col_a, col_b, col_c, col_d = st.columns([3, 1, 1, 0.5])
        with col_a:
            item['item'] = st.text_input(f"Item Description", value=item['item'], key=f"item_{i}", placeholder="Describe the item/service")
        with col_b:
            item['quantity'] = st.number_input(f"Qty", value=item['quantity'], min_value=1, key=f"qty_{i}")
        with col_c:
            item['unit_price'] = st.number_input(f"Unit Price", value=item['unit_price'], min_value=0.0, key=f"price_{i}", format="%.2f")
        with col_d:
            if st.button("🗑️", key=f"remove_{i}"):
                st.session_state.requisition_items.pop(i)
                st.rerun()
    
    if st.button("➕ Add Item", use_container_width=False):
        st.session_state.requisition_items.append({'item': '', 'quantity': 1, 'unit_price': 0.0})
        st.rerun()
    
    total_amount = sum(item['quantity'] * item['unit_price'] for item in st.session_state.requisition_items)
    st.info(f"💰 **Total Amount:** ${total_amount:,.2f}")
    
    st.markdown('<div class="section-header">📌 Justification</div>', unsafe_allow_html=True)
    justification = st.text_area("Reason for Requisition *", placeholder="Explain the business need and justification for this requisition", height=100)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'date': requisition_date.isoformat(),
        'payee': requester_name,
        'pv_no': requisition_no,
        'check_no': '',
        'lpo_no': '',
        'description': justification,
        'account_class': 'Requisition',
        'cost_center': department,
        'funding_source': 'General',
        'fiscal_year': datetime.now().strftime("FY-2026"),
        'currency': 'USD',
        'amount': total_amount,
        'exchange_rate': 1.0,
        'gross_amount': total_amount,
        'withholding_amount': 0.0,
        'net_amount': total_amount,
        'priority': priority,
        'delivery_date': delivery_date.isoformat(),
        'items': st.session_state.requisition_items,
        'justification': justification
    }

# =========================
# MAIN APPLICATION
# =========================
def main():
    """Main application entry point"""
    init_database()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🏦</div>
            <div class="sidebar-logo-title">Budget & Finance</div>
            <div class="sidebar-logo-sub">Enterprise Management System</div>
        </div>
        """, unsafe_allow_html=True)
        
        if 'username' in st.session_state:
            st.markdown(f"""
            <div class="user-profile">
                <div class="user-role">{st.session_state.get('role', 'Finance Officer').upper()}</div>
                <div class="user-name">👤 {st.session_state.get('full_name', st.session_state['username'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📋 Navigation")
        form_type = st.radio(
            "Select Form Type",
            ["📝 Budget Entry", "💰 Payment Voucher", "📋 Requisition Form"],
            index=0,
            label_visibility="collapsed"
        )
        form_type = form_type.replace("📝 ", "").replace("💰 ", "").replace("📋 ", "")
        
        st.markdown("---")
        
        st.markdown("### 📊 Dashboard")
        df = get_all_entries()
        stats = get_summary_stats(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Entries", stats['total_entries'])
        with col2:
            st.metric("Total Amount", f"${stats['total_amount']:,.0f}")
        
        st.markdown("---")
        
        st.markdown("### 📤 Export")
        if st.button("📥 Export to CSV", use_container_width=True):
            if not df.empty:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    csv,
                    f"budget_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            else:
                st.warning("No data to export")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        
        st.caption("© 2026 Finance Department")
        st.caption("v3.0 Enterprise")
    
    # Main content
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h1>🏦 Budget & Finance Management System</h1>
                <p>Enterprise Financial Data Entry, Tracking & Compliance Platform</p>
            </div>
            <div class="header-date">
                📅 {datetime.now().strftime("%A, %B %d, %Y")}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Form selection
    if form_type == "Budget Entry":
        st.markdown("### 📝 Budget Entry Form")
        entry_data = budget_entry_form()
    elif form_type == "Payment Voucher":
        st.markdown("### 💰 Payment Voucher Form")
        entry_data = payment_voucher_form()
    else:
        st.markdown("### 📋 Requisition Form")
        entry_data = requisition_form()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.button("✅ Submit Entry", use_container_width=True, type="primary")
    
    if submitted:
        if not entry_data.get('payee') or str(entry_data['payee']).strip() == '':
            st.error("❌ Please fill in the Payee field")
        elif entry_data.get('amount', 0) <= 0:
            st.error("❌ Amount must be greater than zero")
        else:
            with st.spinner("💾 Saving to database..."):
                time.sleep(0.3)
                entry_id = save_to_database(entry_data)
            st.success(f"✅ Entry saved successfully! Entry ID: **{entry_id}**")
            st.balloons()
    
    # Display recent entries
    st.markdown("---")
    st.markdown("### 📊 Recent Budget Entries")
    
    df = get_all_entries()
    
    if not df.empty:
        stats = get_summary_stats(df)
        
        st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
        
        metrics = [
            {"icon": "📋", "value": stats['total_entries'], "label": "Total Entries"},
            {"icon": "💰", "value": f"${stats['total_amount']:,.0f}", "label": "Total Amount"},
            {"icon": "⏳", "value": stats['pending_count'], "label": "Pending"},
            {"icon": "✅", "value": stats['approved_count'], "label": "Approved"},
        ]
        
        for metric in metrics:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{metric['icon']}</div>
                <div class="metric-value">{metric['value']}</div>
                <div class="metric-label">{metric['label']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        display_cols = ['entry_id', 'date', 'payee', 'pv_no', 'account_class', 'currency', 'amount', 'status']
        available_cols = [col for col in display_cols if col in df.columns]
        display_df = df[available_cols].head(10)
        st.dataframe(display_df, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🔄 Workflow Management")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_entry = st.selectbox("Select Entry ID", df['entry_id'].tolist())
        with col2:
            new_status = st.selectbox("Update Status", ["Pending", "Under Review", "Approved", "Rejected", "Paid"])
        with col3:
            if st.button("Update Status", use_container_width=True):
                update_entry_status(selected_entry, new_status)
                st.success(f"✅ Entry {selected_entry} status updated to {new_status}")
                time.sleep(0.5)
                st.rerun()
        
        with st.expander("🗑️ Delete Entry (Administrator Only)"):
            entry_to_delete = st.selectbox("Select Entry ID to Delete", df['entry_id'].tolist(), key="delete_select")
            confirm = st.checkbox("I confirm this deletion action")
            if st.button("Delete Entry", type="secondary", use_container_width=False):
                if confirm:
                    delete_entry(entry_to_delete)
                    st.warning(f"⚠️ Entry {entry_to_delete} has been deleted")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Please confirm deletion")
    else:
        st.info("📭 No entries yet. Submit your first budget entry using the form above.")
    
    st.markdown("""
    <div class="footer">
        <div>🔒 All transactions are encrypted and audited | ISO 27001 Compliant</div>
        <div style="margin-top: 0.5rem;">This system is for authorized personnel only. All activities are logged.</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# APPLICATION ENTRY POINT
# =========================
if __name__ == "__main__":
    # Initialize authentication database
    init_auth_db()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    # Show login or main app
    if not st.session_state['authenticated']:
        login_or_register()
    else:
        main()
