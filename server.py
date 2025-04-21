import socket
from _thread import *
import pickle
from game import Game

server = "192.168.162.165"
port = 5010

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0
leaderboard = {}

def update_leaderboard(player_name, won):
    """Update leaderboard data for a player."""
    global leaderboard

    if player_name not in leaderboard:
        leaderboard[player_name] = {"streak": 0}

    if won:
        leaderboard[player_name]["streak"] += 1
    else:
        leaderboard[player_name]["streak"] = 0

    # Sort leaderboard by streak in descending order
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["streak"], reverse=True)
    leaderboard = dict(sorted_leaderboard)

def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))

    reply = ""
    print(f"Player {player} connected to game {gameId}")

    player_name=None

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data.startswith("set_name:"):
                        # Extract and set player name
                        player_name = data.split(":")[1]
                        game.set_player_name(player, player_name)
                    elif data == "reset":
                        game.resetMove()
                    elif data != "get":
                        game.play(player, data)

                    if game.bothMoved():
                        winner = game.win()
                        opponent_name = game.get_opponent_name(player)

                        if winner == player:
                            update_leaderboard(player_name, won=True)
                            update_leaderboard(opponent_name, won=False)
                        elif winner != -1:  # If it's not a tie, update opponent's loss
                            update_leaderboard(player_name, won=False)
                            update_leaderboard(opponent_name, won=True)
                        elif winner == 1:
                            update_leaderboard(player_name, won=False)
                            update_leaderboard(opponent_name, won=False)


                    # Add leaderboard to the game data
                    game.leaderboard = list(leaderboard.items())[:3]

                    print(f"Updated leaderboard: {leaderboard}")

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as e:
            print("Error : ",e)
            break
    print("Lost connection")
    try:
        del games[gameId]
        del leaderboard[player_name]
        del leaderboard[opponent_name]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))


