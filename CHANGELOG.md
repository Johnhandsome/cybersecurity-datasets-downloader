# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-10

### Fixed

#### Phase 1: CTF & Bug Bounty Reports
- **Fixed HackerOne dataset repository name**
  - Changed from incorrect `cybersecurity-datasets/hackerone-reports`
  - To correct `Hacker0x01/hackerone_disclosed_reports`
  - Updated all documentation and CLI instructions

#### Phase 2: Exploits & Security Tools
- **Fixed pentesting dataset access issues**
  - Added HuggingFace authentication check using `HfFolder.get_token()`
  - Improved error messages for gated datasets
  - Added clear instructions for authentication:
    - Run `huggingface-cli login` if not authenticated
    - Request access at dataset page if access not granted
  - Better handling of restricted/gated dataset errors

#### Phase 3: YARA & Sigma Rules
- **Fixed SigmaC repository not found error**
  - Replaced deprecated `https://github.com/SigmaHQ/sigmac` (archived/removed)
  - With modern replacement `https://github.com/SigmaHQ/pySigma`
  - Updated documentation to note the change

#### Phase 4: CVE Database
- **Fixed CVE download 404 errors**
  - Corrected NVD API v2.0 datetime format
  - Changed from `YYYY-MM-DDTHH:MM:SS.sss` to `YYYY-MM-DDTHH:MM:SS.sss UTC-00:00`
  - Fixed both `pubStartDate`/`pubEndDate` and `lastModStartDate`/`lastModEndDate`
  - Added graceful handling of 404 responses (no data available for year)
  - Improved error messages for missing CVE data

### Added

#### Smart Duplicate Detection
- **New `check_already_downloaded()` method** in all phases
  - Checks if target directory exists
  - Verifies if it's a valid git repository (`.git` folder)
  - Verifies if directory has content
  - Prevents re-downloading existing data
  - Improves resume capability for interrupted downloads

#### Update Functionality
- **New `--update` flag** in `download_all.py`
  - Updates existing git repositories with `git pull`
  - Skips non-git content (HuggingFace datasets, CVE JSON files)
  - Gracefully handles update failures
  - Can be combined with `--phase` flag for targeted updates
  - Usage: `python download_all.py --update`

#### Enhanced Clone Operations
- All phase downloaders now accept `update` parameter
- Clone methods check for existing repos before downloading
- Automatic update logic when `--update` flag is used
- Better messages distinguishing between:
  - New downloads
  - Skipped (already exists)
  - Updated (git pull succeeded)

### Improved

#### Error Messages
- More descriptive error messages for all failure scenarios
- Clear next-step instructions (💡 hints) for common issues
- Better context for authentication requirements
- Improved formatting with emojis for visual scanning

#### Documentation
- **New TROUBLESHOOTING.md** with comprehensive troubleshooting guide:
  - HuggingFace authentication setup
  - Git repository issues and solutions
  - CVE/NVD API issues and datetime formats
  - Network and timeout troubleshooting
  - Disk space management
  - Python dependencies troubleshooting
  - Quick reference commands
  - Environment variables reference
- **Updated README.md**:
  - Added link to TROUBLESHOOTING.md
  - Documented `--update` flag usage
  - Updated directory structure to show pySigma
  - Enhanced troubleshooting section with quick fixes
  - Added resume capability information
- **Updated command-line help** to include new `--update` flag

#### Robustness
- Better validation of existing downloads
- Improved handling of edge cases (empty directories, incomplete clones)
- More resilient to network interruptions
- Better handling of deprecated or moved repositories

### Developer Experience
- All phase downloaders now have consistent `update` parameter
- Improved code consistency across all phases
- Better separation of concerns (duplicate checking logic)
- Type hints maintained throughout

## [1.0.0] - 2024-01-15

### Added

#### Core Functionality
- Complete cybersecurity datasets downloader implementation
- Master orchestrator (`download_all.py`) for managing all download phases
- Progress checker (`check_progress.py`) for monitoring download status
- Comprehensive error handling and retry logic

#### Phase 1: CTF & Bug Bounty Reports
- Download 5 CTF writeup repositories:
  - ShundaZhang/htb
  - hackplayers/hackthebox-writeups
  - sohailburki1/HackTheBox-Writeups
  - jon-brandy/hackthebox
  - uppusaikiran/awesome-ctf-cheatsheet
