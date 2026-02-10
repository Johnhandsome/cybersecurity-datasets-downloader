# 🛡️ Cybersecurity Datasets Downloader

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive, automated downloader for cybersecurity datasets designed for AI/ML training. This tool aggregates CTF writeups, exploit databases, YARA/Sigma rules, and CVE data into a structured format perfect for training security-focused language models.

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

## 📋 Prerequisites

- **Python 3.8+**
- **Git**
- **10+ GB free disk space** (varies by selected phases)
- **Stable internet connection**
- **(Optional) NVD API key** for faster CVE downloads

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
```

### Custom Directory

```bash
python download_all.py --dir /path/to/custom/directory
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
make check      # Check progress
make clean      # Remove downloaded datasets
```

## 📊 Dataset Details

| Phase | Contents | Estimated Size | Estimated Time |
|-------|----------|----------------|----------------|
| **Phase 1** | CTF writeups (5 repos) + Bug bounty reports (3 repos) | ~500 MB | 5-10 min |
| **Phase 2** | ExploitDB + 6 security tool repos + Python scripts | ~2-3 GB | 15-30 min |
| **Phase 3** | YARA rules (2 repos) + Sigma rules (2 repos) | ~100 MB | 5-10 min |
| **Phase 4** | CVE data for 2024-2025 + recent modifications | ~500 MB | 10-60 min* |

*Time varies based on NVD API key usage and rate limiting

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
│   │   └── sigmahq_sigmac/
│   ├── rules_statistics.json
│   └── phase3_results.json
├── phase4_cve_database/
│   ├── cve_2024.json
│   ├── cve_2025.json
│   ├── cve_recent_modified.json
│   ├── cve_statistics.json
│   └── phase4_results.json
└── download_summary.json
```

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
