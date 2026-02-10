#!/usr/bin/env python3
"""
Phase 4: CVE Database Downloader
Downloads CVE data from the National Vulnerability Database (NVD) API.
"""

import os
import time
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional


class Phase4Downloader:
    """Downloads CVE database from NVD API."""
    
    def __init__(self, base_dir: str = "./cybersecurity_datasets"):
        """Initialize the Phase 4 downloader.
        
        Args:
            base_dir: Base directory for all datasets
        """
        self.base_dir = Path(base_dir)
        self.phase_dir = self.base_dir / "phase4_cve_database"
        self.phase_dir.mkdir(parents=True, exist_ok=True)
        
        self.api_base = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.api_key = os.environ.get("NVD_API_KEY")
        
        # Rate limiting based on API key presence
        self.rate_limit_delay = 0.6 if self.api_key else 6.0
        
        self.results = {
            "cve_files": [],
            "total_cves": 0,
            "api_key_used": bool(self.api_key),
            "errors": []
        }
        
        if self.api_key:
            print("  🔑 NVD API key detected - using faster rate limit (0.6s)")
        else:
            print("  ⚠️  No NVD API key - using slower rate limit (6s)")
            print("  💡 Set NVD_API_KEY environment variable for faster downloads")
    
    def download_cve_by_year(self, year: int, batch_size: int = 2000) -> bool:
        """Download CVEs for a specific year with pagination.
        
        Args:
            year: Year to download CVEs for
            batch_size: Number of CVEs per request
            
        Returns:
            bool: Success status
        """
        print(f"\n🔍 Downloading CVEs for {year}...")
        
        output_file = self.phase_dir / f"cve_{year}.json"
        
        # Check if file already exists
        if output_file.exists():
            print(f"  ⏭️  File already exists: {output_file.name}")
            try:
                with open(output_file, "r") as f:
                    data = json.load(f)
                    cve_count = len(data.get("vulnerabilities", []))
                    print(f"  📊 Contains {cve_count} CVEs")
                    self.results["cve_files"].append({
                        "year": year,
                        "file": output_file.name,
                        "cve_count": cve_count,
                        "status": "already_exists"
                    })
                    self.results["total_cves"] += cve_count
                    return True
            except Exception as e:
                print(f"  ⚠️  Error reading existing file: {e}")
        
        all_vulnerabilities = []
        start_index = 0
        
        # Date range for the year
        pub_start_date = f"{year}-01-01T00:00:00.000"
        pub_end_date = f"{year}-12-31T23:59:59.999"
        
        try:
            while True:
                # Prepare request parameters
                params = {
                    "pubStartDate": pub_start_date,
                    "pubEndDate": pub_end_date,
                    "startIndex": start_index,
                    "resultsPerPage": batch_size
                }
                
                headers = {}
                if self.api_key:
                    headers["apiKey"] = self.api_key
                
                print(f"  📦 Fetching batch starting at index {start_index}...")
                
                # Make API request
                try:
                    response = requests.get(
                        self.api_base,
                        params=params,
                        headers=headers,
                        timeout=30
                    )
                    
                    # Handle rate limiting
                    if response.status_code == 429:
                        print("  ⏸️  Rate limited - waiting 60 seconds...")
                        time.sleep(60)
                        continue
                    
                    response.raise_for_status()
                    data = response.json()
                    
                except requests.exceptions.RequestException as e:
                    error_msg = f"Request failed for year {year}: {str(e)}"
                    print(f"  ❌ {error_msg}")
                    self.results["errors"].append(error_msg)
                    return False
                
                # Extract vulnerabilities
                vulnerabilities = data.get("vulnerabilities", [])
                total_results = data.get("totalResults", 0)
                
                if not vulnerabilities:
                    print(f"  ✅ No more CVEs to fetch")
                    break
                
                all_vulnerabilities.extend(vulnerabilities)
                print(f"  📊 Retrieved {len(vulnerabilities)} CVEs ({len(all_vulnerabilities)}/{total_results})")
                
                # Check if we've retrieved all results
                if len(all_vulnerabilities) >= total_results:
                    break
                
                # Move to next batch
                start_index += len(vulnerabilities)
                
                # Rate limiting delay
                time.sleep(self.rate_limit_delay)
            
            # Save to file
            output_data = {
                "year": year,
                "total_cves": len(all_vulnerabilities),
                "downloaded_at": datetime.now().isoformat(),
                "vulnerabilities": all_vulnerabilities
            }
            
            with open(output_file, "w") as f:
                json.dump(output_data, f, indent=2)
            
            print(f"  ✅ Saved {len(all_vulnerabilities)} CVEs to {output_file.name}")
            
            self.results["cve_files"].append({
                "year": year,
                "file": output_file.name,
                "cve_count": len(all_vulnerabilities),
                "status": "success"
            })
            self.results["total_cves"] += len(all_vulnerabilities)
            
            return True
            
        except Exception as e:
            error_msg = f"Error downloading CVEs for {year}: {str(e)}"
            print(f"  ❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def download_cve_modified_recent(self, days: int = 120) -> bool:
        """Download recently modified CVEs.
        
        Args:
            days: Number of days back to look for modifications
            
        Returns:
            bool: Success status
        """
        print(f"\n🔄 Downloading Recently Modified CVEs (last {days} days)...")
        
        output_file = self.phase_dir / "cve_recent_modified.json"
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        mod_start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        mod_end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        
        all_vulnerabilities = []
        start_index = 0
        batch_size = 2000
        
        try:
            while True:
                params = {
                    "lastModStartDate": mod_start_date,
                    "lastModEndDate": mod_end_date,
                    "startIndex": start_index,
                    "resultsPerPage": batch_size
                }
                
                headers = {}
                if self.api_key:
                    headers["apiKey"] = self.api_key
                
                print(f"  📦 Fetching batch starting at index {start_index}...")
                
                try:
                    response = requests.get(
                        self.api_base,
                        params=params,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 429:
                        print("  ⏸️  Rate limited - waiting 60 seconds...")
                        time.sleep(60)
                        continue
                    
                    response.raise_for_status()
                    data = response.json()
                    
                except requests.exceptions.RequestException as e:
                    error_msg = f"Request failed for recent modifications: {str(e)}"
                    print(f"  ❌ {error_msg}")
                    self.results["errors"].append(error_msg)
                    return False
                
                vulnerabilities = data.get("vulnerabilities", [])
                total_results = data.get("totalResults", 0)
                
                if not vulnerabilities:
                    break
                
                all_vulnerabilities.extend(vulnerabilities)
                print(f"  📊 Retrieved {len(vulnerabilities)} CVEs ({len(all_vulnerabilities)}/{total_results})")
                
                if len(all_vulnerabilities) >= total_results:
                    break
                
                start_index += len(vulnerabilities)
                time.sleep(self.rate_limit_delay)
            
            # Save to file
            output_data = {
                "date_range": f"{days} days",
                "start_date": mod_start_date,
                "end_date": mod_end_date,
                "total_cves": len(all_vulnerabilities),
                "downloaded_at": datetime.now().isoformat(),
                "vulnerabilities": all_vulnerabilities
            }
            
            with open(output_file, "w") as f:
                json.dump(output_data, f, indent=2)
            
            print(f"  ✅ Saved {len(all_vulnerabilities)} recently modified CVEs")
            
            self.results["cve_files"].append({
                "type": "recent_modified",
                "file": output_file.name,
                "cve_count": len(all_vulnerabilities),
                "status": "success"
            })
            
            return True
            
        except Exception as e:
            error_msg = f"Error downloading recent CVEs: {str(e)}"
            print(f"  ❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def create_cve_statistics(self) -> Dict:
        """Create aggregate CVE statistics.
        
        Returns:
            Dict: Statistics summary
        """
        print("\n📊 Creating CVE Statistics...")
        
        stats = {
            "total_cves": self.results["total_cves"],
            "files": len(self.results["cve_files"]),
            "by_year": {},
            "generated_at": datetime.now().isoformat()
        }
        
        # Aggregate by year
        for cve_file in self.results["cve_files"]:
            if "year" in cve_file:
                year = cve_file["year"]
                stats["by_year"][year] = cve_file["cve_count"]
        
        # Save statistics
        stats_file = self.phase_dir / "cve_statistics.json"
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)
        
        print(f"  ✅ Statistics saved to {stats_file.name}")
        
        return stats
    
    def run(self) -> Dict:
        """Execute all Phase 4 downloads.
        
        Returns:
            Dict: Results summary
        """
        print("=" * 80)
        print("🚨 PHASE 4: CVE Database (NVD)")
        print("=" * 80)
        
        # Download CVEs for recent years
        years_to_download = [2024, 2025]
        
        for year in years_to_download:
            self.download_cve_by_year(year)
        
        # Download recently modified CVEs
        self.download_cve_modified_recent(days=120)
        
        # Create statistics
        stats = self.create_cve_statistics()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 PHASE 4 SUMMARY")
        print("=" * 80)
        print(f"  Total CVE Files: {len(self.results['cve_files'])}")
        print(f"  Total CVEs Downloaded: {self.results['total_cves']}")
        
        for cve_file in self.results["cve_files"]:
            if "year" in cve_file:
                print(f"    Year {cve_file['year']}: {cve_file['cve_count']} CVEs")
        
        if self.results["errors"]:
            print(f"\n  ⚠️  {len(self.results['errors'])} errors occurred")
        
        print("=" * 80)
        
        # Save results
        results_file = self.phase_dir / "phase4_results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        return self.results


def main():
    """Main entry point for Phase 4 downloader."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download CVE database from NVD"
    )
    parser.add_argument(
        "--dir",
        default="./cybersecurity_datasets",
        help="Base directory for datasets (default: ./cybersecurity_datasets)"
    )
    parser.add_argument(
        "--year",
        type=int,
        help="Download CVEs for specific year"
    )
    
    args = parser.parse_args()
    
    downloader = Phase4Downloader(args.dir)
    
    if args.year:
        downloader.download_cve_by_year(args.year)
    else:
        downloader.run()


if __name__ == "__main__":
    main()
