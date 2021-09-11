import socket as Socket
from _thread import start_new_thread
import pickle
from game import Game

server = "127.0.0.1"
port = 5555

socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)

try:
    socket.bind((server, port))
except Socket.error as e:
    str(e)

socket.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))
    print(player)

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(player, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = socket.accept()
    print("Connected to:", addr)

    idCount += 1
    player = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        player = 1


    start_new_thread(threaded_client, (conn, player, gameId))