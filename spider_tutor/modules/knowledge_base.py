"""
Spider Cybersecurity Tutor - Knowledge Base
Cybersecurity reference data, flashcards, and templates
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import random


@dataclass
class Flashcard:
    """A study flashcard"""
    question: str
    answer: str
    category: str
    difficulty: str  # beginner, intermediate, advanced
    cert_relevance: List[str]  # Security+, CySA+, CISSP, etc.


@dataclass
class MitreAttackTechnique:
    """MITRE ATT&CK technique reference"""
    technique_id: str
    name: str
    tactic: str
    description: str
    detection: str
    mitigation: str


# Exam flashcard data
FLASHCARDS = [
    # Security+ Basics
    Flashcard(
        question="What is the CIA Triad?",
        answer="Confidentiality, Integrity, and Availability - the three core principles of information security.",
        category="Fundamentals",
        difficulty="beginner",
        cert_relevance=["Security+", "CISSP", "CC"]
    ),
    Flashcard(
        question="What is the difference between symmetric and asymmetric encryption?",
        answer="Symmetric uses the same key for encryption/decryption (AES, DES). Asymmetric uses a key pair - public for encryption, private for decryption (RSA, ECC).",
        category="Cryptography",
        difficulty="beginner",
        cert_relevance=["Security+", "CISSP"]
    ),
    Flashcard(
        question="What is defense in depth?",
        answer="A security strategy using multiple layers of controls (physical, technical, administrative) so that if one fails, others still protect the asset.",
        category="Architecture",
        difficulty="beginner",
        cert_relevance=["Security+", "CISSP", "CySA+"]
    ),
    Flashcard(
        question="What is the principle of least privilege?",
        answer="Users should have only the minimum access rights needed to perform their job functions, reducing potential damage from accidents or attacks.",
        category="Access Control",
        difficulty="beginner",
        cert_relevance=["Security+", "CISSP", "CC"]
    ),
    Flashcard(
        question="What are the three types of security controls?",
        answer="Technical (firewalls, encryption), Administrative (policies, training), and Physical (locks, guards, cameras).",
        category="Controls",
        difficulty="beginner",
        cert_relevance=["Security+", "CISSP"]
    ),
    
    # Intermediate
    Flashcard(
        question="What is the difference between IDS and IPS?",
        answer="IDS (Intrusion Detection System) monitors and alerts. IPS (Intrusion Prevention System) actively blocks threats. IDS is passive; IPS is inline and active.",
        category="Network Security",
        difficulty="intermediate",
        cert_relevance=["Security+", "CySA+"]
    ),
    Flashcard(
        question="What are the phases of incident response?",
        answer="1) Preparation, 2) Identification/Detection, 3) Containment, 4) Eradication, 5) Recovery, 6) Lessons Learned. (NIST SP 800-61)",
        category="Incident Response",
        difficulty="intermediate",
        cert_relevance=["Security+", "CySA+", "CISSP"]
    ),
    Flashcard(
        question="What is SIEM?",
        answer="Security Information and Event Management - collects and analyzes logs from multiple sources for threat detection, compliance, and incident response.",
        category="Detection",
        difficulty="intermediate",
        cert_relevance=["Security+", "CySA+"]
    ),
    Flashcard(
        question="What is the OWASP Top 10?",
        answer="A list of the most critical web application security risks, updated periodically. Includes: Injection, Broken Authentication, XSS, Insecure Design, etc.",
        category="Application Security",
        difficulty="intermediate",
        cert_relevance=["Security+", "CySA+"]
    ),
    
    # Advanced
    Flashcard(
        question="What is STRIDE threat modeling?",
        answer="A threat classification model: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.",
        category="Threat Modeling",
        difficulty="advanced",
        cert_relevance=["CISSP", "CySA+"]
    ),
    Flashcard(
        question="What are the NIST CSF core functions?",
        answer="Identify, Protect, Detect, Respond, Recover - the five core functions of the NIST Cybersecurity Framework.",
        category="Frameworks",
        difficulty="intermediate",
        cert_relevance=["Security+", "CySA+", "CISSP"]
    ),
    Flashcard(
        question="What is the difference between RPO and RTO?",
        answer="RPO (Recovery Point Objective) = maximum acceptable data loss. RTO (Recovery Time Objective) = maximum acceptable downtime.",
        category="Business Continuity",
        difficulty="intermediate",
        cert_relevance=["Security+", "CISSP"]
    ),
]

# MITRE ATT&CK Common Techniques
MITRE_TECHNIQUES = [
    MitreAttackTechnique(
        technique_id="T1566",
        name="Phishing",
        tactic="Initial Access",
        description="Adversaries send phishing messages to gain access to victim systems.",
        detection="Monitor email logs, check for suspicious attachments/links, user reports, sandbox analysis.",
        mitigation="Email filtering, user awareness training, MFA, sandbox attachments."
    ),
    MitreAttackTechnique(
        technique_id="T1059",
        name="Command and Scripting Interpreter",
        tactic="Execution",
        description="Adversaries abuse command/script interpreters to execute commands (PowerShell, Bash, Python).",
        detection="Script block logging, command-line auditing, behavior analysis.",
        mitigation="Disable unused interpreters, application whitelisting, constrained language mode."
    ),
    MitreAttackTechnique(
        technique_id="T1078",
        name="Valid Accounts",
        tactic="Defense Evasion, Persistence, Initial Access",
        description="Adversaries use legitimate credentials to access systems.",
        detection="Monitor for unusual login times/locations, impossible travel, failed auth patterns.",
        mitigation="MFA, privileged access management, regular credential rotation, monitoring."
    ),
    MitreAttackTechnique(
        technique_id="T1486",
        name="Data Encrypted for Impact",
        tactic="Impact",
        description="Adversaries encrypt data to disrupt availability (ransomware).",
        detection="File modification monitoring, unusual file extensions, high file I/O.",
        mitigation="Backups, offline backups, endpoint protection, network segmentation."
    ),
    MitreAttackTechnique(
        technique_id="T1070",
        name="Indicator Removal",
        tactic="Defense Evasion",
        description="Adversaries delete or modify logs/evidence to cover tracks.",
        detection="Log forwarding (SIEM), file integrity monitoring, detect log gaps.",
        mitigation="Centralized logging, immutable logs, access controls on log files."
    ),
]

# Report Templates
INCIDENT_REPORT_TEMPLATE = """
# Incident Report

