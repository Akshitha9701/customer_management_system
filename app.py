import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import re
from fpdf import FPDF
import base64
import io
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_db_connection():
    return mysql.connector.connect(host="localhost",user="root",password="09072001",database="customer_management") #please enter your username and password

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Customer Management System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        mydb = get_db_connection()
        c = mydb.cursor()
        c.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = c.fetchone()
        mydb.close()
        if result:
            st.session_state.logged_in = True
            st.success("Login successful! Welcome.")
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

def insert_feedback(customer_id, order_id, product_name, rating, comment):
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("""
        INSERT INTO feedback (customer_id, order_id, product_name, rating, comment, feedback_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (customer_id, order_id, product_name, rating, comment, datetime.now().date()))
    mydb.commit()
    mydb.close()

def generate_invoice_pdf(order_id, customer_id, product_name, order_amount, quantity):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Customer Order Invoice", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(100, 10, txt=f"Order ID: {order_id}", ln=True)
    pdf.cell(100, 10, txt=f"Customer ID: {customer_id}", ln=True)
    pdf.cell(100, 10, txt=f"Product Name: {product_name}", ln=True)
    pdf.cell(100, 10, txt=f"Quantity: {quantity}", ln=True)
    pdf.cell(100, 10, txt=f"Total Amount: ₹{order_amount * quantity:.2f}", ln=True)
    pdf.cell(100, 10, txt=f"Order Date: {datetime.now().date()}", ln=True)
    filename = f"invoice_{order_id}.pdf"
    pdf.output(filename)
    with open(filename, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return f'<a href="data:application/pdf;base64,{base64_pdf}" download="{filename}">📄 Download Invoice</a>'

def get_db_connection():
    return mysql.connector.connect(host="localhost",user="root",password="09072001",database="customer_management") #please enter your username and password
        
def generate_customer_id():
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1")
    result = c.fetchone()
    mydb.close()
    if result:
        last_id = int(result[0].replace("CUST", ""))
        new_id = f"CUST{last_id + 1:03d}"
    else:
        new_id = "CUST001"
    return new_id
def generate_order_id():
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1")
    result = c.fetchone()
    mydb.close()
    if result:
        last_id = int(result[0].replace("ORD",""))
        new_id = f"ORD{last_id + 1:03d}" 
    else:
        new_id = "ORD001"
    return new_id
def fetch_customer_by_id(customer_id):
    mydb = get_db_connection()
    query = "SELECT * FROM customers WHERE customer_id = %s"
    df = pd.read_sql(query, mydb, params=(customer_id,))
    mydb.close()
    return df

def generate_return_id():
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("SELECT return_id FROM returns ORDER BY return_id DESC LIMIT 1")
    result = c.fetchone()
    mydb.close()
    if result:
        last_id = int(result[0].replace("RET",""))
        new_id = f"RET{last_id + 1:03d}"
    else:
        new_id = "RET001"
    return new_id
def generate_complaint_id():
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("SELECT complaint_id FROM complaints ORDER BY complaint_id DESC LIMIT 1")
    result = c.fetchone()
    mydb.close()
    if result:
        last_id = int(result[0].replace("CMP",""))
        new_id = f"CMP{last_id + 1:03d}"
    else:
        new_id = "CMP001"
    return new_id
def fetch_table(orders):
    mydb = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM {orders}", mydb)
    mydb.close()
    return df
def fetch_table(customers):
    mydb = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM {customers}", mydb)
    mydb.close()
    return df
def fetch_table(returns):
    mydb = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM {returns}", mydb)
    mydb.close()
    return df

def insert_order(order_id, customer_id, product_name, order_amount, quantity):
    mydb = get_db_connection()
    c = mydb.cursor()
    order_date = datetime.now().date()  # Auto-add current date
    query = """
    INSERT INTO orders (order_id, customer_id, product_name, order_amount, quantity, order_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    c.execute(query, (order_id, customer_id, product_name, order_amount, quantity, order_date))  # Single insert
    mydb.commit()
    mydb.close()

def insert_return(return_id, customer_id, order_id, product_name, return_reason, return_date):
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("""
        INSERT INTO returns (return_id, customer_id, order_id, product_name, reason, return_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (return_id, customer_id, order_id, product_name, return_reason, return_date))
    mydb.commit()
    mydb.close()
    
def insert_complaint(complaint_id, customer_id, order_id, product_name, complaint, complaint_date):
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("""
        INSERT INTO complaints (complaint_id, customer_id, order_id, product_name, complaint, complaint_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (complaint_id, customer_id, order_id, product_name, complaint, complaint_date))
    mydb.commit()
    mydb.close()
    
def check_existing_customer(email):
    mydb = get_db_connection()
    c = mydb.cursor()
    c.execute("SELECT customer_id FROM customers WHERE email_id = %s", (email,))
    result = c.fetchone()
    mydb.close()
    return result[0] if result else None

# Check if Customer ID exists
def check_customer_exists(customer_id):
    mydb = get_db_connection()
    query = "SELECT COUNT(*) FROM customers WHERE customer_id = %s"
    c = mydb.cursor()
    c.execute(query, (customer_id,))
    count = c.fetchone()[0]
    mydb.close()
    return count > 0

# Check if Order ID exists
def check_order_exists(order_id):
    mydb = get_db_connection()
    query = "SELECT COUNT(*) FROM orders WHERE order_id = %s"
    c = mydb.cursor()
    c.execute(query, (order_id,))
    count = c.fetchone()[0]
    mydb.close()
    return count > 0

def fetch_product_insights():
    mydb = get_db_connection()
    # Total Products sold
    total_products_query = "SELECT COUNT(DISTINCT product_name) FROM orders"
    total_products_df = pd.read_sql(total_products_query, mydb)
    total_products = total_products_df.iloc[0, 0]
    
    # Top Selling Products
    top_products_query = """
    SELECT product_name, SUM(quantity) as order_count 
    FROM orders 
    GROUP BY product_name 
    ORDER BY order_count DESC 
    LIMIT 5
    """
    top_products_df = pd.read_sql(top_products_query, mydb)
    top_products_df['order_count'] = top_products_df['order_count'].astype(int)
    
    # Return Stats
    return_stats_query = """
    SELECT product_name, COUNT(*) as return_count 
    FROM returns 
    GROUP BY product_name 
    ORDER BY return_count DESC
    """
    return_stats_df = pd.read_sql(return_stats_query, mydb)

    # Revenue by Product
    revenue_query = """
    SELECT product_name, SUM(order_amount * quantity) as total_revenue 
    FROM orders 
    GROUP BY product_name 
    ORDER BY total_revenue DESC
    """
    revenue_df = pd.read_sql(revenue_query, mydb)
    revenue_df['total_revenue'] = revenue_df['total_revenue'].apply(lambda x: f"₹{x:,.2f}")
    mydb.close()
    return total_products, top_products_df, return_stats_df, revenue_df

def fetch_dashboard_data():
    mydb = get_db_connection()
    
    # Customer Segments
    segments_query = "SELECT customer_segment, COUNT(*) as count FROM customers GROUP BY customer_segment"
    segments_df = pd.read_sql(segments_query, mydb)
    
    # Orders Data
    orders_query = "SELECT product_name, order_amount, quantity FROM orders"
    orders_df = pd.read_sql(orders_query, mydb)
    
    # Returns Data
    returns_query = "SELECT reason, COUNT(*) as count FROM returns GROUP BY reason"
    returns_df = pd.read_sql(returns_query, mydb)
    
    # Top Products (for bar graph)
    top_products_query = """
    SELECT product_name, SUM(quantity) as order_count 
    FROM orders 
    GROUP BY product_name 
    ORDER BY order_count DESC 
    LIMIT 5
    """
    top_products_df = pd.read_sql(top_products_query, mydb)
    
    mydb.close()
    return segments_df, orders_df, returns_df, top_products_df

def fetch_customer_stats_data():
    mydb = get_db_connection()
    query = """
    SELECT o.customer_id, c.customer_segment, o.order_date, 
           SUM(o.order_amount * o.quantity) AS total_amount, 
           COUNT(DISTINCT o.order_id) AS order_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id, c.customer_segment, o.order_date
    """
    df = pd.read_sql(query, mydb)
    mydb.close()
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)

st.set_page_config(page_title="Customer Management System",page_icon="https://cdn-icons-png.flaticon.com/512/10397/10397542.png")
st.markdown("""
    <style>
    /* PAGE BACKGROUND */
    body, .stApp {
        background-color: #dce9f9; /* little dark blue */
        color: #1f1f1f;
    }
    /* SIDEBAR STYLING */
    .sidebar .sidebar-content {
        background-color: #f0f8ff; /* slight light blue */
        border-radius: 15px;
        padding: 1rem;
        margin: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
    }
    .stApp {
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #2a2a2a;
    }
    /* BUTTON STYLE */
    .stButton > button, .stDownloadButton > button, .stForm > div > button {
        background-color: #1E90FF;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5em 1.5em;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton > button:hover, .stDownloadButton > button:hover, .stForm > div > button:hover {
        background-color: #0e70c4;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
    }
    #MainMenu, header, footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

st.title("CUSTOMER MANAGEMENT SYSTEM")
choice=st.sidebar.selectbox("📋 Choose Menu", (
    "🏠 Home", "👥 View all Customers", "➕ Add", 
    "🛒 Orders", "🔁 Returns", "📢 Complaints", "📈 Product Insights", 
    "📊 Dashboards", "📉 Customer Stats", "📝 Feedbacks", "💰 Customer CLV", 
    "🔎 Search & Filter", "📤 Export Data", "🚚 Order Status", 
    "🔔 Notify Customers", "🧾 Activity Log","💳 Payment","🛠 Manual overrides","📞 Contact"
))
if(choice=="🏠 Home"):
    st.image("https://media.mopinion.com/wp-content/uploads/2022/03/27133400/customer-feedback-blog-min.jpg")
    st.markdown("<center><h1>WELCOME</h1><center>",unsafe_allow_html=True)
    st.write("This is the Web Application developed by Akshitha as a part of Training project")
    st.markdown("<center><h3>Manage customers with ease!</h3></center>", unsafe_allow_html=True)
    customers_df = fetch_table("customers")
    orders_df = fetch_table("orders")
    total_customers = len(customers_df)
    total_orders = len(orders_df)
    returns_df = fetch_table("returns")
    total_orders = len(orders_df['order_id'].unique()) if not orders_df.empty else 0
    if not orders_df.empty:
        orders_df['order_amount'] = orders_df['order_amount'].astype(float)
        orders_df['total_amount'] = orders_df['order_amount'] * orders_df['quantity'].astype(int)  # Multiply by quantity
        total_revenue = orders_df['total_amount'].sum()
    else:
        total_revenue = 0.0
    
    # Calculate returns amount using order_id
    if not returns_df.empty and not orders_df.empty:
        # Merge returns with orders on order_id to get return amounts
        returns_with_amount = returns_df.merge(orders_df[['order_id', 'total_amount']], on='order_id', how='left')
        returns_with_amount['total_amount'] = returns_with_amount['total_amount'].fillna(0.0).astype(float)
        total_returns = returns_with_amount['total_amount'].sum()
    else:
        total_returns = 0.0
    net_revenue = total_revenue - total_returns
    st.markdown(f"""
        <center>
            <b>Total Customers:</b> {total_customers} | 
            <b>Total Orders:</b> {total_orders} | 
            <b>Total Revenue:</b> ₹{total_revenue:,.2f} | 
            <b>Net Revenue (after returns):</b> ₹{net_revenue:,.2f}
        </center>
    """, unsafe_allow_html=True)

    # WhatsApp floating button in bottom-right corner
    st.markdown("""
        <style>
        .whatsapp-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 100;
        }
        .whatsapp-button img {
            height: 60px;
            width: 60px;
            border-radius: 50%;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }
        </style>
        <div class="whatsapp-button">
            <a href="https://wa.me/919876543210?text=Hi%20Akshitha%2C%20I%20have%20a%20question%20about%20my%20order" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" alt="Chat on WhatsApp">
            </a>
            <div class="whatsapp-label">Contact</div>
        </div>
    """, unsafe_allow_html=True)

elif(choice=="👥 View all Customers"):
    mydb=get_db_connection()
    df=pd.read_sql("select*from customers",mydb)
    def highlight_status(val):
        color = '#d4edda' if val.lower() == 'active' else '#f8d7da'
        text_color = '#155724' if val.lower() == 'active' else '#721c24'
        return f'background-color: {color}; color: {text_color};'

    styled_df = df.style.applymap(highlight_status, subset=['status'])
    st.dataframe(styled_df)
    
    
elif(choice=="➕ Add"):
    custname = st.text_input("Enter Customer Name")
    email = st.text_input("Enter Email")
    phn = st.text_input("Enter Contact Number")
    custseg = st.selectbox("Enter Customer Segment", ["Individual", "Business", "Enterprise"], key="custseg_select")
    if custseg == "Individual":
        gender = st.selectbox("Enter Gender", ["Select", "Male", "Female"], key="gender_select")
    else:
        gender = None
    status = st.selectbox("Enter Status", ["Active", "Inactive"], key="status_select")
    total = st.number_input("Enter Total Orders", min_value=0, value=0)

    btn = st.button("Add")
    if btn:
        if custseg=="Individual" and gender=="Select":
            st.error("Please select a valid Gender for Individual customers")
        elif not custname or not email or not phn or not custseg or not status:
            st.error("All required fields must be filled!")
        else:
            existing_cid = check_existing_customer(email)  # Check if email exists
            if existing_cid:
                st.warning(f"Customer already exists with ID: {existing_cid}. Please use 'Orders' to add a purchase!")
            else:
                cid = generate_customer_id()
                mydb = get_db_connection()
                c = mydb.cursor()
                c.execute("INSERT INTO customers (customer_id, customer_name, gender, email_id, phone_number, customer_segment, status, total_orders) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(cid, custname, gender, email, phn, custseg, status, 0))
                mydb.commit()
                mydb.close()
                st.header("Added Successfully")
elif(choice == "🛒 Orders"):
    mydb=get_db_connection()
    df=pd.read_sql("select*from orders",mydb)
    df['order_amount'] = df['order_amount'].round(2)
    st.dataframe(df)
    st.header("Make an Order")

    c = mydb.cursor()
    c.execute("SELECT product_id, product_name, price FROM products")
    products_data = c.fetchall()
    products_list = [(row[1], row[0], row[2]) for row in products_data]  # (product_name, product_id, price)
    product_options = ["Select"] + [row[0] for row in products_list]
    mydb.close()

    search_name = st.text_input("Search Customer by Name", placeholder="e.g., Akshitha or TechCorp")
    customer_id = None
    if search_name:
        mydb = get_db_connection()
        c = mydb.cursor()
        c.execute("SELECT customer_id, customer_name FROM customers WHERE customer_name LIKE %s LIMIT 5", (f"%{search_name}%",))
        results = c.fetchall()
        mydb.close()
        
        if results:
            options = [f"{row[1]} ({row[0]})" for row in results]
            selected = st.selectbox("Select Customer", options)
            customer_id = selected.split("(")[1].strip(")")
        else:
            st.warning("No customers found with that name!")
    # Product selection dropdown
    selected_product = st.selectbox("Select Product", product_options)
    if selected_product == "Select":
        order_amount = st.number_input("Enter Order Amount", min_value=0.0, value=None, step=0.01, placeholder="Enter amount")
    elif selected_product:
        product_info = next((p for p in products_list if p[0] == selected_product), None)
        if product_info:
            order_amount = product_info[2] #Automatically set price
            st.write(f"Selected Product: {selected_product}, Price: ₹{order_amount:.2f}")
        else:
            order_amount = st.number_input("Enter Order Amount", min_value=0.0, value=None, step=0.01, placeholder="Enter amount")
    else:
        order_amount = st.number_input("Enter Order Amount", min_value=0.0, value=None, step=0.01, placeholder="Enter amount")
    quantity = st.number_input("Quantity", min_value=1, step=1)

    order_id = generate_order_id()
    btn = st.button("Order")
    if btn:
        if not customer_id or not selected_product or order_amount is None or not quantity:
            st.error("All fields are required!")
        else:
            insert_order(order_id, customer_id, selected_product, order_amount, quantity)
            st.success(f"Order Added Successfully! {quantity} items recorded.")
            # Update last_order_date and status
            today = datetime.today().date()
            mydb = get_db_connection()
            c = mydb.cursor()

            # Update last_order_date
            c.execute("UPDATE customers SET last_order_date = %s WHERE customer_id = %s", (today, customer_id))

            # Recalculate status: active if ordered today, else inactive
            c.execute("SELECT last_order_date FROM customers WHERE customer_id = %s", (customer_id,))
            last_date = c.fetchone()[0]
            if last_date and (today - last_date).days <= 90:
                new_status = "active"
            else:
                new_status = "inactive"

            # Update status
            c.execute("UPDATE customers SET status = %s WHERE customer_id = %s", (new_status, customer_id))
            mydb.commit()
            mydb.close()
elif(choice == "🛠 Manual overrides"):
    st.header("Manage Customer")
    st.info("Note: Status is auto-managed based on order history. Use this only for manual overrides.")
    customer_id = st.text_input("Enter Customer ID")
    if customer_id:
        customer_df = fetch_customer_by_id(customer_id)
        if not customer_df.empty:
            customer = customer_df.iloc[0]
            # Display current details
            st.subheader("Customer Details")
            st.write(f"Customer ID: {customer['customer_id']}")
            st.write(f"Name: {customer['customer_name']}")
            st.write(f"Gender: {customer['gender']}")
            st.write(f"Email: {customer['email_id']}")
            st.write(f"Phone: {customer['phone_number']}")
            st.write(f"Segment: {customer['customer_segment']}")
            st.write(f"Status: {customer['status']}")
            st.write(f"Total Orders: {customer['total_orders']}")

            st.subheader("Edit Customer Details")
            with st.form(key="edit_customer_form"):
                # Non-editable fields
                st.write(f"Name: {customer['customer_name']} (Cannot be changed)")
                st.write(f"Gender: {customer['gender']} (Cannot be changed)")
                st.write(f"Email: {customer['email_id']} (Cannot be changed)")
                st.write(f"Segment: {customer['customer_segment']} (Cannot be changed)")
                st.write(f"Total Orders: {customer['total_orders']} (Cannot be changed)")
                
                #Editable fields
                edit_phone = st.text_input("Phone Number", value=customer['phone_number'])
                edit_status = st.selectbox("Status", ["Active", "Inactive"],index=["Active", "Inactive"].index(customer['status'])) 
                update_btn = st.form_submit_button(label="Update")
                if update_btn:
                    if len(edit_phone) != 10 or not edit_phone.isdigit():
                        st.error("Phone Number must be exactly 10 digits!")
                    else:
                        mydb = get_db_connection()
                        c = mydb.cursor()
                        c.execute("UPDATE customers SET phone_number=%s, status=%s WHERE customer_id=%s",(edit_phone, edit_status, customer_id))      
                        mydb.commit()
                        mydb.close()
                        st.success("Customer Updated Successfully!")
        else:
            st.error("Customer ID not found!")

elif(choice == "🔁 Returns"):
    mydb=get_db_connection()
    df=pd.read_sql("select*from returns",mydb)
    st.dataframe(df)
    st.header("Add Return")
    with st.form(key="add_return_form"):
            customer_id = ""
            order_id = st.text_input("Order ID")
            product_name = ""
            if order_id:
                try:
                    mydb = get_db_connection()
                    c = mydb.cursor()
                    c.execute("SELECT customer_id, product_name FROM orders WHERE order_id = %s", (order_id,))
                    result = c.fetchone()
                    mydb.close()
                    if result:
                        customer_id = result[0]
                        product_name = result[1]
                        st.success(f"🔍 Product found: {product_name} | Customer ID: {customer_id}")
                    else:
                        st.warning("⚠️ No product found for this Order ID.")
                except Exception as e:
                    st.error("Database error: " + str(e))
            return_qty = st.number_input("Quantity to return", min_value=1, step=1)
            reason = st.text_area("Reason")
            
            # Auto-generated fields
            return_id = generate_return_id()
            return_date = datetime.now().date()  #Current date
            submit_btn = st.form_submit_button(label="Submit Return")
            if submit_btn:
                if not customer_id or not order_id or not product_name or not reason or not return_qty:
                    st.error("All fields are required!")
                elif not check_customer_exists(customer_id) or not check_order_exists(order_id):
                    st.error("Invalid Customer ID or Order ID!")
                else:
                    mydb = get_db_connection()
                    c = mydb.cursor()
                    c.execute("SELECT order_date, quantity FROM orders WHERE order_id = %s", (order_id,))
                    order_result = c.fetchone()
                    if order_result is None:
                        st.error("⚠️ Order ID not found.")
                    else:
                        order_date = order_result[0]
                        ordered_qty = order_result[1]
                        # Check return window (10 days)
                        days_since_order = (datetime.now().date() - order_date).days
                        if days_since_order > 10:
                            st.error(f"⛔ Return window expired. Only allowed within 10 days of order. ({days_since_order} days passed)")
                        else:
                            # Check already returned quantity
                            c.execute("SELECT SUM(return_quantity) FROM returns WHERE order_id = %s AND product_name = %s", (order_id, product_name))
                            return_result = c.fetchone()
                            already_returned = return_result[0] if return_result[0] else 0
                            remaining_qty = ordered_qty - already_returned
                            if return_qty > remaining_qty:
                                st.error(f"❌ You already returned {already_returned} of {ordered_qty} units. You can only return {remaining_qty} more.")
                            else:
                                # Insert valid return
                                insert_return(return_id, customer_id, order_id, product_name, reason, return_date, return_qty)
                                st.success("✅ Return Added Successfully!")
                mydb.close()
                    
elif(choice=="📢 Complaints"):
    mydb=get_db_connection()
    df=pd.read_sql("select*from complaints",mydb)
    st.dataframe(df)
    st.header("file complaint")
    with st.form(key="add_complaint_form"):
            customer_id = st.text_input("Customer ID")
            order_id = st.text_input("Order ID")
            product_name = st.text_input("Product Name")
            complaint = st.text_area("complaint")
            
            # Auto-generated fields
            complaint_id = generate_complaint_id()
            complaint_date = datetime.now().date()#Current date
            
            submit_btn = st.form_submit_button(label="Submit")
            if submit_btn:
                if not customer_id or not order_id or not product_name or not complaint:
                    st.error("All fields are required!")
                elif not check_customer_exists(customer_id) or not check_order_exists(order_id):
                    st.error("Invalid Customer ID or Order ID!")
                else:
                    insert_complaint(complaint_id, customer_id, order_id, product_name, complaint, complaint_date)
                    st.success("Complaint Submitted Successfully!")

elif choice == "📈 Product Insights":
        st.header("Product Insights")
        total_products, top_products_df, return_stats_df, revenue_df = fetch_product_insights()
        
        #Total Products Sold
        st.subheader("Total Unique Products Sold")
        st.write(total_products)
        
        #Top Selling Products
        st.subheader("Top 5 Selling Products")
        st.table(top_products_df)
        
        #Return Stats
        st.subheader("Product Return Statistics")
        if not return_stats_df.empty:
            st.table(return_stats_df)
        else:
            st.write("No returns recorded yet.")
        
        #Revenue by Product
        st.subheader("Revenue by Product")
        st.table(revenue_df)

elif choice == "📊 Dashboards":
        st.header("Dashboards")
        mydb = get_db_connection()
        df = pd.read_sql("SELECT * FROM customers", mydb)
        segments_df, orders_df, returns_df, top_products_df = fetch_dashboard_data()
        mydb.close()
        
        #Pie Chart: Customer Segments
        st.subheader("Customer Segments Distribution")
        if not segments_df.empty:
            fig_segments = px.pie(segments_df, values='count', names='customer_segment', 
                                 title="Customer Segments")
            st.plotly_chart(fig_segments)
        else:
            st.write("No customer data available.")

        if not df.empty:
            gender_df = df[df['gender'].notnull()].groupby('gender').size().reset_index(name='count')
            st.subheader("🧍 Gender Distribution")
            fig1 = px.pie(gender_df, names='gender', values='count', title="Customers by Gender")
            st.plotly_chart(fig1)
        else:
            st.write("No customer data available.")

        st.subheader("📈 Sales Over Time")
        mydb=get_db_connection()
        sales_df = pd.read_sql("""
            SELECT order_date, SUM(order_amount * quantity) as total_sales
            FROM orders
            GROUP BY order_date
            ORDER BY order_date
        """, mydb)
        sales_df['total_sales'] = sales_df['total_sales'].round(2)
        fig = px.line(
            sales_df,
            x='order_date',
            y='total_sales',
            title='📆 Daily Sales Trend',
            labels={'order_date': 'Date', 'total_sales': 'Total Sales (₹)'},
            markers=True
        )
        st.plotly_chart(fig)
        mydb.close()
        
        # bar graph: activity status
        st.header("📊 Customer Activity Status")
        mydb=get_db_connection()
        df = pd.read_sql("SELECT status FROM customers", mydb)
        mydb.close()
        # Count active vs inactive
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        # Bar graph
        fig = px.bar(
            status_counts, 
            x='Status', 
            y='Count', 
            color='Status',
            color_discrete_map={"active": "#28a745", "inactive": "#dc3545"},
            title="Active vs Inactive Customers",
            labels={'Count': 'Number of Customers'}
        )
        st.plotly_chart(fig)
        
        #Bar Graph: Top Selling Products
        st.subheader("Top 5 Selling Products")
        if not top_products_df.empty:
            fig_top_products = px.bar(top_products_df, x='product_name', y='order_count', 
                                     title="Top Selling Products", labels={'order_count': 'Order Count'})
            st.plotly_chart(fig_top_products)
        else:
            st.write("No order data available.")
        
        #Pie Chart: Return Reasons
        st.subheader("Return Reasons Breakdown")
        mydb = get_db_connection()
        returns_df = pd.read_sql("SELECT reason FROM returns", mydb)
        mydb.close()
        if not returns_df.empty:
            text = " ".join(returns_df['reason'].dropna())
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            st.subheader("🌀 Word Cloud of Return Reasons")
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.write("No return data available.")

elif choice == "📉 Customer Stats":
    stats_choice = st.radio("Choose Stats", 
                                    ["Top Customers", "Segment Stats", "Customer Trends"])

    #Fetch Data
    customer_df = fetch_customer_stats_data()
    current_date = datetime.now().date()
    current_year = current_date.year
    if stats_choice == "Top Customers":
        choice2=st.radio("choose",["By Revenue","By Orders"])
        if choice2 == "By Revenue":
            # Filter for this month (example period)
            this_month_start = current_date.replace(day=1)
            top_customers_df = customer_df[customer_df['order_date'] >= pd.Timestamp(this_month_start)].groupby('customer_id')['total_amount'].sum().reset_index()
            top_customers_df = top_customers_df.sort_values('total_amount', ascending=False).head(5)

            #Bar Graph
            if not top_customers_df.empty:
                fig = px.bar(top_customers_df, x='customer_id', y='total_amount',title="Top 5 Customers This Month by Revenue",labels={'total_amount': 'Total Revenue (₹)', 'customer_id': 'Customer ID'})        
                st.plotly_chart(fig)
                st.write(top_customers_df)
            else:
                st.write("No data available for top customers.")
        if choice2 == "By Orders":
            mydb = get_db_connection()
            df = pd.read_sql("SELECT customer_id, customer_name, total_orders FROM customers ORDER BY total_orders DESC LIMIT 5", mydb)
            mydb.close()

            def highlight_rank(row):
                rank = row.name
                if rank == 0:
                    return ['background-color: gold; color: black'] * len(row)
                elif rank == 1:
                    return ['background-color: silver; color: black'] * len(row)
                elif rank == 2:
                    return ['background-color: #cd7f32; color: white'] * len(row)
                else:
                    return ['background-color: #f0f0f0; color: black'] * len(row)

            styled_top5 = df.style.apply(highlight_rank, axis=1)
            st.dataframe(styled_top5)

    # Segment Stats
    elif stats_choice == "Segment Stats":
        st.header("Customer Segment Stats")
    
        #Filter for this year (example period)
        segment_df = customer_df[customer_df['order_date'].dt.year == current_year].groupby('customer_segment').agg(total_revenue=('total_amount', 'sum'),order_count=('order_count', 'sum')).reset_index()
        
        # Pie Chart for Revenue
        if not segment_df.empty:
            fig = px.pie(segment_df, values='total_revenue', names='customer_segment',title="Revenue Distribution by Customer Segment (This Year)")         
            st.plotly_chart(fig)
            st.write(segment_df)#Display table
        else:
            st.write("No data available for segment stats.")
    #customer trends(searchable)
    elif stats_choice == "Customer Trends":
        st.header("Customer Order Trends")
        # Search by Customer ID
        customer_id = st.text_input("Enter Customer ID (e.g., CUST001)", "")
        if customer_id:
            trends_df = customer_df[customer_df['customer_id'] == customer_id]
            if not trends_df.empty:
                # Monthly trends for the customer
                trends_df = trends_df.groupby(trends_df['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
                trends_df['order_date'] = trends_df['order_date'].astype(str)
                #Line Graph
                fig = px.line(trends_df, x='order_date', y='total_amount',title=f"Monthly Revenue Trend for {customer_id}",markers=True, labels={'order_date': 'Month', 'total_amount': 'Revenue (₹)'})           
                st.plotly_chart(fig)
                st.write(trends_df)
            else:
                st.error("Customer ID not found or no data available.")
        else:
            st.write("Please enter a Customer ID to view trends.")

elif choice == "📝 Feedbacks":
    st.header("Customer Feedback")
    menu = st.radio("Options", ["Submit Feedback", "View Feedbacks"])
    if menu == "Submit Feedback":
        order_id = st.text_input("Enter Order ID")
        customer_id = ""
        product_name = ""
        if order_id:
            try:
                mydb = get_db_connection()
                c = mydb.cursor()
                c.execute("SELECT customer_id, product_name FROM orders WHERE order_id = %s", (order_id,))
                result = c.fetchone()
                mydb.close()
                if result:
                    customer_id = result[0]
                    product_name = result[1]
                    st.success(f"🧾 Order found!\n\nCustomer ID: {customer_id}\nProduct: {product_name}")
                else:
                    st.warning("⚠️ No order found with this Order ID.")
            except Exception as e:
                st.error("❌ Database error: " + str(e))

        rating = st.slider("⭐ Rate the product", 1, 5)
        comment = st.text_area("📝 Your feedback")
        if st.button("Submit Feedback"):
            if not order_id or not customer_id or not product_name or not comment:
                st.error("❌ All fields are required!")
            else:
                insert_feedback(customer_id, order_id, product_name, rating, comment)
                st.success("✅ Feedback submitted successfully!")
    elif menu == "View Feedbacks":
        mydb = get_db_connection()
        df = pd.read_sql("SELECT * FROM feedback ORDER BY feedback_date DESC", mydb)
        mydb.close()

        st.subheader("📋 All Feedbacks")
        st.dataframe(df)
        if not df.empty:
            avg_rating = df['rating'].mean()
            st.markdown(f"**📊 Average Rating:** ⭐ {avg_rating:.2f}")

elif choice == "💰 Customer CLV":
    st.header("Customer Lifetime Value (CLV)")
    mydb = get_db_connection()
    df = pd.read_sql("""
        SELECT o.customer_id, c.customer_name,
               SUM(o.order_amount * o.quantity) AS total_spent,
               COUNT(DISTINCT o.order_id) AS total_orders,
               DATEDIFF(MAX(o.order_date), MIN(o.order_date)) / 30.0 AS months_active
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY o.customer_id, c.customer_name
    """, mydb)
    mydb.close()
    if not df.empty:
        df['avg_order_value'] = df['total_spent'] / df['total_orders']
        df['purchase_frequency'] = df['total_orders'] / df['months_active'].replace(0, 1)
        df['clv'] = df['avg_order_value'] * df['purchase_frequency'] * 6
        st.dataframe(df[['customer_id', 'customer_name', 'total_spent', 'total_orders', 'months_active', 'clv']].round(2))

elif choice == "🔎 Search & Filter":
    st.header("Search & Filter Customers")
    mydb = get_db_connection()
    df = pd.read_sql("SELECT * FROM customers", mydb)
    mydb.close()
    name_search = st.text_input("Search by Name")
    email_search = st.text_input("Search by Email")
    segment_filter = st.selectbox("Filter by Segment", ["All"] + df['customer_segment'].unique().tolist())
    if name_search:
        df = df[df['customer_name'].str.contains(name_search, case=False, na=False)]
    if email_search:
        df = df[df['email_id'].str.contains(email_search, case=False, na=False)]
    if segment_filter != "All":
        df = df[df['customer_segment'] == segment_filter]
    st.dataframe(df)

elif choice == "📤 Export Data":
    st.header("Export Data to CSV")
    export_option = st.selectbox("Select Table to Export", ["customers", "orders", "returns", "complaints", "feedback"])
    if export_option:
        mydb = get_db_connection()
        df = pd.read_sql(f"SELECT * FROM {export_option}", mydb)
        mydb.close()
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download {export_option.capitalize()} Data as CSV",
            data=csv,
            file_name=f"{export_option}_data.csv",
            mime='text/csv')
        
elif choice == "🚚 Order Status":
    st.header("Track or Update Order Status")
    mydb = get_db_connection()
    c = mydb.cursor()
    df = pd.read_sql("SELECT * FROM orders", mydb)
    mydb.close()
    st.dataframe(df[['order_id', 'customer_id', 'product_name', 'order_date', 'delivery_status']])
    order_id = st.text_input("Enter Order ID")
    new_status = st.selectbox("Select New Status", ["Pending", "Shipped", "Delivered", "Cancelled"])
    if st.button("Update Status"):
        mydb = get_db_connection()
        c = mydb.cursor()
        c.execute("UPDATE orders SET delivery_status = %s WHERE order_id = %s", (new_status, order_id))
        mydb.commit()
        mydb.close()
        st.success(f"Order {order_id} delivery_status updated to '{new_status}'")

elif choice == "🔔 Notify Customers":
    import smtplib
    from email.message import EmailMessage
    st.header("📢 Send Email Notification to Customer")
    # Connect to database and fetch customers
    mydb = get_db_connection()
    df = pd.read_sql("SELECT * FROM customers", mydb)
    mydb.close()
    if not df.empty:
        # Build customer selection dropdown
        df['customer_display'] = df['customer_name'] + " (" + df['customer_id'].astype(str) + ")"
        selected_customer = st.selectbox("Select Customer", df['customer_display'])
        # Extract name and ID
        name = selected_customer.split(" (")[0]
        cid = selected_customer.split("(")[1].strip(")")
        # Try to get customer email from DataFrame
        if 'email' in df.columns:
            customer_email = df[df['customer_id'] == int(cid)]['email'].values[0]
        else:
            customer_email = st.text_input("Enter customer's email address")
            
        message = st.text_area("✉️ Message to Send")

        #replace with your email and generated gmail app password
        sender_email = "yourgmail@gmail.com"         #Replace with your gmail
        app_password = "your_gmail_app_password"     #replace with your app password
        if st.button("📤 Send Email"):
            if not customer_email:
                st.error("❌ Please enter customer's email address.")
            elif not message:
                st.error("❌ Message content cannot be empty.")
            else:
                try:
                    # Compose email
                    msg = EmailMessage()
                    msg['Subject'] = "Notification from Customer Management Team"
                    msg['From'] = sender_email
                    msg['To'] = customer_email
                    msg.set_content(f"Dear {name},\n\n{message}\n\nThanks,\nCustomer Management Team")
                    # Send email
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(sender_email, app_password)
                        smtp.send_message(msg)
                    st.success(f"✅ Email successfully sent to {name} ({customer_email})")
                    st.info(f"📨 Message Preview:\n\nDear {name},\n{message}\n\nThanks,\nCustomer Management Team")
                except Exception as e:
                    st.error("❌ Failed to send email: " + str(e))

elif choice == "🧾 Activity Log":
    st.header("Recent Activity Log")
    st.caption("Shows recent orders, returns, and complaints")
    mydb = get_db_connection()
    orders_df = pd.read_sql("SELECT order_id, customer_id, product_name, order_date FROM orders ORDER BY order_date DESC LIMIT 10", mydb)
    returns_df = pd.read_sql("SELECT return_id, customer_id, product_name, return_date FROM returns ORDER BY return_date DESC LIMIT 10", mydb)
    complaints_df = pd.read_sql("SELECT complaint_id, customer_id, product_name, complaint_date FROM complaints ORDER BY complaint_date DESC LIMIT 10", mydb)
    mydb.close()
    st.subheader("🛒 Latest Orders")
    st.dataframe(orders_df)
    st.subheader("🔄 Latest Returns")
    st.dataframe(returns_df)
    st.subheader("⚠️ Latest Complaints")
    st.dataframe(complaints_df)

elif choice == "💳 Payment":
    st.header("💳 Payment Gateway Simulation")
    st.markdown("""
        <div style='text-align: center;'>
            <h3>Scan the UPI QR Code to Make a Payment</h3>
            <p><em>This is a demo payment simulation screen.</em></p>
        </div>
    """, unsafe_allow_html=True)
    import segno
    upi_link = "upi://pay?pa=yourupi@okaxis&pn=YourName&cu=INR" #paste your upi ID here to scan
    qrcode = segno.make(upi_link)
    qrcode.save("upi_qr.png", scale=5)
    st.image("upi_qr.png", caption="Scan to Pay", use_container_width=False)
    if st.button("💸 Simulate Payment"):
        st.success("✅ Payment received successfully!")

elif choice == "📞 Contact":
    st.header("📞 Contact Details")
    st.markdown("""
    <div style='padding: 1rem; background-color: #ffffffdd; border-radius: 10px;'>
        <h4>📱 Phone Numbers</h4>
        <ul>
            <li>support: +91 98765 xxxxx</li>
            <li>         +91 91234 xxxxx</li>
        </ul>
        <h4>📧 Email</h4>
        <ul>
            <li>akshitha.project@example.com</li>
            <li>support@example.com</li>
        </ul>
        <h4>📍 Address</h4>
        <p>xxxxx xxxxxxx xxxxxx,<br>xxxx xxx xx,<br>Hyderabad, India</p>
    </div>
    """, unsafe_allow_html=True)






                     

    
                                     
    
    
        

