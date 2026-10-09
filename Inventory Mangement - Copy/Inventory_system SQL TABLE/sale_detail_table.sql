CREATE TABLE sale_details(
	sale_deatil_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL ,
    
    FOREIGN KEY(sale_id) REFERENCES sales (sale_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);