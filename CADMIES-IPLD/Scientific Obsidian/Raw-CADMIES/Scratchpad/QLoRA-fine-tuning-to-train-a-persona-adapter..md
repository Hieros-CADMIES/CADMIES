# QLoRA fine-tuning to train a persona adapter.

Below is every technical detail from the successful training run on 2026-07-30.

1. Environment
Hardware: Paperspace VM, NVIDIA GPU (A100-SXM4-40GB)

OS: Ubuntu 22.04 LTS + CUDA 12.4

Python: Python 3.11.7

VRAM peak: 6.30 GB

Training time: 467 seconds (~7.8 minutes) 

2. Core Libraries and Versions
The exact versions that successfully ran:

Package	Version	Purpose
transformers	4.35.2	Model loading and tokenization 
accelerate	0.24.1	Distributed training and mixed precision
peft	0.6.2	LoRA adapters 
bitsandbytes	0.41.1	4-bit quantization 
trl	0.7.1	SFTTrainer 
datasets	2.18.0	Dataset loading and processing
huggingface_hub	0.20.3	Model caching and downloading
diffusers	0.20.2	Dependency for TRL import
tokenizers	0.15.1	Tokenizer backend 
pyarrow	14.0.1	Arrow serialization for datasets
torch	2.1.1+cu121	PyTorch with CUDA 12.1 support
Installation order (single command): 

bash
pip install transformers==4.35.2 accelerate==0.24.1 peft==0.6.2 bitsandbytes==0.41.1 trl==0.7.1 datasets==2.18.0 huggingface_hub==0.20.3 diffusers==0.20.2 tokenizers==0.15.1 pyarrow==14.0.1
3. Training Script
File: /notebooks/training/train_persona_fixed.py

python
import torch
import time
import hashlib
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, BitsAndBytesConfig
from trl import SFTTrainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

dataset_file = '/notebooks/training/datasets/zara_persona.jsonl'
dataset_hash = get_file_hash(dataset_file)
dataset = Dataset.from_json(dataset_file)
print(f'Training on {len(dataset)} pairs')
print(f'Dataset hash: {dataset_hash}')

tokenizer = AutoTokenizer.from_pretrained('mistralai/Mistral-7B-Instruct-v0.3', trust_remote_code=True)

# FIXED: Use unk_token instead of eos_token to prevent repetition issues
tokenizer.pad_token = tokenizer.unk_token
tokenizer.padding_side = 'right'

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    'mistralai/Mistral-7B-Instruct-v0.3',
    quantization_config=bnb_config,
    device_map='auto',
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)
print(f"VRAM allocated after model load: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
model.gradient_checkpointing_enable()

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=['q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj'],
    lora_dropout=0.05,
    bias='none',
    task_type='CAUSAL_LM'
)
model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir='/notebooks/training/adapters/persona-fixed-adapter',
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    bf16=True,
    max_grad_norm=1.0,
    report_to='none',
    logging_steps=50,
    save_strategy='no',
    overwrite_output_dir=True
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    dataset_text_field='text',
    max_seq_length=2048
)

start_time = time.time()
trainer.train()
training_time = time.time() - start_time

final_loss = trainer.state.log_history[-1].get('loss', 'N/A')
start_loss = 'N/A'
if trainer.state.log_history:
    for entry in trainer.state.log_history:
        if 'loss' in entry:
            start_loss = entry['loss']
            break

print(f'Done! Training time: {training_time:.0f}s, Start loss: {start_loss}, Final loss: {final_loss}')
vram_peak = torch.cuda.max_memory_allocated()/1024**3
print(f"VRAM peak: {vram_peak:.2f} GB")

trainer.save_model('/notebooks/training/adapters/persona-fixed-adapter')

print(f"\nLOG ENTRY:")
print(f"date=2026-07-31, adapter_name=persona-fixed, base_model=mistralai/Mistral-7B-Instruct-v0.3, dataset_file={dataset_file}, dataset_hash={dataset_hash}, num_pairs={len(dataset)}, epochs=1, learning_rate=2e-4, effective_batch_size=8, start_loss={start_loss}, final_loss={final_loss}, training_time_seconds={training_time:.0f}, vram_peak_gb={vram_peak:.2f}, notes=fixed_tokenizer_unk")
4. Dataset
File: /notebooks/training/datasets/zara_persona.jsonl

