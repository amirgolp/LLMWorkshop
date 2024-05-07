import yaml


# Load the YAML file
with open('quantities.yaml', 'r') as file:
    data = yaml.safe_load(file)


# Loop over all keys and print them
def print_keys(data, indent=''):
    for key, value in data.items():
        description = value['description']
        repeats = 'an' if value['repeats'] else 'not an'
        type = value['type']
        print(key)
        print(description)
        print(repeats)
        print(type)

        prompt_key = f'''
based on the key "{key}" and the type "{type}" and considering that this key
is {repeats} array write 5 possible short exact enough human readable prompt and 5 short readable prompt containing abbreviation parameter (if applicable) that addresses this key.
        '''

        print(prompt_key)


print_keys(data)
