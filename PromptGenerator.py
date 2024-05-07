import yaml
from numpy import random
import numpy as np
import uuid
import random as rnd

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


def random_date_generator(start_date, range_in_days):
    days_to_add = np.arange(0, range_in_days)
    random_date = np.datetime64(start_date) + np.random.choice(days_to_add)
    return random_date


def get_raw_prompts(key):
    prompt_key = f'Based on the path "{key}" write 3 possible short exact enough human readable prompt and 3 short readable prompt containing abbreviation parameter that addresses this path. Just list them. Write it in the following format'
    return ['I need key.a', 'I need key.b']


# Load the YAML file
with open('quantities.yaml', 'r') as file:
    data = yaml.safe_load(file)


def make_quantity_query(key, val, query_type):
    query = dict()
    query_key = f'{key}{query_type}'
    query[query_key] = val
    return query


def list_to_text(items, sep):
    if len(items) == 0:
        return ""
    elif len(items) == 1:
        return items[0]
    else:
        return ', '.join(items[:-1]) + f' {sep} ' + items[-1]


# Loop over all keys and print them
def print_keys(data, indent=''):
    n = 0
    for key, value in data.items():
        # description = value['description']
        repeats = 'an' if value['repeats'] else 'not an'
        type = value['type']

        query_types = [':all', ':any', '']

        values = None

        if isinstance(type, list):
            values = type
        elif type == 'str':
            values = [my_random_string(10), my_random_string(10), my_random_string(10)]
        elif type == 'bool':
            values = ['True', 'False', 'True']
        elif type == 'int' or type == 'int32' or type == 'int64':
            values = [str(random.randint(1000)), str(random.randint(1000)), str(random.randint(1000))]
        elif type == 'float' or type == 'float32' or type == 'float64':
            values = ["{:.5f}".format(random.randint(10) * random.random()),
                      "{:.5f}".format(random.randint(10) * random.random()),
                      "{:.5f}".format(random.randint(10) * random.random())]
        elif type.startswith('<nomad.metainfo.metainfo._Datetime'):
            values = [random_date_generator(f'2010-03-14T15:0{str(random.randint(9))}:20.36', 1000).astype(str),
                      random_date_generator(f'2010-03-14T15:0{str(random.randint(9))}:32.21', 500).astype(str),
                      random_date_generator(f'2010-03-14T15:0{str(random.randint(9))}:32.21', 500).astype(str)]

        raw_prompts = get_raw_prompts(key)
        if isinstance(values, list):
            for raw_prompt in raw_prompts:
                for val in values:
                    for query_type in query_types:

                        quantity_query = None
                        if query_type == '':
                            prompt = raw_prompt + f' with the value {val}'
                            quantity_query = make_quantity_query(key, val, query_type)
                        elif query_type == ':any' or query_type == ':all':
                            multi_val = rnd.sample(values, random.randint(2, min(len(values), 4) + 1))
                            if query_type == ':any':
                                prompt = raw_prompt + f' that could be any of the {list_to_text(multi_val, "or")}'
                            else:
                                prompt = raw_prompt + f' that includes all of the {list_to_text(multi_val, "and")}'
                            quantity_query = make_quantity_query(key, multi_val, query_type)

                        if quantity_query:
                            corresponding_query = dict()
                            corresponding_query.update(quantity_query)

                            print(prompt)
                            print(corresponding_query)



print_keys(data)