Format: JSONL with one {"text": "<s>[INST] question [/INST] answer</s>"} per line

Size: 516 pairs

Hash: 25b4b990f1c97d39b01ff4605e399f08

Format example:

jsonl
{"text": "<s>[INST] Who are you? [/INST] I am Captain Zara Steele. I fly the Stardust Runner. I drink coffee black and I don't trust politicians. Got a scar on my left eyebrow from a plasma leak on Titan. I talk straight. If you don't like it, that's your problem.</s>"}
5. Training Parameters
Parameter	Value
Base model	mistralai/Mistral-7B-Instruct-v0.3
Quantization	4-bit NF4
LoRA rank (r)	16 
LoRA alpha	32 
LoRA dropout	0.05
Target modules	q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
Learning rate	2e-4 
Optimizer	paged_adamw_8bit (default in SFTTrainer)
Batch size	1 per device
Gradient accumulation	8 steps
Effective batch size	8
Epochs	1
BF16	Yes
Max seq length	2048
Gradient checkpointing	Enabled 
Loss reduction	1.329 → N/A (logged after trainer.state update)
6. Output Adapter
Location: /notebooks/training/adapters/persona-fixed-adapter/

Files:

adapter_model.safetensors — LoRA weights (167 MB)

adapter_config.json — Configuration

tokenizer.json — Tokenizer configuration

tokenizer.model — SentencePiece model

tokenizer_config.json — Tokenizer settings

special_tokens_map.json — Special token mappings

training_args.bin — Saved training arguments

README.md — Auto-generated adapter info

adapter_config.json:

json
{
  "alpha_pattern": {},
  "auto_mapping": null,
  "base_model_name_or_path": "mistralai/Mistral-7B-Instruct-v0.3",
  "bias": "none",
  "fan_in_fan_out": false,
  "inference_mode": true,
  "init_lora_weights": true,
  "lora_alpha": 32,
  "lora_dropout": 0.05,
  "modules_to_save": null,
  "peft_type": "LORA",
  "r": 16,
  "target_modules": [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj"
  ],
  "task_type": "CAUSAL_LM"
}
7. Known Issue: Mistral Tokenizer Cache
Error: Exception: data did not match any variant of untagged enum PyPreTokenizerTypeWrapper at line 40 column 3 

Fix: Replace "prepend_scheme": "first" with "add_prefix_space": true in the cached tokenizer.json:

bash
find /root/.cache/huggingface -name "tokenizer.json" -path "*Mistral-7B*" -exec sed -i 's/"prepend_scheme": "first"/"add_prefix_space": true/g' {} \;
Cause: The Mistral tokenizer.json format changed, breaking compatibility with older transformers versions. The add_prefix_space parameter resolves this. 

8. Testing the Trained Adapter
File: /notebooks/test_zara.py

python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=False,
)

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3",
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)

model = PeftModel.from_pretrained(
    model,
    "/notebooks/training/adapters/persona-fixed-adapter",
)

tokenizer = AutoTokenizer.from_pretrained(
    "/notebooks/training/adapters/persona-fixed-adapter"
)

prompt = "[INST] Who are you? [/INST]"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        temperature=0.7,
        do_sample=True,
    )

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
9. Full Dependency Stack (pip freeze output)
bash
accelerate==0.24.1
bitsandbytes==0.41.1
datasets==2.18.0
diffusers==0.20.2
huggingface-hub==0.20.3
peft==0.6.2
pyarrow==14.0.1
tokenizers==0.15.1
torch==2.1.1+cu121
transformers==4.35.2
trl==0.7.1
10. Key Takeaways
QLoRA fine-tuning + persona dataset = adapter that changes the model's identity and voice. The base model provides knowledge; the adapter provides persona. 

Version pinning is mandatory. Installing these packages separately leads to unresolvable dependency conflicts. 

The Mistral tokenizer cache fix (prepend_scheme → add_prefix_space) is required for older transformers versions. 

Training time: 516 pairs, 1 epoch, 64 steps = ~7.8 minutes on an A100. 

