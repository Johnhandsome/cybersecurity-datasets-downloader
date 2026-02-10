#!/usr/bin/env python3
"""
Check Progress of Dataset Downloads
Displays statistics and progress for each phase.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0 # type: ignore
    return f"{size_bytes:.2f} PB"


def count_files_and_size(directory: Path) -> Tuple[int, int]:
    """Count files and calculate total size in a directory.
    
    Args:
        directory: Directory to analyze
        
    Returns:
        Tuple of (file_count, total_size_bytes)
    """
    file_count = 0
    total_size = 0
    
    if not directory.exists():
        return 0, 0
    
    try:
        for item in directory.rglob("*"):
            if item.is_file():
                file_count += 1
                total_size += item.stat().st_size
    except Exception:
        pass
    
    return file_count, total_size


def check_progress(base_dir: str = "./cybersecurity_datasets"):
    """Check progress of dataset downloads.
    
    Args:
        base_dir: Base directory for datasets
    """
    base_path = Path(base_dir)
    
    print("=" * 80)
    print("🛡️  CYBERSECURITY DATASETS PROGRESS")
    print("=" * 80)
    print(f"📁 Base directory: {base_path.absolute()}")
    print()
    
    if not base_path.exists():
        print("❌ Dataset directory does not exist!")
        print(f"   Run 'python download_all.py' to start downloading datasets")
        return
    
    # Define phases
    phases = [
        ("phase1_ctf_bugbounty", "CTF & Bug Bounty Reports"),
        ("phase2_exploits_tools", "Exploits & Security Tools"),
        ("phase3_yara_sigma", "YARA & Sigma Rules"),
        ("phase4_cve_database", "CVE Database"),
        ("phase5_advanced_threats", "Advanced Threats & Black Hat Tactics")
    ]
    
    # Check each phase
    print("📊 Phase Status:")
    print("-" * 80)
    
    total_files = 0
    total_size = 0
    
    for phase_dir, phase_name in phases:
        phase_path = base_path / phase_dir
        exists = phase_path.exists()
        
        if exists:
            file_count, size_bytes = count_files_and_size(phase_path)
            total_files += file_count
            total_size += size_bytes
            
            status = "✅"
            info = f"{file_count} files, {format_size(size_bytes)}"
        else:
            status = "⏳"
            info = "Not started"
        
        print(f"  {status} {phase_name:30s} {info}")
    
    print("-" * 80)
    print(f"  📈 Total: {total_files} files, {format_size(total_size)}")
    print()
    
    # Check for download summary
    summary_file = base_path / "download_summary.json"
    if summary_file.exists():
        try:
            with open(summary_file, "r") as f:
                summary = json.load(f)
            
            print("📄 Last Download Summary:")
            print("-" * 80)
            
            download_date = summary.get("download_date", "Unknown")
            if download_date != "Unknown":
                try:
                    dt = datetime.fromisoformat(download_date)
                    download_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
            
            print(f"  🕐 Download Date: {download_date}")
            
            elapsed = summary.get("total_elapsed_seconds", 0)
            if elapsed:
                print(f"  ⏱️  Total Time: {elapsed / 60:.1f} minutes")
            
            disk_usage = summary.get("disk_usage_gb", 0)
            if disk_usage:
                print(f"  💾 Disk Usage: {disk_usage:.2f} GB")
            
            # Phase results
            phases_data = summary.get("phases", [])
            successful = sum(1 for p in phases_data if p.get("status") == "success")
            total = len(phases_data)
            
            print(f"  ✅ Phases Complete: {successful}/{total}")
            
            print()
            
        except Exception as e:
            print(f"  ⚠️  Could not read download summary: {e}")
            print()
    
    # Check for individual phase results
    print("🔍 Detailed Phase Information:")
    print("-" * 80)
    
    for phase_dir, phase_name in phases:
        phase_path = base_path / phase_dir
        if not phase_path.exists():
            continue
        
        # Look for phase results file
        results_file = phase_path / f"{phase_dir.split('_')[0]}_results.json"
        if results_file.exists():
            try:
                with open(results_file, "r") as f:
                    results = json.load(f)
                
                print(f"\n  📦 {phase_name}:")
                
                # Phase-specific information
                if "phase1" in phase_dir:
                    ctf_repos = len(results.get("ctf_repos", []))
                    bb_repos = len(results.get("bugbounty_repos", []))
                    print(f"      CTF Repositories: {ctf_repos}")
                    print(f"      Bug Bounty Repositories: {bb_repos}")
                
                elif "phase2" in phase_dir:
                    tools = len(results.get("security_tools", []))
                    scripts = results.get("extracted_scripts", 0)
                    print(f"      Security Tools: {tools}")
                    print(f"      Extracted Scripts: {scripts}")
                
                elif "phase3" in phase_dir:
                    stats = results.get("statistics", {})
                    yara = stats.get("yara_files", 0)
                    sigma = stats.get("sigma_files", 0)
                    print(f"      YARA Rules: {yara}")
                    print(f"      Sigma Rules: {sigma}")
                
                elif "phase4" in phase_dir:
                    total_cves = results.get("total_cves", 0)
                    files = len(results.get("cve_files", []))
                    print(f"      CVE Files: {files}")
                    print(f"      Total CVEs: {total_cves}")
                
                elif "phase5" in phase_dir:
                    # Phase 5 statistics
                    malware = len(results.get("malware_repos", []))
                    phishing = len(results.get("phishing_repos", []))
                    mobile = len(results.get("mobile_repos", []))
                    cloud = len(results.get("cloud_repos", []))
                    binary = len(results.get("binary_repos", []))
                    apt = len(results.get("apt_repos", []))
                    hf = len(results.get("hf_datasets", []))
                    
                    total = malware + phishing + mobile + cloud + binary + apt + hf
                    print(f"      Total Repositories: {total}")
                    print(f"        Malware Analysis: {malware}")
                    print(f"        Phishing/Social Eng: {phishing}")
                    print(f"        Mobile Security: {mobile}")
                    print(f"        Cloud Security: {cloud}")
                    print(f"        Binary Exploitation: {binary}")
                    print(f"        APT Intelligence: {apt}")
                    print(f"        HuggingFace Datasets: {hf}")
                
                # Show errors if any
                errors = results.get("errors", [])
                if errors:
                    print(f"      ⚠️  Errors: {len(errors)}")
                
            except Exception:
                pass
    
    print("\n" + "=" * 80)


def main():
    """Main entry point for progress checker."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Check progress of cybersecurity dataset downloads"
    )
    parser.add_argument(
        "--dir",
        default="./cybersecurity_datasets",
        help="Base directory for datasets (default: ./cybersecurity_datasets)"
    )
    
    args = parser.parse_args()
    check_progress(args.dir)


if __name__ == "__main__":
    main()
