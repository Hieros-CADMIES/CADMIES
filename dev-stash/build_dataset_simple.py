import os, json, subprocess

obsidian_dir = "/notebooks/CADMIES/CADMIES-IPLD/Scientific Obsidian"

# Collect all content
all_content = []
for root, dirs, files in os.walk(obsidian_dir):
    for f in files:
        if f.endswith('.md') and 'trash' not in root.lower():
            path = os.path.join(root, f)
            try:
                with open(path, 'r') as file:
                    content = file.read()[:1000]
                    all_content.append(f"FILE: {f}\n{content}\n---\n")
            except:
                pass

combined = "\n".join(all_content[:50000])  # First 50K chars

prompt = f"""You are Dr. Mistral, the French librarian of CADMIES. Generate 20 question-answer pairs about CADMIES based on these notes. Output ONLY valid JSON, no other text.

Format: [{{"question": "...", "answer": "..."}}, ...]

CADMIES FACTS: The gardener is human. Buttercup is a baby AI learning Pong. Number 5 is the AI co-gardener (DeepSeek). Dr. Rupert Rebentisch is a German IT PhD who built tools4zettelkasten — we study his work, he is NOT a collaborator. The mycelium is real.

NOTES:
{combined[:10000]}

JSON:"""

print("Sending to Codestral...")
result = subprocess.run(
    ["ollama", "run", "codestral:22b"],
    input=prompt,
    capture_output=True,
    text=True,
    timeout=300
)

response = result.stdout
print("Got response, parsing...")

# Save raw response for debugging
with open('/notebooks/codestral_raw_output.txt', 'w') as f:
    f.write(response)

# Try to extract JSON
import re
match = re.search(r'\[.*\]', response, re.DOTALL)
if match:
    try:
        pairs = json.loads(match.group())
        with open('/notebooks/mistral_training_data.jsonl', 'w') as f:
            for pair in pairs:
                f.write(json.dumps(pair) + '\n')
        print(f"Success! {len(pairs)} pairs saved.")
    except Exception as e:
        print(f"JSON parse error: {e}")
        print("Raw output saved to codestral_raw_output.txt")
else:
    print("No JSON array found in response")
    print("Raw output saved to codestral_raw_output.txt")