## Summary
| Field | Value |
|-------|-------|
| Incident ID | [INC-XXXX] |
| Date/Time Detected | [YYYY-MM-DD HH:MM UTC] |
| Severity | [Critical/High/Medium/Low] |
| Status | [Open/Investigating/Contained/Resolved] |
| Handler | [Analyst Name] |

## Executive Summary
[2-3 sentence summary of the incident, impact, and current status]

## Timeline
| Time (UTC) | Event |
|------------|-------|
| | Initial detection |
| | Investigation started |
| | Containment actions |
| | Eradication complete |
| | Recovery complete |

## Scope & Impact
- **Affected Systems**: 
- **Affected Users**: 
- **Data Impact**: 
- **Business Impact**: 

## Technical Details
### Attack Vector
[How the attacker gained access]

### Indicators of Compromise (IOCs)
- **IP Addresses**: 
- **Domains**: 
- **File Hashes**: 
- **Other**: 

### MITRE ATT&CK Mapping
| Tactic | Technique | ID |
|--------|-----------|-----|
| | | |

## Response Actions
### Containment
- [ ] 

### Eradication
- [ ] 

### Recovery
- [ ] 

## Lessons Learned
- What went well:
- What could improve:
- Action items:

## References
- [Related tickets, logs, evidence]
"""

VULNERABILITY_REPORT_TEMPLATE = """
# Vulnerability Report

