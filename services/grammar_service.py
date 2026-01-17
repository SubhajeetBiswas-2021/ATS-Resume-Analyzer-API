# import re
# import logging
# from typing import Dict, List, Set
# from spellchecker import SpellChecker

# logger = logging.getLogger(__name__)


# class GrammarChecker:
#     """Check spelling and basic grammar with intelligent filtering."""
    
#     def __init__(self):
#         self.max_score = 10
#         self.spell = SpellChecker()
        
#         # Build comprehensive whitelist
#         self.whitelist = self._build_whitelist()
#         self.spell.word_frequency.load_words(self.whitelist)
    
#     def _build_whitelist(self) -> Set[str]:
#         """Build comprehensive whitelist of technical and domain terms."""
#         return {
#             # Programming languages
#             'python', 'java', 'javascript', 'typescript', 'kotlin', 'swift',
#             'cpp', 'csharp', 'golang', 'rust', 'ruby', 'php', 'scala', 'dart',
#             'objective', 'perl', 'matlab',
            
#             # Frameworks & Libraries
#             'react', 'angular', 'vue', 'vuejs', 'django', 'flask', 'fastapi', 
#             'spring', 'springboot', 'nodejs', 'express', 'expressjs', 'nestjs', 
#             'laravel', 'dotnet', 'pytorch', 'tensorflow', 'keras', 'pandas', 
#             'numpy', 'scikit', 'jquery', 'redux', 'mobx', 'nextjs', 'svelte',
            
#             # Mobile & UI
#             'android', 'ios', 'swiftui', 'uikit', 'jetpack', 'compose',
#             'flutter', 'reactnative', 'ionic', 'xamarin', 'coroutines', 'rxjava',
            
#             # Databases
#             'mongodb', 'postgresql', 'mysql', 'redis', 'sqlite', 'firebase',
#             'firestore', 'dynamodb', 'cassandra', 'elasticsearch', 'neo4j',
#             'oracle', 'mariadb', 'couchdb',
            
#             # Cloud & DevOps
#             'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
#             'ansible', 'jenkins', 'gitlab', 'github', 'bitbucket', 'circleci',
#             'travis', 'heroku', 'vercel', 'netlify', 'cloudflare',
            
#             # Cloud Services
#             'ec2', 's3', 'lambda', 'cloudfront', 'vpc', 'ecs', 'fargate',
#             'cloudwatch', 'dynamodb', 'rds', 'sqs', 'sns',
            
#             # Tools & Technologies
#             'git', 'jira', 'confluence', 'slack', 'trello', 'postman', 'vscode',
#             'intellij', 'figma', 'sketch', 'photoshop', 'illustrator', 'xcode',
#             'androidstudio', 'webstorm', 'pycharm',
            
#             # Protocols & Formats
#             'json', 'xml', 'yaml', 'yml', 'html', 'css', 'scss', 'sass',
#             'http', 'https', 'smtp', 'ftp', 'ssh', 'tcp', 'udp', 'websocket',
#             'graphql', 'grpc', 'soap', 'rest', 'restful',
            
#             # Concepts & Methodologies
#             'api', 'apis', 'microservices', 'devops', 'cicd', 'agile', 'scrum',
#             'kanban', 'mvvm', 'mvc', 'oop', 'tdd', 'bdd', 'oauth', 'jwt',
#             'frontend', 'backend', 'fullstack', 'nosql', 'sql',
            
#             # Testing
#             'junit', 'testng', 'pytest', 'jest', 'mocha', 'chai', 'selenium',
#             'cypress', 'playwright', 'appium', 'jmeter', 'loadrunner',
            
#             # Big Data & ML
#             'hadoop', 'spark', 'kafka', 'airflow', 'luigi', 'opencv', 'nltk',
#             'spacy', 'huggingface', 'sklearn', 'matplotlib', 'seaborn',
            
#             # Common Resume Terms
#             'btech', 'bsc', 'msc', 'mba', 'phd', 'cgpa', 'gpa', 'cgpa',
#             'internship', 'freelance', 'opensource', 'github', 'portfolio',
#             'certifications', 'workflows', 'webapp', 'website', 'app',
            
#             # Common Abbreviations & Months
#             'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep',
#             'oct', 'nov', 'dec', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
#             'am', 'pm', 'ui', 'ux', 'pdf', 'png', 'jpg', 'jpeg', 'svg', 'gif',
#             'mp4', 'www', 'url', 'gmail', 'hotmail', 'yahoo', 'outlook',
#             'linkedin', 'stackoverflow', 'reddit', 'twitter', 'facebook',
            
