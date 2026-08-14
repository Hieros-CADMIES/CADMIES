import os, json, subprocess, re

obsidian_dir = "/notebooks/CADMIES/CADMIES-IPLD/Scientific Obsidian"
output_file = "/notebooks/mistral_training_data.jsonl"

def read_file(path):
    try:
        with open(path, 'r') as f:
            content = f.read()
        return content[:2500]
    except:
        return ""

def generate_pairs(content, filename):
    prompt = f"""You are Dr. Mistral, the French librarian of CADMIES. Generate 3 Q&A pairs about this note. Output ONLY a JSON array, no other text.
Format: [{{"question": "...", "answer": "..."}}]

Note: CADMIES is a real project. The gardener tends the mycelium. Buttercup is a baby AI learning Pong. Number 5 is the AI co-gardener. Dr. Rupert Rebentisch is a German IT PhD who built a similar system (tools4zettelkasten) — we study his work but he is NOT a collaborator.

Note content ({filename}):
{content}

JSON array:"""

    try:
        result = subprocess.run(
            ["ollama", "run", "codestral:22b"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        response = result.stdout.strip()
        # Find anything that looks like a JSON array
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            try:
                pairs = json.loads(match.group())
                return pairs
            except:
                # Try to fix common JSON issues
                text = match.group()
                text = re.sub(r',\s*]', ']', text)  # Remove trailing commas
                text = re.sub(r',\s*}', '}', text)
                try:
                    return json.loads(text)
                except:
                    print(f"  JSON parse failed for {filename}")
                    return []
        return []
    except Exception as e:
        print(f"  Error: {e}")
        return []

# Collect files — focus on key ones first
key_files = []
for root, dirs, files in os.walk(obsidian_dir):
    for f in files:
        if f.endswith('.md') and 'trash' not in root.lower():
            key_files.append(os.path.join(root, f))

# Sort: polished phases first, then raw sessions
key_files.sort()

print(f"Found {len(key_files)} files")
all_pairs = []

for i, filepath in enumerate(key_files):
    filename = os.path.basename(filepath)
    print(f"[{i+1}/{len(key_files)}] {filename[:60]}...")
    
    content = read_file(filepath)
    if len(content) < 50:
        print("  Skipping (too short)")
        continue
    
    pairs = generate_pairs(content, filename)
    if pairs:
        for pair in pairs:
            if 'question' in pair and 'answer' in pair:
                all_pairs.append({
                    "instruction": pair["question"],
                    "response": pair["answer"]
                })
        print(f"  ✓ {len(pairs)} pairs")
    else:
        print(f"  ✗ No pairs")

with open(output_file, 'w') as f:
    for pair in all_pairs:
        f.write(json.dumps(pair) + '\n')

print(f"\nDone! {len(all_pairs)} total pairs saved to {output_file}")
