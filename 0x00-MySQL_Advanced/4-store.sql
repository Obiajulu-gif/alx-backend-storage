-- 4. Buy buy buy
-- Write a SQL script that creates a trigger that decreases the quantity of an item after adding a new order.

DROP TRIGGER IF EXISTS after_order_insert;
DELIMITER $$

-- Creating a triggrt
CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
-- Go to the items table
-- and decrease the quantity of item by new number inserted in order table
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END$$

DELIMITER ;
