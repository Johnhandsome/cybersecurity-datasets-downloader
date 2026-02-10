#!/usr/bin/env python3
"""
Phase 1: CTF Writeups and Bug Bounty Reports Downloader
Downloads CTF challenges writeups and bug bounty reports for cybersecurity training.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple


class Phase1Downloader:
    """Downloads CTF writeups and bug bounty reports."""
    
    def __init__(self, base_dir: str = "./cybersecurity_datasets", update: bool = False):
        """Initialize the Phase 1 downloader.
        
        Args:
            base_dir: Base directory for all datasets
            update: Whether to update existing repositories
        """
        self.base_dir = Path(base_dir)
        self.update = update
        self.phase_dir = self.base_dir / "phase1_ctf_bugbounty"
        self.ctf_dir = self.phase_dir / "ctf_writeups"
        self.bugbounty_dir = self.phase_dir / "bugbounty_repos"
        self.hackerone_dir = self.phase_dir / "hackerone_reports"
        
        # Create directories
        self.ctf_dir.mkdir(parents=True, exist_ok=True)
        self.bugbounty_dir.mkdir(parents=True, exist_ok=True)
        self.hackerone_dir.mkdir(parents=True, exist_ok=True)
        
        self.results = {
            "ctf_repos": [],
            "bugbounty_repos": [],
            "hackerone_dataset": None,
            "errors": []
        }
    
    def check_already_downloaded(self, target_dir: Path) -> bool:
        """Check if repository already exists and is valid.
        
        Args:
            target_dir: Directory to check
            
        Returns:
            bool: True if already exists and valid
        """
        if not target_dir.exists():
            return False
        
        # Check if it's a valid git repo or has content
        if (target_dir / ".git").exists():
            return True
        
        # Check if directory has any content
        try:
            if len(list(target_dir.iterdir())) > 0:
                return True
        except Exception:
            pass
        
        return False
    
    def clone_repo(self, url: str, target_dir: Path) -> Tuple[bool, str]:
        """Clone a git repository with error handling.
        
        Args:
            url: Git repository URL
            target_dir: Target directory for cloning
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Check if already downloaded
            if self.check_already_downloaded(target_dir):
                if self.update and (target_dir / ".git").exists():
                    print(f"  🔄 Updating {target_dir.name}...")
                    try:
                        result = subprocess.run(
                            ["git", "-C", str(target_dir), "pull"],
                            capture_output=True,
                            text=True,
                            timeout=300
                        )
                        if result.returncode == 0:
                            print(f"  ✅ Updated {target_dir.name}")
                            return True, f"Updated: {target_dir.name}"
                        else:
                            print(f"  ⚠️  Update failed, keeping existing: {target_dir.name}")
                            return True, f"Already exists: {target_dir.name}"
                    except Exception as e:
                        print(f"  ⚠️  Update failed: {e}, keeping existing")
                        return True, f"Already exists: {target_dir.name}"
                else:
                    print(f"  ⏭️  Already exists: {target_dir.name}")
                    return True, f"Already exists: {target_dir.name}"
            
            print(f"  📦 Cloning {url}...")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", url, str(target_dir)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"  ✅ Successfully cloned to {target_dir.name}")
                return True, f"Successfully cloned: {target_dir.name}"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                print(f"  ❌ Failed to clone: {error_msg}")
                return False, f"Failed: {error_msg}"
                
        except subprocess.TimeoutExpired:
            error_msg = "Clone operation timed out after 5 minutes"
            print(f"  ❌ {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Error cloning repository: {str(e)}"
            print(f"  ❌ {error_msg}")
            return False, error_msg
    
    def download_hackerone_dataset(self) -> bool:
        """Download HackerOne dataset from Hugging Face or provide instructions.
        
        Returns:
            bool: Success status
        """
        print("\n🎯 Downloading HackerOne Dataset...")
        
        try:
            # Try to download from Hugging Face
            try:
                from huggingface_hub import snapshot_download
                
                print("  📦 Downloading from Hugging Face...")
                snapshot_download(
                    repo_id="Hacker0x01/hackerone_disclosed_reports",
                    repo_type="dataset",
                    local_dir=str(self.hackerone_dir),
                    local_dir_use_symlinks=False
                )
                print("  ✅ HackerOne dataset downloaded")
                self.results["hackerone_dataset"] = "Downloaded from Hugging Face"
                return True
                
            except ImportError:
                print("  ⚠️  huggingface_hub not installed")
                print("  💡 To download HackerOne dataset, install: pip install huggingface-hub")
                print("  💡 Then run: huggingface-cli download Hacker0x01/hackerone_disclosed_reports")
                self.results["hackerone_dataset"] = "Manual download required"
                return False
            except Exception as e:
                print(f"  ⚠️  Could not download from Hugging Face: {str(e)}")
                print("  💡 You may need to manually download HackerOne reports")
                self.results["hackerone_dataset"] = f"Error: {str(e)}"
                return False
                
        except Exception as e:
            error_msg = f"Error with HackerOne dataset: {str(e)}"
            print(f"  ❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def download_ctf_repos(self) -> int:
        """Download CTF writeup repositories.
        
        Returns:
            int: Number of successfully cloned repositories
        """
        print("\n🚩 Downloading CTF Writeup Repositories...")
        
        ctf_repos = [
            ("https://github.com/ShundaZhang/htb", "htb_shundazhang"),
            ("https://github.com/hackplayers/hackthebox-writeups", "htb_hackplayers"),
            ("https://github.com/sohailburki1/HackTheBox-Writeups", "htb_sohailburki1"),
            ("https://github.com/jon-brandy/hackthebox", "htb_jonbrandy"),
            ("https://github.com/uppusaikiran/awesome-ctf-cheatsheet", "awesome_ctf_cheatsheet")
        ]
        
        success_count = 0
        for url, dir_name in ctf_repos:
            target_dir = self.ctf_dir / dir_name
            success, message = self.clone_repo(url, target_dir)
            
            if success:
                success_count += 1
                self.results["ctf_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "success"
                })
            else:
                self.results["ctf_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "failed",
                    "error": message
                })
                self.results["errors"].append(f"CTF repo {url}: {message}")
        
        return success_count
    
    def download_bugbounty_repos(self) -> int:
        """Download bug bounty report repositories.
        
        Returns:
            int: Number of successfully cloned repositories
        """
        print("\n🐛 Downloading Bug Bounty Repositories...")
        
        bugbounty_repos = [
            ("https://github.com/reddelexc/hackerone-reports", "hackerone_reddelexc"),
            ("https://github.com/buildergk/hackerone-bug-bounty-reports", "hackerone_buildergk"),
            ("https://github.com/phlmox/public-reports", "public_reports_phlmox")
        ]
        
        success_count = 0
        for url, dir_name in bugbounty_repos:
            target_dir = self.bugbounty_dir / dir_name
            success, message = self.clone_repo(url, target_dir)
            
            if success:
                success_count += 1
                self.results["bugbounty_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "success"
                })
            else:
                self.results["bugbounty_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "failed",
                    "error": message
                })
                self.results["errors"].append(f"Bug bounty repo {url}: {message}")
        
        return success_count
    
    def run(self) -> Dict:
        """Execute all Phase 1 downloads.
        
        Returns:
            Dict: Results summary
        """
        print("=" * 80)
        print("🛡️  PHASE 1: CTF Writeups & Bug Bounty Reports")
        print("=" * 80)
        
        # Download CTF repos
        ctf_success = self.download_ctf_repos()
        
        # Download bug bounty repos
        bugbounty_success = self.download_bugbounty_repos()
        
        # Download HackerOne dataset
        hackerone_success = self.download_hackerone_dataset()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 PHASE 1 SUMMARY")
        print("=" * 80)
        print(f"  CTF Repositories: {ctf_success}/5 successful")
        print(f"  Bug Bounty Repositories: {bugbounty_success}/3 successful")
        print(f"  HackerOne Dataset: {'✅' if hackerone_success else '⚠️'}")
        
        if self.results["errors"]:
            print(f"\n  ⚠️  {len(self.results['errors'])} errors occurred")
        
        print("=" * 80)
        
        # Save results
        results_file = self.phase_dir / "phase1_results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        return self.results


def main():
    """Main entry point for Phase 1 downloader."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download CTF writeups and bug bounty reports"
    )
    parser.add_argument(
        "--dir",
        default="./cybersecurity_datasets",
        help="Base directory for datasets (default: ./cybersecurity_datasets)"
    )
    
    args = parser.parse_args()
    
    downloader = Phase1Downloader(args.dir)
    downloader.run()


if __name__ == "__main__":
    main()
