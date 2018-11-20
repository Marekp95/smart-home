import yaml
import pprint

pp = pprint.PrettyPrinter(indent=2)

rooms = {}
devices = []
functions = {}
device_types = {}


def build_functions(data):
    for func in data:
        names = set(func['names'])
        command = func['command']
        functions[func['id']] = {'names': names, 'command': command}


def build_device_types(data):
    for device in data:
        device_types[device['id']] = device['names']


def get_data_by_key(key, data):
    return '' if key not in data else data[key]


def build_rooms_and_devices(data):
    for room in data:
        room_id = room['id']
        for device in room['devices']:
            device_data = [
                get_data_by_key('id', device),
                room_id,
                get_data_by_key('deviceType', device),
                set(get_data_by_key('functions', device)),
                set(get_data_by_key('position', device))
            ]
            devices.append(device_data)


def parse_config():
    with open("config.yaml", 'r', encoding='UTF-8') as stream:
        config = yaml.load(stream)
        build_functions(config['functions'])
        build_device_types(config['devices'])
        build_rooms_and_devices(config['rooms'])


rooms_mock = {
    'bedroom': {
        'sypialnia'
    },
}

devices_mock = [
    (
        'B1',
        'bedroom',
        'lamp',
        {'turnOn', 'turnOff'},
        {'górne', 'sufit'},

    ),
    (
        'B2',
        'bedroom',
        'lamp',
        {'turnOn', 'turnOff'},
        {'lewa'},
    ),
    (
        'B3',
        'bedroom',
        'lamp',
        {'turnOn', 'turnOff'},
        {'prawa'},
    ),
    (
        'B7',
        'bedroom',
        'lamp',
        {'turnOn', 'turnOff'},
        set({}),
    ),
]

functions_mock = {
    'turnOn': {
        'names': {
            'włączyć', 'załączyć', 'uruchomić', 'zapalić',
        },
        'commandni': 'on ID',
    },
    'turnOff': {
        'names': {
            'wyłączyć', 'zgasić',
        },
        'command': 'off ID',
    },
}

device_types_mock = {
    'lamp': {
        'lampa',
        'światło',
        'oświetlenie',
    },
}
