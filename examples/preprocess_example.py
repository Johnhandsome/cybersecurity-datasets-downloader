#!/usr/bin/env python3
"""
Complete working example for preprocessing cybersecurity datasets.
This script demonstrates how to extract and format data from all phases.
"""

import re
import json
import csv
from pathlib import Path
from typing import List, Dict


class DatasetPreprocessor:
    """Preprocessor for cybersecurity datasets."""
    
    def __init__(self, base_dir: str = "./cybersecurity_datasets"):
        """Initialize the preprocessor.
        
        Args:
            base_dir: Base directory containing downloaded datasets
        """
        self.base_dir = Path(base_dir)
        self.all_pairs = []
    
    def extract_ctf_qa_pairs(self) -> List[Dict]:
        """Extract Q&A pairs from CTF writeup markdown files.
        
        Returns:
            List of instruction-output pairs
        """
        print("🔄 Processing CTF Writeups...")
        pairs = []
        
        phase1_dir = self.base_dir / "phase1_ctf_bugbounty" / "ctf_writeups"
        if not phase1_dir.exists():
            print("  ⚠️  Phase 1 directory not found")
            return pairs
        
        for md_file in phase1_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Split by headers
                sections = re.split(r'\n#+\s+', content)
                
                for section in sections:
                    if not section.strip() or len(section) < 100:
                        continue
                    
                    lines = section.split('\n', 1)
                    if len(lines) < 2:
                        continue
                    
                    title = lines[0].strip()
                    body = lines[1].strip()
                    
                    # Create instruction pair for solution sections
                    if any(kw in title.lower() for kw in ['solution', 'solve', 'exploit', 'walkthrough']):
                        pairs.append({
                            "instruction": f"Explain how to solve this CTF challenge: {title}",
                            "input": "",
                            "output": body[:2000]
                        })
                    
                    # Extract code blocks
                    code_blocks = re.findall(r'```(.*?)```', body, re.DOTALL)
                    for code in code_blocks:
                        clean_code = code.strip()
                        if 50 < len(clean_code) < 1500:
                            pairs.append({
                                "instruction": "Analyze this CTF exploit code",
                                "input": clean_code,
                                "output": f"This code is part of solving: {title}"
                            })
            
            except Exception as e:
                continue
        
        print(f"  ✅ Extracted {len(pairs)} CTF pairs")
        return pairs
    
    def extract_exploit_code_pairs(self) -> List[Dict]:
        """Extract exploit code and descriptions from ExploitDB.
        
        Returns:
            List of instruction-output pairs
        """
        print("🔄 Processing Exploit Database...")
        pairs = []
        
        exploitdb_dir = self.base_dir / "phase2_exploits_tools" / "exploitdb"
        if not exploitdb_dir.exists():
            print("  ⚠️  ExploitDB directory not found")
            return pairs
        
        csv_file = exploitdb_dir / "files.csv"
        if not csv_file.exists():
            print("  ⚠️  files.csv not found")
            return pairs
        
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader):
                    if i >= 1000:  # Limit for example
                        break
                    
                    description = row.get('description', '').strip()
                    code_type = row.get('type', '').strip()
                    platform = row.get('platform', '').strip()
                    
                    if not description or len(description) < 20:
                        continue
                    
                    pairs.append({
                        "instruction": f"Describe the {platform} {code_type} exploit",
                        "input": description,
                        "output": f"This is a {code_type} vulnerability affecting {platform}. {description[:500]}"
                    })
        
        except Exception as e:
            print(f"  ⚠️  Error reading CSV: {e}")
        
        print(f"  ✅ Extracted {len(pairs)} exploit pairs")
        return pairs
    
    def extract_yara_sigma_pairs(self) -> List[Dict]:
        """Extract YARA and Sigma rules as training data.
        
        Returns:
            List of instruction-output pairs
        """
        print("🔄 Processing YARA & Sigma Rules...")
        pairs = []
        
        # YARA rules
        yara_dir = self.base_dir / "phase3_yara_sigma" / "yara_rules"
        if yara_dir.exists():
            for yara_file in list(yara_dir.rglob("*.yar*"))[:100]:  # Limit for example
                try:
                    with open(yara_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Extract rule names
                    rules = re.findall(r'rule\s+(\w+)\s*\{(.*?)\}', content, re.DOTALL)
                    
                    for rule_name, rule_body in rules[:3]:  # Limit per file
                        if len(rule_body) < 50:
                            continue
                        
                        full_rule = f"rule {rule_name} {{{rule_body[:1000]}}}"
                        
                        pairs.append({
                            "instruction": f"Explain this YARA detection rule: {rule_name}",
                            "input": full_rule,
                            "output": f"This YARA rule detects {rule_name} by matching specific patterns."
                        })
                
                except Exception:
                    continue
        
        # Sigma rules
        sigma_dir = self.base_dir / "phase3_yara_sigma" / "sigma_rules"
        if sigma_dir.exists():
            for sigma_file in list(sigma_dir.rglob("*.yml"))[:100]:  # Limit for example
                try:
                    with open(sigma_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Simple YAML parsing
                    title_match = re.search(r'title:\s*(.+)', content)
                    desc_match = re.search(r'description:\s*(.+)', content)
                    
                    if title_match:
                        title = title_match.group(1).strip()
                        description = desc_match.group(1).strip() if desc_match else ""
                        
                        pairs.append({
                            "instruction": f"Create a Sigma detection rule for: {title}",
                            "input": description,
                            "output": content[:1500]
                        })
                
                except Exception:
                    continue
        
        print(f"  ✅ Extracted {len(pairs)} rule pairs")
        return pairs
    
    def extract_cve_pairs(self) -> List[Dict]:
        """Extract CVE data as Q&A pairs.
        
        Returns:
            List of instruction-output pairs
        """
        print("🔄 Processing CVE Database...")
        pairs = []
        
        phase4_dir = self.base_dir / "phase4_cve_database"
        if not phase4_dir.exists():
            print("  ⚠️  Phase 4 directory not found")
            return pairs
        
        for cve_file in phase4_dir.glob("cve_*.json"):
            try:
                with open(cve_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                vulnerabilities = data.get('vulnerabilities', [])
                
                for i, vuln_item in enumerate(vulnerabilities):
                    if i >= 500:  # Limit per file for example
                        break
                    
                    cve = vuln_item.get('cve', {})
                    cve_id = cve.get('id', '')
                    
                    # Get description
                    descriptions = cve.get('descriptions', [])
                    description = ''
                    for desc in descriptions:
                        if desc.get('lang') == 'en':
                            description = desc.get('value', '')
                            break
                    
                    if not description:
                        continue
                    
                    # Get severity
                    metrics = cve.get('metrics', {})
                    severity = 'Unknown'
                    base_score = 'N/A'
                    
                    cvss_v3 = metrics.get('cvssMetricV31', []) or metrics.get('cvssMetricV30', [])
                    if cvss_v3:
                        cvss_data = cvss_v3[0].get('cvssData', {})
                        severity = cvss_data.get('baseSeverity', 'Unknown')
                        base_score = str(cvss_data.get('baseScore', 'N/A'))
                    
                    pairs.append({
                        "instruction": f"Describe the vulnerability {cve_id}",
                        "input": "",
                        "output": f"{cve_id} is a {severity} severity vulnerability (CVSS: {base_score}). {description[:800]}"
                    })
                    
                    pairs.append({
                        "instruction": f"What is the CVSS score of {cve_id}?",
                        "input": description[:300],
                        "output": f"The CVSS base score is {base_score} with {severity} severity."
                    })
            
            except Exception as e:
                print(f"  ⚠️  Error reading {cve_file.name}: {e}")
                continue
        
        print(f"  ✅ Extracted {len(pairs)} CVE pairs")
        return pairs
    
    def create_training_dataset(self, output_file: str = "training_data.jsonl"):
        """Create complete training dataset from all phases.
        
        Args:
            output_file: Output JSONL file path
        """
        print("=" * 80)
        print("🛡️  CYBERSECURITY DATASET PREPROCESSING")
        print("=" * 80)
        print()
        
        # Extract from all phases
        self.all_pairs.extend(self.extract_ctf_qa_pairs())
        self.all_pairs.extend(self.extract_exploit_code_pairs())
        self.all_pairs.extend(self.extract_yara_sigma_pairs())
        self.all_pairs.extend(self.extract_cve_pairs())
        
        # Save to JSONL
        print()
        print(f"💾 Saving {len(self.all_pairs)} training pairs to {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for pair in self.all_pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + '\n')
        
        print(f"✅ Successfully saved to {output_file}")
        
        # Generate statistics
        stats = {
            "total_pairs": len(self.all_pairs),
            "output_file": output_file,
            "phases_processed": 4,
            "by_type": {
                "ctf": sum(1 for p in self.all_pairs if 'CTF' in p.get('instruction', '')),
                "exploit": sum(1 for p in self.all_pairs if 'exploit' in p.get('instruction', '').lower()),
                "yara": sum(1 for p in self.all_pairs if 'YARA' in p.get('instruction', '')),
                "sigma": sum(1 for p in self.all_pairs if 'Sigma' in p.get('instruction', '')),
                "cve": sum(1 for p in self.all_pairs if 'CVE' in p.get('instruction', ''))
            }
        }
        
        stats_file = "training_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"📊 Statistics saved to {stats_file}")
        
        print()
        print("=" * 80)
        print("📊 PREPROCESSING SUMMARY")
        print("=" * 80)
        print(f"  Total Training Pairs: {stats['total_pairs']}")
        print(f"  CTF Pairs: {stats['by_type']['ctf']}")
        print(f"  Exploit Pairs: {stats['by_type']['exploit']}")
        print(f"  YARA Pairs: {stats['by_type']['yara']}")
        print(f"  Sigma Pairs: {stats['by_type']['sigma']}")
        print(f"  CVE Pairs: {stats['by_type']['cve']}")
        print("=" * 80)
        
        return self.all_pairs


def main():
    """Main entry point for preprocessing example."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Preprocess cybersecurity datasets for AI/ML training"
    )
    parser.add_argument(
        "--dir",
        default="./cybersecurity_datasets",
        help="Base directory for datasets (default: ./cybersecurity_datasets)"
    )
    parser.add_argument(
        "--output",
        default="training_data.jsonl",
        help="Output JSONL file (default: training_data.jsonl)"
    )
    
    args = parser.parse_args()
    
    preprocessor = DatasetPreprocessor(args.dir)
    preprocessor.create_training_dataset(args.output)


if __name__ == "__main__":
    main()
