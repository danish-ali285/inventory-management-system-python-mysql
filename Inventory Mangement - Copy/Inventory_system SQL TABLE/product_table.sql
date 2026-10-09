CREATE TABLE products(
 product_id INT PRIMARY KEY AUTO_INCREMENT,
 product_name VARCHAR(100),
 category VARCHAR(100),
 price DECIMAL (10,2) NOT NULL,
 quantity INT NOT NULL DEFAULT 0,
 supplier_id INT,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 
 FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
 ON DELETE SET NULL
 ON UPDATE CASCADE
);