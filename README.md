# Swiss System Tournament Project
This is a class project for [Intro to Relational Databases](https://classroom.udacity.com/courses/ud197). 
It is not intended for practical use.

A _Swiss system tournament_ is a tournament consisting of two-player matches, 
such that every player plays in every round, against another player who is 
adjacent in the standings. This project facilitates a Swiss system tournament 
by storing player names and match results, displaying standings, and 
determining which players should meet in each round. Names and results are 
stored in a database, so they are saved automatically, and persist even if the 
computer is rebooted.

# Prerequisites
To use this software, you must have Python and PostgreSQL on your system.

# Installation
Copy all files into a folder.

# Suggested usage
Before starting a tournament, be sure you have an even number of players. 

You will interact with the database primarily by executing Python functions. 
Refer to tournament.py to see which arguments should be passed to each 
function.

I recommend using two command-line windows.

1. Browse to the folder that contains the project files. In the first window, type `psql`.
2. At the psql prompt, type `\i tournament.sql` to create the database.
3. In the second window, type `python`.
4. At the Python prompt, call `registerPlayer()` once for each player.
5. At the Python prompt, call `swissPairings()` to see which players should 
play each other. This function outputs a list of tuples. Each tuple contains 
the names and IDs of two players.
6. Play the matches output in step 5. For each match, record the results by 
calling `reportMatch()` from the Python prompt.
7. If a match is recorded incorrectly, use `unreportMatch()` to erase it.
8. From the psql prompt, type `select * from records;` to view the standings. 
(This is more readable than the output of `playerStandings()`).
9. Repeat steps 5 through 8 as many times as desired. Note that if you have 
2<sup>_n_</sup> players, then after _n_ rounds there will be a single undefeated 
player. If the number of players is between  2<sup>_n_</sup> and 2<sup>_n_+1</sup>, 
it may take _n_ or _n_+1 rounds until there is only one undefeated player.
10. If you wish to reuse the database for another tournament, call 
`deleteMatches()` from the Python prompt. This will delete all matches, but 
keep all players.
11. From the Python prompt, call `deletePlayer()` for each player that will 
not be playing in the next tournament, and call `registerPlayer()` for each 
new player. Again, make sure you have an even number of players.
12. Go back to step 5.

# Limitations
The limitations are due to the structure of the database: 

- There is no way to record a match that results in a tie.
- There is no way to deactivate a player who drops out of the tournament 
early. In order to delete a player from the database, you must also delete all 
matches that player has played, and that will affect the win-loss records of 
the remaining players.
- For each match, only the winner and loser is stored; there is no way to 
store other data such as the date, time, or score of the match.

# Nonstandard usage
The software does not enforce the rules of the Swiss system. In particular,

- It is possible to have an odd number of players. In this case, 
`swissPairings()` will omit the player who is last in the standings.
- It is possible to start another round (i.e. call `swissPairings()` again) 
before recording all matches specified by the last call to `swissPairings()`.
- It is possible to record matches that were not specified by `swissPairings()`.
- It is possible to add or remove players during the tournament.

# Ordering the standings
The order of the standings is important, because it determines the pairings. This 
project orders the standings by number of wins, descending, as specified by the 
instructor. Players with the same number of wins are order by number of losses, 
ascending.

Nonstandard usage makes it possible for different players to have very different 
numbers of matches. For example, Robin could have 3 wins and 7 losses at the same 
time that Taylor has 2 wins and 0 losses. In this case Robin will appear above 
Taylor in the standings. This will look strange if you are used to standings that 
are ordered by win percentage. This problem will not arise if you follow the 
suggested usage, because the number of matches played by two players will differ 
by at most 1. In this case, a player with a higher win percentage will always 
appear higher in the standings.