# 🛡️ Cybersecurity Datasets Downloader

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive, automated downloader for cybersecurity datasets designed for AI/ML training. This tool aggregates CTF writeups, exploit databases, YARA/Sigma rules, CVE data, malware analysis, phishing tools, mobile security, cloud security, binary exploitation, and APT intelligence into a structured format perfect for training security-focused language models like **Llama 3 8B**.

## ✨ Features

### 📦 Phase 1: CTF & Bug Bounty Reports
- **5 CTF writeup repositories** from HackTheBox and other platforms
- **3 bug bounty report repositories** with real-world vulnerabilities
- **HackerOne dataset** integration (optional, requires Hugging Face)

### 💣 Phase 2: Exploits & Security Tools
- **ExploitDB** - Complete Offensive Security exploit database
- **6 security tool repositories** (Lockdoor, Nettacker, PayloadsAllTheThings, etc.)
- **Pentesting dataset** from Hugging Face (optional)
- **Automatic Python script extraction** from all repositories

### 🛡️ Phase 3: YARA & Sigma Rules
- **YARA rules** - Malware detection signatures
- **Sigma rules** - Generic SIEM detection rules
- **Automatic rule counting** and statistics generation

### 🚨 Phase 4: CVE Database
- **NVD API integration** - Download CVE data from National Vulnerability Database
- **Configurable year ranges** (defaults to 2024-2025)
- **Recent modifications** tracking (last 120 days)
- **Smart rate limiting** - Automatic handling with/without API key
- **Resumable downloads** - Skip already downloaded years

### ⚠️ 🔥 Phase 5: Advanced Threats & Black Hat Tactics (NEW!)
- **Malware Analysis** - 7 repositories including theZoo and vx-underground (**LIVE MALWARE** ⚠️)
- **Phishing & Social Engineering** - 5 repositories with phishing tools and databases
- **Mobile Security** - 7 repositories covering Android/iOS exploitation and analysis
- **Crypto Attacks** - 4 repositories on cryptojacking and blockchain exploits
- **Cloud Security** - 8 repositories for AWS/Azure/GCP security testing
- **Binary Exploitation** - 7 repositories on ROP, heap, stack exploitation
- **APT Intelligence** - 4 repositories with threat intelligence and APT reports
- **HuggingFace Datasets** - Malware API calls, phishing emails, Android malware
- **Safety Features** - Interactive warnings, `--skip-malware` flag, comprehensive safety documentation

**⚠️ IMPORTANT:** Phase 5 includes live malware samples. Use ONLY in isolated VMs. See [docs/MALWARE_SAFETY.md](docs/MALWARE_SAFETY.md) for safety guidelines.

## 📋 Prerequisites

- **Python 3.8+**
- **Git**
- **15+ GB free disk space** (11 GB for all phases + overhead)
- **Stable internet connection**
- **(Optional) NVD API key** for faster CVE downloads
- **(Optional) HuggingFace account** for gated datasets
- **⚠️ Isolated VM required for Phase 5 malware samples**

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Johnhandsome/cybersecurity-datasets-downloader.git
cd cybersecurity-datasets-downloader

# Run setup script
bash setup.sh

# Activate virtual environment
source venv/bin/activate

# Download all datasets
python download_all.py
```

## 📥 Installation

### Method 1: Using setup script (Recommended)

```bash
bash setup.sh
source venv/bin/activate
```

### Method 2: Manual installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 3: Using Make

```bash
make setup
source venv/bin/activate
```

## 🎯 Usage

### Download All Datasets

```bash
python download_all.py
```

### Download Specific Phase

```bash
# Phase 1: CTF & Bug Bounty
python download_all.py --phase 1

# Phase 2: Exploits & Tools
python download_all.py --phase 2

# Phase 3: YARA & Sigma Rules
python download_all.py --phase 3

# Phase 4: CVE Database
python download_all.py --phase 4

