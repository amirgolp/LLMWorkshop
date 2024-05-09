import random
import json
import re


def to_dict(input_file):
    all_prompts = list()
    with open(input_file, 'r') as infile:
        while True:
            prompt = infile.readline().strip()
            if not prompt:
                break
            completion = infile.readline().strip().replace("'", '"')
            if not completion:
                break
            normalized_completion = completion.replace("True", "true").replace("False", "false")
            prompt = dict(prompt=prompt, completion=json.loads(normalized_completion))
            all_prompts.append(prompt)
     
    return all_prompts


starting_prompts = [
    'Write a Nomad query.',
    'Give me a Nomad query.',
    'I need a Nomad query.',
    'A Nomad query.',
    'Nomad query.'
]

n_total = 0


def shuffle(primary_prompts, n, semantic):
    samples = random.sample(primary_prompts, n)
    prompts = [sample['prompt'] for sample in samples]

    and_semantic = ['and', 'in which', 'considering that']
    or_semantic = ['or', 'and the materials that', 'or the materials that']
    final_prompt = prompts[0]
    for i in range(1, len(prompts)):
        if semantic == 'and':
            final_prompt = f"{final_prompt} {random.sample(and_semantic, 1)[0]} {prompts[i]}"
        elif semantic == 'or':
            final_prompt = f"{final_prompt} {random.sample(or_semantic, 1)[0]} {prompts[i]}"
    
    queries = [sample['completion'] for sample in samples]
    final_query = {semantic: {}}
    for d in queries:
        final_query[semantic].update(d)
    final_dict = dict(prompt=f'{random.sample(starting_prompts, 1)[0]} {final_prompt}', response=final_query)
    if len(final_query[semantic]) == n:
        return final_dict
    else:
        return None


def make_final_prompts(primary_prompts):
    all = []
    for item in primary_prompts:
        prompt = item['prompt']
        query = item['completion']
        final_dict = dict(prompt=f'{random.sample(starting_prompts, 1)[0]} {prompt}', response=query)
        all.append(final_dict)

    return all


primary_prompts = to_dict('version_8.txt')
all_final_prompts = make_final_prompts(primary_prompts)

for i in range(20000):
    and2 = shuffle(primary_prompts, 2, 'and')
    and3 = shuffle(primary_prompts, 3, 'and')
    and4 = shuffle(primary_prompts, 4, 'and')
    or2 = shuffle(primary_prompts, 2, 'or')
    or3 = shuffle(primary_prompts, 3, 'or')
    or4 = shuffle(primary_prompts, 4, 'or')
    if and2 is not None:
        all_final_prompts.append(and2)
    if and3 is not None:
        all_final_prompts.append(and3)
    if and4 is not None:
        all_final_prompts.append(and4)
    if or2 is not None:
        all_final_prompts.append(or2)
    if or3 is not None:
        all_final_prompts.append(or3)
    if or4 is not None:
        all_final_prompts.append(or4)

with open('all_prompts.json', 'w') as json_file:
    json.dump(all_final_prompts, json_file)
