CREATE TABLE Customers(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL
);

CREATE TABLE Orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE TABLE InventoryLog(
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    change INTEGER,
    log_date TEXT,
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE INDEX idx_customer_id ON Orders(customer_id);
CREATE INDEX idx_product_id ON Orders(product_id);
CREATE INDEX idx_inventory_product ON InventoryLog(product_id);