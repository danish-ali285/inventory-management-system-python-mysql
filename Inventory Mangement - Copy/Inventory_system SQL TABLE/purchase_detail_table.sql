CREATE TABLE purchase_details(
	purchase_details_id INT PRIMARY KEY AUTO_INCREMENT,
    purchase_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    unit_price DECIMAL (10,2),
    
    FOREIGN KEY(purchase_id) REFERENCES purchases(purchase_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);