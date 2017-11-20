import socket
import random
import pickle
import threading


def prepare_to_game(data, connection):

    while True:
        if data == 'y':
            answer = "\nGO!\n"
            send_to_client(answer)

            while True:
                ind_x = random.randint(0, 4)
                ind_y = random.randint(0, 4)
                if (ind_x != 0 and ind_y != 0) and (ind_x != 4 and ind_y != 4):
                    break
            player = [0, 0, ind_x, ind_y]
            create_and_send_table(player)
            data = get_from_client()
            if data == 'game':
                game_start(player, connection)
                break

        elif data == 'n':
            answer = "See you next time!"
            send_to_client(answer)
            close_connection(connection)
            break

        elif data != 'y' and data != 'n':
            answer = "Incorrect input value"
            send_to_client(answer)
            close_connection(connection)
            break


def create_and_send_table(player):
    print('player=',  player)
    x = player[0]
    y = player[1]
    ind_x = player[2]
    ind_y = player[3]
    table = [['.' for i in range(5)]for i in range(5)]
    table[x][y] = "X"
    table[ind_x][ind_y] = "■"
    table[-1][-1] = "/\Exit"
    send_to_client(table)


def game_start(player, connection):
    message = 'start'
    send_to_client(message)
    move = ['', player]
    send_to_client(move)
    make_move(connection)


def make_move(connection):
    while True:
        move = conn.recv(1024)
        if not move:
            break
        else:
            move = pickle.loads(move)
        print(move)
        if move == 'break':
            close_connection(connection)
            break
        turn = move[0]

        player = move[1]
        if turn == 'w':
            player = up(player)

        elif turn == 's':
            player = down(player)

        elif turn == 'd':
            player = right(player)

        elif turn == 'a':
            player = left(player)

        move = ['', player]
        send_to_client(move)

        create_and_send_table(player)


def up(player):
    x = player[0]
    y = player[1]
    ind_x = player[2]
    ind_y = player[3]

    if x != 0:
        x -= 1
    else:
        if y != 4:
            x = 4
        else:
            x = 3
    if x == ind_x and y == ind_y:
        if ind_x == 0:
            ind_x = 4
        else:
            ind_x -= 1
    player = [x, y, ind_x, ind_y]
    return player


def down(player):
    x = player[0]
    y = player[1]
    ind_x = player[2]
    ind_y = player[3]

    if x == 3 and y == 4:
        x = 0
    elif x != 4:
        x += 1
    else:
        x = 0
    if x == ind_x and y == ind_y:
        if ind_x == 4:
            ind_x = 0
        else:
            ind_x += 1

    player = [x, y, ind_x, ind_y]
    return player


def right(player):
    x = player[0]
    y = player[1]
    ind_x = player[2]
    ind_y = player[3]

    if y == 3 and x == 4:
        y = 0
    elif y != 4:
        y += 1
    else:
        y = 0
    if x == ind_x and y == ind_y:
        if ind_y == 4:
            ind_y = 0
        else:
            ind_y += 1

    player = [x, y, ind_x, ind_y]
    return player


def left(player):
    x = player[0]
    y = player[1]
    ind_x = player[2]
    ind_y = player[3]

    if y != 0:
        y -= 1
    else:
        if x != 4:
            y = 4
        else:
            y = 3
    if x == ind_x and y == ind_y:
        if ind_y == 0:
            ind_y = 4
        else:
            ind_y -= 1

    player = [x, y, ind_x, ind_y]
    return player


def send_to_client(package):
    package = pickle.dumps(package)
    conn.send(package)


def get_from_client():
    answer = conn.recv(1024)
    answer = pickle.loads(answer)
    return answer


def close_connection(connection):
    connection.close()



sock = socket.socket()
sock.bind(('', 5000))
sock.listen(5)
while True:
    conn, address = sock.accept()
    print('connected:', address)
    data = get_from_client()
    print('first data:', data)

    event = threading.Event()
    thread = threading.Thread(target=prepare_to_game, args=(data, conn, ))
    print(threading.enumerate())
    thread.start()
    event.set()
    thread.join()
    # if not (thread.isAlive()):
    #     break

# prepare_to_game(data)

sock.close()