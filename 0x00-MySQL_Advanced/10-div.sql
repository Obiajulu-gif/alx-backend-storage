-- 10-div.sql

DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE result FLOAT;
    IF b = 0 THEN
        RETURN 0;
    ELSE
        SET result = a / b;
        RETURN result;
    END IF;
END //

DELIMITER ;