- Download 3 bug bounty report repositories:
  - reddelexc/hackerone-reports
  - buildergk/hackerone-bug-bounty-reports
  - phlmox/public-reports
- Optional Hugging Face dataset integration for HackerOne reports

#### Phase 2: Exploits & Security Tools
- ExploitDB complete database download
- 6 security tool repositories:
  - Lockdoor-Framework
  - AdbNet
  - bane
  - Nettacker (OWASP)
  - fsociety
  - PayloadsAllTheThings
- Pentesting dataset from Hugging Face (optional)
- Automatic Python script extraction from all repositories

#### Phase 3: YARA & Sigma Rules
- YARA rules from Yara-Rules/rules and Neo23x0/signature-base
- Sigma rules from SigmaHQ/sigma and SigmaHQ/sigmac
- Automatic rule counting and statistics generation
- JSON statistics output

#### Phase 4: CVE Database
- NVD API integration for CVE downloads
- Support for year-based CVE downloads (default: 2024-2025)
- Recent modifications tracking (configurable, default: 120 days)
- Intelligent rate limiting (6s without API key, 0.6s with API key)
- Automatic retry on rate limit (429) responses
- Resumable downloads (skip existing files)
- Pagination support for large CVE datasets

#### Configuration & Setup
- `requirements.txt` with all Python dependencies
- `.gitignore` for Python and dataset directories
- `setup.sh` bash script for automated environment setup
- `Makefile` with convenient targets for all operations
- Virtual environment support

#### Documentation
- Comprehensive README.md with:
  - Feature overview and badges
  - Installation instructions (3 methods)
  - Usage examples for all scenarios
  - Dataset details and size estimates
  - NVD API key setup guide
  - Complete directory structure
  - Example output
  - Troubleshooting section
  - Legal and ethical use warnings
- CONTRIBUTING.md with contribution guidelines
- Code style guidelines
- Pull request process
- Instructions for adding new datasets
- CHANGELOG.md for version tracking

#### User Experience
- Emoji-rich console output for better readability
- Progress indicators for all operations
- Clear error messages with troubleshooting hints
- JSON result files for each phase
- Aggregate statistics and summaries
- Disk usage calculation
- Elapsed time tracking for each phase

#### Developer Features
- Modular phase-based architecture
- Consistent error handling across all phases
- Type hints for better code maintainability
- Comprehensive docstrings
- JSON output for programmatic access
- Resumable operations

### Features

- **Automated Downloads**: Clone git repositories with depth=1 for faster downloads
- **Error Recovery**: Graceful handling of network errors, timeouts, and rate limits
- **Progress Tracking**: Real-time progress display with emojis and statistics
- **Flexible Configuration**: Custom base directory and phase selection
- **API Key Support**: Optional NVD API key for 10x faster CVE downloads
- **Statistics Generation**: Automatic counting and aggregation of downloaded data
- **Resumability**: Skip existing downloads to support interrupted sessions
- **Multiple Interfaces**: Command-line, Makefile, and Python script interfaces

### Technical Details

- **Python Version**: Requires Python 3.8 or higher
- **Dependencies**: requests, tqdm, datasets, huggingface-hub
- **Git Operations**: Subprocess-based git cloning with timeout protection
- **API Integration**: RESTful NVD API with pagination and rate limiting
- **File Operations**: Path-based file management with pathlib
- **Error Handling**: Try-except blocks for all network and file operations
- **JSON Output**: Structured results in JSON format for each phase

### Known Limitations

- Hugging Face datasets require optional `huggingface-hub` installation
- NVD API rate limiting affects Phase 4 download speed without API key
- Large repositories (ExploitDB, PayloadsAllTheThings) may take significant time
- Network timeouts set to 5-10 minutes per repository
- Git operations require Git to be installed on the system

### Security Considerations

- No sensitive data storage or transmission
- All downloads from public repositories
- Optional API key storage via environment variable
- No execution of downloaded code
- Read-only operations on downloaded data

## [Unreleased]

### Planned Features

- Docker support for containerized downloads
- Preprocessing examples for AI/ML training
- Dataset filtering and customization options
- Parallel downloads for faster execution
- Web UI for download management
- Integration with more cybersecurity datasets
- Automatic dataset updates
- Compression options for storage optimization

---

## Version History

- **1.0.0** (2024-01-15) - Initial release with all 4 phases

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
