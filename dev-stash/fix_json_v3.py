import re, json

with open('/notebooks/codestral_raw_output.txt', 'r') as f:
    raw = f.read()

# Strip ANSI codes and control characters
raw = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', raw)
raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)

# Find each individual {"question": ..., "answer": ...} pair
# Match from { to } that contains both question and answer keys
pattern = r'\{\s*"question"\s*:\s*"([^"]*)"\s*,\s*"answer"\s*:\s*"([^"]*)"\s*\}'
matches = re.findall(pattern, raw, re.DOTALL)

pairs = []
for q, a in matches:
    # Clean up newlines in answers
    a = a.replace('\n', ' ').strip()
    q = q.replace('\n', ' ').strip()
    if q and a:
        pairs.append({"instruction": q, "response": a})

if pairs:
    with open('/notebooks/mistral_training_data.jsonl', 'w') as f:
        for pair in pairs:
            f.write(json.dumps(pair) + '\n')
    print(f'Success! {len(pairs)} pairs saved.')
    for i, p in enumerate(pairs[:3]):
        print(f'  [{i+1}] Q: {p["instruction"][:60]}...')
else:
    print('No pairs found')
