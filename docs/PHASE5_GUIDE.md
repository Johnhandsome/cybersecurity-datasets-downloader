# Phase 5: Advanced Threats & Black Hat Tactics Guide

## 🎯 Overview

Phase 5 extends your cybersecurity dataset with advanced threat intelligence, black hat tactics, and sophisticated attack vectors. This phase is specifically designed for training AI models on:

- **Malware analysis and detection**
- **Phishing and social engineering tactics**
- **Mobile security (Android/iOS exploitation)**
- **Cryptojacking and blockchain attacks**
- **Cloud security vulnerabilities (AWS/Azure/GCP)**
- **Binary exploitation and reverse engineering**
- **Advanced Persistent Threats (APT) intelligence**

## ⚠️ Safety Warning

**CRITICAL:** Phase 5 includes repositories with **LIVE MALWARE SAMPLES**. This phase is intended for:
- Cybersecurity researchers
- Malware analysts
- Security professionals with proper training
- AI/ML engineers building security models

**You MUST:**
- Use an isolated virtual machine (VMware, VirtualBox, QEMU)
- Disable network access or use host-only networking
- Take VM snapshots before proceeding
- Understand malware analysis fundamentals
- Have proper authorization for malware research

See [MALWARE_SAFETY.md](./MALWARE_SAFETY.md) for comprehensive safety guidelines.

## 📦 What's Included

### 1. Malware Analysis (2.5 GB estimated)

**Safe Repositories:**
- `awesome-malware-analysis` - Comprehensive malware analysis resources
- `pan-unit42/iocs` - Palo Alto Unit 42 Indicators of Compromise
- `MalwareBazaar` - Malware sample information and hashes
- `Ransomware-Guide` - Ransomware tactics and detection
- `ransomware-simulator` - Safe ransomware behavior simulation

**Live Malware (with safety check):**
- `theZoo` - Live malware samples collection (⚠️ DANGEROUS)
- `vx_underground` - Malware source code archive (⚠️ DANGEROUS)

### 2. Phishing & Social Engineering (0.5 GB estimated)

- `Phishing.Database` - Extensive phishing URL database
- `social-engineer-toolkit` - SET framework and tactics
- `gophish` - Open-source phishing framework
- `evilginx2` - Advanced phishing with MFA bypass
- `Modlishka` - Reverse proxy phishing toolkit

### 3. Mobile Security (1.5 GB estimated)

**Android:**
- `Mobile-Security-Framework-MobSF` - Automated mobile app pentesting
- `androguard` - Android app reverse engineering
- `android-security-awesome` - Android vulnerabilities collection
- `apkleaks` - APK data leak detection
- `frida` - Dynamic instrumentation toolkit

**iOS:**
- `ios-resources` - iOS security resources
- `objection` - Mobile exploration toolkit

### 4. Crypto Attacks (0.3 GB estimated)

- `cryptominer` - Cryptojacking samples and analysis
- `MetaMask` - Blockchain security research
- `DeFiHackLabs` - DeFi smart contract exploits
- `not-so-smart-contracts` - Vulnerable smart contracts

### 5. Cloud Security (0.5 GB estimated)

**AWS:**
- `pacu` - AWS exploitation framework
- `cloudgoat` - Intentionally vulnerable AWS environment
- `prowler` - AWS security assessment tool

**Azure:**
- `AzureGoat` - Vulnerable Azure infrastructure
- `MicroBurst` - Azure exploitation toolkit

**GCP:**
- `GCPBucketBrute` - GCP bucket enumeration

**Multi-Cloud:**
- `cloudsploit` - Cloud security scanning
- `ScoutSuite` - Multi-cloud auditing tool

### 6. Binary Exploitation (1.0 GB estimated)

- `rop_emporium` - Return-oriented programming challenges
- `pwncollege` - Binary exploitation education
- `how2heap` - Heap exploitation techniques
- `CTF-pwn-tips` - Binary exploitation tips and tricks
- `MBE` - Modern Binary Exploitation course
- `RPISEC/Malware` - Malware reverse engineering challenges
- `Flare-On-Challenges` - FireEye Flare-On CTF archives

### 7. APT Intelligence (0.5 GB estimated)

- `aptnotes/data` - APT group reports and analysis
- `attack-stix-data` - MITRE ATT&CK framework in STIX format
- `awesome-threat-intelligence` - Threat intelligence resources
- `Ukraine-Cyber-Operations` - Real-world cyber conflict intelligence

### 8. Hugging Face Datasets

- `malware_api_call_sequences` - Malware API behavior patterns
- `phishing-dataset` - Labeled phishing emails
- `android-malware` - Android malware samples metadata

