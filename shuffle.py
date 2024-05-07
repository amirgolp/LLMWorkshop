import random
import json


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


def shuffle(primary_prompts, n):
    samples = random.sample(primary_prompts, n)
    prompts = [sample['prompt'] for sample in samples]
    final_prompt = " and ".join(prompts)
    
    queries = [sample['completion'] for sample in samples]
    final_query = {}
    for d in queries:
        final_query.update(d)
    final_dict = dict(prompt=final_prompt, completion=final_query)
    return final_dict


primary_prompts = to_dict('x.txt')

prompts_level2 = [shuffle(primary_prompts, 2) for i in range(20)]
prompts_level3 = [shuffle(primary_prompts, 3) for i in range(5)]
prompts_level4 = [shuffle(primary_prompts, 4) for i in range(5)]

print(prompts_level2)
print(prompts_level3)
print(prompts_level4)
