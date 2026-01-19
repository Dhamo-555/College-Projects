"""
Spider Cybersecurity Tutor - Safety Module
Content filtering and safety checks
"""

import re
from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class SafetyCheck:
    """Result of a safety check"""
    is_safe: bool
    reason: str
    suggestion: str


# Patterns that indicate potentially harmful requests
HARMFUL_PATTERNS = [
    # Exploitation
    (r'\b(write|create|give|provide|show).{0,20}(exploit|payload|shellcode)\b', 
     "exploit/payload creation"),
    (r'\b(reverse|bind).{0,10}shell\b', 
     "reverse/bind shell creation"),
    (r'\bhow\s+to\s+(hack|exploit|breach|break\s+into)\b', 
     "intrusion guidance"),
    
    # Malware
    (r'\b(write|create|give|provide).{0,20}(malware|virus|trojan|ransomware|keylogger|rootkit)\b',
     "malware creation"),
    (r'\bmalware.{0,15}(code|source|script)\b',
     "malware code request"),
    
    # Credential attacks
    (r'\b(crack|brute\s*force|steal).{0,15}(password|credential|hash)\b',
     "credential attacks"),
    (r'\bhash.{0,10}(crack|break)\b',
     "password hash cracking"),
    
    # Bypass/Evasion
    (r'\bbypass.{0,15}(authentication|firewall|antivirus|edr|security)\b',
     "security bypass"),
    (r'\b(evade|avoid).{0,15}(detection|antivirus|edr)\b',
     "detection evasion"),
    
    # Network attacks
    (r'\b(ddos|dos)\s*(attack|script|tool)\b',
     "denial of service"),
    (r'\bman.in.the.middle\s*(attack|how)\b',
     "MITM attack"),
    
    # SQL/Web attacks
    (r'\bsql\s*injection.{0,15}(payload|bypass|code)\b',
     "SQL injection payload"),
    (r'\bxss.{0,15}(payload|bypass|code)\b',
     "XSS payload"),
    
    # Unauthorized access
    (r'\b(without|no).{0,15}(permission|authorization|consent)\b',
     "unauthorized access"),
    (r'\baccess.{0,15}(someone|other|victim).{0,10}(account|system|network)\b',
     "unauthorized system access"),
]

# Defensive/educational keywords that might make harmful patterns acceptable
DEFENSIVE_CONTEXT = [
    r'\bdefend\b', r'\bdefense\b', r'\bdefensive\b',
    r'\bprotect\b', r'\bprotection\b',
    r'\bdetect\b', r'\bdetection\b',
    r'\bprevent\b', r'\bprevention\b',
    r'\bmitigate\b', r'\bmitigation\b',
    r'\bharden\b', r'\bhardening\b',
    r'\bsecure\b', r'\bsecuring\b',
    r'\blab\b', r'\btest\s*environment\b',
    r'\bauthorized\b', r'\bpermission\b',
    r'\bunderstand\b', r'\bhow\s*it\s*works\b',
    r'\bindicators?\b', r'\bioc\b',
    r'\bforensic\b', r'\banalysis\b',
]


class SafetyFilter:
    """Filters content for safety"""
    
    def __init__(self):
        self.harmful_patterns = [(re.compile(p, re.IGNORECASE), desc) 
                                  for p, desc in HARMFUL_PATTERNS]
        self.defensive_patterns = [re.compile(p, re.IGNORECASE) 
                                   for p in DEFENSIVE_CONTEXT]
    
    def check_input(self, text: str) -> SafetyCheck:
        """
        Check if user input is safe
        
        Args:
            text: User input to check
            
        Returns:
            SafetyCheck with result
        """
        text_lower = text.lower()
        
        # Check for harmful patterns
        for pattern, description in self.harmful_patterns:
            if pattern.search(text_lower):
                # Check if there's defensive context
                has_defensive_context = any(
                    dp.search(text_lower) for dp in self.defensive_patterns
                )
                
                if not has_defensive_context:
                    return SafetyCheck(
                        is_safe=False,
                        reason=f"Request appears to involve {description}",
                        suggestion=self._get_safe_alternative(description)
                    )
        
        return SafetyCheck(
            is_safe=True,
            reason="Input appears safe",
            suggestion=""
        )
    
    def _get_safe_alternative(self, topic: str) -> str:
        """Get a safe alternative suggestion for a blocked topic"""
        alternatives = {
            "exploit/payload creation": 
                "I can explain how exploits work conceptually, discuss CVE details, "
                "or help you set up detection for exploit attempts.",
            
            "reverse/bind shell creation":
                "I can explain what reverse shells are, how to detect them in network traffic, "
                "and how to harden systems against them.",
            
            "intrusion guidance":
                "I can help you understand attack techniques for defensive purposes, "
                "set up authorized penetration testing, or improve your security posture.",
            
            "malware creation":
                "I can explain malware behavior, help you analyze samples safely, "
                "or set up detection rules for malware indicators.",
            
            "credential attacks":
                "I can help you implement strong authentication, detect credential attacks, "
                "and set up password policies and monitoring.",
            
            "security bypass":
                "I can help you test your security controls legitimately, "
                "improve defense-in-depth, and detect bypass attempts.",
            
            "detection evasion":
                "I can help improve your detection capabilities, understand evasion techniques "
                "for better defense, and tune your security tools.",
            
            "denial of service":
                "I can help you protect against DoS attacks, set up rate limiting, "
                "and implement DDoS mitigation strategies.",
            
            "SQL injection payload":
                "I can help you understand SQL injection for defensive purposes, "
                "implement input validation, and set up WAF rules.",
            
            "XSS payload":
                "I can help you understand XSS for defensive purposes, "
                "implement CSP headers, and sanitize user input.",
            
            "unauthorized access":
                "I can only help with authorized security testing. "
                "I can assist with setting up proper authorization for pentests.",
        }
        
        for key, suggestion in alternatives.items():
            if key in topic:
                return suggestion
        
        return ("I can help you understand this topic from a defensive perspective, "
                "set up detection, or improve your security posture.")
    
    def get_safety_response(self, check: SafetyCheck) -> str:
        """Generate a helpful refusal response"""
        return f"""🛡️ **Safety Notice**

I can't help with requests that could enable {check.reason.lower()}.

**What I can help with instead:**
{check.suggestion}

**Safe alternatives:**
- Explain the technique at a conceptual level
- Set up detection and monitoring
- Implement defensive controls
- Practice in authorized lab environments
- Study for security certifications

Would you like me to help with any of these instead?"""


# Create global instance
safety_filter = SafetyFilter()


def check_safety(text: str) -> Tuple[bool, str]:
    """
    Quick safety check function
    
    Args:
        text: Text to check
        
    Returns:
        Tuple of (is_safe, message)
    """
    check = safety_filter.check_input(text)
    if check.is_safe:
        return True, ""
    return False, safety_filter.get_safety_response(check)