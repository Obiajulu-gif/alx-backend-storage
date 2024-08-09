-- 7. Average score

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Calculate the average score for the given user_id
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average_score in the users table for the given user_id
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;

END$$
DELIMITER ;
