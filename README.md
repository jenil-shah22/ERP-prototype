# ERP System Prototype

## 1. Company Assessment
Based on the provided Excel management report, the current workflow at Amba Enterprises relies heavily on manual spreadsheet tracking. While this method works for basic record keeping, it introduces several operational challenges.
Some of the key issues identified are:
- High probability of human error due to manual data entry  
- Lack of real-time visibility into product inventory and order status  
- Difficulty maintaining a structured workflow for tracking orders and stock movement  
The objective of this project is to design a lightweight ERP prototype that improves data organization, introduces automation, and provides a scalable structure for future development.

## 2. Build vs Buy Strategy

### Recommendation: Build a Lightweight Custom ERP
Considering the constraints of a small development team and the need for cost-effective implementation, building a custom solution using Python is a practical choice.
**Cost**  
Using open-source technologies such as Python and Streamlit eliminates licensing costs associated with commercial ERP platforms.
**Speed**  
A custom Python solution allows rapid development and can directly automate the existing Excel-based workflows used by the company.
**Future-Proofing**  
A custom system provides flexibility to integrate future technologies such as AI models, intelligent search, or automated order processing using LLMs.

### Key Advantages
- Open-source tools keep costs minimal  
- Easier customization according to business requirements  
- Faster development cycle compared to large ERP systems  
- Flexible architecture that allows future integrations

## 3. System Architecture

### Technology Stack
**Frontend:** Streamlit (rapid user interface development)  
**Backend:** Python (business logic and API simulation)  
**Database (Proposed):** SQLite (lightweight relational database)  
**Data Source:** Reference dataset derived from the provided Excel file

### Design Overview
The prototype uses Streamlit to create a simple interactive interface and Python to simulate backend logic.  
Although the current prototype does not connect to a live database, the architecture is designed assuming a relational database such as SQLite will manage structured data.

### High-Level System Flow
User (Streamlit Interface)  
↓  
Python Backend (Validation + Processing Logic)  
↓  
SQLite Database (Proposed Storage Layer)  
↓  
Future Integrations (AI Modules / Power Automate)

## 4. Database Design
The database schema models the lifecycle of products from inventory storage to customer order fulfillment. The system separates **master data** (customers, products) from **transactional data** (orders and inventory logs).

```sql
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE TABLE InventoryLog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    change INTEGER,
    log_date TEXT,
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE INDEX idx_customer_id ON Orders(customer_id);
CREATE INDEX idx_product_id ON Orders(product_id);
CREATE INDEX idx_inventory_product ON InventoryLog(product_id);
```

## 5. Detailed Implementation Flow

This section explains how the system processes the most common operation in the ERP system: **creating a new sales order**. The goal is to demonstrate how the frontend interface interacts with backend logic and how the database would be updated in a real ERP environment.

### Workflow Steps
1. ***User Submission**
The user enters the **Customer Name**, selects a **Product**, and specifies the **Quantity** through the Streamlit interface.

2. **Validation**
Before processing the order, the system performs basic validation checks:
- Ensures the customer name field is not empty  
- Verifies that the requested quantity does not exceed the available inventory stock  
If validation fails, the system displays an error message in the UI.

3. **Order Processing (Simulated Transaction)**
Once validation succeeds, the system generates SQL operations that would normally run in the backend database.

**Step A — Insert Order Record**
A new entry is added to the `Orders` table containing the customer ID, product ID, quantity, and timestamp.

**Step B — Update Product Inventory**
The stock level of the selected product is reduced according to the ordered quantity.
Example logic:new_stock = old_stock - ordered_quantity

**Step C — Log Inventory Movement**
A new entry is added to the `InventoryLog` table to maintain a record of stock movement for auditing and tracking purposes.

4. **System Feedback**
After processing the order, the system provides confirmation to the user and displays the SQL queries that would normally be executed in the database.

### REST API Simulation
In a full production system, the frontend would communicate with a backend service (such as **FastAPI** or **Flask**) through REST APIs.
For this prototype, the process is simulated but follows the same architectural logic.
**Endpoint**

**Request JSON Example**
```json
{
  "customer_name": "Customer 1",
  "product_name": "Transformer Core",
  "quantity": 5
}
```
**Response JSON Example**

```json
{
  "status": "success",
  "message": "Order processed successfully"
}
```
## Live Application

**Streamlit Cloud URL**
https://REPLACE_WITH_YOUR_STREAMLIT_APP_URL.streamlit.app


## Local Setup Instructions
Follow these steps to run the project locally on your machine.

```bash
git clone <your-repository-link>
cd <repository-folder-name>
pip install -r requirements.txt
pip install streamlit pandas
streamlit run app.py
```