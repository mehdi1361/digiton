import socket

HOST = "127.0.0.1"  
PORT = 6378
def send_to_socket(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command)
        data = s.recv(1024)

    return data

def main():
    while True:
        command = input("PyInMemStore>>")
        if command == "q" or command =="exit":
            exit()
        result = send_to_socket(bytes(command, "utf-8"))
        print(result)



if __name__ == "__main__":
    main()