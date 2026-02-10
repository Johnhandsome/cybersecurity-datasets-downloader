# Dataset Balancing Guide

## 🎯 Overview

This guide helps you optimize the balance of cybersecurity datasets for different use cases when training language models. Different applications require different distributions of offensive, defensive, and analytical content.

## 📊 Default Balanced Distribution

### General-Purpose Cybersecurity Model

Balanced across all categories for comprehensive security knowledge:

```python
GENERAL_BALANCE = {
    # Phase 1: CTF & Bug Bounty (15%)
    "ctf_writeups": 0.08,           # 8%  - Practical problem-solving
    "bugbounty_reports": 0.07,      # 7%  - Real-world vulnerabilities
    
    # Phase 2: Exploits & Tools (20%)
    "exploitdb": 0.12,              # 12% - Exploit techniques
    "security_tools": 0.08,          # 8%  - Tool usage and techniques
    
    # Phase 3: YARA & Sigma Rules (8%)
    "yara_rules": 0.04,             # 4%  - Malware signatures
    "sigma_rules": 0.04,            # 4%  - SIEM detection
    
    # Phase 4: CVE Database (10%)
    "cve_data": 0.10,               # 10% - Vulnerability knowledge
    
    # Phase 5: Advanced Threats (47%)
    "malware_analysis": 0.20,       # 20% - Malware understanding
    "phishing_social": 0.08,        # 8%  - Social engineering
    "mobile_security": 0.08,        # 8%  - Mobile threats
    "crypto_attacks": 0.03,         # 3%  - Blockchain security
    "cloud_security": 0.05,         # 5%  - Cloud vulnerabilities
    "binary_exploit": 0.05,         # 5%  - Low-level exploitation
    "apt_intelligence": 0.08,       # 8%  - Threat intelligence
}
# Total: 100%
```

**Best for:** General security analysts, SOC analysts, security researchers

## 🛡️ Defensive Security (Blue Team)

Focused on detection, defense, and incident response:

```python
DEFENSIVE_BALANCE = {
    # Detection & Rules (35%)
    "yara_rules": 0.15,             # 15% - Malware detection
    "sigma_rules": 0.12,            # 12% - SIEM rules
    "malware_analysis": 0.08,       # 8%  - Understanding threats
    
    # Threat Intelligence (25%)
    "apt_intelligence": 0.15,       # 15% - APT tracking
    "cve_data": 0.10,               # 10% - Vulnerability management
    
    # Security Monitoring (20%)
    "phishing_social": 0.12,        # 12% - Phishing detection
    "cloud_security": 0.08,         # 8%  - Cloud monitoring
    
    # Response & Mitigation (20%)
    "ctf_writeups": 0.05,           # 5%  - Problem solving
    "bugbounty_reports": 0.10,      # 10% - Vulnerability analysis
    "security_tools": 0.05,          # 5%  - Defensive tools
    
    # Reduced Offensive (0% - optional)
    "exploitdb": 0.00,              # 0%  - Skip exploitation
    "binary_exploit": 0.00,         # 0%  - Skip low-level exploits
    "mobile_security": 0.00,        # 0%  - Skip if not needed
    "crypto_attacks": 0.00,         # 0%  - Skip if not needed
}
# Total: 100%
```

**Best for:** SOC analysts, threat hunters, incident responders, malware analysts

## ⚔️ Offensive Security (Red Team)

Focused on exploitation, penetration testing, and attack techniques:

