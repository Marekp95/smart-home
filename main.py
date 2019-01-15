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
    mapping['%'] = '%'
    return mapping


mapping_to_base_form = create_word_to_basic_form_mapping()

c.parse_config(mapping_to_base_form)
rooms = c.rooms
devices = c.devices
functions = c.functions
device_types = c.device_types
colors = c.colors

test_cases = [
    ('Załącz oświetlenie górne na poddaszu w sekcji pierwszej', {'on A1'}),
    ('Wyłącz oświetlenie górne na poddaszu w sekcji pierwszej', {'off A1'}),
    ('oświetlenie górne na poddaszu w sekcji pierwszej', {'xchg A1'}),
    ('poddasze sekcja pierwsza oświetlenie górne Załącz', {'on A1'}),
    ('oświetlenie biurka na poddaszu Załącz', {'on A2'}),
    ('poddasze oświetlenie biurka Załącz', {'on A2'}),
    ('Wyłącz oświetlenie biurka na poddaszu', {'off A2'}),
    ('oświetlenie biurka na poddaszu', {'xchg A2'}),
    ('Załącz radio na poddaszu', {'on A3'}),
    ('Wyłącz radio na poddaszu', {'off A3'}),
    ('poddasze radio Załącz', {'on A3'}),
    ('Załącz radio na poddaszu kanał trzeci', {'set A3 ch 3'}),
    ('radio na poddaszu Ustaw głośność na 5', {'set A3 vol 5'}),
    ('radio na poddaszu głośniej', {'vol_up A3'}),
    ('radio na poddaszu ciszej', {'vol_down A3'}),
    ('radio na poddaszu zmień kanał na 4', {'set A3 ch 4'}),
    ('Załącz komputer na poddaszu', {'on A4'}),
    ('Wyłącz komputer na poddaszu', {'off A4'}),
    ('poddasze komputer Załącz', {'on A4'}),
    ('poddasze komputer wyłącz', {'off A4'}),
    ('komputer na poddaszu', {'xchg A4'}),
    ('monitor na poddaszu', {'xchg A5'}),
    ('Załącz monitor na poddaszu', {'on A5'}),
    ('Wyłącz monitor na poddaszu', {'off A5'}),
    ('Załącz oświetlenie górne w sekcji drugiej na poddaszu', {'on A6'}),
    ('Wyłącz oświetlenie górne w sekcji drugiej na poddaszu', {'off A6'}),
    ('oświetlenie górne w sekcji drugiej na poddaszu', {'xchg A6'}),
    ('Załącz lampy nad Oławą na poddaszu', {'on A7', 'error'}),
    ('Wyłącz lampę nad ławą na poddaszu', {'off A7'}),
    ('lampa nad Oławą', {'xchg A7', 'error'}),
    ('lampa lewa na poddaszu', {'xchg A8'}),
    ('Załącz lampę lewą na poddaszu', {'on A8'}),
    ('Wyłącz lampę lewą na poddaszu', {'off A8'}),
    ('lampa prawa na poddaszu', {'xchg A9'}),
    ('Załącz lampę lewą na poddaszu', {'on A8'}),
    ('Wyłącz lampę lewą na poddaszu', {'off A8'}),
    ('Załącz telewizor na poddaszu', {'on A10'}),
    ('telewizor na poddaszu', {'xchg A10'}),
    ('telewizor na poddaszu kanał piąty', {'set A10 ch 5'}),
    ('telewizor na poddaszu Ustaw kanał trzeci', {'set A10 ch 3'}),
    ('telewizor na poddaszu Ustaw głośność na 4', {'set A10 vol 4'}),
    ('telewizor na poddaszu ciszej', {'vol_down A10'}),
    ('telewizor na poddaszu głośniej', {'vol_up A10'}),
    ('ścisz telewizor na poddaszu', {'vol_down A10'}),
    ('oświetlenie za telewizorem na poddaszu Załącz', {'on A11'}),
    ('Załącz oświetlenie za telewizorem na poddaszu', {'on A11'}),
    ('poddasze telewizor oświetlenie Załącz', {'on A11'}),
    ('oświetlenie za telewizorem na poddaszu wyłącz', {'off A11'}),
    ('całe oświetlenie na poddaszu wyłącz', {'off A12'}),
    ('całe oświetlenie na poddaszu Załącz', {'on A12'}),
    ('całe oświetlenie na poddaszu', {'xchg A12'}),
    ('Załącz oświetlenie górne w sypialni', {'on B1'}),
    ('Wyłącz oświetlenie górne w sypialni', {'off B1'}),
    ('sypialnia oświetlenie górne Załącz', {'on B1'}),
    ('sypialnia Załącz oświetlenie górne', {'on B1'}),
    ('sypialnia Wyłącz oświetlenie górne', {'off B1'}),
    ('sypialnia oświetlenie główne', {'xchg B1'}),
    ('sypialnia oświetlenie główne w barwa ciepła', {'warm B1'}),
    ('sypialnia oświetlenie górne barwa zimna', {'cold B1'}),
    ('Załącz lampę w sypialni', {'on B4'}),
    ('Załącz lampy lewo w sypialni', {'on B2', 'error'}),
    ('Załącz lampę lewą w sypialni', {'on B2'}),
    ('lampa lewa w sypialni', {'xchg B2'}),
    ('Wyłącz lampę lewą w sypialni', {'off B2'}),
    ('Załącz lampę prawą w sypialni', {'on B3'}),
    ('Wyłącz lampę prawą w sypialni', {'off B3'}),
    ('Załącz lampy w sypialni', {'error', 'on B2'}),
    ('Wyłącz lampę w sypialni', {'off B4'}),
    ('sypialnia salon światło', {'xchg B1'}),
    ('sypialnia Wyłącz światło', {'off B1'}),
    ('Załącz światło w sypialni', {'on B1'}),
    ('Wyłącz światło w sypialni', {'off B1'}),
    ('lampa w sypialni', {'xchg B4'}),
    ('lampy w sypialni', {'xchg B4', 'error'}),
    ('Wyłącz lampę w sypialni', {'off B4'}),
    ('sypialnia Załącz telewizor', {'on B5'}),
    ('Załącz telewizor w sypialni', {'on B5'}),
    ('Wyłącz telewizor w sypialni', {'off B5'}),
    ('telewizor sypialni kanał 7', {'set B5 ch 7'}),
    ('Wybierz kanał 7 telewizor sypialni', {'set B5 ch 7'}),
    ('Ustaw kanał 11 telewizor sypialni', {'set B5 ch 11'}),
    ('telewizor w sypialni kanał 12', {'set B5 ch 12'}),
    ('sypialnia Załącz telewizor w sypialni', {'on B5'}),
    ('sypialnia załącza oświetlenie za telewizorem', {'on B6', 'error'}),
    ('sypialnia Wyłącz oświetlenie za telewizorem', {'off B6'}),
    ('sypialnia Załącz oświetlenie za telewizorem', {'on B6'}),
    ('sypialnia oświetlenie za telewizorem', {'xchg B6'}),
    ('Wyłącz całe oświetlenie w sypialni', {'off B7'}),
    ('Załącz całe oświetlenie w sypialni', {'on B7'}),
    ('cały oświetlenie w sypialni', {'xchg B7', 'error'}),
    ('Załącz budzik w sypialni', {'on B8'}),
    ('Wyłącz budzik w sypialni', {'off B8'}),
    ('Załącz budzik', {'on B8', 'error'}),
    ('Wyłącz budzik', {'off B8', 'error'}),
    ('Ustaw budzik na 6:00', {'set B8 time 6:00'}),
    ('Ustaw budzik na 5:30', {'set B8 time 5:30'}),
    ('Ustaw budzik na godzinę 0', {'set B8 time 0:00', 'error'}),
    ('Ustaw budzenie na 7:00 rano', {'set B8 time 7:00'}),
    ('Ustaw budzenie na', {'error'}),
    ('Ustaw budzenie na 7:00 rano', {'set B8 time 7:00'}),
    ('Ustaw budzenie na 20:00', {'set B8 time 20:00'}),
    ('Załącz oświetlenie w łazience', {'on C1'}),
    ('Załącz oświetlenie górne w łazience', {'on C1'}),
    ('Załącz światło w łazience', {'on C1'}),
    ('Wyłącz światło w łazience', {'off C1'}),
    ('Wyłącz oświetlenie górne w łazience', {'off C1'}),
    ('Wyłącz światło Górne w łazience', {'off C1'}),
    ('światło w łazience', {'xchg C1'}),
    ('oświetlenie górne w łazience', {'xchg C1'}),
    ('Załącz lampy nad lustrem w łazience', {'on C2'}),
    ('Wyłącz lampy nad lustrem w łazience', {'off C2'}),
    ('łazienka las lampa nad lustrem Załącz', {'on C2'}),
    ('łazienka Wyłącz lampy nad lustrem', {'off C2', 'error'}),
    ('łazienka Wyłącz lampę nad lustrem', {'off C2'}),
    ('łazienka lampa nad lustrem', {'xchg C2'}),
    ('Załącz wentylator w łazience', {'on C3'}),
    ('Wyłącz wentylator w łazience', {'off C3'}),
    ('wentylator w łazience', {'xchg C3'}),
    ('łazienka wentylator Załącz', {'on C3'}),
    ('łazienka Załącz wentylator', {'on C3'}),
    ('łazienka wyłączyłem ty lator', {'error'}),
    ('łazienka Wyłącz wentylator', {'off C3'}),
    ('Załóż dmuchawę w łazience', {'error', 'on C4'}),
    ('Załącz dmuchawy w łazience', {'on C4', 'error'}),
    ('Załącz dmuchawę w łazience', {'on C4'}),
    ('Wyłącz dmuchawę w łazience', {'off C4'}),
    ('dmuchawa w łazience', {'xchg C4'}),
    ('łazienka Załóż druha we', {'error'}),
    ('łazienka Załącz dmuchawy', {'on C4'}),
    ('łazienka Załącz dmuchawę', {'on C4'}),
    ('łazienka Wyłącz dmuchawę', {'off C4'}),
    ('Wyłącz całe oświetlenie w łazience', {'off C5'}),
    ('Załącz całe oświetlenie w łazience', {'on C5'}),
    ('całe oświetlenie w łazience', {'xchg C5'}),
    ('Załącz światło w salonie', {'on D1'}),
    ('wyłącz światło w salonie', {'off D1'}),
    ('Załącz oświetlenie górne w salonie', {'on D1'}),
    ('Wyłącz oświetlenie górne w salonie', {'off D1'}),
    ('oświetlenie górne w salonie', {'xchg D1'}),
    ('światło w salonie', {'xchg D1'}),
    ('lampa lewa w salonie', {'xchg D2'}),
    ('Załączyłem telefon w salonie', {'error'}),
    ('Załącz lampę lewą w salonie', {'on D2'}),
    ('Wyłącz lampę lewą w salonie', {'off D2'}),
    ('wyłączyłem telefon w salonie', {'error'}),
    ('salon lampa prawa', {'xchg D3'}),
    ('salon Załącz prawą lampę', {'on D3'}),
    ('salon Załącz lampę prawą', {'on D3'}),
    ('lampa lewa w salonie kolor niebieski', {'set D2 color blue'}),
    ('lampa prawa w salonie kolor czerwony', {'set D3 color red'}),
    ('salon lampa lewa kolor czerwony', {'set D2 color red'}),
    ('salon lampa lewa kolor zielony', {'set D2 color green'}),
    ('Wyłącz całe oświetlenie w salonie', {'off D4'}),
    ('Załącz całe oświetlenie w salonie', {'on D4'}),
    ('salon Wyłącz całe oświetlenie', {'off D4'}),
    ('salon roleta lewa w górę', {'up D5'}),
    ('salon roleta lewa w dół', {'down D5'}),
    ('salon roleta lewa', {'error'}),
    ('salon roleta lewa stop', {'stop D5'}),
    ('roleta prawa w salonie Do góry', {'up D6'}),
    ('roleta lewa w salonie w dół', {'down D5'}),
    ('Podnieś roletę nową w salonie', {'error'}),
    ('Opuść roletę prawą w salonie', {'down D6'}),
    ('rolety w salonie Do góry', {'up D7'}),
    ('Podnieść rolety w salonie', {'up D7'}),
    ('Opuść rolety w salonie', {'down D7'}),
    ('Ale ty w salonie na dół', {'error'}),
    ('Zatrzymaj rolety w salonie', {'stop D7'}),
    ('rolety w salonie stop', {'stop D7'}),
    ('rolety w salonie w górę', {'up D7'}),
    ('Odsłoń rolety w salonie', {'up D7'}),
    ('Zasłoń rolety w salonie', {'down D7'}),
    ('Zasłoń rolety', {'down D7', 'error'}),
    ('Załącz oświetlenie w kuchni', {'on E1'}),
    ('Wyłącz oświetlenie w kuchni', {'off E1'}),
    ('Załącz oświetlenie górne w kuchni', {'on E1'}),
    ('Wyłącz oświetlenie górne w kuchni', {'off E1'}),
    ('Załącz światło w kuchni', {'on E1'}),
    ('Wyłącz światło w kuchni', {'off E1'}),
    ('Załącz oświetlenie nad szafkami', {'on E2'}),
    ('Wyłącz oświetlenie nad szafkami', {'off E2'}),
    ('Ustaw oświetlenie górne nad szafkami w kuchni na 50%', {'set E2 bright 50'}),
    ('kuchnia oświetlenie górne nad szafkami 5%', {'set E2 bright 5'}),
    ('kuchnia oświetlenie nad szafkami', {'xchg E2'}),
    ('kuchnia oświetlenie pod szafkami', {'xchg E3'}),
    ('Załóż oświetlenie pod szafkami w kuchni', {'error', 'on E3'}),
    ('Wyłącz oświetlenie pod szafkami w kuchni', {'off E3'}),
    ('kuchnia Załącz oświetlenie pod szafkami', {'on E3'}),
    ('kuchnia Wyłącz oświetlenie pod szafkami', {'off E3'}),
    ('kuchnia oświetlenie pod szafkami', {'xchg E3'}),
    ('kuchnia oświetlenie nad szafkami 50%', {'set E2 bright 50'}),
    ('kuchnia oświetlenie nad szafkami 10%', {'set E2 bright 10'}),
    ('kuchnia oświetlenie nad szafkami Ustaw na 20%', {'set E2 bright 20'}),
    ('Załącz oświetlenie okapu w kuchni', {'on E4'}),
    ('Wyłącz oświetlenie okapu w kuchni', {'off E4'}),
    ('oświetlenie okapu w kuchni', {'xchg E4'}),
    ('wentylator okapu w kuchni Załącz', {'on E5'}),
    ('Załącz wentylator okapu w kuchni', {'on E5'}),
    ('Wyłącz wentylator okapu w kuchni', {'off E5'}),
    ('wentylator okapu w kuchni', {'xchg E5'}),
    ('kuchnia okap wentylator Załącz', {'on E5'}),
    ('kuchnia okap wentylator wyłącz', {'off E5'}),
    ('wentylator okapu w kuchni wolno', {'slow E5'}),
    ('wentylator okapu w kuchni szybko', {'fast E5'}),
    ('kuchnia okap wentylator wolno', {'slow E5'}),
    ('kuchnia okap wentylator szybko', {'fast E5'}),
    ('kuchnia wentylator okapu szybko', {'fast E5'}),
    ('Załącz wentylator w kuchni', {'on E6'}),
    ('Wyłącz wentylator w kuchni', {'off E6'}),
    ('wentylator w kuchni', {'xchg E6'}),
    ('wentylator w kuchni Załącz', {'on E6'}),
    ('całe oświetlenie w kuchni wyłącz', {'off E7'}),
    ('Wyłącz cały oświetlenie w kuchni', {'off E7'}),
    ('kuchnia cały oświetlenie wyłącz', {'off E7'}),
]


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


correct = 0
for test_case in test_cases:
    command_txt, expected_results = test_case
    command = get_command_safe(command_txt)
    if command in expected_results or 'error' in expected_results and command.startswith('error'):
        correct += 1
    else:
        print(f'command: {command}, expected: {expected_results}, text: {command_txt}')

print(f'Total result: {correct} out of {len(test_cases)}')
