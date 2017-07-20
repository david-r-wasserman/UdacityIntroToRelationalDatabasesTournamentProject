#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database
    connection.
    """
    try:
        return psycopg2.connect("dbname=tournament")
    except psycopg2.OperationalError:
        print("Tournament database does not exist.")
        print("Follow these instructions to create it:")
        print("1. At the shell prompt, type psql")
        print("2. At the psql prompt, type \i tournament.sql")


def executeQuery(query, query_args):
    """Connect to the database, execute the query, commit changes,
    and close the connection.

    Args:
      query: a string, containing the query to be executed
      query_args: a tuple, containing the arguments to be substituted
          for conversion specifiers in query. Use () if query has no
          conversion specifiers.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, query_args)
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    executeQuery("DELETE FROM matches", ())


def deletePlayers():
    """Remove all the player records from the database."""
    executeQuery("DELETE FROM players", ())


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM players"
    cursor.execute(query)
    numPlayers = cursor.fetchone()[0]
    conn.close()
    return numPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.
    (This should be handled by your SQL database schema, not in your
    Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES(%s)"
    query_args = (name,)
    executeQuery(query, query_args)


def playerStandings():
    """Returns a list of the players and their win records, sorted by
    wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins,
      matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM records"
    cursor.execute(query)
    ps = [(row[0], row[1], row[2], row[4]) for row in cursor.fetchall()]
    conn.close()
    return ps


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "INSERT INTO matches (winner, loser) VALUES(%s, %s)"
    query_args = (winner, loser)
    executeQuery(query, query_args)


def unreportMatch(winner, loser):
    """Deletes a matches that was incorrectly recorded.

    Args:
      winner, loser:  same arguments used in the incorrect call to
          reportMatch()
    """
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT match_id FROM matches WHERE winner = %s " + \
            "and loser = %s ORDER BY match_id desc limit 1"
    query_args = (winner, loser)
    cursor.execute(query, query_args)
    result = cursor.fetchall()
    if not result:
        print("No such match")
        return
    query = "DELETE FROM matches WHERE match_id = %s"
    query_args = result
    cursor.execute(query, query_args)
    conn.commit()
    conn.close()


def deletePlayer(id):
    """Deletes a player from the database.

    Args:
      id:  the id of the player to be deleted
    """
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM players WHERE player_id = (%s)"
    query_args = (id,)
    cursor.execute(query, query_args)
    if cursor.fetchone()[0] < 1:
        print("Player %d does not exist" % (id,))
        return
    query = "SELECT * FROM matches WHERE winner = (%s) OR loser = (%s)"
    query_args = (id, id)
    cursor.execute(query, query_args)
    matches = cursor.fetchall()
    if len(matches):
        print(("If player %d is deleted, the following matches must also " +
               "be deleted:") % (id,))
        for match in matches:
            print("match id: %d, winner: %d, loser %d" %
                  (match[0], match[1], match[2]))
        print("This will change the win-loss records of other players.")
        choice = raw_input("Continue? (y/n): ")
        if choice.lower() != 'y':
            return
        query = "DELETE FROM matches WHERE winner = (%s) OR loser = (%s)"
        query_args = (id, id)
        cursor.execute(query, query_args)
    query = "DELETE FROM players WHERE player_id = (%s)"
    query_args = (id,)
    cursor.execute(query, query_args)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a
    match.

    Assuming that there are an even number of players registered, each
    player appears exactly once in the pairings.  Each player is paired
    with another player with an equal or nearly-equal win record, that
    is, a player adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ps = playerStandings()
    return([(ps[n][0], ps[n][1], ps[n + 1][0], ps[n + 1][1])
            for n in range(0, len(ps) - 1, 2)])