```python
OFFENSIVE_BALANCE = {
    # Exploitation (45%)
    "exploitdb": 0.20,              # 20% - Exploit techniques
    "ctf_writeups": 0.15,           # 15% - Practical exploitation
    "binary_exploit": 0.10,         # 10% - Advanced exploitation
    
    # Bug Hunting (20%)
    "bugbounty_reports": 0.15,      # 15% - Vulnerability discovery
    "cve_data": 0.05,               # 5%  - Known vulnerabilities
    
    # Attack Tools (15%)
    "security_tools": 0.15,         # 15% - Offensive tooling
    
    # Advanced Attacks (20%)
    "mobile_security": 0.08,        # 8%  - Mobile pentesting
    "cloud_security": 0.08,         # 8%  - Cloud exploitation
    "crypto_attacks": 0.04,         # 4%  - Blockchain attacks
    
    # Minimal Defense
    "yara_rules": 0.00,             # 0%  - Skip detection rules
    "sigma_rules": 0.00,            # 0%  - Skip SIEM rules
    "malware_analysis": 0.00,       # 0%  - Skip malware analysis
    "phishing_social": 0.00,        # 0%  - Skip social engineering
    "apt_intelligence": 0.00,       # 0%  - Skip APT intel
}
# Total: 100%
```

**Best for:** Penetration testers, red team operators, exploit developers, bug bounty hunters

## 🔬 Malware Analysis & Reverse Engineering

Specialized for malware research and reverse engineering:

```python
MALWARE_ANALYSIS_BALANCE = {
    # Malware Focus (60%)
    "malware_analysis": 0.35,       # 35% - Malware samples & analysis
    "yara_rules": 0.15,             # 15% - Malware signatures
    "apt_intelligence": 0.10,       # 10% - APT campaigns
    
    # Reverse Engineering (20%)
    "binary_exploit": 0.15,         # 15% - Binary analysis
    "ctf_writeups": 0.05,           # 5%  - RE challenges
    
    # Related Threats (15%)
    "phishing_social": 0.08,        # 8%  - Malware delivery
    "mobile_security": 0.07,        # 7%  - Mobile malware
    
    # Supporting Knowledge (5%)
    "cve_data": 0.03,               # 3%  - Exploited vulnerabilities
    "crypto_attacks": 0.02,         # 2%  - Cryptominers
    
    # Minimal Focus
    "exploitdb": 0.00,              # 0%  - Skip general exploits
    "security_tools": 0.00,         # 0%  - Skip pentesting tools
    "sigma_rules": 0.00,            # 0%  - Skip SIEM rules
    "cloud_security": 0.00,         # 0%  - Skip cloud security
    "bugbounty_reports": 0.00,      # 0%  - Skip bug bounty
}
# Total: 100%
```

**Best for:** Malware analysts, reverse engineers, threat researchers

## ☁️ Cloud Security Specialist

Focused on cloud security across AWS, Azure, and GCP:

```python
CLOUD_SECURITY_BALANCE = {
    # Cloud Focus (40%)
    "cloud_security": 0.30,         # 30% - Cloud exploits & defense
    "cve_data": 0.10,               # 10% - Cloud CVEs
    
    # Web Security (25%)
    "bugbounty_reports": 0.15,      # 15% - Web vulnerabilities
    "exploitdb": 0.10,              # 10% - Web exploits
    
    # API & Container Security (15%)
    "security_tools": 0.10,         # 10% - Cloud security tools
    "ctf_writeups": 0.05,           # 5%  - Cloud CTF challenges
    
    # Detection & Response (10%)
    "sigma_rules": 0.05,            # 5%  - Cloud SIEM rules
    "apt_intelligence": 0.05,       # 5%  - Cloud-targeted APTs
    
    # Related Topics (10%)
    "crypto_attacks": 0.05,         # 5%  - Crypto in cloud
    "phishing_social": 0.05,        # 5%  - Cloud account takeover
    
    # Minimal Focus
    "yara_rules": 0.00,             # 0%  - Skip malware rules
    "malware_analysis": 0.00,       # 0%  - Skip malware
    "mobile_security": 0.00,        # 0%  - Skip mobile
    "binary_exploit": 0.00,         # 0%  - Skip binary exploits
}
# Total: 100%
```

**Best for:** Cloud security engineers, DevSecOps, cloud architects

## 📱 Mobile Security Specialist

Focused on Android and iOS security:

