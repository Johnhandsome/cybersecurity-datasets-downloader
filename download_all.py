#!/usr/bin/env python3
"""
Master Downloader for Cybersecurity Datasets
Orchestrates all 5 phases of dataset downloads.
"""

import os
import sys
import time
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import phase downloaders
from phase1_ctf_bugbounty import Phase1Downloader
from phase2_exploits_tools import Phase2Downloader
from phase3_yara_sigma import Phase3Downloader
from phase4_cve_database import Phase4Downloader
from phase5_advanced_threats import Phase5Downloader


class MasterDownloader:
    """Master orchestrator for all dataset downloads."""
    
    def __init__(self, base_dir: str = "./cybersecurity_datasets", update: bool = False, skip_malware: bool = False):
        """Initialize the master downloader.
        
        Args:
            base_dir: Base directory for all datasets
            update: Whether to update existing repositories
            skip_malware: Skip downloading live malware samples
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.update = update
        self.skip_malware = skip_malware
        
        self.phases = {
            1: ("CTF & Bug Bounty", Phase1Downloader),
            2: ("Exploits & Tools", Phase2Downloader),
            3: ("YARA & Sigma Rules", Phase3Downloader),
            4: ("CVE Database", Phase4Downloader),
            5: ("Advanced Threats & Black Hat Tactics", Phase5Downloader)
        }
        
        self.results = {}
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed.
        
        Returns:
            bool: True if all dependencies are available
        """
        print("🔍 Checking Dependencies...")
        
        dependencies_ok = True
        
        # Check git
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("  ✅ git is installed")
            else:
                print("  ❌ git is not installed")
                dependencies_ok = False
        except FileNotFoundError:
            print("  ❌ git is not installed")
            dependencies_ok = False
        
        # Check Python 3
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 8:
            print(f"  ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} is installed")
        else:
            print(f"  ❌ Python 3.8+ required (found {python_version.major}.{python_version.minor})")
            dependencies_ok = False
        
        # Check requests
        try:
            import requests
            print("  ✅ requests library is installed")
        except ImportError:
            print("  ❌ requests library is not installed")
            print("     Run: pip install requests")
            dependencies_ok = False
        
        # Check tqdm (optional)
        try:
            import tqdm
            print("  ✅ tqdm library is installed")
        except ImportError:
            print("  ⚠️  tqdm library is not installed (optional)")
        
        # Check huggingface-hub (optional)
        try:
            import huggingface_hub
            print("  ✅ huggingface-hub is installed")
        except ImportError:
            print("  ⚠️  huggingface-hub is not installed (optional, for HF datasets)")
        
        print()
        return dependencies_ok
    
    def run_phase(self, phase_num: int, phase_name: str, downloader_class) -> Dict:
        """Execute a single phase with timing.
        
        Args:
            phase_num: Phase number (1-5)
            phase_name: Human-readable phase name
            downloader_class: Downloader class to instantiate
            
        Returns:
            Dict: Phase results with timing
        """
        print(f"\n{'=' * 80}")
        print(f"🚀 Starting Phase {phase_num}: {phase_name}")
        print(f"{'=' * 80}\n")
        
        start_time = time.time()
        
        try:
            # Phase 5 needs skip_malware parameter
            if phase_num == 5:
                downloader = downloader_class(str(self.base_dir), update=self.update, skip_malware=self.skip_malware)
            else:
                downloader = downloader_class(str(self.base_dir), update=self.update)
            results = downloader.run()
            
            elapsed = time.time() - start_time
            
            return {
                "phase": phase_num,
                "name": phase_name,
                "status": "success",
                "elapsed_seconds": round(elapsed, 2),
                "results": results
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = f"Phase {phase_num} failed: {str(e)}"
            print(f"\n❌ {error_msg}\n")
            
            return {
                "phase": phase_num,
                "name": phase_name,
                "status": "failed",
                "elapsed_seconds": round(elapsed, 2),
                "error": error_msg
            }
    
    def run_all(self) -> Dict:
        """Execute all 5 phases sequentially.
        
        Returns:
            Dict: All results with timing
        """
        print("=" * 80)
        print("🛡️  CYBERSECURITY DATASETS DOWNLOADER")
        print("=" * 80)
        print(f"📁 Base directory: {self.base_dir.absolute()}")
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed. Please install missing dependencies.")
            return {"status": "failed", "error": "Missing dependencies"}
        
        start_time = time.time()
        phase_results = []
        
        # Run all phases
        for phase_num in sorted(self.phases.keys()):
            phase_name, downloader_class = self.phases[phase_num]
            result = self.run_phase(phase_num, phase_name, downloader_class)
            phase_results.append(result)
        
        total_elapsed = time.time() - start_time
        
        # Compile results
        results = {
            "download_date": datetime.now().isoformat(),
            "total_elapsed_seconds": round(total_elapsed, 2),
            "phases": phase_results,
            "base_directory": str(self.base_dir.absolute())
        }
        
        self.results = results
        
        return results
    
    def calculate_disk_usage(self) -> float:
        """Calculate total disk usage of downloaded datasets.
        
        Returns:
            float: Total size in GB
        """
        try:
            total_size = 0
            for item in self.base_dir.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
            
            return round(total_size / (1024 ** 3), 2)  # Convert to GB
        except Exception as e:
            print(f"  ⚠️  Could not calculate disk usage: {e}")
            return 0.0
    
    def print_final_summary(self, results: Dict, elapsed: float):
        """Display final summary of all downloads.
        
        Args:
            results: Results dictionary
            elapsed: Total elapsed time in seconds
        """
        print("\n" + "=" * 80)
        print("🎉 FINAL SUMMARY")
        print("=" * 80)
        
        successful_phases = sum(1 for p in results["phases"] if p["status"] == "success")
        total_phases = len(results["phases"])
        
        print(f"  Phases Completed: {successful_phases}/{total_phases}")
        print(f"  Total Time: {elapsed / 60:.1f} minutes")
        
        # Calculate disk usage
        disk_usage = self.calculate_disk_usage()
        if disk_usage > 0:
            print(f"  Total Disk Usage: {disk_usage:.2f} GB")
        
        print("\n  Phase Details:")
        for phase in results["phases"]:
            status_icon = "✅" if phase["status"] == "success" else "❌"
            elapsed_min = phase["elapsed_seconds"] / 60
            print(f"    {status_icon} Phase {phase['phase']}: {phase['name']} ({elapsed_min:.1f} min)")
        
        print(f"\n  📁 Dataset location: {results['base_directory']}")
        print("=" * 80)
    
    def save_results(self, results: Dict, elapsed: float):
        """Save download results to JSON file.
        
        Args:
            results: Results dictionary
            elapsed: Total elapsed time
        """
        output_file = self.base_dir / "download_summary.json"
        
        # Add disk usage to results
        results["disk_usage_gb"] = self.calculate_disk_usage()
        
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Summary saved to: {output_file}")


def main():
    """Main entry point for the master downloader."""
    parser = argparse.ArgumentParser(
        description="Download cybersecurity datasets for AI/ML training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download_all.py                    # Download all phases
  python download_all.py --phase 1          # Download only Phase 1
  python download_all.py --phase 5          # Download Phase 5 (with safety prompts)
  python download_all.py --skip-malware     # Download all, skip live malware
  python download_all.py --dir /data        # Use custom directory
  python download_all.py --phase 5 --skip-malware  # Phase 5 without malware
        """
    )
    
    parser.add_argument(
        "--dir",
        default="./cybersecurity_datasets",
        help="Base directory for datasets (default: ./cybersecurity_datasets)"
    )
    
    parser.add_argument(
        "--phase",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Run only a specific phase (1-5)"
    )
    
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing repositories (git pull)"
    )
    
    parser.add_argument(
        "--skip-malware",
        action="store_true",
        help="Skip downloading live malware samples in Phase 5 (safer option)"
    )
    
    args = parser.parse_args()
    
    # Create master downloader
    master = MasterDownloader(args.dir, update=args.update, skip_malware=args.skip_malware)
    
    if args.update:
        print("🔄 Update mode enabled - will update existing repositories\n")
    
    if args.skip_malware:
        print("⏭️  Skip malware mode enabled - live malware samples will be skipped\n")
    
    if args.phase:
        # Run single phase
        phase_name, downloader_class = master.phases[args.phase]
        start_time = time.time()
        result = master.run_phase(args.phase, phase_name, downloader_class)
        elapsed = time.time() - start_time
        
        results = {
            "download_date": datetime.now().isoformat(),
            "total_elapsed_seconds": round(elapsed, 2),
            "phases": [result],
            "base_directory": str(master.base_dir.absolute())
        }
        
        master.print_final_summary(results, elapsed)
        master.save_results(results, elapsed)
        
    else:
        # Run all phases
        start_time = time.time()
        results = master.run_all()
        elapsed = time.time() - start_time
        
        master.print_final_summary(results, elapsed)
        master.save_results(results, elapsed)


if __name__ == "__main__":
    main()
