#!/usr/bin/python3

import config_data as c
import test_cases as t
import re
import socket


def snd_cmd(res):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(res.encode('utf-8'), ('172.19.129.11', 1965))

    s.close()
# end def


def create_word_to_basic_form_mapping():
    dictionary = open('dictionary.txt', 'rb+')
    content = dictionary.read().decode('utf-8')
    lines = content.split('\n')
    mapping = {}
    for line in lines:
        line = line.lower()
        words = line.split(', ')
        words = list(map(lambda x: x.strip(), words))
        value = words[0]
        for w in words:
            if w in mapping:
                value = mapping[w]
        for word in words:
            key = word.strip()
            if key not in mapping:
                mapping[key] = value
    mapping['%'] = '%'
    return mapping


mapping_to_base_form = create_word_to_basic_form_mapping()

c.parse_config(mapping_to_base_form)
rooms = c.rooms
devices = c.devices
functions = c.functions
device_types = c.device_types
colors = c.colors


def get_command(phrase):
    ints = re.compile('\d+').findall(phrase)
    words = re.split('[\s\d]', phrase)
    words = [x.lower() for x in words if x != '']
    words = [mapping_to_base_form[x] for x in words if x in mapping_to_base_form]
    words = set(words)
    # print(words)
    function_list = list(filter(
        lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), functions[x]['names']))) > 0,
        functions))
    if len(function_list) > 0:
        function = function_list[0]
        for alias in functions[function]['names']:
            if alias in words:
                words.remove(alias)
    else:
        function = 'invoke'
    # print(function)

    filtered_rooms = list(
        filter(lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), rooms[x]))) > 0, rooms))

    if len(filtered_rooms) > 0:
        room = filtered_rooms[0]
        for x in rooms[room]:
            for alias in x:
                if alias in words:
                    words.remove(alias)
    else:
        room = 'undefined'
    # print(room)

    # print(words)
    device_type = list(filter(lambda x: len(device_types[x].intersection(words)) > 0, device_types))[0]
    # print(device_type)
    for alias in device_types[device_type]:
        if alias in words:
            words.remove(alias)

    # print(words)
    filtered_devices = devices
    filtered_devices = list(filter(lambda x: x[2] == device_type, filtered_devices))
    filtered_devices_from_room = list(filter(lambda x: x[1] == room, filtered_devices))
    filtered_devices_supporting_function = list(filter(lambda x: function in x[3], filtered_devices))
    filtered_devices_supporting_function_from_room = list(
        filter(lambda x: x[1] == room, filtered_devices_supporting_function))
    candidate_devices = list(
        filter(lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), x[4]))) > 0,
               filtered_devices_supporting_function))
    candidate_devices_from_room = list(filter(lambda x: x[1] == room, candidate_devices))

    if len(candidate_devices_from_room) > 0:
        device_id = candidate_devices_from_room[0][0]
    else:
        devices_list = list(filter(lambda x: len(x[4]) == 0, filtered_devices_supporting_function_from_room))
        if len(devices_list) == 1:
            device_id = devices_list[0][0]
        else:
            devices_list = list(
                filter(lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), x[4]))) > 0,
                       filtered_devices_from_room))
            if len(devices_list) > 0:
                return 'error: Urządzenie nie obsługuje tego polecenia'
            else:
                if len(filtered_devices_supporting_function_from_room) > 0:
                    device_id = filtered_devices_supporting_function_from_room[0][0]
                elif len(candidate_devices) > 0:
                    device_id = candidate_devices[0][0]
                elif len(filtered_devices) > 0:
                    device_id = filtered_devices[0][0]
                else:
                    return 'error: Polecenie jest niejednoznaczne'

    cmd = functions[function]['command'].replace('ID', device_id)
    if len(ints) < cmd.count('INT'):
        return 'error: Niepoprawne parametry polecenia'
    for i in range(min(len(ints), len(cmd.split('INT')) - 1)):
        cmd = cmd.replace('INT', ints[i], 1)
    if cmd.count('COLOR') > 0:
        color = list(filter(lambda x: len(colors[x].intersection(words)) > 0, colors))[0]
        cmd = cmd.replace('COLOR', color)
    return cmd


def get_command_safe(phrase):
    try:
        return get_command(phrase)
    except:
        return 'error: Nie rozpoznano polecenia'


print('-------------------TESTING-------------------------')
correct = 0
for test_case in t.test_cases:
    command_txt, expected_results = test_case
    command = get_command_safe(command_txt)
    if command in expected_results or 'error' in expected_results and command.startswith('error'):
        correct += 1
    else:
        print(f'command: {command}, expected: {expected_results}, text: {command_txt}')

print(f'Total result: {correct} out of {len(t.test_cases)}')
print('-----------------END TESTING-----------------------')

# Create socket and bind to address
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind(('', 1964))

# Receive messages
while True:
    data, addr = UDPSock.recvfrom(1964)
    txt = data.decode('utf-8')
    print("<<", txt)
    cmd = get_command_safe(txt)
    print(">>", cmd)
    snd_cmd(cmd)
# end while

# Close socket
UDPSock.close()