## Finding Summary
| Field | Value |
|-------|-------|
| Finding ID | [VULN-XXXX] |
| Title | [Descriptive Title] |
| Severity | [Critical/High/Medium/Low] |
| CVSS Score | [0.0-10.0] |
| CVE ID | [CVE-XXXX-XXXXX] (if applicable) |
| Status | [Open/Remediation/Verified/Closed] |

## Affected Asset(s)
| Asset | Type | Owner |
|-------|------|-------|
| | | |

## Description
[Clear description of the vulnerability]

## Evidence
[Screenshots, logs, proof of concept details - sanitized]

## Risk Assessment
- **Likelihood**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Risk Rating**: [Critical/High/Medium/Low]

## Recommended Remediation
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Workaround (if applicable)
[Temporary mitigation if patch not immediately available]

## Remediation SLA
| Severity | SLA |
|----------|-----|
| Critical | 24-72 hours |
| High | 7 days |
| Medium | 30 days |
| Low | 90 days |

## References
- [Vendor advisory]
- [NVD link]
- [Additional resources]
"""


class KnowledgeBase:
    """Manages cybersecurity knowledge and resources"""
    
    def __init__(self):
        self.flashcards = FLASHCARDS
        self.mitre_techniques = MITRE_TECHNIQUES
    
    def get_flashcards(self, 
                       category: Optional[str] = None,
                       difficulty: Optional[str] = None,
                       cert: Optional[str] = None,
                       count: int = 5) -> List[Flashcard]:
        """Get flashcards matching criteria"""
        cards = self.flashcards
        
        if category:
            cards = [c for c in cards if category.lower() in c.category.lower()]
        if difficulty:
            cards = [c for c in cards if c.difficulty == difficulty.lower()]
        if cert:
            cards = [c for c in cards if any(cert.upper() in cr.upper() for cr in c.cert_relevance)]
        
        # Shuffle and return requested count
        random.shuffle(cards)
        return cards[:count]
    
    def get_quiz(self, 
                 category: Optional[str] = None,
                 count: int = 5) -> List[Dict]:
        """Generate a quiz from flashcards"""
        cards = self.get_flashcards(category=category, count=count)
        quiz = []
        
        for i, card in enumerate(cards, 1):
            quiz.append({
                "number": i,
                "question": card.question,
                "answer": card.answer,
                "category": card.category,
                "difficulty": card.difficulty
            })
        
        return quiz
    
    def format_quiz(self, quiz: List[Dict], show_answers: bool = False) -> str:
        """Format quiz for display"""
        output = "# 🎯 Cybersecurity Quiz\n\n"
        
        for q in quiz:
            output += f"**Q{q['number']}** [{q['category']}] ({q['difficulty']})\n"
            output += f"{q['question']}\n\n"
            
            if show_answers:
                output += f"**Answer:** {q['answer']}\n\n"
                output += "---\n\n"
        
        if not show_answers:
            output += "\n*Say 'show answers' to reveal the answers*"
        
        return output
    
    def get_mitre_technique(self, technique_id: str) -> Optional[MitreAttackTechnique]:
        """Get a MITRE ATT&CK technique by ID"""
        for tech in self.mitre_techniques:
            if tech.technique_id.upper() == technique_id.upper():
                return tech
        return None
    
    def search_mitre(self, keyword: str) -> List[MitreAttackTechnique]:
        """Search MITRE techniques by keyword"""
        keyword = keyword.lower()
        results = []
        
        for tech in self.mitre_techniques:
            if (keyword in tech.name.lower() or 
                keyword in tech.tactic.lower() or
                keyword in tech.description.lower()):
                results.append(tech)
        
        return results
    
    def format_mitre_technique(self, tech: MitreAttackTechnique) -> str:
        """Format a MITRE technique for display"""
        return f"""## {tech.technique_id}: {tech.name}