```python
MOBILE_SECURITY_BALANCE = {
    # Mobile Focus (50%)
    "mobile_security": 0.35,        # 35% - Mobile tools & exploits
    "malware_analysis": 0.15,       # 15% - Mobile malware
    
    # Reverse Engineering (20%)
    "binary_exploit": 0.15,         # 15% - Binary analysis
    "ctf_writeups": 0.05,           # 5%  - Mobile CTF
    
    # App Security (15%)
    "bugbounty_reports": 0.10,      # 10% - Mobile app bugs
    "cve_data": 0.05,               # 5%  - Mobile CVEs
    
    # Related Threats (10%)
    "phishing_social": 0.05,        # 5%  - Mobile phishing
    "crypto_attacks": 0.05,         # 5%  - Mobile cryptominers
    
    # Detection (5%)
    "yara_rules": 0.03,             # 3%  - Mobile malware rules
    "apt_intelligence": 0.02,       # 2%  - Mobile APTs
    
    # Minimal Focus
    "exploitdb": 0.00,              # 0%  - Skip general exploits
    "security_tools": 0.00,         # 0%  - Skip general tools
    "sigma_rules": 0.00,            # 0%  - Skip SIEM rules
    "cloud_security": 0.00,         # 0%  - Skip cloud
}
# Total: 100%
```

**Best for:** Mobile security researchers, Android/iOS pentesters, mobile app developers

## 🎓 Education & Training

Balanced for learning and teaching cybersecurity:

```python
EDUCATION_BALANCE = {
    # Hands-On Learning (40%)
    "ctf_writeups": 0.20,           # 20% - Problem-solving
    "bugbounty_reports": 0.10,      # 10% - Real vulnerabilities
    "security_tools": 0.10,         # 10% - Tool usage
    
    # Vulnerability Knowledge (20%)
    "cve_data": 0.12,               # 12% - CVE database
    "exploitdb": 0.08,              # 8%  - Exploit examples
    
    # Detection & Defense (20%)
    "yara_rules": 0.08,             # 8%  - Malware detection
    "sigma_rules": 0.07,            # 7%  - SIEM rules
    "phishing_social": 0.05,        # 5%  - Social engineering
    
    # Advanced Topics (20%)
    "malware_analysis": 0.08,       # 8%  - Malware basics
    "mobile_security": 0.04,        # 4%  - Mobile security
    "cloud_security": 0.04,         # 4%  - Cloud basics
    "binary_exploit": 0.02,         # 2%  - Binary exploitation
    "apt_intelligence": 0.02,       # 2%  - Threat intelligence
    "crypto_attacks": 0.00,         # 0%  - Advanced topic
}
# Total: 100%
```

**Best for:** Students, instructors, training platforms, certification prep

## 🔍 Implementing Custom Balance

### Method 1: Sampling During Preprocessing

```python
import json
import random
from pathlib import Path

def balance_dataset(base_dir, balance_config, output_file, total_samples=100000):
    """
    Create balanced dataset based on configuration.
    
    Args:
        base_dir: Base directory with all phase data
        balance_config: Dictionary with category weights
        output_file: Output JSON file path
        total_samples: Total number of samples to include
    """
    balanced_data = []
    
    for category, weight in balance_config.items():
        # Calculate samples for this category
        num_samples = int(total_samples * weight)
        
        # Load category data
        category_dir = Path(base_dir) / f"processed/{category}"
        category_files = list(category_dir.glob("*.json"))
        
        # Sample data
        for file in category_files:
            with open(file, 'r') as f:
                data = json.load(f)
                samples = random.sample(data, min(num_samples, len(data)))
                balanced_data.extend(samples)
                
                if len(balanced_data) >= total_samples:
                    break
    
    # Shuffle and save
    random.shuffle(balanced_data)
    
    with open(output_file, 'w') as f:
        json.dump(balanced_data, f, indent=2)
    
    print(f"✅ Created balanced dataset with {len(balanced_data)} samples")
    return balanced_data

# Usage
balance_dataset(
    base_dir="./cybersecurity_datasets",
    balance_config=DEFENSIVE_BALANCE,  # or your custom config
    output_file="balanced_defensive.json",
    total_samples=100000
)
```

