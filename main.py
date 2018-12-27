import config_data as c
import re


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
    return mapping


mapping_to_base_form = create_word_to_basic_form_mapping()

c.parse_config(mapping_to_base_form)
rooms = c.rooms
devices = c.devices
functions = c.functions
device_types = c.device_types
colors = c.colors

test_cases = [
    'włącz światło na suficie w lewej sekcji poddasza',
    'włącz światło za telewizorem w sypialni',
    'wyłącz oświetlenie w sypialni',
    'zapal lewą lampę w sypialni',
    'zgaś prawą lampę w sypialni',
    'załącz lampę na suficie w sypialni',
    'jakieś bzdury nie mające sensu',
    'włącz wentylator w łazience',
    'wyłącz światło pod szafkami w kuchni',
    'wycisz radio w lewej sekcji poddasza',
    'wycisz radio w lewej części poddasza',
    'zgaś telewizor w sypialni',
    'wyłącz dmuchawę w łazience',
    'budzik w sypialni budzenie 6:00',
    'lampa lewa w sypialni kolor czerwony',
    'lampa lewa w salonie kolor czerwony',
]


def get_command(phrase):
    ints = re.compile('\d+').findall(phrase)
    words = phrase.split(' ')
    words = [x.lower() for x in words if x != '']
    words = [mapping_to_base_form[x] for x in words if x in mapping_to_base_form]
    words = set(words)
    # print(words)
    function_list = list(filter(
        lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), functions[x]['names']))) > 0,
        functions))
    function = function_list[0]
    # print(function)
    for alias in functions[function]['names']:
        if alias in words:
            words.remove(alias)

    room = \
        list(filter(lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), rooms[x]))) > 0,
                    rooms))[0]
    # print(room)
    for x in rooms[room]:
        for alias in x:
            if alias in words:
                words.remove(alias)

    # print(words)
    device_type = list(filter(lambda x: len(device_types[x].intersection(words)) > 0, device_types))[0]
    # print(device_type)
    for alias in device_types[device_type]:
        if alias in words:
            words.remove(alias)

    # print(words)
    filtered_devices = devices
    filtered_devices = list(filter(lambda x: x[1] == room, filtered_devices))
    filtered_devices = list(filter(lambda x: x[2] == device_type, filtered_devices))
    filtered_devices_supporting_function = list(filter(lambda x: function in x[3], filtered_devices))
    candidate_devices = list(
        filter(lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), x[4]))) > 0,
               filtered_devices_supporting_function))

    if len(candidate_devices) > 0:
        device_id = candidate_devices[0][0]
    else:
        devices_list = list(filter(lambda x: len(x[4]) == 0, filtered_devices_supporting_function))
        if len(devices_list) == 1:
            device_id = devices_list[0][0]
        else:
            devices_list = list(
                filter(lambda x: len(list(filter(lambda y: len(set(y).intersection(words)) == len(y), x[4]))) > 0,
                       filtered_devices))
            if len(devices_list) > 0:
                return 'error: Urządzenie nie obsługuje tego polecenia'
            else:
                return 'error: Polecenie jest niejednoznaczne'

    cmd = functions[function]['command'].replace('ID', device_id)
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


for test_case in test_cases:
    command = get_command_safe(test_case)
    print('case: ' + test_case)
    print('result: ' + command)
    print()
