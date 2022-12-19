DROP TABLE IF EXISTS teams, players, statistic;

CREATE TABLE teams (
	team_id INTEGER NOT NULL,
	team_name VARCHAR(50) NOT NULL,
	team_country VARCHAR(100) NOT NULL
);

CREATE TABLE players (
	player_id INTEGER NOT NULL,
	team_id INTEGER,
	player_name VARCHAR(50) NOT NULL,
	player_country VARCHAR(100) NOT NULL
);

CREATE TABLE statistic (
	stat_id INTEGER NOT NULL,
	player_id INTEGER NOT NULL,
	score FLOAT NOT NULL,
	date DATE NOT NULL
);

ALTER TABLE teams
 ADD CONSTRAINT PK_team_id
  PRIMARY KEY (team_id);

ALTER TABLE players
 ADD CONSTRAINT PK_player_id
  PRIMARY KEY (player_id);
  
ALTER TABLE players
 ADD CONSTRAINT FK_CurrentTeam
  FOREIGN KEY (team_id) REFERENCES teams(team_id);
 
ALTER TABLE statistic
 ADD CONSTRAINT PK_stat_id
  PRIMARY KEY (stat_id);
  
ALTER TABLE statistic
 ADD CONSTRAINT FK_PlayerStat
  FOREIGN KEY (player_id) REFERENCES players(player_id);