### Method 2: Weighted Random Sampling During Training

```python
from torch.utils.data import WeightedRandomSampler

def create_weighted_sampler(dataset, balance_config):
    """
    Create sampler with custom weights.
    """
    # Assign weights to each sample based on category
    weights = []
    for item in dataset:
        category = item['category']
        weight = balance_config.get(category, 0.0)
        weights.append(weight)
    
    sampler = WeightedRandomSampler(
        weights=weights,
        num_samples=len(weights),
        replacement=True
    )
    
    return sampler

# Usage in DataLoader
from torch.utils.data import DataLoader

sampler = create_weighted_sampler(dataset, OFFENSIVE_BALANCE)
dataloader = DataLoader(dataset, sampler=sampler, batch_size=32)
```

## 📈 Monitoring Balance During Training

### Log Category Distribution

```python
import wandb
from collections import Counter

def log_batch_distribution(batch, step):
    """Log category distribution in training batch."""
    categories = [item['category'] for item in batch]
    distribution = Counter(categories)
    
    wandb.log({
        f"batch_dist/{cat}": count / len(batch)
        for cat, count in distribution.items()
    }, step=step)
```

### Validate Balance

```python
def validate_balance(dataset, target_balance, tolerance=0.05):
    """
    Validate dataset balance matches target.
    
    Args:
        dataset: List of samples with 'category' field
        target_balance: Target distribution dictionary
        tolerance: Acceptable deviation (default 5%)
    """
    categories = [item['category'] for item in dataset]
    actual_dist = Counter(categories)
    total = len(categories)
    
    print("Balance Validation:")
    print("-" * 60)
    
    for category, target_pct in target_balance.items():
        actual_count = actual_dist.get(category, 0)
        actual_pct = actual_count / total
        diff = abs(actual_pct - target_pct)
        
        status = "✅" if diff <= tolerance else "❌"
        print(f"{status} {category:20s}: {actual_pct:.2%} (target: {target_pct:.2%})")
        
    print("-" * 60)
```

## 🎯 Best Practices

### 1. Start with General Balance
- Begin training with general balanced distribution
- Evaluate model performance across all domains
- Identify weak areas

### 2. Iterative Refinement
- Adjust weights based on evaluation results
- Over-sample weak categories
- Under-sample over-represented categories

### 3. Maintain Diversity
- Don't zero out categories completely unless necessary
- Maintain at least 2-3% from each major category
- Diversity improves generalization

### 4. Use Case Alignment
- Match balance to deployment use case
- Red team tools need offensive focus
- SOC tools need defensive focus

### 5. Validation Split
- Ensure validation set has same balance
- Test on out-of-distribution data too
- Monitor for overfitting to specific categories

## 📊 Calculating Token Distribution

Estimate tokens per category:

```python
def estimate_tokens(file_size_gb, avg_chars_per_token=4):
    """
    Estimate token count from file size.
    
    Args:
        file_size_gb: File size in gigabytes
        avg_chars_per_token: Average characters per token (default 4)
    """
    bytes_total = file_size_gb * (1024 ** 3)
    chars_total = bytes_total  # Assume 1 byte = 1 char for text
    tokens = chars_total / avg_chars_per_token
    
    return int(tokens)

# Example
malware_tokens = estimate_tokens(2.5)  # 2.5 GB
print(f"Malware category: ~{malware_tokens:,} tokens")
# Output: Malware category: ~671,088,640 tokens
```

## 📚 Additional Resources

- [LLAMA3_TRAINING_GUIDE.md](./LLAMA3_TRAINING_GUIDE.md) - Complete training guide
- [PHASE5_GUIDE.md](./PHASE5_GUIDE.md) - Phase 5 dataset details
- [Hugging Face Dataset Balancing](https://huggingface.co/docs/datasets/process)

---

**Pro Tip:** Experiment with different balances for your specific use case. What works for one application may not work for another! 🎯
