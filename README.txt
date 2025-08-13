TITLE : CUSTOMER MANAGEMENT SYSTEM WEB APPLICATION
Developer : Akshitha

🟢 Objective : 
The objective of this project is to build a web-based Customer Management System that allows a business or seller to manage their customers, orders, returns, complaints, feedback, and various analytics in one place. The system provides interactive dashboards, secure login, and modern UI to simulate a real-world business management tool.

● MODULES IMPLEMENTED:
  1. Login Authentication
     Users must log in using credentials stored in the database.
     Prevents unauthorized access.
  2. Home Dashboard
     • Shows summary of:
         Total customers
         Total orders
         Total revenue
         Net revenue (after returns)
     • Uses styling and WhatsApp floating contact button.
  3. Customer Management
      • Add new customers with email, phone, gender, and segment.
      • View all customers table (status highlighted).
      • Manual overrides to update phone number or status.
      • Auto-calculates and updates Active/Inactive status based on last order.
  4. Order Management
      • Add new orders by selecting product and customer.
      • Price auto-fills from product table.
      • Quantity entered by user.
      • Automatically updates:
          • last_order_date
          • Customer status
      • Invoice generation and PDF download (optional).
  5. Returns Management
      • Customer can return full or partial product.
      • Allows only return of quantity <= ordered - already returned.
      • Includes 10-day return limit check.
      • Prevents duplicate or invalid returns.
  6. Complaints Management
      • Records customer complaints with order details.
      • Displays recent complaints.
  7. Product Insights
      • Total unique products sold.
      • Top selling products.
      • Products with most returns.
      • Revenue generated per product.
  8. Dashboards
      • Pie chart of customer segments.
      • Gender distribution.
      • Line chart of sales over time.
      • Bar chart: Active vs Inactive customers.
      • Word cloud: Common return reasons.    
  9. Customer Stats
      • Top 5 customers by orders or revenue.
      • Revenue distribution by segment.
      • Monthly customer trend for specific ID.
  10. Feedback System
      • Submit feedback (1–5 star rating + comment).
      • View feedback with average score.
  11. Customer Lifetime Value (CLV)
      • Calculates CLV based on:
      • Average Order Value
      • Frequency
      • Active months
      • Shows top valuable customers.
  12. Search & Filter
      • Search customers by name, email.
      • Filter by customer segment. 
  13. Export Data
      • Export any table (customers, orders, returns, complaints, feedback) to CSV.
  14. Order Status Tracking
      • View all orders with delivery status.
      • Manually update status (Pending, Shipped, Delivered, Cancelled).
  15. Notifications
      • Simulate sending notification to customer.
      • Message preview shown.
  16. Activity Log
      Shows 10 most recent:
       • Orders
       • Returns
       • Complaints
  17. Payment Simulation
      • Generates UPI QR code.
      • Simulates payment with confirmation. 
  18. Contact Page
      • Contact numbers, emails, address.

🔵 USER INTERFACE DESIGN:
   Sidebar with icons and color styling.
   Page background: Gradient blue.
   Sidebar background: Light blue.
   Buttons and inputs: Custom styled.

🔵 DATABASE USED: MySQL:
   Tables used:
   • customers
   • orders
   • returns
   • feedback
   • complaints
   • products
   • users (for login) 

🔵 VALIDATION AND LOGIC: 
   • Phone number: 10 digits only
   • Email: Valid format check
   • Product name & customer ID auto-fill from order ID
   • Return only possible within 10 days
   • Quantity-based return validation  

🔵 ADVANCED FEATURES:
   • Customer status automatically updates based on last order
   • CLV (Customer Lifetime Value) calculated
   • Word cloud for return reasons
   • Realistic order flow and return window

● CONCLUSION:
  This project helped me build a complete Customer Management System using Python, Streamlit, and MySQL. I designed this application to handle real-life needs like managing customers,      orders, returns, feedback, and tracking overall business performance — all from one simple dashboard.
  While working on it, I tried to include features that are usually found in modern business tools — like login authentication, customer lifetime value, return logic, dashboards, payment  simulation, and even WhatsApp support. Some parts are kept manual (like delivery status) because this is a project, not a live business with real delivery systems.
 This project not only helped me improve my technical skills but also gave me confidence to think like a real developer — how users interact, what data they need, and how to make the interface simple and useful. I also learned how important user experience and design are in making a project easy to use.
 Overall, I really enjoyed building this system, and I believe it’s a strong example of what I’ve learned so far in my training.
              



























  