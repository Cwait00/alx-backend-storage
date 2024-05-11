-- Procedure: ComputeAverageScoreForUser
-- Description: This procedure computes and stores the average score for a specified user.
-- Input: user_id - The ID of the user for whom the average score is to be computed.
-- Output: None

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Declare variables
    DECLARE total_score DECIMAL(10, 2);
    DECLARE num_corrections INT;
    DECLARE average_score DECIMAL(10, 2);
    
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
