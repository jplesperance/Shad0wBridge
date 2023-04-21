import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target_ip = '127.0.0.1'
target_port = 2222

def session_handler():
    print(f'[+] Connecting to {target_ip}.')
    sock.connect((target_ip, target_port))
    print(f'[+] Connected to {target_ip}.')
    while True:
        try:
            print('[+] Awaiting response...')
            message = sock.recv(1024).decode()
            if message == 'exit':
                print('[-] The server has terminated the session.')
                sock.close()
                break
            print(message)
            response = input('Message to send#> ')
            if response == 'exit':
                sock.send(response.encode())
                sock.close()
                break
            sock.send(response.encode())
        except KeyboardInterrupt:
            print('[+] Keyboard interrupt issued.')
            sock.close()
            break
        except Exception:
            sock.close()
            break


session_handler()