# Phase 5: Advanced Threats & Black Hat Tactics (⚠️ includes live malware)
python download_all.py --phase 5

# Phase 5 without live malware samples (safer)
python download_all.py --phase 5 --skip-malware
```

### Custom Directory

```bash
python download_all.py --dir /path/to/custom/directory
```

### Update Existing Repositories

```bash
# Update all git repositories with latest changes
python download_all.py --update

# Update specific phase
python download_all.py --phase 3 --update
```

### Check Progress

```bash
python check_progress.py
```

### Using Makefile

```bash
make run        # Download all datasets
make phase1     # Download Phase 1 only
make phase2     # Download Phase 2 only
make phase3     # Download Phase 3 only
make phase4     # Download Phase 4 only
make phase5     # Download Phase 5 only
make check      # Check progress
make clean      # Remove downloaded datasets
```

## 📊 Dataset Details

| Phase | Contents | Estimated Size | Estimated Time |
|-------|----------|----------------|----------------|
| **Phase 1** | CTF writeups (5 repos) + Bug bounty reports (3 repos) | ~1.5 GB | 10-15 min |
| **Phase 2** | ExploitDB + 6 security tool repos + Python scripts | ~2 GB | 15-30 min |
| **Phase 3** | YARA rules (2 repos) + Sigma rules (2 repos) | ~0.5 GB | 5-10 min |
| **Phase 4** | CVE data for 2024-2025 + recent modifications | ~0.5 GB | 10-60 min* |
| **Phase 5** | Malware, phishing, mobile, cloud, binary, APT (45 repos) | ~6.5 GB | 30-60 min |
| **TOTAL** | **All 5 Phases** | **~11 GB** | **70-175 min** |

*Time varies based on NVD API key usage and rate limiting

**Perfect for training Llama 3 8B!** The ~11 GB dataset size provides optimal coverage for fine-tuning an 8B parameter model.

## 🔑 NVD API Key Setup

For faster CVE downloads in Phase 4, obtain a free API key from NVD:

1. Visit [NVD API Request](https://nvd.nist.gov/developers/request-an-api-key)
2. Request an API key (free, no account needed)
3. Set the environment variable:

```bash
export NVD_API_KEY=your_api_key_here
```

**Rate Limits:**
- With API key: 50 requests per 30 seconds (0.6s delay)
- Without API key: 5 requests per 30 seconds (6s delay)

## 📁 Directory Structure

```
cybersecurity_datasets/
├── phase1_ctf_bugbounty/
│   ├── ctf_writeups/
│   │   ├── htb_shundazhang/
│   │   ├── htb_hackplayers/
│   │   ├── htb_sohailburki1/
│   │   ├── htb_jonbrandy/
│   │   └── awesome_ctf_cheatsheet/
│   ├── bugbounty_repos/
│   │   ├── hackerone_reddelexc/
│   │   ├── hackerone_buildergk/
│   │   └── public_reports_phlmox/
│   ├── hackerone_reports/
│   └── phase1_results.json
├── phase2_exploits_tools/
│   ├── exploitdb/
│   ├── security_tools/
│   │   ├── lockdoor_framework/
│   │   ├── adbnet/
│   │   ├── bane/
│   │   ├── nettacker/
│   │   ├── fsociety/
│   │   └── payloadsallthethings/
│   ├── pentesting_dataset/
│   ├── extracted_python_scripts/
│   └── phase2_results.json
├── phase3_yara_sigma/
│   ├── yara_rules/
│   │   ├── yara_rules_official/
│   │   └── neo23x0_signature_base/
│   ├── sigma_rules/
│   │   ├── sigmahq_sigma/
│   │   └── pysigma/
│   ├── rules_statistics.json
│   └── phase3_results.json
├── phase4_cve_database/
│   ├── cve_2024.json
│   ├── cve_2025.json
│   ├── cve_recent_modified.json
│   ├── cve_statistics.json
│   └── phase4_results.json
├── phase5_advanced_threats/
│   ├── malware_analysis/
│   │   ├── malware_analysis/
│   │   ├── malware_traffic_analysis/
│   │   ├── theZoo/ (⚠️ LIVE MALWARE)
│   │   └── vx_underground/ (⚠️ LIVE MALWARE)
│   ├── phishing_social_eng/
│   │   ├── phishing_database/
│   │   ├── gophish/
│   │   └── evilginx2/
│   ├── mobile_security/
│   │   ├── mobsf/
│   │   ├── androguard/
│   │   └── frida/
│   ├── crypto_attacks/
│   ├── cloud_security/
│   │   ├── pacu/
│   │   ├── cloudgoat/
│   │   └── prowler/
│   ├── binary_exploitation/
│   │   ├── how2heap/
│   │   └── pwn_college/
│   ├── apt_intelligence/
│   │   ├── apt_notes/
│   │   └── mitre_attack/
│   ├── huggingface_datasets/
│   └── phase5_results.json
└── download_summary.json
```

## ⚠️ Phase 5 Safety Warning

**CRITICAL:** Phase 5 includes repositories with **LIVE MALWARE SAMPLES**. 

Before downloading Phase 5:
1. Read [docs/MALWARE_SAFETY.md](docs/MALWARE_SAFETY.md) completely
2. Set up an isolated VM (VMware/VirtualBox/QEMU)
3. Disable network access in the VM
4. Take VM snapshots before proceeding

**Safer option:** Use `--skip-malware` flag to skip live malware repositories:
```bash
python download_all.py --phase 5 --skip-malware
```

This downloads all Phase 5 content EXCEPT theZoo and vx-underground (live malware).

## 📚 Documentation

### Phase 5 Specific Guides
- **[docs/PHASE5_GUIDE.md](docs/PHASE5_GUIDE.md)** - Complete Phase 5 guide and usage
- **[docs/MALWARE_SAFETY.md](docs/MALWARE_SAFETY.md)** - Essential safety procedures for malware handling
- **[docs/LLAMA3_TRAINING_GUIDE.md](docs/LLAMA3_TRAINING_GUIDE.md)** - Fine-tuning Llama 3 8B on these datasets
- **[docs/DATASET_BALANCE.md](docs/DATASET_BALANCE.md)** - Dataset balancing strategies

### General Documentation
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[docs/PREPROCESSING.md](docs/PREPROCESSING.md)** - Data preprocessing guides

## 📋 Example Output

```
================================================================================
🛡️  CYBERSECURITY DATASETS DOWNLOADER
================================================================================
📁 Base directory: /path/to/cybersecurity_datasets
🕐 Started at: 2024-01-15 10:30:00
================================================================================

