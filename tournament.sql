-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

create table IF NOT EXISTS players (
	player_id serial primary key,
	name text
);
create table IF NOT EXISTS matches (
	match_id serial primary key,
	winner int references players(player_id),
	loser int references players(player_id)
);
CREATE OR REPLACE view wins as
	select players.player_id, players.name, count(matches.winner) as wins 
	from players left join matches
	on players.player_id = matches.winner
	group by players.player_id
;
CREATE OR REPLACE view  losses as
	select players.player_id, players.name, count(matches.loser) as losses 
	from players left join matches
	on players.player_id = matches.loser
	group by players.player_id
;	
CREATE OR REPLACE view records as	
	select wins.player_id, wins.name, wins, losses, 
		wins + losses as matches
	from wins inner join losses
	on wins.player_id = losses.player_id
	order by wins desc, losses asc
;