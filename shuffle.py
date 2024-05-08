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
            prompt = dict(prompt=prompt, completion=json.loads(completion))
            all_prompts.append(prompt)
     
    return all_prompts


def remove_starting_phrases(sentence):
    patterns = [r'^I need the materials that\s+', r'^Give me the materials that\s+', r'^List the materials that\s+', r'^Search for the materials that\s+', r'^Look for the materials that\s+', r'^I need\s+', r'^Give me\s+', r'^List the\s+', r'^Search for\s+', r'^Look for\s+']
    regex_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for pattern in regex_patterns:
        match = pattern.match(sentence)
        if match:
            sentence = sentence[match.end():].lstrip()
            break

    return sentence


def shuffle(primary_prompts, n, semantic):
    samples = random.sample(primary_prompts, n)
    prompts = [sample['prompt'] for sample in samples]

    cleared_prompts = [remove_starting_phrases(prompts[i]) for i in range(1, len(prompts))]
    cleared_prompts.insert(0, prompts[0])

    and_semantic = ['and', 'in which', 'considering that']
    or_semantic = ['or', 'and the materials that', 'or the materials that']
    final_prompt = cleared_prompts[0]
    for i in range(1, len(cleared_prompts)):
        if semantic == 'and':
            final_prompt = f"{final_prompt} {random.sample(and_semantic, 1)[0]} {cleared_prompts[i]}"
        elif semantic == 'or':
            final_prompt = f"{final_prompt} {random.sample(or_semantic, 1)[0]} {cleared_prompts[i]}"
    
    queries = [sample['completion'] for sample in samples]
    final_query = {semantic: {}}
    for d in queries:
        final_query[semantic].update(d)
    final_dict = dict(prompt=final_prompt, completion=final_query)
    if len(final_query[semantic]) == n:
        return final_dict
    else:
        return None


primary_prompts = to_dict('version_1.txt')

# prompts_level2 = [shuffle(primary_prompts, 2, 'and') for i in range(20)]
# prompts_level3 = [shuffle(primary_prompts, 3, 'and') for i in range(5)]
prompts_level4 = [shuffle(primary_prompts, 4, 'and') for i in range(5)]

# print(prompts_level2)
# print(prompts_level3)
print(prompts_level4)
