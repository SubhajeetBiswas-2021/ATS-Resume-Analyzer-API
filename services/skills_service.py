# import re
# import logging
# from typing import Dict, List, Set, Tuple

# logger = logging.getLogger(__name__)


# class SkillsAnalyzer:
#     """Analyze skills matching between resume and job description."""
    
#     def __init__(self):
#         self.max_score = 35
#         self.technical_skills_db = self._build_technical_skills_database()
        
#         # Common stop words to ignore when extracting general skills
#         self.stop_words = {
#             'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
#             'of', 'with', 'by', 'from', 'about', 'as', 'into', 'through', 'during',
#             'before', 'after', 'above', 'below', 'between', 'under', 'again',
#             'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
#             'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
#             'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
#             'will', 'just', 'should', 'now', 'work', 'working', 'experience',
#             'job', 'role', 'position', 'candidate', 'team', 'company', 'year',
#             'years', 'must', 'required', 'preferred', 'looking', 'seeking',
#             'able', 'ability', 'strong', 'good', 'excellent', 'great', 'best',
#             'well', 'including', 'using', 'across', 'within', 'around', 'along',
#             'including', 'plus', 'also', 'like', 'even', 'may', 'might', 'would',
#             'could', 'should', 'shall', 'need', 'want', 'like', 'make', 'get',
#             'take', 'go', 'come', 'see', 'know', 'think', 'use', 'find', 'give',
#             'tell', 'ask', 'feel', 'try', 'leave', 'call', 'keep', 'let', 'begin',
#             'seem', 'help', 'show', 'play', 'run', 'move', 'live', 'believe',
#             'hold', 'bring', 'happen', 'write', 'provide', 'sit', 'stand', 'lose',
#             'pay', 'meet', 'include', 'continue', 'set', 'learn', 'change', 'lead',
#             'understand', 'watch', 'follow', 'stop', 'create', 'speak', 'read',
#             'allow', 'add', 'spend', 'grow', 'open', 'walk', 'win', 'offer',
#             'remember', 'love', 'consider', 'appear', 'buy', 'wait', 'serve',
#             'die', 'send', 'expect', 'build', 'stay', 'fall', 'cut', 'reach',
#             'kill', 'remain', 'suggest', 'raise', 'pass', 'sell', 'require',
#             'report', 'decide', 'pull'
#         }
    
#     def _build_technical_skills_database(self) -> Dict[str, List[str]]:
#         """Build comprehensive technical skills database by category."""
#         return {
#             'programming_languages': [
#                 'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C',
#                 'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R',
#                 'MATLAB', 'Dart', 'Objective-C', 'Perl', 'Shell', 'Bash', 'PowerShell'
#             ],
#             'web_frontend': [
#                 'React', 'Angular', 'Vue.js', 'Next.js', 'Svelte', 'HTML', 'CSS',
#                 'SCSS', 'Sass', 'Bootstrap', 'Tailwind CSS', 'Material-UI', 'jQuery',
#                 'Redux', 'MobX', 'Webpack', 'Vite', 'Babel'
#             ],
#             'web_backend': [
#                 'Node.js', 'Express.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot',
#                 'Spring', 'ASP.NET', '.NET Core', 'Laravel', 'Ruby on Rails', 'Nest.js'
#             ],
#             'mobile': [
#                 'Android', 'iOS', 'React Native', 'Flutter', 'SwiftUI', 'UIKit',
#                 'Jetpack Compose', 'Kotlin Multiplatform', 'Xamarin', 'Ionic'
#             ],
#             'databases': [
#                 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
#                 'SQL Server', 'Cassandra', 'DynamoDB', 'Firebase', 'Firestore',
#                 'Elasticsearch', 'Neo4j', 'CouchDB'
#             ],
#             'cloud_devops': [
#                 'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes',
#                 'Terraform', 'Ansible', 'Jenkins', 'GitLab CI', 'GitHub Actions',
#                 'CircleCI', 'Travis CI', 'Heroku', 'Vercel', 'Netlify'
#             ],
#             'data_science_ml': [
#                 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy',
#                 'Matplotlib', 'Seaborn', 'Jupyter', 'Apache Spark', 'Hadoop',
#                 'Power BI', 'Tableau', 'OpenCV', 'NLTK', 'SpaCy', 'Hugging Face'
#             ],
#             'tools_technologies': [
#                 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN', 'Jira', 'Confluence',
#                 'Slack', 'Trello', 'Postman', 'Swagger', 'GraphQL', 'REST API',
#                 'gRPC', 'Microservices', 'OAuth', 'JWT', 'WebSocket'
#             ],
#             'concepts_methodologies': [
#                 'Agile', 'Scrum', 'Kanban', 'DevOps', 'CI/CD', 'TDD', 'BDD',
#                 'Microservices', 'RESTful', 'MVC', 'MVVM', 'OOP', 'Design Patterns',
#                 'System Design', 'Data Structures', 'Algorithms'
#             ],
#             'testing': [
#                 'JUnit', 'TestNG', 'Pytest', 'Jest', 'Mocha', 'Chai', 'Selenium',
#                 'Cypress', 'Playwright', 'Appium', 'Postman', 'JMeter', 'LoadRunner'
#             ]
#         }
    
