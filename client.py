import socket
import pickle


def send_to_server(package):
    package = pickle.dumps(package)
    sock.send(package)


def get_from_server():
    answer = sock.recv(1024)
    answer = pickle.loads(answer)
    return answer

def print_table(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(str(table[i][j]), end='')
        print()


sock = socket.socket()
sock.connect((socket.gethostname(), 5000))

message = input("Are you ready? [y/n]  ")
send_to_server(message)
answer = get_from_server()
print(answer)

if answer == "See you next time!" or answer == "Incorrect input value":
    sock.close()

else:
    table = get_from_server()

    print_table(table)

    message = 'game'
    send_to_server(message)

    message = get_from_server()
    move = get_from_server()

    if message == 'start':
        while True:
            player = move[1]
            if player[2] == 4 and player[3] == 4:
                print("\n", "YOU WIN!", "\n")
                break

            turn = input("Next turn: ")
            move[0] = turn
            send_to_server(move)

            move = get_from_server()
            table = get_from_server()

            print_table(table)

send_to_server('break')

sock.close()
