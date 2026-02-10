#!/usr/bin/env python3
"""
Phase 3: YARA and Sigma Rules Downloader
Downloads YARA and Sigma detection rules for threat detection.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Tuple


class Phase3Downloader:
    """Downloads YARA and Sigma rules."""
    
    def __init__(self, base_dir: str = "./cybersecurity_datasets", update: bool = False):
        """Initialize the Phase 3 downloader.
        
        Args:
            base_dir: Base directory for all datasets
            update: Whether to update existing repositories
        """
        self.base_dir = Path(base_dir)
        self.update = update
        self.phase_dir = self.base_dir / "phase3_yara_sigma"
        self.yara_dir = self.phase_dir / "yara_rules"
        self.sigma_dir = self.phase_dir / "sigma_rules"
        
        # Create directories
        self.yara_dir.mkdir(parents=True, exist_ok=True)
        self.sigma_dir.mkdir(parents=True, exist_ok=True)
        
        self.results = {
            "yara_repos": [],
            "sigma_repos": [],
            "statistics": {},
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
    
    def download_yara_rules(self) -> int:
        """Download YARA rules repositories.
        
        Returns:
            int: Number of successfully cloned repositories
        """
        print("\n🛡️  Downloading YARA Rules...")
        
        yara_repos = [
            ("https://github.com/Yara-Rules/rules", "yara_rules_official"),
            ("https://github.com/Neo23x0/signature-base", "neo23x0_signature_base")
        ]
        
        success_count = 0
        for url, dir_name in yara_repos:
            target_dir = self.yara_dir / dir_name
            success, message = self.clone_repo(url, target_dir)
            
            if success:
                success_count += 1
                self.results["yara_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "success"
                })
            else:
                self.results["yara_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "failed",
                    "error": message
                })
                self.results["errors"].append(f"YARA repo {url}: {message}")
        
        return success_count
    
    def download_sigma_rules(self) -> int:
        """Download Sigma rules repositories.
        
        Returns:
            int: Number of successfully cloned repositories
        """
        print("\n🚨 Downloading Sigma Rules...")
        
        sigma_repos = [
            ("https://github.com/SigmaHQ/sigma", "sigmahq_sigma"),
            ("https://github.com/SigmaHQ/pySigma", "pysigma")  # Modern replacement for deprecated sigmac
        ]
        
        success_count = 0
        for url, dir_name in sigma_repos:
            target_dir = self.sigma_dir / dir_name
            success, message = self.clone_repo(url, target_dir)
            
            if success:
                success_count += 1
                self.results["sigma_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "success"
                })
            else:
                self.results["sigma_repos"].append({
                    "url": url,
                    "directory": dir_name,
                    "status": "failed",
                    "error": message
                })
                self.results["errors"].append(f"Sigma repo {url}: {message}")
        
        return success_count
    
    def count_rules(self) -> Dict[str, int]:
        """Count YARA and Sigma rule files.
        
        Returns:
            Dict: Statistics about rule files
        """
        print("\n📊 Counting Rules...")
        
        stats = {
            "yara_files": 0,
            "sigma_files": 0,
            "total_files": 0
        }
        
        # Count YARA rules (.yar, .yara)
        if self.yara_dir.exists():
            yara_files = list(self.yara_dir.rglob("*.yar")) + list(self.yara_dir.rglob("*.yara"))
            stats["yara_files"] = len(yara_files)
            print(f"  🛡️  YARA rules: {stats['yara_files']}")
        
        # Count Sigma rules (.yml, .yaml)
        if self.sigma_dir.exists():
            sigma_files = list(self.sigma_dir.rglob("*.yml")) + list(self.sigma_dir.rglob("*.yaml"))
            stats["sigma_files"] = len(sigma_files)
            print(f"  🚨 Sigma rules: {stats['sigma_files']}")
        
        stats["total_files"] = stats["yara_files"] + stats["sigma_files"]
        print(f"  📈 Total rules: {stats['total_files']}")
        
        self.results["statistics"] = stats
        
        # Save statistics
        stats_file = self.phase_dir / "rules_statistics.json"
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)
        print(f"  ✅ Statistics saved to {stats_file.name}")
        
        return stats
    
    def run(self) -> Dict:
        """Execute all Phase 3 downloads.
        
        Returns:
            Dict: Results summary
        """
        print("=" * 80)
        print("🛡️  PHASE 3: YARA & Sigma Rules")
        print("=" * 80)
        
        # Download YARA rules
        yara_success = self.download_yara_rules()
        
        # Download Sigma rules
        sigma_success = self.download_sigma_rules()
        
        # Count rules
        stats = self.count_rules()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 PHASE 3 SUMMARY")
        print("=" * 80)
        print(f"  YARA Repositories: {yara_success}/2 successful")
        print(f"  Sigma Repositories: {sigma_success}/2 successful")
        print(f"  Total YARA Rules: {stats['yara_files']}")
        print(f"  Total Sigma Rules: {stats['sigma_files']}")
        print(f"  Total Rules: {stats['total_files']}")
        
        if self.results["errors"]:
            print(f"\n  ⚠️  {len(self.results['errors'])} errors occurred")
        
        print("=" * 80)
        
        # Save results
        results_file = self.phase_dir / "phase3_results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        return self.results


def main():
    """Main entry point for Phase 3 downloader."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download YARA and Sigma rules"
    )
    parser.add_argument(
        "--dir",
        default="./cybersecurity_datasets",
        help="Base directory for datasets (default: ./cybersecurity_datasets)"
    )
    
    args = parser.parse_args()
    
    downloader = Phase3Downloader(args.dir)
    downloader.run()


if __name__ == "__main__":
    main()
