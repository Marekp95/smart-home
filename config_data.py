import yaml
import pprint

pp = pprint.PrettyPrinter(indent=2)

rooms = {}
devices = []
functions = {}
device_types = {}
colors = {}
digits = {}


def get_base_form(mapping, key):
    return mapping[key] if key in mapping else key


def build_functions(data, mapping_to_base_form):
    for func in data:
        names = set(map(lambda x: tuple(get_base_form(mapping_to_base_form, y) for y in x.split(' ')), func['names']))
        command = func['command']
        functions[func['id']] = {'names': names, 'command': command}


def build_rooms(data, mapping_to_base_form):
    for room in data:
        rooms[room['id']] = set(map(lambda x: tuple(get_base_form(mapping_to_base_form, y) for y in x.split(' ')),
                                    get_data_by_key('names', room)))


def build_device_types(data, mapping_to_base_form):
    for device in data:
        device_types[device['id']] = set(map(lambda x: get_base_form(mapping_to_base_form, x), device['names']))


def build_colors(data, mapping_to_base_form):
    for color in data:
        colors[color['id']] = set(map(lambda x: get_base_form(mapping_to_base_form, x), color['names']))


def build_digits(data):
    for digit in data:
        digits[digit['id']] = set(digit['names'])


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
                set(map(lambda x: tuple(get_base_form(mapping_to_base_form, y) for y in x.split(' ')),
                        get_data_by_key('position', device)))
            ]
            devices.append(device_data)


def parse_config(mapping_to_base_form):
    with open("config.yaml", 'r', encoding='UTF-8') as stream:
        config = yaml.load(stream)
        build_functions(config['functions'], mapping_to_base_form)
        build_device_types(config['devices'], mapping_to_base_form)
        build_colors(config['colors'], mapping_to_base_form)
        build_digits(config['digits'])
        build_rooms(config['rooms'], mapping_to_base_form)
        build_rooms_and_devices(config['rooms'], mapping_to_base_form)
