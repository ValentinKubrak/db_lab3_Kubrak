DO $$
	DECLARE
		TestTeam_name team.team_name%TYPE;
		team_country team.country%TYPE;
		
	BEGIN
		TestTeam_name := 'TestTeam_';
		team_country := 'TestCountry_';
		FOR counter IN 1..5
			LOOP
				INSERT INTO team (team_id, team_name, country)
            		VALUES (counter + 7, TestTeam_name || counter, team_country || counter);
        	END LOOP;
 END;
 $$