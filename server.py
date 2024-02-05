import socket
import threading
import datetime
db = {}

def custom_error(*args):
    return "ERROR"

def set_value(*args):
    if len(args) == 2:
        db[args[0]] = {"value": args[1]}
        return "ok"

    if len(args) == 3:
        db[args[0]] = {
            "value": args[1], 
            "exp": datetime.datetime.now() + datetime.timedelta(0, int(args[2]))
        }
        return "ok"

    return custom_error()

def get_value(*args):
    if len(*args) != 1:
        return custom_error()

    row = db.get(*args[0], "null") 
    if row == "null":
        return row
    
    if "exp" in row.keys() and (row.get("exp") - datetime.datetime.now()).total_seconds() < 0:
        del[*args[0]]
        return "null"
    
    return row.get("value")

def delete_key(*args):
    if len(*args) != 1:
        return custom_error()

    if args[0] in db.keys():
        del db[args[0]]
        return "OK"
    
    return "null"

def get_ttl(*args):



command_dict = {
    "set":set_value,
    "get": get_value,
    "del": delete_key,
    "error": custom_error
}

def handle_command(command):
    command_parts = command.split()
    if len(command_parts) == 0:
        return ""
    
    return command_dict.get(command_parts[0].lower(), custom_error)(*command_parts[1:])


def handle_client_connection(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break
        result = handle_command(command)
        client_socket.send(result.encode())
    client_socket.close()



def start_server(host='127.0.0.1', port=6378):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port)) 
    server.listen(5)
    print(f'Server started on {host}:{port}')
    while True:
        client_sock, address = server.accept()
        print(f'Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()


if __name__ == '__main__':
   start_server()