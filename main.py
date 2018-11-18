def create_word_to_basic_form_mapping():
    dictionary = open('dictionary.txt', 'rb+')
    content = dictionary.read().decode('utf-8')
    lines = content.split('\n')
    mapping = {}
    for line in lines:
        line = line.lower()
        words = line.split(', ')
        for word in words:
            mapping[word.strip()] = words[0].strip()
    return mapping


print(create_word_to_basic_form_mapping()['arcyosłów'])
