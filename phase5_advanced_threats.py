#!/usr/bin/env python3
"""
Phase 5: Advanced Threats & Black Hat Tactics Downloader
Downloads malware samples, phishing tools, mobile security, cryptojacking, 
cloud security, binary exploitation, APT intelligence, and more.

⚠️  WARNING: This phase includes LIVE MALWARE samples. 
    Use ONLY in isolated environments (VMs with no network access).
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple


class Phase5Downloader:
    """Downloads advanced threat intelligence and black hat tactics datasets."""
    
    def __init__(self, base_dir: str = "./cybersecurity_datasets", update: bool = False, skip_malware: bool = False):
        """Initialize the Phase 5 downloader.
        
        Args:
            base_dir: Base directory for all datasets
            update: Whether to update existing repositories
            skip_malware: Skip downloading live malware samples
        """
        self.base_dir = Path(base_dir)
        self.update = update
        self.skip_malware = skip_malware
        self.phase_dir = self.base_dir / "phase5_advanced_threats"
        
        # Create subdirectories
        self.malware_dir = self.phase_dir / "malware_analysis"
        self.phishing_dir = self.phase_dir / "phishing_social_eng"
        self.mobile_dir = self.phase_dir / "mobile_security"
        self.crypto_dir = self.phase_dir / "crypto_attacks"
        self.cloud_dir = self.phase_dir / "cloud_security"
        self.binary_dir = self.phase_dir / "binary_exploitation"
        self.apt_dir = self.phase_dir / "apt_intelligence"
        self.hf_dir = self.phase_dir / "huggingface_datasets"
        
        # Create all directories
        for directory in [self.malware_dir, self.phishing_dir, self.mobile_dir, 
                          self.crypto_dir, self.cloud_dir, self.binary_dir, 
                          self.apt_dir, self.hf_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.results = {
            "malware_repos": [],
            "phishing_repos": [],
            "mobile_repos": [],
            "crypto_repos": [],
            "cloud_repos": [],
            "binary_repos": [],
            "apt_repos": [],
            "hf_datasets": [],
            "errors": []
        }
        
        # Define repositories
        self.malware_repos = {
            "malware_analysis": "https://github.com/rshipp/awesome-malware-analysis",
            "malware_traffic_analysis": "https://github.com/pan-unit42/iocs",
            "malware_bazaar": "https://github.com/abuse-ch/MalwareBazaar",
            "ransomware_overview": "https://github.com/arieljaufman/Ransomware-Guide",
            "ransomware_simulator": "https://github.com/NextronSystems/ransomware-simulator",
        }
        
        # Live malware samples - only if not skipping
        self.malware_live_repos = {
            "theZoo": "https://github.com/ytisf/theZoo",
            "vx_underground": "https://github.com/vxunderground/MalwareSourceCode",
        }
        
        self.phishing_repos = {
            "phishing_database": "https://github.com/mitchellkrogza/Phishing.Database",
            "social_engineering_toolkit": "https://github.com/trustedsec/social-engineer-toolkit",
            "gophish": "https://github.com/gophish/gophish",
            "evilginx2": "https://github.com/kgretzky/evilginx2",
            "modlishka": "https://github.com/drk1wi/Modlishka",
        }
        
        self.mobile_security_repos = {
            "mobsf": "https://github.com/MobSF/Mobile-Security-Framework-MobSF",
            "androguard": "https://github.com/androguard/androguard",
            "android_vulnerabilities": "https://github.com/SecWiki/android-security-awesome",
            "apkleaks": "https://github.com/dwisiswant0/apkleaks",
            "frida": "https://github.com/frida/frida",
            "ios_security": "https://github.com/Siguza/ios-resources",
            "objection": "https://github.com/sensepost/objection",
        }
        
        self.crypto_attack_repos = {
            "cryptojacking_samples": "https://github.com/r00t-3xp10it/cryptominer",
            "blockchain_attacks": "https://github.com/Mechanism-Labs/MetaMask",
            "smart_contract_exploits": "https://github.com/SunWeb3Sec/DeFiHackLabs",
            "not_so_smart_contracts": "https://github.com/crytic/not-so-smart-contracts",
        }
        
        self.cloud_security_repos = {
            # AWS
            "pacu": "https://github.com/RhinoSecurityLabs/pacu",
            "cloudgoat": "https://github.com/RhinoSecurityLabs/cloudgoat",
            "prowler": "https://github.com/prowler-cloud/prowler",
            # Azure
            "azure_redteam": "https://github.com/RhinoSecurityLabs/AzureGoat",
            "microburst": "https://github.com/NetSPI/MicroBurst",
            # GCP
            "gcpbucketbrute": "https://github.com/RhinoSecurityLabs/GCPBucketBrute",
            # Multi-cloud
            "cloudsploit": "https://github.com/aquasecurity/cloudsploit",
            "scoutsuite": "https://github.com/nccgroup/ScoutSuite",
        }
        
        self.binary_exploit_repos = {
            "rop_emporium": "https://github.com/ropemporium/ropemporium.github.io",
            "pwn_college": "https://github.com/pwncollege/pwncollege.github.io",
            "how2heap": "https://github.com/shellphish/how2heap",
            "ret2libc": "https://github.com/Naetw/CTF-pwn-tips",
            "reversing_challenges": "https://github.com/rpisec/MBE",
            "crackmes": "https://github.com/RPISEC/Malware",
            "flare_on": "https://github.com/fareedfauzi/Flare-On-Challenges",
        }
        
        self.apt_repos = {
            "apt_notes": "https://github.com/aptnotes/data",
            "mitre_attack": "https://github.com/mitre-attack/attack-stix-data",
            "threat_intelligence": "https://github.com/hslatman/awesome-threat-intelligence",
            "cyber_threat_intel": "https://github.com/curated-intel/Ukraine-Cyber-Operations",
        }
        
        self.huggingface_datasets = {
            "malware_api_calls": "santhisenan/malware_api_call_sequences",
            "phishing_emails": "ealvaradob/phishing-dataset",
            "android_malware": "EMCS-JKUAT/android-malware",
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
            
            # Clone the repository
            print(f"  📥 Cloning {target_dir.name}...")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", url, str(target_dir)],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                print(f"  ✅ Cloned {target_dir.name}")
                return True, f"Cloned: {target_dir.name}"
            else:
                error_msg = result.stderr.strip()
                print(f"  ❌ Failed to clone {target_dir.name}: {error_msg}")
                return False, f"Failed: {error_msg}"
        
        except subprocess.TimeoutExpired:
            print(f"  ❌ Timeout cloning {target_dir.name}")
            return False, "Timeout"
        except Exception as e:
            print(f"  ❌ Error cloning {target_dir.name}: {e}")
            return False, str(e)
    
    def show_safety_warning(self) -> bool:
        """Show comprehensive safety warning for malware downloads.
        
        Returns:
            bool: True if user accepts risks
        """
        print("\n" + "⚠️ " * 30)
        print("=" * 80)
        print("                  ⚠️  DANGER: LIVE MALWARE SAMPLES ⚠️")
        print("=" * 80)
        print("\n⚠️  Phase 5 includes repositories with LIVE MALWARE SAMPLES")
        print("\nYou MUST:")
        print("  ✓ Use an isolated VM (VMware/VirtualBox/QEMU)")
        print("  ✓ Disable network or use host-only networking")
        print("  ✓ Take VM snapshots before proceeding")
        print("  ✓ Understand malware analysis fundamentals")
        print("  ✓ Have antivirus disabled in VM (intentionally)")
        print("\nYou MUST NOT:")
        print("  ✗ Run on your main system")
        print("  ✗ Run with network access")
        print("  ✗ Extract archives without understanding risks")
        print("  ✗ Share samples irresponsibly")
        print("  ✗ Use for illegal purposes")
        print("\n📚 IMPORTANT NOTES:")
        print("  • Malware archives are password-protected (password: 'infected')")
        print("  • Legal responsibility is yours - research local laws")
        print("  • See docs/MALWARE_SAFETY.md for detailed safety guide")
        print("\n" + "⚠️ " * 30)
        print()
        
        try:
            response = input("Type 'I UNDERSTAND THE RISKS' to continue (or 'skip' to skip malware): ")
            return response.strip() == "I UNDERSTAND THE RISKS"
        except (EOFError, KeyboardInterrupt):
            print("\n\n⚠️  User cancelled - skipping malware downloads")
            return False
    
    def download_malware_analysis(self) -> Dict[str, bool]:
        """Download malware analysis repositories (non-live samples).
        
        Returns:
            Dict mapping repo names to success status
        """
        print("\n" + "=" * 80)
        print("🦠 Downloading Malware Analysis Repositories")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.malware_repos.items():
            target_dir = self.malware_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["malware_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message
            })
            
            if not success:
                self.results["errors"].append(f"Malware repo {repo_name}: {message}")
        
        return results
    
    def download_malware_live_samples(self) -> Dict[str, bool]:
        """Download LIVE malware sample repositories (WITH SAFETY CHECK).
        
        Returns:
            Dict mapping repo names to success status
        """
        if self.skip_malware:
            print("\n⏭️  Skipping live malware samples (--skip-malware flag set)")
            return {}
        
        # Show safety warning
        if not self.show_safety_warning():
            print("\n⏭️  Skipping live malware samples (safety check not confirmed)")
            return {}
        
        print("\n" + "=" * 80)
        print("☠️  Downloading LIVE Malware Samples (DANGER ZONE)")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.malware_live_repos.items():
            target_dir = self.malware_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["malware_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message,
                "live_malware": True
            })
            
            if not success:
                self.results["errors"].append(f"Live malware repo {repo_name}: {message}")
        
        return results
    
    def download_phishing_tools(self) -> Dict[str, bool]:
        """Download phishing and social engineering tools.
        
        Returns:
            Dict mapping repo names to success status
        """
        print("\n" + "=" * 80)
        print("🎣 Downloading Phishing & Social Engineering Tools")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.phishing_repos.items():
            target_dir = self.phishing_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["phishing_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message
            })
            
            if not success:
                self.results["errors"].append(f"Phishing repo {repo_name}: {message}")
        
        return results
    
    def download_mobile_security(self) -> Dict[str, bool]:
        """Download mobile security (Android/iOS) repositories.
        
        Returns:
            Dict mapping repo names to success status
        """
        print("\n" + "=" * 80)
        print("📱 Downloading Mobile Security Tools")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.mobile_security_repos.items():
            target_dir = self.mobile_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["mobile_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message
            })
            
            if not success:
                self.results["errors"].append(f"Mobile security repo {repo_name}: {message}")
        
        return results
    
    def download_crypto_attacks(self) -> Dict[str, bool]:
        """Download cryptojacking and crypto attack repositories.
        
        Returns:
            Dict mapping repo names to success status
        """
        print("\n" + "=" * 80)
        print("₿ Downloading Crypto Attack Tools")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.crypto_attack_repos.items():
            target_dir = self.crypto_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["crypto_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message
            })
            
            if not success:
                self.results["errors"].append(f"Crypto attack repo {repo_name}: {message}")
        
        return results
    
    def download_cloud_security(self) -> Dict[str, bool]:
        """Download cloud security (AWS/Azure/GCP) repositories.
        
        Returns:
            Dict mapping repo names to success status
        """
        print("\n" + "=" * 80)
        print("☁️  Downloading Cloud Security Tools")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.cloud_security_repos.items():
            target_dir = self.cloud_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["cloud_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message
            })
            
            if not success:
                self.results["errors"].append(f"Cloud security repo {repo_name}: {message}")
        
        return results
    
    def download_binary_exploitation(self) -> Dict[str, bool]:
        """Download binary exploitation and reverse engineering repositories.
        
        Returns:
            Dict mapping repo names to success status
        """
        print("\n" + "=" * 80)
        print("💾 Downloading Binary Exploitation & Reverse Engineering Tools")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.binary_exploit_repos.items():
            target_dir = self.binary_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["binary_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message
            })
            
            if not success:
                self.results["errors"].append(f"Binary exploitation repo {repo_name}: {message}")
        
        return results
    
    def download_apt_intelligence(self) -> Dict[str, bool]:
        """Download APT reports and threat intelligence repositories.
        
        Returns:
            Dict mapping repo names to success status
        """
        print("\n" + "=" * 80)
        print("🎯 Downloading APT & Threat Intelligence")
        print("=" * 80)
        
        results = {}
        
        for repo_name, repo_url in self.apt_repos.items():
            target_dir = self.apt_dir / repo_name
            success, message = self.clone_repo(repo_url, target_dir)
            results[repo_name] = success
            
            self.results["apt_repos"].append({
                "name": repo_name,
                "url": repo_url,
                "success": success,
                "message": message
            })
            
            if not success:
                self.results["errors"].append(f"APT intelligence repo {repo_name}: {message}")
        
        return results
    
    def download_hf_datasets(self) -> Dict[str, bool]:
        """Download Hugging Face datasets for malware, phishing, etc.
        
        Returns:
            Dict mapping dataset names to success status
        """
        print("\n" + "=" * 80)
        print("🤗 Downloading Hugging Face Datasets")
        print("=" * 80)
        
        try:
            from huggingface_hub import snapshot_download
        except ImportError:
            print("  ⚠️  huggingface-hub not installed - skipping HF datasets")
            print("     Install with: pip install huggingface-hub")
            return {}
        
        results = {}
        
        for dataset_name, dataset_id in self.huggingface_datasets.items():
            print(f"\n  📥 Downloading {dataset_name} ({dataset_id})...")
            target_dir = self.hf_dir / dataset_name
            
            try:
                if self.check_already_downloaded(target_dir):
                    print(f"  ⏭️  Already exists: {dataset_name}")
                    results[dataset_name] = True
                    self.results["hf_datasets"].append({
                        "name": dataset_name,
                        "id": dataset_id,
                        "success": True,
                        "message": "Already exists"
                    })
                    continue
                
                snapshot_download(
                    repo_id=dataset_id,
                    repo_type="dataset",
                    local_dir=str(target_dir),
                    local_dir_use_symlinks=False
                )
                
                print(f"  ✅ Downloaded {dataset_name}")
                results[dataset_name] = True
                
                self.results["hf_datasets"].append({
                    "name": dataset_name,
                    "id": dataset_id,
                    "success": True,
                    "message": "Downloaded successfully"
                })
                
            except Exception as e:
                print(f"  ❌ Failed to download {dataset_name}: {e}")
                results[dataset_name] = False
                self.results["hf_datasets"].append({
                    "name": dataset_name,
                    "id": dataset_id,
                    "success": False,
                    "message": str(e)
                })
                self.results["errors"].append(f"HF dataset {dataset_name}: {e}")
        
        return results
    
    def print_summary(self):
        """Print download summary."""
        print("\n" + "=" * 80)
        print("📊 Phase 5 Download Summary")
        print("=" * 80)
        
        categories = [
            ("Malware Analysis", self.results["malware_repos"]),
            ("Phishing & Social Engineering", self.results["phishing_repos"]),
            ("Mobile Security", self.results["mobile_repos"]),
            ("Crypto Attacks", self.results["crypto_repos"]),
            ("Cloud Security", self.results["cloud_repos"]),
            ("Binary Exploitation", self.results["binary_repos"]),
            ("APT Intelligence", self.results["apt_repos"]),
            ("Hugging Face Datasets", self.results["hf_datasets"]),
        ]
        
        total_repos = 0
        total_success = 0
        
        for category_name, repos in categories:
            if repos:
                success_count = sum(1 for r in repos if r.get("success", False))
                total_count = len(repos)
                total_repos += total_count
                total_success += success_count
                print(f"  {category_name}: {success_count}/{total_count} successful")
        
        print(f"\n  Total: {total_success}/{total_repos} repositories downloaded")
        
        if self.results["errors"]:
            print(f"\n  ⚠️  Errors: {len(self.results['errors'])}")
            for error in self.results["errors"][:5]:  # Show first 5 errors
                print(f"    - {error}")
            if len(self.results["errors"]) > 5:
                print(f"    ... and {len(self.results['errors']) - 5} more")
        
        print("=" * 80)
    
    def save_results(self):
        """Save phase results to JSON file."""
        results_file = self.phase_dir / "phase5_results.json"
        
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Results saved to: {results_file}")
    
    def run(self) -> Dict:
        """Execute Phase 5 downloads.
        
        Returns:
            Dict: Download results
        """
        print("\n" + "=" * 80)
        print("🚀 Phase 5: Advanced Threats & Black Hat Tactics")
        print("=" * 80)
        print(f"📁 Output directory: {self.phase_dir.absolute()}")
        
        if self.skip_malware:
            print("⏭️  Skip malware flag is SET - live malware samples will be skipped")
        
        print()
        
        # Download all categories
        self.download_malware_analysis()
        self.download_malware_live_samples()  # Has built-in safety check
        self.download_phishing_tools()
        self.download_mobile_security()
        self.download_crypto_attacks()
        self.download_cloud_security()
        self.download_binary_exploitation()
        self.download_apt_intelligence()
        self.download_hf_datasets()
        
        # Print summary
        self.print_summary()
        
        # Save results
        self.save_results()
        
        return self.results


def main():
    """Main entry point for Phase 5 downloader."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Phase 5: Download advanced threats and black hat tactics datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  WARNING: This phase includes LIVE MALWARE samples!
    Use ONLY in isolated VMs with no network access.
    See docs/MALWARE_SAFETY.md for safety guidelines.

Examples:
  python phase5_advanced_threats.py                    # Download all (with safety prompts)
  python phase5_advanced_threats.py --skip-malware     # Skip live malware samples
  python phase5_advanced_threats.py --dir /data        # Use custom directory
        """
    )
    
    parser.add_argument(
        "--dir",
        default="./cybersecurity_datasets",
        help="Base directory for datasets (default: ./cybersecurity_datasets)"
    )
    
    parser.add_argument(
        "--skip-malware",
        action="store_true",
        help="Skip downloading live malware samples (safer option)"
    )
    
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing repositories (git pull)"
    )
    
    args = parser.parse_args()
    
    # Create and run downloader
    downloader = Phase5Downloader(
        base_dir=args.dir,
        update=args.update,
        skip_malware=args.skip_malware
    )
    
    downloader.run()
    
    print("\n✅ Phase 5 download complete!")


if __name__ == "__main__":
    main()
