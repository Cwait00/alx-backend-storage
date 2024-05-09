-- Create a stored procedure to add a bonus correction
DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    -- Declare variables
    DECLARE project_id INT;
    
    -- Check if the project exists
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    
    -- If the project exists, add the correction
    IF project_id IS NOT NULL THEN
        INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
    ELSE
        -- If the project does not exist, create it and then add the correction
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
        INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
    END IF;
END //
DELIMITER ;
