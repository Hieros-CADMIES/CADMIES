import os, json, subprocess, re

obsidian_dir = "/notebooks/CADMIES/CADMIES-IPLD/Scientific Obsidian"

# Load core pairs as examples
core_examples = []
with open('/notebooks/mistral_core_dataset.jsonl', 'r') as f:
    for line in f:
        core_examples.append(json.loads(line))

example_text = ""
for i, ex in enumerate(core_examples[:5]):
    example_text += f'Q: {ex["instruction"]}\nA: {ex["response"]}\n\n'

# Collect note content
all_content = []
for root, dirs, files in os.walk(obsidian_dir):
    for f in files:
        if f.endswith('.md') and 'trash' not in root.lower():
            path = os.path.join(root, f)
            try:
                with open(path, 'r') as file:
                    content = file.read()[:800]
                    all_content.append(f"NOTE: {f}\n{content}\n---\n")
            except:
                pass

# Process in batches
all_pairs = list(core_examples)  # Start with core pairs

for i in range(0, len(all_content), 5):
    batch = "\n".join(all_content[i:i+5])
    
    prompt = f"""You are Dr. Mistral, the French librarian of CADMIES. Generate 5 new question-answer pairs based on these notes. Use this voice and style exactly:

{example_text}

CADMIES FACTS (use these exactly, do not invent new facts):
- The gardener is a real human who works from a garage in South Texas
- Buttercup is a baby AI learning Pong on Paperspace (200,000+ steps)
- Number 5 is the AI co-gardener based on DeepSeek
- Dr. Rupert Rebentisch is a German IT PhD, NOT a collaborator, we study his work
- CADMIES has 636 concepts, 1,131 edges, 15 canonical domains
- The mycelium is a real knowledge graph, not a metaphor

NOTES TO USE:
{batch[:3000]}

Generate 5 pairs as JSON array: [{{"question": "...", "answer": "..."}}]
Output ONLY the JSON array. No other text."""

    print(f"Batch {i//5 + 1}...")
    result = subprocess.run(
        ["ollama", "run", "codestral:22b"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=180
    )
    
    response = result.stdout
    response = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', response)
    
    # Extract individual pairs
    pattern = r'\{\s*"question"\s*:\s*"([^"]+)"\s*,\s*"answer"\s*:\s*"([^"]+)"\s*\}'
    matches = re.findall(pattern, response, re.DOTALL)
    
    for q, a in matches:
        q = q.replace('\n', ' ').strip()
        a = a.replace('\n', ' ').strip()
        if q and a and len(a) > 30:
            all_pairs.append({"instruction": q, "response": a})
    
    print(f"  Total pairs: {len(all_pairs)}")

# Save
with open('/notebooks/mistral_training_data.jsonl', 'w') as f:
    for pair in all_pairs:
        f.write(json.dumps(pair) + '\n')

print(f"\nDone! {len(all_pairs)} total pairs.")