**Tactic:** {tech.tactic}

**Description:**
{tech.description}

**Detection:**
{tech.detection}

**Mitigation:**
{tech.mitigation}

🔗 Reference: https://attack.mitre.org/techniques/{tech.technique_id}/
"""
    
    def get_incident_template(self) -> str:
        """Get incident report template"""
        return INCIDENT_REPORT_TEMPLATE
    
    def get_vulnerability_template(self) -> str:
        """Get vulnerability report template"""
        return VULNERABILITY_REPORT_TEMPLATE
    
    def get_hardening_checklist(self, system_type: str = "general") -> str:
        """Get a hardening checklist"""
        checklists = {
            "general": """
# 🛡️ General Security Hardening Checklist

## System Configuration
- [ ] Disable unnecessary services and ports
- [ ] Remove default accounts and passwords
- [ ] Enable automatic security updates
- [ ] Configure host-based firewall
- [ ] Enable audit logging

## Access Control
- [ ] Implement least privilege principle
- [ ] Enable multi-factor authentication
- [ ] Set strong password policies
- [ ] Review and remove stale accounts
- [ ] Disable local admin accounts (use PAM)

## Network Security
- [ ] Segment networks appropriately
- [ ] Enable encryption in transit (TLS 1.2+)
- [ ] Configure DNS security (DNSSEC, DoH)
- [ ] Block unnecessary outbound traffic
- [ ] Monitor network traffic

## Endpoint Protection
- [ ] Deploy EDR/antivirus solution
- [ ] Enable application whitelisting
- [ ] Configure browser security settings
- [ ] Disable macros in Office documents
- [ ] Enable full disk encryption

## Monitoring & Detection
- [ ] Forward logs to SIEM
- [ ] Enable command-line logging
- [ ] Configure file integrity monitoring
- [ ] Set up alerting for critical events
- [ ] Perform regular vulnerability scans
""",
            "linux": """
# 🐧 Linux Hardening Checklist

## System
- [ ] Keep system updated: `apt update && apt upgrade` or `yum update`
- [ ] Disable root SSH login: `PermitRootLogin no` in /etc/ssh/sshd_config
- [ ] Use SSH keys, disable password auth
- [ ] Configure firewall: `ufw` or `firewalld`
- [ ] Enable SELinux/AppArmor

## Users & Access
- [ ] Remove unnecessary users
- [ ] Set password aging: `/etc/login.defs`
- [ ] Configure sudo properly, avoid NOPASSWD
- [ ] Use PAM for authentication

## Services
- [ ] Disable unused services: `systemctl disable <service>`
- [ ] Review listening ports: `ss -tulnp`
- [ ] Configure fail2ban for SSH

## Logging
- [ ] Enable auditd
- [ ] Configure log rotation
- [ ] Forward logs to central server
- [ ] Monitor auth logs: `/var/log/auth.log`
""",
            "windows": """
# 🪟 Windows Hardening Checklist

## System
- [ ] Enable Windows Update
- [ ] Configure Windows Firewall
- [ ] Enable BitLocker
- [ ] Disable SMBv1
- [ ] Enable Credential Guard (if supported)

## Users & Access
- [ ] Disable local Administrator account
- [ ] Use LAPS for local admin passwords
- [ ] Configure account lockout policy
- [ ] Enable MFA where possible

## Logging
- [ ] Enable PowerShell Script Block Logging
- [ ] Enable command-line auditing
- [ ] Configure Windows Event Forwarding
- [ ] Enable Sysmon

## Group Policy
- [ ] Block macros in Office
- [ ] Disable WScript/CScript
- [ ] Enable ASR rules
- [ ] Configure AppLocker/WDAC
"""
        }
        
        return checklists.get(system_type.lower(), checklists["general"])


# Global instance
knowledge_base = KnowledgeBase()