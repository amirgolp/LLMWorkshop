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
    final_dict = dict(prompt=f'{random.sample(starting_prompts, 1)[0]} {final_prompt}', completion=final_query)
    if len(final_query[semantic]) == n:
        print(final_dict)
    else:
        return None


def make_final_prompts(primary_prompts):
    for item in primary_prompts:
        prompt = item['prompt']
        query = item['completion']
        final_dict = dict(prompt=f'{random.sample(starting_prompts, 1)[0]} {prompt}', completion=query)
        print(final_dict)


primary_prompts = to_dict('version_8.txt')
make_final_prompts(primary_prompts)
and_prompts_level2 = [shuffle(primary_prompts, 2, 'and') for i in range(20000)]
and_prompts_level3 = [shuffle(primary_prompts, 3, 'and') for i in range(20000)]
and_prompts_level4 = [shuffle(primary_prompts, 4, 'and') for i in range(20000)]
or_prompts_level2 = [shuffle(primary_prompts, 2, 'or') for i in range(20000)]
or_prompts_level3 = [shuffle(primary_prompts, 3, 'or') for i in range(20000)]
or_prompts_level4 = [shuffle(primary_prompts, 4, 'or') for i in range(20000)]