#     def _extract_technical_skills(self, text: str) -> Set[str]:
#         """Extract technical skills from predefined database."""
#         text_lower = text.lower()
#         found_skills = set()
        
#         # Flatten skills database
#         all_technical_skills = []
#         for category_skills in self.technical_skills_db.values():
#             all_technical_skills.extend(category_skills)
        
#         for skill in all_technical_skills:
#             skill_lower = skill.lower()
            
#             # SPECIAL HANDLING for single-letter skills (C, R, etc.)
#             if len(skill_lower) == 1:
#                 # Use stricter pattern: must be surrounded by non-alphanumeric characters
#                 # This prevents matching 'c' in 'chess' or 'r' in 'player'
#                 pattern = r'(?<![a-z])' + re.escape(skill_lower) + r'(?![a-z])'
#                 if re.search(pattern, text_lower):
#                     found_skills.add(skill)
#             else:
#                 # Match exact skill or skill as word boundary
#                 pattern = r'\b' + re.escape(skill_lower) + r'\b'
#                 if re.search(pattern, text_lower):
#                     found_skills.add(skill)
#                 # Check for common variations
#                 elif skill_lower.replace('.', '') in text_lower:
#                     found_skills.add(skill)
#                 elif skill_lower.replace(' ', '') in text_lower.replace(' ', ''):
#                     found_skills.add(skill)
        
#         return found_skills
    
#     def _extract_general_skills_and_keywords(self, text: str) -> Set[str]:
#         """
#         Extract general skills and important keywords from job description.
#         This catches non-technical requirements like 'chess player', 'team lead', etc.
#         Prioritizes multi-word phrases over single words to avoid duplicates.
#         """
#         text_lower = text.lower()
#         skills_keywords = set()
#         extracted_phrases = set()
        
#         # STEP 1: Extract explicit skill indicators first (highest priority)
#         skill_patterns = [
#             r'(?:skills?|knowledge|experience|proficiency|expertise)\s+(?:in|with|of)\s+([a-z\s,]+?)(?:\.|,|;|\n|$)',
#             r'(?:proficient|skilled|experienced)\s+(?:in|with|at)\s+([a-z\s,]+?)(?:\.|,|;|\n|$)',
#             r'(?:must|should)\s+(?:have|know|understand)\s+([a-z\s,]+?)(?:\.|,|;|\n|$)',
#             r'(?:required|preferred|desired):\s*([a-z\s,]+?)(?:\.|;|\n|$)',
#         ]
        
