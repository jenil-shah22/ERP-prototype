import streamlit as st
import pandas as pd
from datetime import datetime
st.set_page_config(page_title="ERP Prototype",layout="wide")
if 'inventory_df'not in st.session_state:
    inventory_data={
        "Product ID":[1,2,3,4],
        "Product Name":["Transformer Core","Motor Stamping","Copper Coil","Steel Lamination"],
        "Stock":[120,80,200,150],
        "Price":[500,350,150,200]
    }
    st.session_state.inventory_df=pd.DataFrame(inventory_data)
def api_create_order(customer_name,product_name,quantity):
    if not customer_name.strip():
        return {"status":400,"message":"Customer name is required"}
    product_row=st.session_state.inventory_df[st.session_state.inventory_df["Product Name"]==product_name]
    current_stock=product_row["Stock"].values[0]
    product_id=product_row["Product ID"].values[0]
    if quantity>current_stock:
        return{"status":400,"message":f"Insufficient stock. Available:{current_stock}"}
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_script=f"""
INSERT INTO Orders(customer_id,product_id,quantity,order_date)
VALUES(
    (SELECT customer_id FROM Customers WHERE name='{customer_name}'),
    {product_id},
    {quantity},
    '{timestamp}'
);
UPDATE Products SET stock=stock - {quantity} WHERE product_id={product_id};
INSERT INTO InventoryLog(product_id,change,log_date)
VALUES({product_id},{quantity},'{timestamp}');
    """
    return {
        "status":201, 
        "message":"Order processed successfully", 
        "sql":sql_script,
        "data":{"customer":customer_name,"product":product_name,"qty":quantity}
    }
st.title("ERP Prototype")
st.subheader("Inventory Status")
st.table(st.session_state.inventory_df)
st.markdown("---")
st.subheader("Create New Order")
col1, col2 = st.columns(2)
with col1:
    cust_input=st.text_input("Customer Name")
    prod_input=st.selectbox("Select Product",st.session_state.inventory_df["Product Name"])
    qty_input=st.number_input("Quantity",min_value=1, step=1)
with col2:
    st.write("API Preview")
    st.json({
        "customer_name":cust_input,
        "product_name":prod_input,
        "quantity":qty_input
    })
if st.button("Submit Order"):
    response = api_create_order(cust_input, prod_input, qty_input)
    if response["status"]==201:
        st.success(f"{response['message']}")
        st.write("Database Transaction:")
        st.code(response["sql"],language="sql")
    else:
        st.error(f"Error {response['status']}: {response['message']}")