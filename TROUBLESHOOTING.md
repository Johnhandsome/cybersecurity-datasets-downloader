# 🔧 Troubleshooting Guide

This guide helps you resolve common issues when downloading cybersecurity datasets.

---

## Table of Contents

- [HuggingFace Authentication](#huggingface-authentication)
- [Git Repository Issues](#git-repository-issues)
- [CVE/NVD API Issues](#cvenvd-api-issues)
- [Network and Timeout Issues](#network-and-timeout-issues)
- [Disk Space Issues](#disk-space-issues)
- [Python Dependencies](#python-dependencies)

---

## HuggingFace Authentication

### Issue: "Access to dataset X is restricted"

Some HuggingFace datasets (like `Canstralian/pentesting_dataset`) require authentication and access approval.

**Solution:**

1. **Create a HuggingFace account** (if you don't have one):
   - Visit: https://huggingface.co/join
   - Complete the registration

2. **Login via CLI:**
   ```bash
   huggingface-cli login
   ```
   - Enter your HuggingFace token when prompted
   - Token can be found at: https://huggingface.co/settings/tokens

3. **Request dataset access:**
   - Visit the dataset page (e.g., https://huggingface.co/datasets/Canstralian/pentesting_dataset)
   - Click "Request Access" or "Access Dataset"
   - Wait for approval (can take a few hours to days)

4. **Re-run the downloader:**
   ```bash
   python download_all.py --phase 2
   ```

### Issue: "Not logged in to HuggingFace"

**Solution:**

Ensure you've installed the HuggingFace CLI and logged in:

```bash
pip install huggingface-hub
huggingface-cli login
```

---

## Git Repository Issues

### Issue: "Repository not found" or "404"

Some repositories may be moved, renamed, or deleted.

**For Phase 1 - HackerOne Dataset:**

✅ **Fixed!** The downloader now uses the correct repository:
- Correct: `Hacker0x01/hackerone_disclosed_reports`

**For Phase 3 - SigmaC:**

✅ **Fixed!** The downloader now uses pySigma instead of the deprecated sigmac:
- Old (deprecated): `https://github.com/SigmaHQ/sigmac`
- New: `https://github.com/SigmaHQ/pySigma`

### Issue: "Authentication failed" when cloning

**Solution:**

If you're cloning private repositories, ensure you have:

1. **SSH keys configured:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ssh-add ~/.ssh/id_ed25519
   ```
   - Add the public key to GitHub: https://github.com/settings/keys

2. **Or use Personal Access Token (PAT):**
   - Create token at: https://github.com/settings/tokens
   - Use it in git URL: `https://TOKEN@github.com/user/repo.git`

### Issue: "Git clone timeout"

**Solution:**

For large repositories, increase timeout or use shallow clone (already implemented):

```bash
git clone --depth 1 <url>
```

---

## CVE/NVD API Issues

### Issue: "404 Client Error" for CVE queries

✅ **Fixed!** The downloader now uses the correct NVD API v2.0 datetime format:
- Format: `YYYY-MM-DDTHH:MM:SS.sss UTC-00:00`

### Issue: "Rate limiting" or "429 Too Many Requests"

**Solution:**

1. **Get an NVD API key** (recommended):
   - Register at: https://nvd.nist.gov/developers/request-an-api-key
   - Set environment variable:
     ```bash
     export NVD_API_KEY="your-api-key"
     ```
   - Rate limit increases from 6s to 0.6s per request

2. **Without API key:**
   - The downloader automatically uses a 6-second delay
   - Be patient, downloads will take longer

### Issue: "No CVEs found for year YYYY"

**Solution:**

This is normal for:
- Future years (e.g., 2025 early in the year)
- Years without published CVEs yet

The downloader handles this gracefully and continues.

---

## Network and Timeout Issues

### Issue: "Connection timeout" or "Network unreachable"

**Solution:**

1. **Check internet connection:**
   ```bash
   ping github.com
   ping nvd.nist.gov
   ```

2. **Check firewall/proxy settings:**
   - Ensure git and HTTPS traffic is allowed
   - Configure proxy if needed:
     ```bash
     git config --global http.proxy http://proxy:port
     export HTTPS_PROXY=http://proxy:port
     ```

3. **Retry with longer timeout:**
   - The downloader has built-in timeouts (5-10 minutes)
   - If interrupted, simply re-run - existing downloads are skipped

### Issue: "SSL Certificate verification failed"

**Solution:**

Update CA certificates:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ca-certificates

# macOS
brew install ca-certificates
```

---

## Disk Space Issues

### Issue: "No space left on device"

**Solution:**

1. **Check disk space:**
   ```bash
   df -h
   ```

2. **Expected dataset sizes:**
   - Phase 1 (CTF & Bug Bounty): ~500 MB
   - Phase 2 (Exploits & Tools): ~2-3 GB
   - Phase 3 (YARA & Sigma): ~100 MB
   - Phase 4 (CVE Database): ~500 MB - 2 GB
   - **Total: ~5-7 GB**

3. **Free up space or change download directory:**
   ```bash
   python download_all.py --dir /path/to/larger/disk
   ```

---

## Python Dependencies

### Issue: "ModuleNotFoundError" or import errors

**Solution:**

1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Required packages:**
   - `requests>=2.31.0` (required)
   - `tqdm>=4.66.0` (optional, for progress bars)
   - `datasets>=2.14.0` (optional, for HF datasets)
   - `huggingface-hub>=0.17.0` (optional, for HF datasets)

3. **Use virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## Avoiding Re-downloads

### Resume Interrupted Downloads

✅ **Built-in!** The downloader automatically:
- Skips existing repositories
- Checks for valid git repositories
- Validates downloaded content

**To resume:**
Simply re-run the same command:
```bash
python download_all.py
```

### Update Existing Repositories

To pull latest changes from existing repositories:
```bash
python download_all.py --update
```

This will:
- Skip non-git downloaded content (HF datasets, CVE files)
- Run `git pull` on existing git repositories
- Download any new repositories

---

## Common Error Messages

### "git: command not found"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git

# Verify
git --version
```

### "Python version mismatch"

**Solution:**
Requires Python 3.8 or higher:
```bash
python3 --version
# If < 3.8, upgrade Python
```

### "Permission denied" when creating directories

**Solution:**
```bash
# Use a directory you have write access to
python download_all.py --dir ~/cybersecurity_datasets

# Or fix permissions
sudo chown -R $USER:$USER ./cybersecurity_datasets
```

---

## Getting Help

If you continue to experience issues:

1. **Check existing issues:**
   - Visit: https://github.com/Johnhandsome/cybersecurity-datasets-downloader/issues

2. **Create a new issue:**
   - Include error message
   - Include Python version: `python --version`
   - Include OS: `uname -a` (Linux/Mac) or `ver` (Windows)
   - Include steps to reproduce

3. **Enable debug output:**
   ```bash
   python download_all.py 2>&1 | tee download.log
   ```

---

## Quick Reference

### Essential Commands

```bash
# Full download
python download_all.py

# Single phase
python download_all.py --phase 1

# Custom directory
python download_all.py --dir /path/to/data

# Update existing repos
python download_all.py --update

# HuggingFace login
huggingface-cli login

# Check progress
python check_progress.py
```

### Environment Variables

```bash
# NVD API key (optional, but recommended)
export NVD_API_KEY="your-api-key"

# HuggingFace token (if not using CLI login)
export HF_TOKEN="your-hf-token"

# Proxy settings (if needed)
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
```

---

**Last Updated:** 2026-02-10
