# Dataset Preprocessing Guide

This guide explains how to preprocess the downloaded cybersecurity datasets for AI/ML training, particularly for instruction-tuning large language models.

## 📋 Table of Contents

- [Overview](#overview)
- [Data Format](#data-format)
- [Phase 1: CTF Writeups](#phase-1-ctf-writeups)
- [Phase 2: Exploit Code](#phase-2-exploit-code)
- [Phase 3: Detection Rules](#phase-3-detection-rules)
- [Phase 4: CVE Data](#phase-4-cve-data)
- [Complete Pipeline](#complete-pipeline)
- [Llama 3 Instruction Format](#llama-3-instruction-format)
- [Best Practices](#best-practices)

## Overview

The downloaded datasets need to be converted into structured training formats. This guide focuses on creating instruction-following pairs suitable for fine-tuning models like Llama 3, GPT, or other instruction-tuned LLMs.

### Target Format

```json
{
  "instruction": "Question or task description",
  "input": "Additional context (optional)",
  "output": "Expected response"
}
```

For complete code examples, see [examples/preprocess_example.py](../examples/preprocess_example.py).

## Data Format

Save preprocessed data as JSONL (JSON Lines) for efficient streaming during training.

## Best Practices

### Data Quality

1. **Filter duplicates** - Remove similar instruction pairs
2. **Length control** - Limit input/output lengths (e.g., 2048 tokens)
3. **Quality checks** - Remove malformed or empty entries
4. **Balance** - Ensure diverse representation from all phases

### Safety Considerations

1. **Filter sensitive data** - Remove any leaked credentials or PII
2. **Add disclaimers** - Include ethical use warnings
3. **Test thoroughly** - Validate model outputs for safety

---

For a complete working example with full preprocessing pipeline, see [examples/preprocess_example.py](../examples/preprocess_example.py).
