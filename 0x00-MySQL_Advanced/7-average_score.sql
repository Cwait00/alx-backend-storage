DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id_param INT)
BEGIN
    DECLARE user_score FLOAT;
    
    -- Compute average score for the given user_id
    SELECT AVG(score) INTO user_score
    FROM corrections
    WHERE user_id = user_id_param;
    
    -- Update average_score for the given user_id
    UPDATE users
    SET average_score = user_score
    WHERE id = user_id_param;
    
END //

DELIMITER ;