🔍 Checking Dependencies...
  ✅ git is installed
  ✅ Python 3.11.5 is installed
  ✅ requests library is installed
  ✅ tqdm library is installed
  ⚠️  huggingface-hub is not installed (optional, for HF datasets)

================================================================================
🚀 Starting Phase 1: CTF & Bug Bounty
================================================================================

🚩 Downloading CTF Writeup Repositories...
  📦 Cloning https://github.com/ShundaZhang/htb...
  ✅ Successfully cloned to htb_shundazhang
  [... more downloads ...]

================================================================================
📊 PHASE 1 SUMMARY
================================================================================
  CTF Repositories: 5/5 successful
  Bug Bounty Repositories: 3/3 successful
  HackerOne Dataset: ⚠️
================================================================================

[... continues with all phases ...]

================================================================================
🎉 FINAL SUMMARY
================================================================================
  Phases Completed: 4/4
  Total Time: 25.3 minutes
  Total Disk Usage: 3.45 GB

  Phase Details:
    ✅ Phase 1: CTF & Bug Bounty (7.2 min)
    ✅ Phase 2: Exploits & Tools (12.5 min)
    ✅ Phase 3: YARA & Sigma Rules (3.1 min)
    ✅ Phase 4: CVE Database (2.5 min)

  📁 Dataset location: /path/to/cybersecurity_datasets