#             # Companies (Common)
#             'google', 'microsoft', 'amazon', 'meta', 'facebook', 'apple',
#             'netflix', 'uber', 'airbnb', 'spotify', 'adobe', 'salesforce',
#             'oracle', 'ibm', 'intel', 'nvidia', 'tesla', 'spacex',
            
#             # Additional technical terms
#             'gameplay', 'api', 'ui', 'ux', 'sdk', 'ide', 'cli', 'gui',
#             'cdn', 'dns', 'ssl', 'tls', 'vpn', 'lan', 'wan', 'wifi',
#             'bluetooth', 'nfc', 'gps', 'ar', 'vr', 'iot', 'ml', 'ai',
#             'nlp', 'cv', 'dl', 'cnn', 'rnn', 'lstm', 'gan',
#         }
    
#     def _is_likely_proper_noun(self, word: str, context: str) -> bool:
#         """Check if a word is likely a proper noun based on context."""
#         # Check if word is capitalized in original text
#         pattern = r'\b' + re.escape(word.capitalize()) + r'\b'
#         if re.search(pattern, context):
#             return True
        
#         # Check if word appears after common titles
#         title_pattern = r'\b(Mr|Mrs|Ms|Dr|Prof|Sir)\s+' + re.escape(word) + r'\b'
#         if re.search(title_pattern, context, re.IGNORECASE):
#             return True
        
#         # Check if word is part of a company/institution name pattern
#         # (often followed by Company, Inc, Corp, University, College, etc.)
#         org_pattern = r'\b' + re.escape(word) + r'\s+(Company|Inc|Corp|Ltd|University|College|Institute|School)\b'
#         if re.search(org_pattern, context, re.IGNORECASE):
#             return True
        
#         return False
    
#     def _is_acronym_or_abbreviation(self, word: str) -> bool:
#         """Check if word is likely an acronym or abbreviation."""
#         # All uppercase and short (2-6 chars)
#         if word.isupper() and 2 <= len(word) <= 6:
#             return True
        
#         # Mixed case acronym (like PhD, iOS)
#         if len(word) <= 6 and sum(1 for c in word if c.isupper()) >= 2:
#             return True
        
#         return False
    
#     def _extract_meaningful_words(self, text: str) -> tuple[List[str], str]:
#         """Extract words that should be spell-checked, return cleaned text too."""
#         original_text = text
        
#         # Remove URLs
#         text = re.sub(r'http\S+|www\.\S+', ' ', text)
        
#         # Remove email addresses
#         text = re.sub(r'\S+@\S+', ' ', text)
        
#         # Remove file paths
#         text = re.sub(r'[A-Za-z]:\\[\S]+', ' ', text)
#         text = re.sub(r'/[\w/.-]+', ' ', text)
        
#         # Remove phone numbers
#         text = re.sub(r'\+?\d[\d\s\-()]{7,}', ' ', text)
        
#         # Remove dates and numbers
#         text = re.sub(r'\b\d+[\d\s\-/.,]*\b', ' ', text)
        
#         # Remove common resume section headers (case insensitive)
#         section_headers = [
#             'education', 'experience', 'skills', 'projects', 'certifications',
#             'achievements', 'summary', 'objective', 'profile', 'work experience',
#             'professional experience', 'technical skills', 'soft skills'
#         ]
#         for header in section_headers:
#             text = re.sub(r'\b' + header + r'\b', ' ', text, flags=re.IGNORECASE)
        
#         # Extract words (minimum 3 characters, allow hyphens)
#         words = re.findall(r'\b[a-zA-Z][a-zA-Z\-]{2,}\b', text)
        
#         # Filter words
#         filtered_words = []
#         for word in words:
#             word_lower = word.lower().strip('-')
            
#             # Skip if in whitelist
#             if word_lower in self.whitelist:
#                 continue
            
#             # Skip if likely proper noun
#             if self._is_likely_proper_noun(word, original_text):
#                 continue
            
#             # Skip if acronym/abbreviation
#             if self._is_acronym_or_abbreviation(word):
#                 continue
            
#             # Skip if looks like a version number or code
#             if re.search(r'[0-9]|v\d|\d+x|\dx\d', word_lower):
#                 continue
            
#             filtered_words.append(word_lower)
        
#         return filtered_words, original_text
    
#     def _is_contextually_correct(self, word: str, suggestions: List[str]) -> bool:
#         """Check if the word might be correct in a resume context."""
#         # If the top suggestion is very different from the original word,
#         # it might be a proper noun or technical term we don't know
#         if not suggestions:
#             return True
        
#         top_suggestion = suggestions[0]
        
