# Contributing to Cybersecurity Datasets Downloader

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

1. Check if the issue already exists in the [issue tracker](https://github.com/Johnhandsome/cybersecurity-datasets-downloader/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Any error messages or logs

### Suggesting Enhancements

1. Open an issue with the "enhancement" label
2. Describe the feature or improvement
3. Explain why it would be useful
4. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of feature"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```
7. Open a Pull Request against the `main` branch

## 📝 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters (flexible for readability)
- Use type hints where appropriate
- Add docstrings to all classes and public functions

Example:
```python
def download_dataset(url: str, target_dir: Path) -> bool:
    """Download dataset from URL to target directory.
    
    Args:
        url: Dataset URL
        target_dir: Target directory path
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Implementation here
    pass
```

### Documentation

- Keep README.md up to date
- Document all new features
- Update CHANGELOG.md for significant changes
- Add inline comments for complex logic
- Use emojis consistently in console output

### Commit Messages

Follow conventional commit format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for downloading MITRE ATT&CK data
fix: handle timeout errors in CVE API requests
docs: update README with Docker instructions
```

## 🎯 Adding New Datasets

### Adding to Existing Phase

To add a new repository to an existing phase:

1. Edit the appropriate phase downloader (`phase1_ctf_bugbounty.py`, etc.)
2. Add the repository URL to the relevant list
3. Update the counter in the summary section
4. Test the download
5. Update README.md with the new dataset

Example for Phase 1:
```python
ctf_repos = [
    # Existing repos...
    ("https://github.com/username/new-ctf-repo", "new_ctf_repo")
]
```

### Creating a New Phase

To add a completely new phase (e.g., Phase 5):

1. Create `phase5_category_name.py` following the existing pattern:
   ```python
   class Phase5Downloader:
       def __init__(self, base_dir: str = "./cybersecurity_datasets"):
           # Initialize directories and results
           
       def clone_repo(self, url: str, target_dir: Path) -> Tuple[bool, str]:
           # Standard git clone with error handling
           
       def download_something(self) -> int:
           # Download logic
           
       def run(self) -> Dict:
           # Execute all downloads and return results
   ```

2. Update `download_all.py`:
   ```python
   from phase5_category_name import Phase5Downloader
   
   self.phases = {
       # Existing phases...
       5: ("Category Name", Phase5Downloader)
   }
   ```

3. Update `check_progress.py` to include the new phase
4. Add Makefile target: `make phase5`
5. Update README.md with Phase 5 information
6. Update CHANGELOG.md

## 🧪 Testing

### Before Submitting PR

1. Test the download process:
   ```bash
   python download_all.py --phase X  # Test your phase
   ```

2. Verify error handling:
   - Test with invalid URLs
   - Test with network interruptions
   - Test with existing directories

3. Check progress tracking:
   ```bash
   python check_progress.py
   ```

4. Validate JSON output:
   - Check that results files are valid JSON
   - Verify statistics are accurate

### Test Checklist

- [ ] Code runs without errors
- [ ] Downloads complete successfully
- [ ] Error handling works correctly
- [ ] Progress is displayed clearly
- [ ] Results are saved to JSON
- [ ] Documentation is updated
- [ ] No sensitive data is committed

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cybersecurity-datasets-downloader.git
cd cybersecurity-datasets-downloader

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install black flake8 mypy

# Make changes and test
python download_all.py --phase 1

# Format code (optional)
black *.py

# Check code style (optional)
flake8 *.py
```

## 🔍 Code Review Process

Pull requests will be reviewed for:

1. **Functionality** - Does it work as intended?
2. **Code Quality** - Is it readable and maintainable?
3. **Documentation** - Is it properly documented?
4. **Testing** - Has it been tested?
5. **Style** - Does it follow conventions?

### Review Timeline

- Initial review: Within 1 week
- Feedback provided on all PRs
- Multiple iterations may be needed

## 🎨 Design Principles

### Consistency
- All phase downloaders follow the same structure
- Error handling is consistent across modules
- Console output uses consistent emojis and formatting

### Robustness
- Handle network errors gracefully
- Implement proper timeouts
- Validate all inputs
- Resume interrupted downloads when possible

### User Experience
- Clear progress indicators
- Helpful error messages
- Comprehensive documentation
- Easy to use CLI

### Maintainability
- Modular code structure
- Clear separation of concerns
- Comprehensive docstrings
- Type hints where appropriate

## 🚫 What Not to Do

- Don't commit sensitive data (API keys, credentials)
- Don't commit large binary files
- Don't commit `cybersecurity_datasets/` directory
- Don't break existing functionality
- Don't add malicious code or links
- Don't violate licenses of source datasets

## 📚 Resources

- [Python Style Guide (PEP 8)](https://peps.python.org/pep-0008/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)
- [Semantic Versioning](https://semver.org/)

## 🙏 Recognition

Contributors will be:
- Listed in CHANGELOG.md for significant contributions
- Credited in release notes
- Acknowledged in the project

## 📧 Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues and discussions
- Review this document and other documentation

Thank you for contributing to making cybersecurity datasets more accessible! 🛡️