================================================================================
```

## 🔧 Troubleshooting

**📖 For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

### Quick Fixes

#### HuggingFace Datasets Require Authentication

If you see "Access to dataset X is restricted":

1. Create HuggingFace account: https://huggingface.co/join
2. Login via CLI:
   ```bash
   huggingface-cli login
   ```
3. Request access to gated datasets
4. Re-run the downloader

#### Avoiding Re-downloads

The downloader automatically skips existing repositories. To update them:

```bash
python download_all.py --update
```

#### Resume Interrupted Downloads

Simply re-run the same command. Already downloaded items will be skipped.

### Git Clone Failures

**Problem:** Repository cloning times out or fails

**Solutions:**
- Check internet connection
- Try running single phase: `python download_all.py --phase 1`
- Manually clone failed repositories
- Check if repositories still exist (some may be archived/deleted)

### Python Import Errors

**Problem:** `ModuleNotFoundError` when running scripts

**Solutions:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### NVD API Rate Limiting

**Problem:** CVE downloads are very slow

**Solutions:**
- Obtain and set NVD API key (see [NVD API Key Setup](#-nvd-api-key-setup))
- Download CVEs in smaller batches
- Run Phase 4 separately during off-peak hours

### Disk Space Issues

**Problem:** Running out of disk space

**Solutions:**
- Download phases individually
- Use custom directory on larger disk: `python download_all.py --dir /path/to/large/disk`
- Skip optional phases
- Clean up between phases: `make clean`

### Hugging Face Dataset Errors

**Problem:** Cannot download HackerOne or pentesting datasets

**Solutions:**
```bash
# Install huggingface_hub
pip install huggingface-hub

# Login to Hugging Face (if dataset requires authentication)
huggingface-cli login
```

**See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions.**

## ⚖️ Legal and Ethical Use

**⚠️ IMPORTANT:** This tool downloads publicly available cybersecurity data for educational and research purposes.

### Acceptable Use
- ✅ Security research and education
- ✅ AI/ML model training for defensive purposes
- ✅ Academic research
- ✅ Improving security tools and practices

### Prohibited Use
- ❌ Illegal hacking or unauthorized access
- ❌ Malicious exploitation of vulnerabilities
- ❌ Harassment or harm to others
- ❌ Violation of computer fraud laws

**You are responsible for using this data ethically and legally.** Always obtain proper authorization before testing security vulnerabilities. Follow responsible disclosure practices.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Datasets
See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding new datasets to any phase.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## 🔗 Dataset Preprocessing

For guidance on preprocessing downloaded datasets for AI/ML training, see [docs/PREPROCESSING.md](docs/PREPROCESSING.md).

Example preprocessing script: [examples/preprocess_example.py](examples/preprocess_example.py)

## 📚 Related Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [Exploit Database](https://www.exploit-db.com/)
- [HackerOne Disclosed Reports](https://hackerone.com/hacktivity)

## 🙏 Credits

This project aggregates data from numerous open-source repositories and datasets:

- **CTF Writeups:** ShundaZhang, hackplayers, sohailburki1, jon-brandy, uppusaikiran
- **Bug Bounty:** reddelexc, buildergk, phlmox
- **Exploits:** Offensive Security ExploitDB
- **Security Tools:** SofianeHamlaoui, 0x1CA3, AlaBouali, OWASP, Manisso, swisskyrepo
- **YARA Rules:** Yara-Rules, Neo23x0
- **Sigma Rules:** SigmaHQ
- **CVE Data:** NIST National Vulnerability Database

Thank you to all contributors and maintainers of these projects!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Cybersecurity Datasets Downloader Contributors

## 📧 Contact

For questions, issues, or suggestions:
- Open an issue on [GitHub](https://github.com/Johnhandsome/cybersecurity-datasets-downloader/issues)
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ for the cybersecurity and AI/ML community**
