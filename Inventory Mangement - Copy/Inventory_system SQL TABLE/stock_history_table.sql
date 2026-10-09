CREATE TABLE stock_history(
	stock_history_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    transcation_type VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    previous_quantity INT NOT NULL,
    new_quantity INT NOT NULL,
    trascation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id ) REFERENCES products(product_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);