#         # Calculate simple similarity (common prefix length)
#         common_prefix = 0
#         for i in range(min(len(word), len(top_suggestion))):
#             if word[i] == top_suggestion[i]:
#                 common_prefix += 1
#             else:
#                 break
        
#         similarity = common_prefix / max(len(word), len(top_suggestion))
        
#         # If similarity is very low, likely a proper noun
#         if similarity < 0.3:
#             return True
        
#         return False
    
#     def check(self, text: str) -> Dict:
#         """
#         Check spelling in resume text with intelligent filtering.
        
#         Returns:
#             Dictionary with score and spelling issues
#         """
#         issues = []
        
#         # Extract words to check
#         words, original_text = self._extract_meaningful_words(text)
        
#         if not words:
#             logger.info("No words to check after filtering")
#             return {
#                 'score': self.max_score,
#                 'max_score': self.max_score,
#                 'percentage': 100.0,
#                 'issues': [],
#                 'spelling_errors': []
#             }
        
#         # Find misspelled words
#         misspelled = self.spell.unknown(words)
        
#         # Further filter misspelled words
#         genuine_errors = []
#         for word in misspelled:
#             # Get correction suggestions
#             candidates = self.spell.candidates(word)
#             suggestions = list(candidates)[:3] if candidates else []
            
#             # Skip if suggestions don't make sense
#             if not suggestions or suggestions[0] == word:
#                 continue
            
#             # Skip if contextually might be correct
#             if self._is_contextually_correct(word, suggestions):
#                 continue
            
#             genuine_errors.append({
#                 'word': word,
#                 'suggestions': suggestions
#             })
        
#         # Limit to first 8 unique errors
#         spelling_errors = genuine_errors[:8]
#         error_count = len(spelling_errors)
        
#         # Calculate score based on improved logic
#         if error_count == 0:
#             score = self.max_score
#         elif error_count <= 2:
#             score = self.max_score  # No penalty for 1-2 minor errors
#             issues.append(f"Found {error_count} potential spelling error(s) - please review")
#         elif error_count <= 5:
#             score = self.max_score - 2  # Minor penalty
#             issues.append(f"Found {error_count} spelling errors - review carefully")
#         else:
#             score = self.max_score - 3  # Max 3 points deduction
#             issues.append(f"Found {error_count} spelling errors - proofreading recommended")
        
#         logger.info(f"Spelling check: {error_count} genuine errors found, score: {score}/{self.max_score}")
        
#         return {
#             'score': max(0, score),
#             'max_score': self.max_score,
#             'percentage': round((max(0, score) / self.max_score) * 100, 2),
#             'issues': issues,
#             'spelling_errors': spelling_errors
#         }




import re 
import logging
from typing import Dict, List, Set
from spellchecker import SpellChecker

logger = logging.getLogger(__name__)


