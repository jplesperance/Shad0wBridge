import socket

target_ip = '127.0.0.1'
target_port = 2222

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'[+] Connecting to {target_ip}.')
sock.connect((target_ip, target_port))
print(f'[+] Connected to {target_ip}.')


sock.close()
