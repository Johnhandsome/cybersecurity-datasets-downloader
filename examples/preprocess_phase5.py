#!/usr/bin/env python3
"""
Phase 5 Preprocessing Example
Demonstrates how to preprocess Phase 5 datasets for Llama 3 fine-tuning.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import hashlib


class Phase5Preprocessor:
    """Preprocessor for Phase 5 advanced threats datasets."""
    
    def __init__(self, base_dir: str = "./cybersecurity_datasets"):
        """Initialize preprocessor.
        
        Args:
            base_dir: Base directory containing downloaded datasets
        """
        self.base_dir = Path(base_dir)
        self.phase5_dir = self.base_dir / "phase5_advanced_threats"
        self.output_dir = Path("./processed_phase5")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.processed_samples = []
    
    def create_instruction_sample(
        self, 
        instruction: str, 
        input_text: str, 
        output_text: str,
        category: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Create a single instruction-tuning sample.
        
        Args:
            instruction: Task instruction
            input_text: Input context
            output_text: Expected output
            category: Dataset category
            metadata: Optional metadata
        
        Returns:
            Dict: Formatted instruction sample
        """
        sample = {
            "instruction": instruction,
            "input": input_text,
            "output": output_text,
            "category": category,
        }
        
        if metadata:
            sample["metadata"] = metadata
        
        # Generate unique ID
        sample_str = f"{instruction}{input_text}{output_text}"
        sample["id"] = hashlib.md5(sample_str.encode()).hexdigest()
        
        return sample
    
    def process_malware_analysis(self) -> List[Dict]:
        """Process malware analysis repositories.
        
        Returns:
            List of instruction samples
        """
        print("🦠 Processing malware analysis data...")
        samples = []
        
        malware_dir = self.phase5_dir / "malware_analysis"
        if not malware_dir.exists():
            print("  ⚠️  Malware directory not found")
            return samples
        
        # Example: Process malware analysis markdown files
        for md_file in malware_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                
                # Skip if too short
                if len(content) < 100:
                    continue
                
                # Extract sections
                sections = self._extract_markdown_sections(content)
                
                # Create Q&A pairs
                if "description" in sections and "analysis" in sections:
                    sample = self.create_instruction_sample(
                        instruction="Analyze this malware and provide detailed insights.",
                        input_text=sections["description"][:1000],
                        output_text=sections["analysis"][:2000],
                        category="malware_analysis",
                        metadata={"source_file": str(md_file.name)}
                    )
                    samples.append(sample)
                
            except Exception as e:
                print(f"  ⚠️  Error processing {md_file}: {e}")
                continue
        
        print(f"  ✅ Processed {len(samples)} malware analysis samples")
        return samples
    
    def process_phishing_data(self) -> List[Dict]:
        """Process phishing and social engineering data.
        
        Returns:
            List of instruction samples
        """
        print("🎣 Processing phishing data...")
        samples = []
        
        phishing_dir = self.phase5_dir / "phishing_social_eng"
        if not phishing_dir.exists():
            print("  ⚠️  Phishing directory not found")
            return samples
        
        # Process phishing database
        phishing_db = phishing_dir / "phishing_database"
        if phishing_db.exists():
            # Look for phishing URLs or email samples
            for txt_file in phishing_db.rglob("*.txt"):
                try:
                    content = txt_file.read_text(encoding='utf-8', errors='ignore')
                    lines = content.strip().split('\n')
                    
                    for line in lines[:100]:  # Process first 100
                        if line.strip() and self._is_url(line):
                            sample = self.create_instruction_sample(
                                instruction="Is this URL a phishing attempt? Explain your reasoning.",
                                input_text=line.strip(),
                                output_text=self._analyze_phishing_url(line.strip()),
                                category="phishing_detection"
                            )
                            samples.append(sample)
                            
                except Exception as e:
                    continue
        
        print(f"  ✅ Processed {len(samples)} phishing samples")
        return samples
    
    def process_mobile_security(self) -> List[Dict]:
        """Process mobile security data.
        
        Returns:
            List of instruction samples
        """
        print("📱 Processing mobile security data...")
        samples = []
        
        mobile_dir = self.phase5_dir / "mobile_security"
        if not mobile_dir.exists():
            print("  ⚠️  Mobile directory not found")
            return samples
        
        # Process mobile vulnerability descriptions
        for md_file in mobile_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                
                if len(content) < 100:
                    continue
                
                # Extract Android/iOS specific content
                if "Android" in content or "iOS" in content:
                    # Create learning samples
                    sample = self.create_instruction_sample(
                        instruction="Explain this mobile security vulnerability.",
                        input_text=self._extract_summary(content, max_length=500),
                        output_text=self._extract_details(content, max_length=1500),
                        category="mobile_security",
                        metadata={"platform": self._detect_platform(content)}
                    )
                    samples.append(sample)
                    
            except Exception as e:
                continue
        
        print(f"  ✅ Processed {len(samples)} mobile security samples")
        return samples
    
    def process_cloud_security(self) -> List[Dict]:
        """Process cloud security data.
        
        Returns:
            List of instruction samples
        """
        print("☁️  Processing cloud security data...")
        samples = []
        
        cloud_dir = self.phase5_dir / "cloud_security"
        if not cloud_dir.exists():
            print("  ⚠️  Cloud directory not found")
            return samples
        
        # Process cloud security tools and vulnerabilities
        for readme in cloud_dir.rglob("README.md"):
            try:
                content = readme.read_text(encoding='utf-8', errors='ignore')
                
                # Extract cloud platform
                platform = self._detect_cloud_platform(content)
                
                if platform:
                    sections = self._extract_markdown_sections(content)
                    
                    if sections:
                        for section_name, section_content in sections.items():
                            if len(section_content) > 200:
                                sample = self.create_instruction_sample(
                                    instruction=f"Explain this {platform} security concept.",
                                    input_text=section_name,
                                    output_text=section_content[:1500],
                                    category="cloud_security",
                                    metadata={"platform": platform}
                                )
                                samples.append(sample)
                                
            except Exception as e:
                continue
        
        print(f"  ✅ Processed {len(samples)} cloud security samples")
        return samples
    
    def process_apt_intelligence(self) -> List[Dict]:
        """Process APT and threat intelligence data.
        
        Returns:
            List of instruction samples
        """
        print("🎯 Processing APT intelligence...")
        samples = []
        
        apt_dir = self.phase5_dir / "apt_intelligence"
        if not apt_dir.exists():
            print("  ⚠️  APT directory not found")
            return samples
        
        # Process APT notes and reports
        for file in apt_dir.rglob("*.md"):
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                
                if len(content) < 200:
                    continue
                
                # Extract APT information
                sections = self._extract_markdown_sections(content)
                
                # Create threat intelligence samples
                if sections:
                    sample = self.create_instruction_sample(
                        instruction="Analyze this APT campaign and provide threat intelligence.",
                        input_text=self._extract_summary(content, max_length=800),
                        output_text=self._extract_analysis(content, max_length=2000),
                        category="apt_intelligence",
                        metadata={"apt_group": self._extract_apt_name(file.name)}
                    )
                    samples.append(sample)
                    
            except Exception as e:
                continue
        
        print(f"  ✅ Processed {len(samples)} APT intelligence samples")
        return samples
    
    def process_binary_exploitation(self) -> List[Dict]:
        """Process binary exploitation data.
        
        Returns:
            List of instruction samples
        """
        print("💾 Processing binary exploitation data...")
        samples = []
        
        binary_dir = self.phase5_dir / "binary_exploitation"
        if not binary_dir.exists():
            print("  ⚠️  Binary exploitation directory not found")
            return samples
        
        # Process exploitation techniques
        for md_file in binary_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                
                if len(content) < 150:
                    continue
                
                # Extract exploitation techniques
                if any(keyword in content.lower() for keyword in 
                       ["rop", "buffer overflow", "heap", "stack", "pwn"]):
                    
                    sample = self.create_instruction_sample(
                        instruction="Explain this binary exploitation technique.",
                        input_text=self._extract_summary(content, max_length=600),
                        output_text=self._extract_details(content, max_length=1800),
                        category="binary_exploitation",
                        metadata={"technique": self._extract_technique(content)}
                    )
                    samples.append(sample)
                    
            except Exception as e:
                continue
        
        print(f"  ✅ Processed {len(samples)} binary exploitation samples")
        return samples
    
    # Helper methods
    
    def _extract_markdown_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from markdown content."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('#'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.strip('#').strip().lower()
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _extract_summary(self, content: str, max_length: int = 500) -> str:
        """Extract summary from content."""
        lines = content.split('\n')
        summary = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                summary.append(line)
                if len(' '.join(summary)) > max_length:
                    break
        
        return ' '.join(summary)[:max_length]
    
    def _extract_details(self, content: str, max_length: int = 1500) -> str:
        """Extract detailed information."""
        # Skip first few lines (usually title/summary)
        lines = content.split('\n')[3:]
        details = ' '.join([l.strip() for l in lines if l.strip()])
        return details[:max_length]
    
    def _extract_analysis(self, content: str, max_length: int = 2000) -> str:
        """Extract analysis section."""
        sections = self._extract_markdown_sections(content)
        
        # Look for analysis-related sections
        for key in ['analysis', 'technical details', 'indicators', 'ttps']:
            if key in sections:
                return sections[key][:max_length]
        
        # Return general content
        return self._extract_details(content, max_length)
    
    def _is_url(self, text: str) -> bool:
        """Check if text is a URL."""
        url_pattern = r'https?://[^\s]+'
        return bool(re.match(url_pattern, text))
    
    def _analyze_phishing_url(self, url: str) -> str:
        """Generate phishing analysis for URL."""
        indicators = []
        
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            indicators.append("Uses IP address instead of domain name")
        
        if url.count('-') > 3:
            indicators.append("Excessive hyphens in domain")
        
        if any(word in url.lower() for word in ['login', 'secure', 'account', 'verify']):
            indicators.append("Contains common phishing keywords")
        
        if len(url) > 100:
            indicators.append("Unusually long URL")
        
        if indicators:
            return f"This appears to be a phishing URL. Red flags: {'; '.join(indicators)}."
        else:
            return "This URL shows potential phishing characteristics and should be investigated."
    
    def _detect_platform(self, content: str) -> str:
        """Detect mobile platform."""
        content_lower = content.lower()
        if "android" in content_lower and "ios" in content_lower:
            return "cross-platform"
        elif "android" in content_lower:
            return "android"
        elif "ios" in content_lower:
            return "ios"
        return "unknown"
    
    def _detect_cloud_platform(self, content: str) -> Optional[str]:
        """Detect cloud platform."""
        content_lower = content.lower()
        if "aws" in content_lower or "amazon" in content_lower:
            return "AWS"
        elif "azure" in content_lower or "microsoft" in content_lower:
            return "Azure"
        elif "gcp" in content_lower or "google cloud" in content_lower:
            return "GCP"
        return None
    
    def _extract_apt_name(self, filename: str) -> str:
        """Extract APT group name from filename."""
        # Simple extraction - improve based on actual filenames
        name = filename.replace('.md', '').replace('_', ' ').title()
        return name
    
    def _extract_technique(self, content: str) -> str:
        """Extract exploitation technique."""
        content_lower = content.lower()
        
        techniques = {
            "rop": "Return-Oriented Programming",
            "buffer overflow": "Buffer Overflow",
            "heap": "Heap Exploitation",
            "stack": "Stack Overflow",
            "format string": "Format String",
            "use after free": "Use-After-Free",
        }
        
        for key, value in techniques.items():
            if key in content_lower:
                return value
        
        return "General Binary Exploitation"
    
    def process_all(self) -> List[Dict]:
        """Process all Phase 5 datasets.
        
        Returns:
            List of all processed samples
        """
        print("\n" + "=" * 80)
        print("🚀 Processing Phase 5 Datasets for Llama 3 Training")
        print("=" * 80)
        
        # Process all categories
        all_samples = []
        
        all_samples.extend(self.process_malware_analysis())
        all_samples.extend(self.process_phishing_data())
        all_samples.extend(self.process_mobile_security())
        all_samples.extend(self.process_cloud_security())
        all_samples.extend(self.process_apt_intelligence())
        all_samples.extend(self.process_binary_exploitation())
        
        print("\n" + "=" * 80)
        print(f"📊 Total Samples Processed: {len(all_samples)}")
        print("=" * 80)
        
        return all_samples
    
    def save_samples(self, samples: List[Dict], output_file: str = "phase5_processed.jsonl"):
        """Save processed samples to JSONL file.
        
        Args:
            samples: List of processed samples
            output_file: Output filename
        """
        output_path = self.output_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')
        
        print(f"\n✅ Saved {len(samples)} samples to {output_path}")
        
        # Also save as regular JSON for easy viewing
        json_path = self.output_dir / output_file.replace('.jsonl', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(samples, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Also saved as JSON to {json_path}")
    
    def generate_statistics(self, samples: List[Dict]):
        """Generate and print statistics about processed samples.
        
        Args:
            samples: List of processed samples
        """
        from collections import Counter
        
        print("\n" + "=" * 80)
        print("📊 Dataset Statistics")
        print("=" * 80)
        
        # Category distribution
        categories = [s['category'] for s in samples]
        category_counts = Counter(categories)
        
        print("\nCategory Distribution:")
        for category, count in category_counts.most_common():
            percentage = (count / len(samples)) * 100
            print(f"  {category:25s}: {count:6d} ({percentage:5.1f}%)")
        
        # Average lengths
        avg_instruction_len = sum(len(s['instruction']) for s in samples) / len(samples)
        avg_input_len = sum(len(s['input']) for s in samples) / len(samples)
        avg_output_len = sum(len(s['output']) for s in samples) / len(samples)
        
        print("\nAverage Lengths:")
        print(f"  Instruction: {avg_instruction_len:.0f} characters")
        print(f"  Input:       {avg_input_len:.0f} characters")
        print(f"  Output:      {avg_output_len:.0f} characters")
        
        print("=" * 80)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Preprocess Phase 5 datasets")
    parser.add_argument(
        "--base-dir",
        default="./cybersecurity_datasets",
        help="Base directory with downloaded datasets"
    )
    parser.add_argument(
        "--output",
        default="phase5_processed.jsonl",
        help="Output filename"
    )
    
    args = parser.parse_args()
    
    # Process datasets
    preprocessor = Phase5Preprocessor(args.base_dir)
    samples = preprocessor.process_all()
    
    if samples:
        # Generate statistics
        preprocessor.generate_statistics(samples)
        
        # Save results
        preprocessor.save_samples(samples, args.output)
        
        print("\n✅ Preprocessing complete!")
        print(f"📁 Output directory: {preprocessor.output_dir.absolute()}")
    else:
        print("\n⚠️  No samples processed. Check that Phase 5 data is downloaded.")


if __name__ == "__main__":
    main()
