import socket
def board_to_string(board):
    return "\n".join(["".join(row) for row in board])

def string_to_board(board_str, size):
    rows = board_str.split("\n")
    return [list(row) for row in rows]

#client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("157.51.128.93", 8000)) 

while True:
    a = client_socket.recv(1024).decode()
    a = int(a)
    if a == 0:
        print("Game exited.")
        break
    elif a == 1:
        board_size = int(client_socket.recv(1024).decode())
        name1 = client_socket.recv(1024).decode()
        name2 = input("Enter Player 2 Name: ")
        client_socket.send(name2.encode())

        while True:
            # Receive updated board after Player 1 move
            board_str = client_socket.recv(4096).decode()
            board = string_to_board(board_str, board_size)

            # Display 
            print("\nCurrent Board:")
            for row in board:
                print(" | ".join(row))
            print()

            client_socket.send(board_to_string(board).encode())

            # Loop until Player 2 enters a valid position
            while True:
                try:
                    p2_pos = input(f"{name2} Enter Your Position (1-{board_size*board_size}): ")
                    
                    # check input is a digit
                    if not p2_pos.isdigit():
                        print("Invalid input! Please enter a number.")
                        continue
                    
                    p2_pos = int(p2_pos)

                    if p2_pos < 1 or p2_pos > board_size * board_size:
                        print(f"Position out of range! Enter between 1 and {board_size*board_size}.")
                        continue

                    # check position is not already occupied
                    r, c = (p2_pos - 1) // board_size, (p2_pos - 1) % board_size
                    if board[r][c] != "-":
                        print("Position already occupied. Please enter another position.")
                        continue

                    #else sent to server
                    client_socket.send(str(p2_pos).encode())
                    break

                except ValueError:
                    print("Invalid input! Please enter a number.")
                    continue

            # Receive updated board after Player 2 move
            board_str = client_socket.recv(4096).decode()
            board = string_to_board(board_str, board_size)

            # Display after Player 2 move
            print("\nUpdated Board:")
            for row in board:
                print(" | ".join(row))
            print()