## 🚀 Usage

### Download Everything (with safety prompts)

```bash
python download_all.py --phase 5
```

When prompted about live malware, type `I UNDERSTAND THE RISKS` to proceed.

### Skip Live Malware Samples (Safer)

```bash
python download_all.py --phase 5 --skip-malware
```

This downloads all safe repositories and skips theZoo and vx_underground.

### Run as Part of Complete Download

```bash
# Download all phases
python download_all.py

# Download all phases, skip malware
python download_all.py --skip-malware
```

### Run Independently

```bash
# From phase5_advanced_threats.py
python phase5_advanced_threats.py --skip-malware
```

## 📊 Expected Results

After Phase 5 completion:

| Category | Repositories | Est. Size |
|----------|-------------|-----------|
| Malware Analysis | 7 | 2.5 GB |
| Phishing/Social Eng | 5 | 0.5 GB |
| Mobile Security | 7 | 1.5 GB |
| Crypto Attacks | 4 | 0.3 GB |
| Cloud Security | 8 | 0.5 GB |
| Binary Exploitation | 7 | 1.0 GB |
| APT Intelligence | 4 | 0.5 GB |
| HF Datasets | 3 | 0.5 GB |
| **Total** | **45** | **~7 GB** |

Combined with Phases 1-4: **~11 GB total** - perfect for Llama 3 8B fine-tuning!

## 🔍 Troubleshooting

### "Permission Denied" on Git Clone

Some repositories require authentication. If you encounter this:
1. Ensure you're not behind a restrictive firewall
2. Try cloning with HTTPS instead of SSH
3. Check if the repository still exists (some may be archived)

### Slow Downloads

Phase 5 includes large repositories. To speed up:
- Ensure stable internet connection
- Use `--update` flag for incremental updates
- Consider running overnight for first download

### Repository Not Found

Some repositories may be:
- Moved to new locations
- Renamed or archived
- Temporarily unavailable

The downloader will skip failed repos and continue.

### Hugging Face Datasets Not Downloading

Install the optional dependency:
```bash
pip install huggingface-hub
```

## 🎓 Using the Data

### For Llama 3 Training

See [LLAMA3_TRAINING_GUIDE.md](./LLAMA3_TRAINING_GUIDE.md) for:
- Recommended dataset balancing
- QLoRA configuration
- Training parameters
- Evaluation metrics

### Preprocessing Examples

See [../examples/preprocess_phase5.py](../examples/preprocess_phase5.py) for:
- Extracting malware analysis reports
- Parsing phishing email patterns
- Structuring APT intelligence
- Formatting for instruction tuning

### Dataset Balancing

See [DATASET_BALANCE.md](./DATASET_BALANCE.md) for:
- Recommended category percentages
- Offensive vs defensive balance
- Use case specific configurations

## 📚 Additional Resources

### Malware Analysis
- [Practical Malware Analysis Book](https://practicalmalwareanalysis.com/)
- [SANS FOR610](https://www.sans.org/cyber-security-courses/reverse-engineering-malware-malware-analysis-tools-techniques/)
- [Malware Unicorn](https://malwareunicorn.org/)

### Mobile Security
- [OWASP Mobile Security Testing Guide](https://mobile-security.gitbook.io/mobile-security-testing-guide/)
- [Android Security Internals](https://nostarch.com/androidsecurity)

### Binary Exploitation
- [LiveOverflow Binary Exploitation](https://www.youtube.com/playlist?list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN)
- [Nightmare](https://guyinatuxedo.github.io/)
- [pwn.college](https://pwn.college/)

### Cloud Security
- [Cloud Security Alliance](https://cloudsecurityalliance.org/)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [Azure Security Documentation](https://docs.microsoft.com/en-us/azure/security/)

## 🤝 Contributing

Found a valuable dataset missing from Phase 5? See [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Suggesting new repositories
- Reporting broken links
- Improving documentation
- Sharing preprocessing scripts

## ⚖️ Legal Considerations

**IMPORTANT:** 
- Malware research may be regulated in your jurisdiction
- Research local laws before downloading malware samples
- Use only for legitimate security research
- Never use for malicious purposes
- Respect repository licenses
- Do not redistribute malware samples

## 🆘 Getting Help

- Check [../TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for common issues
- Review safety guidelines in [MALWARE_SAFETY.md](./MALWARE_SAFETY.md)
- Open an issue on GitHub for specific problems
- Join cybersecurity communities (Reddit: r/netsec, r/malware)

---

**Remember:** With great data comes great responsibility. Use Phase 5 ethically and legally! 🛡️