#         for pattern in skill_patterns:
#             matches = re.finditer(pattern, text_lower)
#             for match in matches:
#                 skill_text = match.group(1)
#                 # Split by commas and 'and'
#                 skill_parts = re.split(r',|\s+and\s+', skill_text)
#                 for part in skill_parts:
#                     part = part.strip()
#                     if part and len(part) > 3 and not any(word in self.stop_words for word in part.split()):
#                         skills_keywords.add(part)
#                         extracted_phrases.add(part)
        
#         # STEP 2: Extract 2-4 word phrases (medium priority)
#         phrases_2word = re.findall(r'\b([a-z]+\s+[a-z]+)\b', text_lower)
#         phrases_3word = re.findall(r'\b([a-z]+\s+[a-z]+\s+[a-z]+)\b', text_lower)
        
#         for phrase in phrases_2word + phrases_3word:
#             words = phrase.split()
#             # Skip if contains stop words
#             if any(word in self.stop_words for word in words):
#                 continue
#             # Skip if any word is too short
#             if any(len(word) < 3 for word in words):
#                 continue
#             # Skip if already extracted from explicit patterns
#             if phrase in extracted_phrases:
#                 continue
            
#             skills_keywords.add(phrase.strip())
#             extracted_phrases.add(phrase.strip())
        
#         # STEP 3: Extract single meaningful words (lowest priority)
#         # But ONLY if they are NOT part of any phrase already extracted
#         single_words = re.findall(r'\b[a-z]{4,}\b', text_lower)
#         for word in single_words:
#             if word in self.stop_words:
#                 continue
            
#             # Check if this word is part of any already extracted phrase
#             is_part_of_phrase = False
#             for phrase in extracted_phrases:
#                 if word in phrase.split():
#                     is_part_of_phrase = True
#                     break
            
#             # Only add if NOT part of a phrase
#             if not is_part_of_phrase:
#                 skills_keywords.add(word)
        
#         return skills_keywords
    
#     def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
#         """Categorize technical skills."""
#         categorized = {}
        
#         for category, category_skills in self.technical_skills_db.items():
#             matching = [skill for skill in skills if skill in category_skills]
#             if matching:
#                 categorized[category] = matching
        
#         return categorized
    
#     def _calculate_match_score(
#         self, 
#         matched: Set[str], 
#         total_job_requirements: int
#     ) -> Tuple[float, int]:
#         """
#         Calculate skills match percentage and score.
        
#         Args:
#             matched: Set of matched skills
#             total_job_requirements: Total number of job requirements
        
#         Returns:
#             Tuple of (match_percentage, score)
#         """
#         if total_job_requirements == 0:
#             # No specific requirements - score based on resume skills count
#             return 100.0, min(10 * 2, self.max_score)
        
#         # Calculate match percentage
#         match_percentage = (len(matched) / total_job_requirements) * 100
        
#         # Calculate score with penalties for missing critical skills
#         if match_percentage >= 90:
#             score = self.max_score
#         elif match_percentage >= 75:
#             score = int(self.max_score * 0.85)  # 85% of max
#         elif match_percentage >= 60:
#             score = int(self.max_score * 0.70)  # 70% of max
#         elif match_percentage >= 40:
#             score = int(self.max_score * 0.50)  # 50% of max
#         elif match_percentage >= 20:
#             score = int(self.max_score * 0.30)  # 30% of max
#         else:
#             score = int(self.max_score * 0.15)  # 15% of max
        
#         return match_percentage, score
    
#     def analyze(self, resume_text: str, job_description: str) -> Dict:
#         """
#         Analyze skills matching between resume and job description.
#         Extracts BOTH technical skills AND general keywords/requirements.
        
#         Returns:
#             Dictionary with comprehensive skills analysis and score
#         """
#         # Extract technical skills from both
#         resume_technical = self._extract_technical_skills(resume_text)
#         job_technical = self._extract_technical_skills(job_description)
        
#         # Extract general skills/keywords from job description
#         job_general_raw = self._extract_general_skills_and_keywords(job_description)
        
