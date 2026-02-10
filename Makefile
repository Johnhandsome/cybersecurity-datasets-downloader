.PHONY: help install setup run phase1 phase2 phase3 phase4 check clean

help:
	@echo "🛡️  Cybersecurity Datasets Downloader - Commands"
	@echo "================================================"
	@echo ""
	@echo "Available targets:"
	@echo "  make help      - Show this help message"
	@echo "  make install   - Install Python dependencies"
	@echo "  make setup     - Run setup script (create venv and install deps)"
	@echo "  make run       - Download all datasets"
	@echo "  make phase1    - Download Phase 1 (CTF & Bug Bounty)"
	@echo "  make phase2    - Download Phase 2 (Exploits & Tools)"
	@echo "  make phase3    - Download Phase 3 (YARA & Sigma)"
	@echo "  make phase4    - Download Phase 4 (CVE Database)"
	@echo "  make check     - Check download progress"
	@echo "  make clean     - Remove downloaded datasets (prompts for confirmation)"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

setup:
	@echo "🔧 Running setup script..."
	bash setup.sh

run:
	@echo "🚀 Starting all downloads..."
	python download_all.py

phase1:
	@echo "🚀 Starting Phase 1: CTF & Bug Bounty..."
	python download_all.py --phase 1

phase2:
	@echo "🚀 Starting Phase 2: Exploits & Tools..."
	python download_all.py --phase 2

phase3:
	@echo "🚀 Starting Phase 3: YARA & Sigma..."
	python download_all.py --phase 3

phase4:
	@echo "🚀 Starting Phase 4: CVE Database..."
	python download_all.py --phase 4

check:
	@echo "📊 Checking progress..."
	python check_progress.py

clean:
	@echo "⚠️  This will delete the cybersecurity_datasets/ directory"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "🗑️  Removing cybersecurity_datasets/..."; \
		rm -rf cybersecurity_datasets/; \
		echo "✅ Cleaned"; \
	else \
		echo "❌ Cancelled"; \
	fi
