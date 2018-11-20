import config_data as c


def create_word_to_basic_form_mapping():
    dictionary = open('dictionary.txt', 'rb+')
    content = dictionary.read().decode('utf-8')
    lines = content.split('\n')
    mapping = {}
    for line in lines:
        line = line.lower()
        words = line.split(', ')
        for word in words:
            key = word.strip()
            if key not in mapping:
                value = words[0].strip()
                if value in mapping:
                    value = mapping[value]
                mapping[key] = value
    return mapping


mapping_to_base_form = create_word_to_basic_form_mapping()
# print(mapping['prawa'])
#
rooms = c.rooms_mock
# devices = c.devices_mock
# functions = c.functions_mock
# device_types = c.device_types_mock

c.parse_config()
# rooms = c.rooms
devices = c.devices
functions = c.functions
device_types = c.device_types

# print(mapping['lampa'])
# print(mapping['światło'])
# print(mapping['oświetlenie'])
# print(mapping['górne'])

test_cases = [
    'włącz światło w sypialni',
    'wyłącz oświetlenie w sypialni',
    'zapal lewą lampę w sypialni',
    'zgaś prawą lampę w sypialni',
    'załącz lampę na suficie w sypialni',
]


def get_command(phrase):
    words = phrase.split(' ')
    words = [x.lower() for x in words if x != '']
    words = [mapping_to_base_form[x] for x in words if x in mapping_to_base_form]
    words = set(words)
    # print(words)
    function_list = list(filter(lambda x: len(functions[x]['names'].intersection(words)) > 0, functions))
    function = function_list[0]
    # print(function)
    for alias in functions[function]['names']:
        if alias in words:
            words.remove(alias)

    room = list(filter(lambda x: len(rooms[x].intersection(words)) > 0, rooms))[0]
    # print(room)
    for alias in rooms[room]:
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
    filtered_devices = list(filter(lambda x: function in x[3], filtered_devices))
    candidate_devices = list(filter(lambda x: len(x[4].intersection(words)) > 0, filtered_devices))

    if len(candidate_devices) > 0:
        device_id = candidate_devices[0][0]
    else:
        device_id = list(filter(lambda x: len(x[4]) == 0, filtered_devices))[0][0]

    cmd = functions[function]['command'].replace('ID', device_id)
    return cmd


for test_case in test_cases:
    command = get_command(test_case)
    print('case: ' + test_case)
    print('result: ' + command)