#         # Filter out general keywords that overlap with technical skills (case-insensitive)
#         job_technical_lower = {skill.lower() for skill in job_technical}
#         job_general = set()
        
#         for keyword in job_general_raw:
#             keyword_lower = keyword.lower()
#             # Skip if this keyword is already a technical skill
#             if keyword_lower not in job_technical_lower:
#                 # Also check if any word in the phrase is a technical skill
#                 words = keyword_lower.split()
#                 if not any(word in job_technical_lower for word in words):
#                     job_general.add(keyword)
        
#         # Combine all job requirements (technical + filtered general)
#         all_job_requirements = job_technical.union(job_general)
        
#         # Extract all potential skills from resume (technical + general keywords)
#         resume_general_raw = self._extract_general_skills_and_keywords(resume_text)
        
#         # Filter resume general keywords too
#         resume_technical_lower = {skill.lower() for skill in resume_technical}
#         resume_general = set()
        
#         for keyword in resume_general_raw:
#             keyword_lower = keyword.lower()
#             if keyword_lower not in resume_technical_lower:
#                 words = keyword_lower.split()
#                 if not any(word in resume_technical_lower for word in words):
#                     resume_general.add(keyword)
        
#         all_resume_skills = resume_technical.union(resume_general)
        
#         # Calculate matching
#         matched_skills = all_resume_skills.intersection(all_job_requirements)
#         missing_skills = all_job_requirements - all_resume_skills
        
#         # Calculate match percentage and score
#         match_percentage, score = self._calculate_match_score(
#             matched_skills,
#             len(all_job_requirements)
#         )
        
#         # Categorize technical skills only
#         resume_categorized = self._categorize_skills(resume_technical)
#         job_categorized = self._categorize_skills(job_technical)
        
#         # Separate technical and non-technical for better reporting
#         matched_technical = matched_skills.intersection(job_technical)
#         matched_general = matched_skills - matched_technical
#         missing_technical = missing_skills.intersection(job_technical)
#         missing_general = missing_skills - missing_technical
        
#         # Log detailed analysis
#         if missing_skills:
#             logger.warning(
#                 f"Missing {len(missing_skills)} required skills/keywords: "
#                 f"{', '.join(sorted(list(missing_skills))[:5])}"
#             )
        
#         logger.info(
#             f"Skills analysis: {len(matched_skills)}/{len(all_job_requirements)} matched "
#             f"({len(matched_technical)} technical, {len(matched_general)} general), "
#             f"match: {match_percentage:.1f}%, score: {score}/{self.max_score}"
#         )
        
#         return {
#             'score': score,
#             'max_score': self.max_score,
#             'percentage': round((score / self.max_score) * 100, 2),
#             'resume_skills': sorted(list(resume_technical)),  # Show technical skills in main list
#             'job_skills': sorted(list(all_job_requirements)),  # Show ALL job requirements
#             'matched_skills': sorted(list(matched_skills)),  # All matched (technical + general)
#             'missing_skills': sorted(list(missing_skills)),  # All missing (technical + general)
#             'match_percentage': round(match_percentage, 2),
#             'resume_skills_categorized': resume_categorized,
#             'job_skills_categorized': job_categorized,
#             'total_resume_skills': len(all_resume_skills),
#             'total_job_skills': len(all_job_requirements),
#             # Additional details for debugging/transparency
#             'matched_technical': sorted(list(matched_technical)),
#             'matched_general': sorted(list(matched_general)),
#             'missing_technical': sorted(list(missing_technical)),
#             'missing_general': sorted(list(missing_general)),
#             'job_general_requirements': sorted(list(job_general))
#         }




import re
import logging
from typing import Dict, List, Set, Tuple

logger = logging.getLogger(__name__)


