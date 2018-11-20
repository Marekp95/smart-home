import yaml
import pprint

pp = pprint.PrettyPrinter(indent=2)

rooms = {}
devices = []
functions = {}
device_types = {}


def build_functions(data, mapping_to_base_form):
    for func in data:
        names = set(map(lambda x: mapping_to_base_form[x], func['names']))
        command = func['command']
        functions[func['id']] = {'names': names, 'command': command}


def build_rooms(data, mapping_to_base_form):
    for room in data:
        rooms[room['id']] = set(map(lambda x: tuple(mapping_to_base_form[y] for y in x.split(' ')), get_data_by_key('names', room)))


def build_device_types(data, mapping_to_base_form):
    for device in data:
        device_types[device['id']] = set(map(lambda x: mapping_to_base_form[x], device['names']))


def get_data_by_key(key, data):
    return '' if key not in data else data[key]


def build_rooms_and_devices(data, mapping_to_base_form):
    for room in data:
        room_id = room['id']
        for device in room['devices']:
            device_data = [
                get_data_by_key('id', device),
                room_id,
                get_data_by_key('deviceType', device),
                set(get_data_by_key('functions', device)),
                set(map(lambda x: tuple(mapping_to_base_form[y] for y in x.split(' ')), get_data_by_key('position', device)))
            ]
            devices.append(device_data)


def parse_config(mapping_to_base_form):
    with open("config.yaml", 'r', encoding='UTF-8') as stream:
        config = yaml.load(stream)
        build_functions(config['functions'], mapping_to_base_form)
        build_device_types(config['devices'], mapping_to_base_form)
        build_rooms(config['rooms'], mapping_to_base_form)
        build_rooms_and_devices(config['rooms'], mapping_to_base_form)


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
