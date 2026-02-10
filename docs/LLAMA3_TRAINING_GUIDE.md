# Llama 3 8B Training Guide for Cybersecurity Datasets

## 🎯 Overview

This guide provides comprehensive instructions for fine-tuning **Meta Llama 3 8B** on the cybersecurity datasets collected through Phases 1-5. The complete dataset (~11 GB) is optimally sized for creating a cybersecurity-focused language model.

## 📊 Dataset Size & Composition

### Total Dataset Breakdown

| Phase | Category | Size | Token Estimate |
|-------|----------|------|----------------|
| Phase 1 | CTF & Bug Bounty | 1.5 GB | ~400M tokens |
| Phase 2 | Exploits & Tools | 2.0 GB | ~500M tokens |
| Phase 3 | YARA & Sigma Rules | 0.5 GB | ~100M tokens |
| Phase 4 | CVE Database | 0.5 GB | ~100M tokens |
| Phase 5 | Malware Analysis | 2.5 GB | ~600M tokens |
| Phase 5 | Phishing/Social Eng | 0.5 GB | ~100M tokens |
| Phase 5 | Mobile Security | 1.5 GB | ~350M tokens |
| Phase 5 | Crypto Attacks | 0.3 GB | ~70M tokens |
| Phase 5 | Cloud Security | 0.5 GB | ~100M tokens |
| Phase 5 | Binary Exploitation | 1.0 GB | ~250M tokens |
| Phase 5 | APT Intelligence | 0.5 GB | ~100M tokens |
| **TOTAL** | **ALL PHASES** | **~11 GB** | **~2.67B tokens** |

### Why This Size is Optimal for Llama 3 8B

- **8B parameters** benefit from **8-15 GB** of diverse, high-quality data
- **2.67B tokens** provides sufficient exposure without overfitting
- **Diverse categories** ensure well-rounded cybersecurity knowledge
- **Real-world data** from actual vulnerabilities, exploits, and reports

## 🏗️ Training Architecture

### Recommended: QLoRA (Quantized Low-Rank Adaptation)

**Why QLoRA?**
- Train on consumer GPUs (24GB VRAM)
- Preserve base model knowledge
- Fast convergence
- Production-ready efficiency

**Hardware Requirements:**

| Configuration | VRAM | Training Time | Cost |
|--------------|------|---------------|------|
| **Minimum** | RTX 3090/4090 (24GB) | ~5-7 days | $50-100 (cloud) |
| **Recommended** | A100 40GB | ~2-3 days | $200-300 (cloud) |
| **Optimal** | A100 80GB | ~1-2 days | $400-500 (cloud) |
| **Multi-GPU** | 4x A100 40GB | ~12-18 hours | $500-700 (cloud) |

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
# Create environment
conda create -n llama3-cyber python=3.10
conda activate llama3-cyber

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install training libraries
pip install transformers==4.36.0
pip install peft==0.7.1
pip install bitsandbytes==0.41.3
pip install accelerate==0.25.0
pip install datasets==2.16.0
pip install trl==0.7.10

# Optional: Monitoring
pip install wandb tensorboard
```

### 2. Download Llama 3 8B Base Model

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "meta-llama/Meta-Llama-3-8B"

# Requires Hugging Face access token and Meta approval
tokenizer = AutoTokenizer.from_pretrained(model_id, token="YOUR_HF_TOKEN")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    token="YOUR_HF_TOKEN",
    device_map="auto",
    torch_dtype=torch.float16
)
```