class GrammarChecker:
    """Check spelling and basic grammar with intelligent filtering."""
    
    def __init__(self):
        self.max_score = 10
        self.spell = SpellChecker()
        
        # Build comprehensive whitelist
        self.whitelist = self._build_whitelist()
        self.spell.word_frequency.load_words(self.whitelist)
    
    def _build_whitelist(self) -> Set[str]:
        """Build comprehensive whitelist of technical and domain terms."""
        return {
            # Programming languages
            'python', 'java', 'javascript', 'typescript', 'kotlin', 'swift',
            'cpp', 'csharp', 'golang', 'rust', 'ruby', 'php', 'scala', 'dart',
            'objective', 'perl', 'matlab',
            
            # Frameworks & Libraries
            'react', 'angular', 'vue', 'vuejs', 'django', 'flask', 'fastapi', 
            'spring', 'springboot', 'nodejs', 'express', 'expressjs', 'nestjs', 
            'laravel', 'dotnet', 'pytorch', 'tensorflow', 'keras', 'pandas', 
            'numpy', 'scikit', 'jquery', 'redux', 'mobx', 'nextjs', 'svelte',
            
            # Mobile & UI
            'android', 'ios', 'swiftui', 'uikit', 'jetpack', 'compose',
            'flutter', 'reactnative', 'ionic', 'xamarin', 'coroutines', 'rxjava',
            
            # Databases
            'mongodb', 'postgresql', 'mysql', 'redis', 'sqlite', 'firebase',
            'firestore', 'dynamodb', 'cassandra', 'elasticsearch', 'neo4j',
            'oracle', 'mariadb', 'couchdb',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'ansible', 'jenkins', 'gitlab', 'github', 'bitbucket', 'circleci',
            'travis', 'heroku', 'vercel', 'netlify', 'cloudflare',
            
            # Cloud Services
            'ec2', 's3', 'lambda', 'cloudfront', 'vpc', 'ecs', 'fargate',
            'cloudwatch', 'dynamodb', 'rds', 'sqs', 'sns',
            
            # Tools & Technologies
            'git', 'jira', 'confluence', 'slack', 'trello', 'postman', 'vscode',
            'intellij', 'figma', 'sketch', 'photoshop', 'illustrator', 'xcode',
            'androidstudio', 'webstorm', 'pycharm',
            
            # Protocols & Formats
            'json', 'xml', 'yaml', 'yml', 'html', 'css', 'scss', 'sass',
            'http', 'https', 'smtp', 'ftp', 'ssh', 'tcp', 'udp', 'websocket',
            'graphql', 'grpc', 'soap', 'rest', 'restful',
            
            # Concepts & Methodologies
            'api', 'apis', 'microservices', 'devops', 'cicd', 'agile', 'scrum',
            'kanban', 'mvvm', 'mvc', 'oop', 'tdd', 'bdd', 'oauth', 'jwt',
            'frontend', 'backend', 'fullstack', 'nosql', 'sql',
            
            # Testing
            'junit', 'testng', 'pytest', 'jest', 'mocha', 'chai', 'selenium',
            'cypress', 'playwright', 'appium', 'jmeter', 'loadrunner',
            
            # Big Data & ML
            'hadoop', 'spark', 'kafka', 'airflow', 'luigi', 'opencv', 'nltk',
            'spacy', 'huggingface', 'sklearn', 'matplotlib', 'seaborn',
            
            # Common Resume Terms
            'btech', 'bsc', 'msc', 'mba', 'phd', 'cgpa', 'gpa', 'cgpa',
            'internship', 'freelance', 'opensource', 'github', 'portfolio',
            'certifications', 'workflows', 'webapp', 'website', 'app',
            
            # Common Abbreviations & Months
            'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep',
            'oct', 'nov', 'dec', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
            'am', 'pm', 'ui', 'ux', 'pdf', 'png', 'jpg', 'jpeg', 'svg', 'gif',
            'mp4', 'www', 'url', 'gmail', 'hotmail', 'yahoo', 'outlook',
            'linkedin', 'stackoverflow', 'reddit', 'twitter', 'facebook',
            
            # Companies (Common)
            'google', 'microsoft', 'amazon', 'meta', 'facebook', 'apple',
            'netflix', 'uber', 'airbnb', 'spotify', 'adobe', 'salesforce',
            'oracle', 'ibm', 'intel', 'nvidia', 'tesla', 'spacex',
            
            # Additional technical terms
            'gameplay', 'api', 'ui', 'ux', 'sdk', 'ide', 'cli', 'gui',
            'cdn', 'dns', 'ssl', 'tls', 'vpn', 'lan', 'wan', 'wifi',
            'bluetooth', 'nfc', 'gps', 'ar', 'vr', 'iot', 'ml', 'ai',
            'nlp', 'cv', 'dl', 'cnn', 'rnn', 'lstm', 'gan',
        }
    
    def _is_likely_proper_noun(self, word: str, context: str) -> bool:
        """Check if a word is likely a proper noun based on context."""
        # Check if word is capitalized in original text
        pattern = r'\b' + re.escape(word.capitalize()) + r'\b'
        if re.search(pattern, context):
            return True
        
        # Check if word appears after common titles
        title_pattern = r'\b(Mr|Mrs|Ms|Dr|Prof|Sir)\s+' + re.escape(word) + r'\b'
        if re.search(title_pattern, context, re.IGNORECASE):
            return True
        
        # Check if word is part of a company/institution name pattern
        # (often followed by Company, Inc, Corp, University, College, etc.)
        org_pattern = r'\b' + re.escape(word) + r'\s+(Company|Inc|Corp|Ltd|University|College|Institute|School)\b'
        if re.search(org_pattern, context, re.IGNORECASE):
            return True
        
        return False
    
    def _is_acronym_or_abbreviation(self, word: str) -> bool:
        """Check if word is likely an acronym or abbreviation."""
        # All uppercase and short (2-6 chars)
        if word.isupper() and 2 <= len(word) <= 6:
            return True
        
        # Mixed case acronym (like PhD, iOS)
        if len(word) <= 6 and sum(1 for c in word if c.isupper()) >= 2:
            return True
        
        return False
    
    def _extract_meaningful_words(self, text: str) -> tuple[List[str], str]:
        """Extract words that should be spell-checked, return cleaned text too."""
        original_text = text
        
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', ' ', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # Remove file paths
        text = re.sub(r'[A-Za-z]:\\[\S]+', ' ', text)
        text = re.sub(r'/[\w/.-]+', ' ', text)
        
        # Remove phone numbers
        text = re.sub(r'\+?\d[\d\s\-()]{7,}', ' ', text)
        
        # Remove dates and numbers
        text = re.sub(r'\b\d+[\d\s\-/.,]*\b', ' ', text)
        
        # Remove common resume section headers (case insensitive)
        section_headers = [
            'education', 'experience', 'skills', 'projects', 'certifications',
            'achievements', 'summary', 'objective', 'profile', 'work experience',
            'professional experience', 'technical skills', 'soft skills'
        ]
        for header in section_headers:
            text = re.sub(r'\b' + header + r'\b', ' ', text, flags=re.IGNORECASE)
        
        # Extract words (minimum 3 characters, allow hyphens)
        words = re.findall(r'\b[a-zA-Z][a-zA-Z\-]{2,}\b', text)
        
        # Filter words
        filtered_words = []
        for word in words:
            word_lower = word.lower().strip('-')
            
            # Skip if in whitelist
            if word_lower in self.whitelist:
                continue
            
            # Skip if likely proper noun
            if self._is_likely_proper_noun(word, original_text):
                continue
            
            # Skip if acronym/abbreviation
            if self._is_acronym_or_abbreviation(word):
                continue
            
            # Skip if looks like a version number or code
            if re.search(r'[0-9]|v\d|\d+x|\dx\d', word_lower):
                continue
            
            filtered_words.append(word_lower)
        
        return filtered_words, original_text
    
    def _is_contextually_correct(self, word: str, suggestions: List[str]) -> bool:
        """Check if the word might be correct in a resume context."""
        # If the top suggestion is very different from the original word,
        # it might be a proper noun or technical term we don't know
        if not suggestions:
            return True
        
        top_suggestion = suggestions[0]
        
        # Calculate simple similarity (common prefix length)
        common_prefix = 0
        for i in range(min(len(word), len(top_suggestion))):
            if word[i] == top_suggestion[i]:
                common_prefix += 1
            else:
                break
        
        similarity = common_prefix / max(len(word), len(top_suggestion))
        
        # If similarity is very low, likely a proper noun
        if similarity < 0.3:
            return True
        
        return False
    
    def check(self, text: str) -> Dict:
        """
        Check spelling in resume text with intelligent filtering.
        
        Returns:
            Dictionary with score, warnings, and spelling issues
        """
        issues = []
        warnings = []
        
        # Extract words to check
        words, original_text = self._extract_meaningful_words(text)
        
        if not words:
            logger.info("No words to check after filtering")
            return {
                'score': self.max_score,
                'max_score': self.max_score,
                'percentage': 100.0,
                'issues': [],
                'warnings': [],
                'spelling_errors': []
            }
        
        # Find misspelled words
        misspelled = self.spell.unknown(words)
        
        # Further filter misspelled words
        genuine_errors = []
        for word in misspelled:
            # Get correction suggestions
            candidates = self.spell.candidates(word)
            suggestions = list(candidates)[:3] if candidates else []
            
            # Skip if suggestions don't make sense
            if not suggestions or suggestions[0] == word:
                continue
            
            # Skip if contextually might be correct
            if self._is_contextually_correct(word, suggestions):
                continue
            
            genuine_errors.append({
                'word': word,
                'suggestions': suggestions
            })
        
        # Limit to first 8 unique errors
        spelling_errors = genuine_errors[:8]
        error_count = len(spelling_errors)
        
        # Calculate score based on improved logic
        if error_count == 0:
            score = self.max_score
        elif error_count <= 2:
            points = 0
            score = self.max_score  # No penalty for 1-2 minor errors
            message = f"Found {error_count} potential spelling error(s) - please review"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        elif error_count <= 5:
            points = 2
            score = self.max_score - points  # Minor penalty
            message = f"Found {error_count} spelling errors - review carefully"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        else:
            points = 3
            score = self.max_score - points  # Max 3 points deduction
            message = f"Found {error_count} spelling errors - proofreading recommended"
            issues.append(message)
            warnings.append({"message": message, "points_deducted": points})
        
        logger.info(f"Spelling check: {error_count} genuine errors found, score: {score}/{self.max_score}")
        
        return {
            'score': max(0, score),
            'max_score': self.max_score,
            'percentage': round((max(0, score) / self.max_score) * 100, 2),
            'issues': issues,
            'warnings': warnings,
            'spelling_errors': spelling_errors
        }