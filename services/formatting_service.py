# import re
# import logging
# from typing import Dict, List

# logger = logging.getLogger(__name__)


# class FormattingChecker:
#     """Check resume formatting and structure for ATS compatibility."""
    
#     def __init__(self):
#         self.max_score = 25
        
#         # Common section headers (case-insensitive)
#         self.required_sections = {
#             'education': ['education', 'academic', 'qualification'],
#             'experience': ['experience', 'work history', 'employment', 'professional experience'],
#             'skills': ['skills', 'technical skills', 'core competencies', 'expertise'],
#             'projects': ['projects', 'project work', 'key projects']
#         }
    
#     def check(self, text: str) -> Dict:
#         """
#         Check resume formatting and structure.
        
#         Returns:
#             Dictionary with score, issues, and found sections
#         """
#         score = self.max_score
#         issues = []
#         found_sections = []
#         text_lower = text.lower()
        
#         # Check for required sections
#         # Education
#         if any(keyword in text_lower for keyword in self.required_sections['education']):
#             found_sections.append('Education')
#             logger.info("Education section found")
#         else:
#             score -= 7
#             issues.append("Education section missing - Critical for ATS")
        
#         # Experience or Projects (at least one should exist)
#         has_experience = any(keyword in text_lower for keyword in self.required_sections['experience'])
#         has_projects = any(keyword in text_lower for keyword in self.required_sections['projects'])
        
#         if has_experience:
#             found_sections.append('Experience')
#             logger.info("Experience section found")
#         if has_projects:
#             found_sections.append('Projects')
#             logger.info("Projects section found")
        
#         if not has_experience and not has_projects:
#             score -= 8
#             issues.append("Neither Experience nor Projects section found - Critical for ATS")
        
#         # Skills section
#         if any(keyword in text_lower for keyword in self.required_sections['skills']):
#             found_sections.append('Skills')
#             logger.info("Skills section found")
#         else:
#             score -= 6
#             issues.append("Skills section missing - Critical for ATS")
        
#         # Check for bullet points (indicators: •, *, -, →)
#         bullet_patterns = [r'[•\*\-→]', r'^\s*[\d]+\.', r'^\s*[a-z]\)']
#         has_bullets = any(re.search(pattern, text, re.MULTILINE) for pattern in bullet_patterns)
        
#         if not has_bullets:
#             score -= 2
#             issues.append("No bullet points detected - Use bullets for better ATS parsing")
#         else:
#             logger.info("Bullet points detected")
        
#         # Check for dates (indicates timeline/chronology)
#         date_patterns = [
#             r'\b(19|20)\d{2}\b',  # Years like 2020, 2021
#             r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(19|20)\d{2}\b',  # Jan 2020
#             r'\b\d{1,2}/\d{4}\b'  # 01/2020
#         ]
#         has_dates = any(re.search(pattern, text, re.IGNORECASE) for pattern in date_patterns)
        
#         if not has_dates:
#             score -= 2
#             issues.append("No dates found - Include timeline for experience/education")
#         else:
#             logger.info("Timeline dates detected")
        
#         return {
#             'score': max(0, score),
#             'max_score': self.max_score,
#             'percentage': round((max(0, score) / self.max_score) * 100, 2),
#             'issues': issues,
#             'sections_found': found_sections
#         }






import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class FormattingChecker:
    """Check resume formatting and structure for ATS compatibility."""
    
    def __init__(self):
        self.max_score = 25
        
        # Common section headers (case-insensitive)
        self.required_sections = {
            'education': ['education', 'academic', 'qualification'],
            'experience': ['experience', 'work history', 'employment', 'professional experience'],
            'skills': ['skills', 'technical skills', 'core competencies', 'expertise'],
            'projects': ['projects', 'project work', 'key projects']
        }
    
    def check(self, text: str) -> Dict:
        """
        Check resume formatting and structure.
        
        Returns:
            Dictionary with score, issues, warnings, and found sections
        """
        score = self.max_score
        issues = []
        warnings = []
        found_sections = []
        text_lower = text.lower()
        
        # Check for required sections
        # Education
        if any(keyword in text_lower for keyword in self.required_sections['education']):
            found_sections.append('Education')
            logger.info("Education section found")
        else:
            points = 7
            score -= points
            message = "Education section missing - Critical for ATS"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        # Experience or Projects (at least one should exist)
        has_experience = any(keyword in text_lower for keyword in self.required_sections['experience'])
        has_projects = any(keyword in text_lower for keyword in self.required_sections['projects'])
        
        if has_experience:
            found_sections.append('Experience')
            logger.info("Experience section found")
        if has_projects:
            found_sections.append('Projects')
            logger.info("Projects section found")
        
        if not has_experience and not has_projects:
            points = 8
            score -= points
            message = "Neither Experience nor Projects section found - Critical for ATS"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        # Skills section
        if any(keyword in text_lower for keyword in self.required_sections['skills']):
            found_sections.append('Skills')
            logger.info("Skills section found")
        else:
            points = 6
            score -= points
            message = "Skills section missing - Critical for ATS"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        # Check for bullet points (indicators: •, *, -, →)
        bullet_patterns = [r'[•\*\-→]', r'^\s*[\d]+\.', r'^\s*[a-z]\)']
        has_bullets = any(re.search(pattern, text, re.MULTILINE) for pattern in bullet_patterns)
        
        if not has_bullets:
            points = 2
            score -= points
            message = "No bullet points detected - Use bullets for better ATS parsing"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        else:
            logger.info("Bullet points detected")
        
        # Check for dates (indicates timeline/chronology)
        date_patterns = [
            r'\b(19|20)\d{2}\b',  # Years like 2020, 2021
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(19|20)\d{2}\b',  # Jan 2020
            r'\b\d{1,2}/\d{4}\b'  # 01/2020
        ]
        has_dates = any(re.search(pattern, text, re.IGNORECASE) for pattern in date_patterns)
        
        if not has_dates:
            points = 2
            score -= points
            message = "No dates found - Include timeline for experience/education"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        else:
            logger.info("Timeline dates detected")
        
        return {
            'score': max(0, score),
            'max_score': self.max_score,
            'percentage': round((max(0, score) / self.max_score) * 100, 2),
            'issues': issues,
            'warnings': warnings,
            'sections_found': found_sections
        }