**Note:** Request access at [Meta Llama Downloads](https://ai.meta.com/llama/)

### 3. Preprocess Your Datasets

Use the preprocessing examples in `examples/preprocess_phase5.py`:

```bash
# Preprocess all phases
python examples/preprocess_example.py --all-phases --output processed_data/

# Results in instruction-tuning format
# {"instruction": "...", "input": "...", "output": "..."}
```

## 📝 Training Configuration

### QLoRA Configuration

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# LoRA config
lora_config = LoraConfig(
    r=64,                        # Rank (higher = more capacity, slower)
    lora_alpha=16,              # Scaling factor
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# Load model with quantization
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)

# Prepare for training
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

# Print trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 335M || all params: 8.37B || trainable%: 4.00%
```

### Training Hyperparameters

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    # Output
    output_dir="./llama3-cyber-qlora",
    
    # Training schedule
    num_train_epochs=3,                    # Start with 3, adjust based on validation
    max_steps=-1,                           # -1 = use num_train_epochs
    
    # Batch size (adjust for your GPU)
    per_device_train_batch_size=4,         # 24GB VRAM: 4, 40GB VRAM: 8
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,         # Effective batch size = 16
    
    # Learning rate
    learning_rate=2e-4,                    # QLoRA sweet spot
    lr_scheduler_type="cosine",            # Smooth learning rate decay
    warmup_steps=100,                      # Warmup for stable training
    
    # Optimization
    optim="paged_adamw_8bit",              # Memory-efficient optimizer
    weight_decay=0.01,                     # Prevent overfitting
    max_grad_norm=1.0,                     # Gradient clipping
    
    # Mixed precision
    bf16=True,                              # Use bfloat16 if available
    fp16=False,                             # Fallback to fp16 if no bf16
    
    # Logging
    logging_steps=10,
    logging_dir="./logs",
    
    # Evaluation
    evaluation_strategy="steps",
    eval_steps=100,                        # Evaluate every 100 steps
    save_strategy="steps",
    save_steps=100,
    save_total_limit=3,                    # Keep only 3 checkpoints
    
    # Performance
    dataloader_num_workers=4,
    dataloader_pin_memory=True,
    group_by_length=True,                  # More efficient batching
    
    # Misc
    report_to="tensorboard",               # or "wandb"
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
)
```

## 🎨 Data Preprocessing

### Instruction Format

Convert datasets to instruction-tuning format:

```python
# Example: CVE to instruction format
{
    "instruction": "Analyze this CVE and provide exploitation details",
    "input": "CVE-2024-1234: Buffer overflow in Apache HTTPd 2.4.50...",
    "output": "This is a stack-based buffer overflow vulnerability. Exploitation requires..."
}

# Example: Malware analysis
{
    "instruction": "What are the key indicators of this malware?",
    "input": "Hash: abc123... Behavior: Creates registry key HKLM\\...",
    "output": "This malware exhibits characteristics of ransomware: 1) Registry persistence..."
}

# Example: Phishing detection
{
    "instruction": "Is this email a phishing attempt?",
    "input": "From: security@paypa1.com Subject: Your account has been locked...",
    "output": "Yes, this is a phishing email. Red flags: 1) Misspelled domain (paypa1 vs paypal)..."
}
```

### Dataset Balancing

**Recommended distribution for general cybersecurity model:**

```python
dataset_weights = {
    "ctf_bugbounty": 0.15,      # 15% - Practical exploitation
    "exploits_tools": 0.20,      # 20% - Attack techniques
    "yara_sigma": 0.08,          # 8%  - Detection rules
    "cve_database": 0.10,        # 10% - Vulnerability knowledge
    "malware_analysis": 0.20,    # 20% - Threat analysis
    "phishing_social": 0.08,     # 8%  - Social engineering
    "mobile_security": 0.08,     # 8%  - Mobile threats
    "crypto_attacks": 0.03,      # 3%  - Blockchain security
    "cloud_security": 0.05,      # 5%  - Cloud vulnerabilities
    "binary_exploit": 0.05,      # 5%  - Low-level exploitation
    "apt_intelligence": 0.08,    # 8%  - Threat intelligence
}
```

See [DATASET_BALANCE.md](./DATASET_BALANCE.md) for use-case specific distributions.

## 🚂 Training Script

### Complete Training Example

```python
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from trl import SFTTrainer
from peft import LoraConfig

# Load processed dataset
dataset = load_dataset("json", data_files="processed_data/train.jsonl")
eval_dataset = load_dataset("json", data_files="processed_data/eval.jsonl")

# Format prompt template
def format_instruction(example):
    return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""

# Tokenize
def tokenize_function(examples):
    return tokenizer(
        [format_instruction(ex) for ex in examples],
        truncation=True,
        max_length=2048,
        padding="max_length",
    )

# Initialize trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    eval_dataset=eval_dataset["train"],
    peft_config=lora_config,
    dataset_text_field="text",
    max_seq_length=2048,
    tokenizer=tokenizer,
    args=training_args,
    packing=False,
)

# Train!
trainer.train()

# Save final model
trainer.save_model("./llama3-cyber-final")
```

### Running Training

```bash
# Single GPU
python train_llama3_cyber.py

# Multi-GPU with DeepSpeed
accelerate launch --config_file deepspeed_config.yaml train_llama3_cyber.py

# With W&B logging
WANDB_PROJECT=llama3-cyber python train_llama3_cyber.py
```

## 📈 Monitoring Training

### Key Metrics to Watch

1. **Training Loss:** Should decrease steadily
2. **Evaluation Loss:** Should track training loss (watch for overfitting)
3. **Perplexity:** Lower is better (e^loss)
4. **Learning Rate:** Should follow schedule
5. **GPU Memory:** Should be stable

### TensorBoard

```bash
tensorboard --logdir ./logs --port 6006
```

### Weights & Biases

```python
import wandb

wandb.init(
    project="llama3-cyber",
    config={
        "model": "meta-llama/Meta-Llama-3-8B",
        "dataset_size": "11GB",
        "method": "QLoRA",
        "lora_r": 64,
        "epochs": 3,
    }
)
```

## 🧪 Evaluation

### Validation Metrics

```python
# Perplexity
from math import exp
perplexity = exp(eval_loss)

# Accuracy on held-out test set
# BLEU score for specific tasks
# Human evaluation for quality
```

### Cybersecurity-Specific Tests

Create test cases for:

1. **CVE Analysis:**
   ```
   Input: "Explain CVE-2021-44228 (Log4Shell)"
   Expected: Accurate technical description, exploitation details, mitigation
   ```

2. **Malware Classification:**
   ```
   Input: "Classify malware with these behaviors: [...]"
   Expected: Correct family (e.g., ransomware, trojan)
   ```

3. **Phishing Detection:**
   ```
   Input: "[Email content]"
   Expected: Accurate phishing detection with reasoning
   ```

4. **Exploit Development:**
   ```
   Input: "How would you exploit [vulnerability description]"
   Expected: Ethical, accurate technical steps
   ```

## 🎯 Fine-Tuning Strategies

### Early Stopping

Stop training when validation loss plateaus:

```python
from transformers import EarlyStoppingCallback

trainer = SFTTrainer(
    # ... other args
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)
```

### Learning Rate Finding

Find optimal learning rate:

```python
from torch_lr_finder import LRFinder

lr_finder = LRFinder(model, optimizer, criterion)
lr_finder.range_test(train_loader, end_lr=1, num_iter=100)
lr_finder.plot()  # Suggests optimal LR
```

### Curriculum Learning

Train on easier examples first:

1. Start with structured data (CVEs, YARA rules)
2. Progress to complex analysis (APT reports, exploit chains)
3. Finish with nuanced tasks (phishing detection, social engineering)

## 💾 Model Deployment

### Merge LoRA Weights

```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")

# Load LoRA weights
model = PeftModel.from_pretrained(base_model, "./llama3-cyber-final")

# Merge and save
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./llama3-cyber-merged")
tokenizer.save_pretrained("./llama3-cyber-merged")
```

### Quantization for Inference

```python
# 4-bit quantization for deployment
from transformers import BitsAndBytesConfig

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    "./llama3-cyber-merged",
    quantization_config=quant_config,
    device_map="auto"
)
```

## 🐛 Troubleshooting

### OOM (Out of Memory)

```python
# Reduce batch size
per_device_train_batch_size = 2

# Increase gradient accumulation
gradient_accumulation_steps = 8

# Enable gradient checkpointing
model.gradient_checkpointing_enable()

# Use 4-bit training
load_in_4bit = True
```

### Slow Training

```python
# Enable Flash Attention 2
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    attn_implementation="flash_attention_2",
)

# Optimize dataloader
dataloader_num_workers = 8
dataloader_pin_memory = True
```

### Poor Convergence

- Check learning rate (try 1e-4 to 5e-4)
- Increase warmup steps
- Verify data quality and format
- Check for label noise
- Ensure sufficient training data

## 📚 Additional Resources

### Papers
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [Llama 3: Technical Report](https://ai.meta.com/research/)

### Tutorials
- [Hugging Face Fine-Tuning Guide](https://huggingface.co/docs/transformers/training)
- [QLoRA Tutorial](https://huggingface.co/blog/4bit-transformers-bitsandbytes)
- [Weights & Biases LLM Course](https://www.wandb.courses/courses/training-fine-tuning-LLMs)

### Tools
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) - LLM training framework
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) - Easy fine-tuning UI
- [vLLM](https://github.com/vllm-project/vllm) - Fast inference

## 🎓 Expected Results

After successful training, your model should:

✅ **Understand cybersecurity concepts** across all domains  
✅ **Analyze CVEs** and explain exploitation techniques  
✅ **Detect phishing** and social engineering attempts  
✅ **Classify malware** based on behavior and indicators  
✅ **Suggest mitigations** for vulnerabilities  
✅ **Understand cloud security** issues (AWS/Azure/GCP)  
✅ **Explain binary exploitation** techniques  
✅ **Recognize APT tactics** and threat intelligence  

## ⚠️ Ethical Considerations

When deploying your model:

- **Include safety guardrails** to prevent malicious use
- **Add ethical disclaimers** in responses
- **Monitor for misuse** in production
- **Restrict access** appropriately
- **Document limitations** clearly

---

**Good luck with your training!** 🚀🛡️

For questions or issues, see the main [README.md](../README.md) or open a GitHub issue.
