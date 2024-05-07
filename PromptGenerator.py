import yaml
import re
from numpy import random
import numpy as np
import uuid
import random as rnd
from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import dotenv_values
from langchain_community.llms import Ollama

prompt_starter = [
    'I need the materials that',
    'Give me the materials that',
    'List the materials that',
    'Search for the materials that',
    'Look for the materials that'
]

config = dotenv_values(".env")


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_bot_api(message, model=config['GPT_MODEL']):
    try:
        llm = Ollama(model="llama3:70b")
        llm.base_url = 'http://172.28.105.30/backend'
        response = llm.invoke(message)
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.


def random_date_generator(start_date, range_in_days):
    days_to_add = np.arange(0, range_in_days)
    random_date = np.datetime64(start_date) + np.random.choice(days_to_add)
    return random_date


def get_raw_prompts(key):
    message = (f'Based on the path "{key}" write 4 possible short exact enough human readable prompt and 2 short '
               f'readable prompt containing abbreviation parameter that addresses this path. Just list them and'
               f'wrap each one around @.'
               f'Write it in the following format'
               f'1) <First Short exact prompts>'
               f'2) <Second Short exact prompts>'
               f'3) <Third Short exact prompts>'
               f'3) <Forth Short exact prompts>'
               f'4) <First Short prompts with abbreviations>'
               f'5) <Second Short prompts with abbreviations>'
               f'start prompts using any of {prompt_starter}'
               )
    response = chat_bot_api(message)

    # Finding all matches in the text
    matches = re.findall(r"@([^@]+)@", response)
    return matches


# Load the YAML file
with open('quantities.yaml', 'r') as file:
    data = yaml.safe_load(file)


def make_quantity_query(key, val, query_type, gte=None, lte=None):
    query = None
    if query_type != 'gte_lte' and query_type != 'gte' and query_type != 'lte':
        query = dict()
        query_key = f'{key}{query_type}'
        query[query_key] = val
        return query
    else:
        if gte and lte:
            query = dict()
            query[key] = dict(gte=gte, lte=lte)
        elif gte:
            query = dict()
            query[key] = dict(gte=gte)
        elif lte:
            query = dict()
            query[key] = dict(lte=lte)
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
    n_prompts = 0
    for key, value in data.items():
        # description = value['description']
        repeats = 'an' if value['repeats'] else 'not an'
        type = value['type']

        query_types = [':all', ':any', '', 'gte', 'lte', 'gte_lte']

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
                            prompt = raw_prompt + f' that is {val}'
                            quantity_query = make_quantity_query(key, val, query_type)
                        elif type == 'str' and query_type == ':any' or query_type == ':all':
                            multi_val = rnd.sample(values, random.randint(2, min(len(values), 4) + 1))
                            if query_type == ':any':
                                prompt = raw_prompt + f' that could be any of the {list_to_text(multi_val, "or")}'
                            else:
                                prompt = raw_prompt + f' that includes all of the {list_to_text(multi_val, "and")}'
                            quantity_query = make_quantity_query(key, multi_val, query_type)
                        elif (query_type == 'gte_lte', query_type == 'gte', query_type == 'lte') and (type == 'int' or type == 'int32' or type == 'int64' or type == 'float' or type == 'float32' or type == 'float64'):
                            range = rnd.sample([float(v) for v in values], 2)
                            if type == 'int' or type == 'int32' or type == 'int64':
                                range = rnd.sample([int(v) for v in values], 2)
                            gte = np.min(range)
                            lte = np.max(range)
                            if query_type == 'gte_lte':
                                prompt = raw_prompt + f' between {str(gte)} and {str(lte)}'
                                quantity_query = make_quantity_query(key, val, query_type, str(gte), str(lte))
                            elif query_type == 'gte':
                                prompt = raw_prompt + f' that is grater than {val}'
                                quantity_query = make_quantity_query(key, val, query_type, str(gte), None)
                            elif query_type == 'lte':
                                prompt = raw_prompt + f' that is less than {val}'
                                quantity_query = make_quantity_query(key, val, query_type, None, str(lte))

                        if quantity_query:
                            corresponding_query = dict()
                            corresponding_query.update(quantity_query)

                            print(prompt)
                            print(corresponding_query)
                            n_prompts = n_prompts +1

        print(f'n_prompts = {n_prompts}')



print_keys(data)
