import socket

def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    remote_target, remote_ip = sock.accept()
    print(f'[+] Connection received from {remote_ip[0]}')
    remote_target.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = '127.0.0.1'
host_port = 2222
listener_handler()