class SkillsAnalyzer:
    """Analyze skills matching between resume and job description."""
    
    def __init__(self):
        self.max_score = 35
        self.technical_skills_db = self._build_technical_skills_database()
        
        # Common stop words to ignore when extracting general skills
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'about', 'as', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
            'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
            'will', 'just', 'should', 'now', 'work', 'working', 'experience',
            'job', 'role', 'position', 'candidate', 'team', 'company', 'year',
            'years', 'must', 'required', 'preferred', 'looking', 'seeking',
            'able', 'ability', 'strong', 'good', 'excellent', 'great', 'best',
            'well', 'including', 'using', 'across', 'within', 'around', 'along',
            'including', 'plus', 'also', 'like', 'even', 'may', 'might', 'would',
            'could', 'should', 'shall', 'need', 'want', 'like', 'make', 'get',
            'take', 'come', 'see', 'know', 'think', 'use', 'find', 'give',
            'tell', 'ask', 'feel', 'try', 'leave', 'call', 'keep', 'let', 'begin',
            'seem', 'help', 'show', 'play', 'run', 'move', 'live', 'believe',
            'hold', 'bring', 'happen', 'write', 'provide', 'sit', 'stand', 'lose',
            'pay', 'meet', 'include', 'continue', 'set', 'learn', 'change', 'lead',
            'understand', 'watch', 'follow', 'stop', 'create', 'speak', 'read',
            'allow', 'add', 'spend', 'grow', 'open', 'walk', 'win', 'offer',
            'remember', 'love', 'consider', 'appear', 'buy', 'wait', 'serve',
            'die', 'send', 'expect', 'build', 'stay', 'fall', 'cut', 'reach',
            'kill', 'remain', 'suggest', 'raise', 'pass', 'sell', 'require',
            'report', 'decide', 'pull', 'go'  # Added 'go' to stop words
        }
    
    def _build_technical_skills_database(self) -> Dict[str, List[str]]:
        """Build comprehensive technical skills database by category."""
        return {
            'programming_languages': [
                'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C',
                'Go', 'Golang', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R',
                'MATLAB', 'Dart', 'Objective-C', 'Perl', 'Shell', 'Bash', 'PowerShell'
            ],
            'web_frontend': [
                'React', 'Angular', 'Vue.js', 'Next.js', 'Svelte', 'HTML', 'CSS',
                'SCSS', 'Sass', 'Bootstrap', 'Tailwind CSS', 'Material-UI', 'jQuery',
                'Redux', 'MobX', 'Webpack', 'Vite', 'Babel'
            ],
            'web_backend': [
                'Node.js', 'Express.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot',
                'Spring', 'ASP.NET', '.NET Core', 'Laravel', 'Ruby on Rails', 'Nest.js'
            ],
            'mobile': [
                'Android', 'iOS', 'React Native', 'Flutter', 'SwiftUI', 'UIKit',
                'Jetpack Compose', 'Kotlin Multiplatform', 'Xamarin', 'Ionic'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
                'SQL Server', 'Cassandra', 'DynamoDB', 'Firebase', 'Firestore',
                'Elasticsearch', 'Neo4j', 'CouchDB'
            ],
            'cloud_devops': [
                'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes',
                'Terraform', 'Ansible', 'Jenkins', 'GitLab CI', 'GitHub Actions',
                'CircleCI', 'Travis CI', 'Heroku', 'Vercel', 'Netlify'
            ],
            'data_science_ml': [
                'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy',
                'Matplotlib', 'Seaborn', 'Jupyter', 'Apache Spark', 'Hadoop',
                'Power BI', 'Tableau', 'OpenCV', 'NLTK', 'SpaCy', 'Hugging Face'
            ],
            'tools_technologies': [
                'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN', 'Jira', 'Confluence',
                'Slack', 'Trello', 'Postman', 'Swagger', 'GraphQL', 'REST API',
                'gRPC', 'Microservices', 'OAuth', 'JWT', 'WebSocket'
            ],
            'concepts_methodologies': [
                'Agile', 'Scrum', 'Kanban', 'DevOps', 'CI/CD', 'TDD', 'BDD',
                'Microservices', 'RESTful', 'MVC', 'MVVM', 'OOP', 'Design Patterns',
                'System Design', 'Data Structures', 'Algorithms'
            ],
            'testing': [
                'JUnit', 'TestNG', 'Pytest', 'Jest', 'Mocha', 'Chai', 'Selenium',
                'Cypress', 'Playwright', 'Appium', 'Postman', 'JMeter', 'LoadRunner'
            ]
        }
    
    def _extract_technical_skills(self, text: str) -> Set[str]:
        """Extract technical skills from predefined database with very strict matching."""
        text_lower = text.lower()
        found_skills = set()
        
        # Flatten skills database
        all_technical_skills = []
        for category_skills in self.technical_skills_db.values():
            all_technical_skills.extend(category_skills)
        
        for skill in all_technical_skills:
            skill_lower = skill.lower()
            
            # CRITICAL FIX: Very strict handling for short skills (≤2 characters)
            if len(skill_lower) <= 2:
                # For single letter skills like 'C' or 'R'
                if len(skill_lower) == 1:
                    # Must appear as standalone with clear boundaries
                    # Pattern: space/comma/start before, space/comma/end after
                    pattern = r'(?:^|[\s,;|]|Programming\s+Language[s]?\s*:?\s*)' + re.escape(skill_lower.upper()) + r'(?=[\s,;|]|$|Programming|\+\+)'
                    if re.search(pattern, text, re.IGNORECASE):
                        found_skills.add(skill)
                    # Also check for explicit "C Programming" pattern
                    elif skill_lower == 'c' and re.search(r'\bC\s+Programming\b', text, re.IGNORECASE):
                        found_skills.add(skill)
                
                # For 2-letter skills like 'Go'
                elif len(skill_lower) == 2:
                    # MUST be standalone word with strict boundaries
                    # Exclude if it's part of common words
                    pattern = r'(?:^|[\s,;|]|Language[s]?\s*:?\s*)' + re.escape(skill_lower) + r'(?=[\s,;|.]|$)'
                    
                    # Find all matches
                    matches = list(re.finditer(pattern, text_lower))
                    
                    # For "Go", verify it's not part of words like "going", "logo", etc.
                    if skill_lower == 'go':
                        for match in matches:
                            start = match.start()
                            end = match.end()
                            
                            # Check context before and after
                            before_char = text_lower[start-1] if start > 0 else ' '
                            after_char = text_lower[end] if end < len(text_lower) else ' '
                            
                            # Make sure it's truly standalone
                            if before_char in ' ,;|\n' and after_char in ' ,;|\n.':
                                # Additional check: make sure it's in a skills/tech context
                                # Look at surrounding 50 characters
                                context_start = max(0, start - 50)
                                context_end = min(len(text_lower), end + 50)
                                context = text_lower[context_start:context_end]
                                
                                # Only accept if near keywords like: programming, language, skill, tech, etc.
                                context_keywords = ['programming', 'language', 'skill', 'tech', 'stack', 'golang']
                                if any(kw in context for kw in context_keywords):
                                    found_skills.add(skill)
                                    break
                    else:
                        # For other 2-letter skills, just verify it's standalone
                        if matches:
                            found_skills.add(skill)
            
            else:
                # For longer skills (>2 chars), use standard word boundary matching
                pattern = r'\b' + re.escape(skill_lower) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.add(skill)
                # Check for common variations
                elif skill_lower.replace('.', '') in text_lower:
                    found_skills.add(skill)
                elif skill_lower.replace(' ', '') in text_lower.replace(' ', ''):
                    found_skills.add(skill)
        
        return found_skills
    
    def _extract_general_skills_and_keywords(self, text: str) -> Set[str]:
        """
        Extract general skills and important keywords from job description.
        This catches non-technical requirements like 'chess player', 'team lead', etc.
        Prioritizes multi-word phrases over single words to avoid duplicates.
        """
        text_lower = text.lower()
        skills_keywords = set()
        extracted_phrases = set()
        
        # STEP 1: Extract explicit skill indicators first (highest priority)
        skill_patterns = [
            r'(?:skills?|knowledge|experience|proficiency|expertise)\s+(?:in|with|of)\s+([a-z\s,]+?)(?:\.|,|;|\n|$)',
            r'(?:proficient|skilled|experienced)\s+(?:in|with|at)\s+([a-z\s,]+?)(?:\.|,|;|\n|$)',
            r'(?:must|should)\s+(?:have|know|understand)\s+([a-z\s,]+?)(?:\.|,|;|\n|$)',
            r'(?:required|preferred|desired):\s*([a-z\s,]+?)(?:\.|;|\n|$)',
        ]
        
        for pattern in skill_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                skill_text = match.group(1)
                # Split by commas and 'and'
                skill_parts = re.split(r',|\s+and\s+', skill_text)
                for part in skill_parts:
                    part = part.strip()
                    if part and len(part) > 3 and not any(word in self.stop_words for word in part.split()):
                        skills_keywords.add(part)
                        extracted_phrases.add(part)
        
        # STEP 2: Extract 2-4 word phrases (medium priority)
        phrases_2word = re.findall(r'\b([a-z]+\s+[a-z]+)\b', text_lower)
        phrases_3word = re.findall(r'\b([a-z]+\s+[a-z]+\s+[a-z]+)\b', text_lower)
        
        for phrase in phrases_2word + phrases_3word:
            words = phrase.split()
            # Skip if contains stop words
            if any(word in self.stop_words for word in words):
                continue
            # Skip if any word is too short
            if any(len(word) < 3 for word in words):
                continue
            # Skip if already extracted from explicit patterns
            if phrase in extracted_phrases:
                continue
            
            skills_keywords.add(phrase.strip())
            extracted_phrases.add(phrase.strip())
        
        # STEP 3: Extract single meaningful words (lowest priority)
        # But ONLY if they are NOT part of any phrase already extracted
        single_words = re.findall(r'\b[a-z]{4,}\b', text_lower)
        for word in single_words:
            if word in self.stop_words:
                continue
            
            # Check if this word is part of any already extracted phrase
            is_part_of_phrase = False
            for phrase in extracted_phrases:
                if word in phrase.split():
                    is_part_of_phrase = True
                    break
            
            # Only add if NOT part of a phrase
            if not is_part_of_phrase:
                skills_keywords.add(word)
        
        return skills_keywords
    
    def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Categorize technical skills."""
        categorized = {}
        
        for category, category_skills in self.technical_skills_db.items():
            matching = [skill for skill in skills if skill in category_skills]
            if matching:
                categorized[category] = matching
        
        return categorized
    
    def _calculate_match_score(
        self, 
        matched: Set[str], 
        total_job_requirements: int
    ) -> Tuple[float, int]:
        """
        Calculate skills match percentage and score.
        
        Args:
            matched: Set of matched skills
            total_job_requirements: Total number of job requirements
        
        Returns:
            Tuple of (match_percentage, score)
        """
        if total_job_requirements == 0:
            # No specific requirements - score based on resume skills count
            return 100.0, min(10 * 2, self.max_score)
        
        # Calculate match percentage
        match_percentage = (len(matched) / total_job_requirements) * 100
        
        # Calculate score with penalties for missing critical skills
        if match_percentage >= 90:
            score = self.max_score
        elif match_percentage >= 75:
            score = int(self.max_score * 0.85)  # 85% of max
        elif match_percentage >= 60:
            score = int(self.max_score * 0.70)  # 70% of max
        elif match_percentage >= 40:
            score = int(self.max_score * 0.50)  # 50% of max
        elif match_percentage >= 20:
            score = int(self.max_score * 0.30)  # 30% of max
        else:
            score = int(self.max_score * 0.15)  # 15% of max
        
        return match_percentage, score
    
    def analyze(self, resume_text: str, job_description: str) -> Dict:
        """
        Analyze skills matching between resume and job description.
        Extracts BOTH technical skills AND general keywords/requirements.
        
        Returns:
            Dictionary with comprehensive skills analysis and score
        """
        # Extract technical skills from both
        resume_technical = self._extract_technical_skills(resume_text)
        job_technical = self._extract_technical_skills(job_description)
        
        # Extract general skills/keywords from job description
        job_general_raw = self._extract_general_skills_and_keywords(job_description)
        
        # Filter out general keywords that overlap with technical skills (case-insensitive)
        job_technical_lower = {skill.lower() for skill in job_technical}
        job_general = set()
        
        for keyword in job_general_raw:
            keyword_lower = keyword.lower()
            # Skip if this keyword is already a technical skill
            if keyword_lower not in job_technical_lower:
                # Also check if any word in the phrase is a technical skill
                words = keyword_lower.split()
                if not any(word in job_technical_lower for word in words):
                    job_general.add(keyword)
        
        # Combine all job requirements (technical + filtered general)
        all_job_requirements = job_technical.union(job_general)
        
        # Extract all potential skills from resume (technical + general keywords)
        resume_general_raw = self._extract_general_skills_and_keywords(resume_text)
        
        # Filter resume general keywords too
        resume_technical_lower = {skill.lower() for skill in resume_technical}
        resume_general = set()
        
        for keyword in resume_general_raw:
            keyword_lower = keyword.lower()
            if keyword_lower not in resume_technical_lower:
                words = keyword_lower.split()
                if not any(word in resume_technical_lower for word in words):
                    resume_general.add(keyword)
        
        all_resume_skills = resume_technical.union(resume_general)
        
        # Calculate matching
        matched_skills = all_resume_skills.intersection(all_job_requirements)
        missing_skills = all_job_requirements - all_resume_skills
        
        # Calculate match percentage and score
        match_percentage, score = self._calculate_match_score(
            matched_skills,
            len(all_job_requirements)
        )
        
        # Categorize technical skills only
        resume_categorized = self._categorize_skills(resume_technical)
        job_categorized = self._categorize_skills(job_technical)
        
        # Separate technical and non-technical for better reporting
        matched_technical = matched_skills.intersection(job_technical)
        matched_general = matched_skills - matched_technical
        missing_technical = missing_skills.intersection(job_technical)
        missing_general = missing_skills - missing_technical
        
        # Log detailed analysis
        if missing_skills:
            logger.warning(
                f"Missing {len(missing_skills)} required skills/keywords: "
                f"{', '.join(sorted(list(missing_skills))[:5])}"
            )
        
        logger.info(
            f"Skills analysis: {len(matched_skills)}/{len(all_job_requirements)} matched "
            f"({len(matched_technical)} technical, {len(matched_general)} general), "
            f"match: {match_percentage:.1f}%, score: {score}/{self.max_score}"
        )
        
        return {
            'score': score,
            'max_score': self.max_score,
            'percentage': round((score / self.max_score) * 100, 2),
            'resume_skills': sorted(list(resume_technical)),  # Show technical skills in main list
            'job_skills': sorted(list(all_job_requirements)),  # Show ALL job requirements
            'matched_skills': sorted(list(matched_skills)),  # All matched (technical + general)
            'missing_skills': sorted(list(missing_skills)),  # All missing (technical + general)
            'match_percentage': round(match_percentage, 2),
            'resume_skills_categorized': resume_categorized,
            'job_skills_categorized': job_categorized,
            'total_resume_skills': len(all_resume_skills),
            'total_job_skills': len(all_job_requirements),
            # Additional details for debugging/transparency
            'matched_technical': sorted(list(matched_technical)),
            'matched_general': sorted(list(matched_general)),
            'missing_technical': sorted(list(missing_technical)),
            'missing_general': sorted(list(missing_general)),
            'job_general_requirements': sorted(list(job_general))
        }