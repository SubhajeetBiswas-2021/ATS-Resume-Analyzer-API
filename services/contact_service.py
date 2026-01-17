# import re
# import logging
# from typing import Tuple, List, Dict

# logger = logging.getLogger(__name__)


# class ContactInfoChecker:
#     """Check for essential contact information in resume."""
    
#     def __init__(self):
#         self.max_score = 15
        
#         # Regex patterns
#         self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
#         self.linkedin_pattern = r'linkedin\.com/in/[\w-]+'
#         self.github_pattern = r'github\.com/[\w-]+'
    
#     def check(self, text: str) -> Dict:
#         """
#         Check contact information in resume.
        
#         Returns:
#             Dictionary with score, issues, and found contact info
#         """
#         score = self.max_score
#         issues = []
#         found = {
#             'has_email': False,
#             'has_phone': False,
#             'has_linkedin': False,
#             'has_github': False
#         }
        
#         # Check email
#         email_match = re.search(self.email_pattern, text)
#         if email_match:
#             found['has_email'] = True
#             found['email'] = email_match.group()
#             logger.info(f"Email found: {email_match.group()}")
#         else:
#             score -= 5
#             issues.append("Email address is missing - Critical for ATS")
        
#         # Check phone
#         phone_match = re.search(self.phone_pattern, text)
#         if phone_match:
#             found['has_phone'] = True
#             found['phone'] = phone_match.group()
#             logger.info(f"Phone found: {phone_match.group()}")
#         else:
#             score -= 5
#             issues.append("Phone number is missing - Critical for ATS")
        
#         # Check LinkedIn (optional but recommended)
#         if re.search(self.linkedin_pattern, text, re.IGNORECASE):
#             found['has_linkedin'] = True
#             logger.info("LinkedIn profile found")
#         else:
#             score -= 3
#             issues.append("LinkedIn profile missing - Highly recommended")
        
#         # Check GitHub (optional, good for tech roles)
#         if re.search(self.github_pattern, text, re.IGNORECASE):
#             found['has_github'] = True
#             logger.info("GitHub profile found")
#         else:
#             score -= 2
#             issues.append("GitHub profile missing - Recommended for tech roles")
        
#         return {
#             'score': max(0, score),
#             'max_score': self.max_score,
#             'percentage': round((max(0, score) / self.max_score) * 100, 2),
#             'issues': issues,
#             'found': found
#         }




import re 
import logging
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)


class ContactInfoChecker:
    """Check for essential contact information in resume."""
    
    def __init__(self):
        self.max_score = 15
        
        # Regex patterns
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
        self.github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
    
    def check(self, text: str) -> Dict:
        """
        Check contact information in resume.
        
        Returns:
            Dictionary with score, issues, warnings, and found contact info
        """
        score = self.max_score
        issues = []
        warnings = []
        found = {
            'has_email': False,
            'has_phone': False,
            'has_linkedin': False,
            'has_github': False,
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None
        }
        
        # Check email
        email_match = re.search(self.email_pattern, text)
        if email_match:
            found['has_email'] = True
            found['email'] = email_match.group()
            logger.info(f"Email found: {email_match.group()}")
        else:
            points = 5
            score -= points
            message = "Email address is missing - Critical for ATS"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        # Check phone
        phone_match = re.search(self.phone_pattern, text)
        if phone_match:
            found['has_phone'] = True
            found['phone'] = phone_match.group()
            logger.info(f"Phone found: {phone_match.group()}")
        else:
            points = 5
            score -= points
            message = "Phone number is missing - Critical for ATS"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        # Check LinkedIn (optional but recommended)
        linkedin_match = re.search(self.linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            found['has_linkedin'] = True
            found['linkedin'] = linkedin_match.group()
            logger.info(f"LinkedIn profile found: {linkedin_match.group()}")
        else:
            points = 3
            score -= points
            message = "LinkedIn profile missing - Highly recommended"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        # Check GitHub (optional, good for tech roles)
        github_match = re.search(self.github_pattern, text, re.IGNORECASE)
        if github_match:
            found['has_github'] = True
            found['github'] = github_match.group()
            logger.info(f"GitHub profile found: {github_match.group()}")
        else:
            points = 2
            score -= points
            message = "GitHub profile missing - Recommended for tech roles"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        return {
            'score': max(0, score),
            'max_score': self.max_score,
            'percentage': round((max(0, score) / self.max_score) * 100, 2),
            'issues': issues,
            'warnings': warnings,
            'found': found
        }