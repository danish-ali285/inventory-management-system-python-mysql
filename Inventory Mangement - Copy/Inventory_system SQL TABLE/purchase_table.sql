CREATE TABLE purchases(
	purchase_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_id INT NOT NULL,
	total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    purchase_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(supplier_id) REFERENCES suppliers (supplier_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);