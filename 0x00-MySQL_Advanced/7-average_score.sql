-- Create a stored procedure to compute and store the average score for a student
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Declare variables
    DECLARE total_score INT;
    DECLARE num_corrections INT;
    DECLARE average_score FLOAT;
    
    -- Calculate total score and number of corrections
    SELECT SUM(score), COUNT(*) INTO total_score, num_corrections
    FROM corrections
    WHERE user_id = user_id;
    
    -- Calculate the average score
    IF num_corrections > 0 THEN
        SET average_score = total_score / num_corrections;
    ELSE
        SET average_score = 0;
    END IF;
    
    -- Update the average_score in the users table
    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END //
DELIMITER ;
