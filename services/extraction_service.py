# import re
# import logging
# from typing import List, Dict, Optional

# logger = logging.getLogger(__name__)


# class PerfectResumeExtractor:
#     """
#     Universal extraction service that extracts ALL sections from a resume.
#     Handles education, projects, certifications, achievements, experience, and any other sections.
#     """
    
#     def __init__(self):
#         self.degree_keywords = [
#             'btech', 'b.tech', 'bachelor', 'mtech', 'm.tech', 'master',
#             'be', 'b.e', 'bs', 'b.s', 'bsc', 'b.sc',
#             'me', 'm.e', 'ms', 'm.s', 'msc', 'm.sc',
#             'mba', 'mca', 'bca', 'phd', 'ph.d', 'diploma',
#             'class 10', 'class 11', 'class 12', 'class x', 'class xi', 'class xii'
#         ]
        
#         # All possible section headers in resumes
#         self.all_section_headers = [
#             'EDUCATION',
#             'PROJECTS?',
#             'EXPERIENCE',
#             'WORK HISTORY',
#             'EMPLOYMENT',
#             'INTERNSHIPS?',
#             'SKILLS?',
#             'CERTIFICATIONS?',
#             'CERTIFICATES?',
#             'POSITION OF RESPONSIBILITY',
#             'RESPONSIBILITIES',
#             'ACHIEVEMENTS?',
#             'AWARDS?',
#             'ACHIEVEMENTS & AWARDS',
#             'ACHIEVEMENTS AND AWARDS',
#             'OBJECTIVE',
#             'SUMMARY',
#             'PROFESSIONAL SUMMARY',
#             'VOLUNTEER',
#             'VOLUNTEERING',
#             'LANGUAGES?',
#             'INTERESTS?',
#             'HOBBIES',
#             'REFERENCES?',
#             'PUBLICATIONS?',
#             'RESEARCH',
#             'TRAINING'
#         ]
    
#     def _find_all_section_positions(self, text: str) -> List[Dict]:
#         """Find all section headers and their positions in the text."""
#         sections = []
        
#         # Create pattern that matches any section header
#         for header in self.all_section_headers:
#             pattern = r'\n\s*' + header + r'\s*\n'
#             for match in re.finditer(pattern, text, re.IGNORECASE):
#                 section_name = match.group().strip()
#                 sections.append({
#                     'name': section_name,
#                     'normalized_name': self._normalize_section_name(section_name),
#                     'start': match.end(),
#                     'header_start': match.start()
#                 })
        
#         # Sort by position
#         sections.sort(key=lambda x: x['start'])
#         return sections
    
#     def _normalize_section_name(self, section_name: str) -> str:
#         """Normalize section names for consistent keys."""
#         name = section_name.strip().upper()
        
#         # Map variations to standard names
#         if 'PROJECT' in name:
#             return 'PROJECTS'
#         elif 'EXPERIENCE' in name or 'INTERNSHIP' in name or 'WORK' in name or 'EMPLOYMENT' in name:
#             return 'EXPERIENCE'
#         elif 'EDUCATION' in name:
#             return 'EDUCATION'
#         elif 'SKILL' in name:
#             return 'SKILLS'
#         elif 'CERTIF' in name:
#             return 'CERTIFICATIONS'
#         elif 'ACHIEVEMENT' in name or 'AWARD' in name:
#             return 'ACHIEVEMENTS'
#         elif 'POSITION' in name or 'RESPONSIB' in name:
#             return 'RESPONSIBILITIES'
#         elif 'OBJECTIVE' in name:
#             return 'OBJECTIVE'
#         elif 'SUMMARY' in name:
#             return 'SUMMARY'
#         else:
#             return name
    
#     def _find_section_boundaries(self, text: str, section_name: str) -> tuple[int, int]:
#         """Find exact start and end of a section using all sections as boundaries."""
        
#         # Find all sections
#         all_sections = self._find_all_section_positions(text)
        
#         if not all_sections:
#             return -1, -1
        
#         # Find the target section
#         target_section = None
#         target_index = -1
        
#         section_name_lower = section_name.lower()
        
#         for i, section in enumerate(all_sections):
#             section_header_lower = section['name'].lower()
            
#             # Match the section we're looking for
#             if section_name_lower in section_header_lower or \
#                (section_name == 'projects' and 'project' in section_header_lower) or \
#                (section_name == 'experience' and any(x in section_header_lower for x in ['experience', 'internship', 'work history', 'employment'])):
#                 target_section = section
#                 target_index = i
#                 break
        
#         if not target_section:
#             return -1, -1
        
#         start = target_section['start']
        
#         # End is the start of the next section (or end of text)
#         if target_index + 1 < len(all_sections):
#             end = all_sections[target_index + 1]['header_start']
#         else:
#             end = len(text)
        
#         return start, end
    
#     def extract_all_sections(self, text: str) -> Dict:
#         """
#         Extract ALL sections from the resume dynamically.
#         Returns a dictionary with all found sections and their content.
#         """
#         all_sections = self._find_all_section_positions(text)
        
#         extracted = {
#             'education': [],
#             'projects': [],
#             'experience': [],
#             'certifications': [],
#             'achievements': [],
#             'responsibilities': [],
#             'skills': [],
#             'objective': None,
#             'summary': None,
#             'other_sections': {}
#         }
        
#         for i, section in enumerate(all_sections):
#             section_name = section['normalized_name']
#             start = section['start']
            
#             # Get end boundary
#             if i + 1 < len(all_sections):
#                 end = all_sections[i + 1]['header_start']
#             else:
#                 end = len(text)
            
#             section_content = text[start:end].strip()
            
#             # Route to appropriate extraction method
#             if section_name == 'EDUCATION':
#                 extracted['education'] = self._extract_education_items(section_content)
#             elif section_name == 'PROJECTS':
#                 extracted['projects'] = self._extract_project_items(section_content)
#             elif section_name == 'EXPERIENCE':
#                 extracted['experience'] = self._extract_experience_items(section_content)
#             elif section_name == 'CERTIFICATIONS':
#                 extracted['certifications'] = self._extract_list_items(section_content, 'certification')
#             elif section_name == 'ACHIEVEMENTS':
#                 extracted['achievements'] = self._extract_list_items(section_content, 'achievement')
#             elif section_name == 'RESPONSIBILITIES':
#                 extracted['responsibilities'] = self._extract_list_items(section_content, 'responsibility')
#             elif section_name == 'OBJECTIVE':
#                 extracted['objective'] = section_content
#             elif section_name == 'SUMMARY':
#                 extracted['summary'] = section_content
#             else:
#                 # Store other sections as-is
#                 extracted['other_sections'][section_name] = section_content
        
#         return extracted
    
#     def _extract_education_items(self, text: str) -> List[Dict]:
#         """Extract education entries."""
#         education_entries = []
#         lines = text.split('\n')
        
#         i = 0
#         while i < len(lines):
#             line = lines[i].strip()
            
#             if not line:
#                 i += 1
#                 continue
            
#             line_lower = line.lower()
#             is_education_start = any(keyword in line_lower for keyword in self.degree_keywords)
            
#             if is_education_start:
#                 entry_lines = [line]
#                 i += 1
                
#                 while i < len(lines):
#                     next_line = lines[i].strip()
                    
#                     if not next_line:
#                         i += 1
#                         while i < len(lines) and not lines[i].strip():
#                             i += 1
#                         if i < len(lines):
#                             next_non_empty = lines[i].strip().lower()
#                             if any(keyword in next_non_empty for keyword in self.degree_keywords):
#                                 break
#                         continue
                    
#                     next_lower = next_line.lower()
#                     is_next_education = any(keyword in next_lower for keyword in self.degree_keywords)
                    
#                     if is_next_education:
#                         break
                    
#                     entry_lines.append(next_line)
#                     i += 1
                
#                 entry_text = '\n'.join(entry_lines)
#                 parsed = self._parse_education_entry(entry_text)
#                 if parsed:
#                     education_entries.append(parsed)
#             else:
#                 i += 1
        
#         return education_entries
    
#     def _parse_education_entry(self, text: str) -> Optional[Dict]:
#         """Parse a single education entry."""
#         lines = [l.strip() for l in text.split('\n') if l.strip()]
        
#         if not lines:
#             return None
        
#         degree = lines[0]
#         institution = None
#         year = None
        
#         for line in lines:
#             if re.match(r'^\|\s*[\d.]+', line):
#                 continue
            
#             if re.search(r'(Institute|University|College|School|Academy)', line, re.IGNORECASE):
#                 institution = line
#                 institution = re.sub(r'\s*\d{4}\s*-?\s*\d{0,4}\s*$', '', institution).strip()
#                 break
        
#         full_text = ' '.join(lines)
#         year_match = re.search(r'(\d{4})\s*-\s*(\d{4})', full_text)
#         if year_match:
#             year = f"{year_match.group(1)}-{year_match.group(2)}"
#         else:
#             year_match = re.search(r'\b(\d{4})\b', full_text)
#             if year_match:
#                 year = year_match.group(1)
        
#         if institution and institution in degree:
#             degree = degree.replace(institution, '').strip()
        
#         if year:
#             degree = re.sub(r'\s*\d{4}\s*-?\s*\d{0,4}\s*', '', degree).strip()
        
#         return {
#             'degree': degree if degree else None,
#             'institution': institution,
#             'year': year,
#             'raw_text': text.strip()
#         }
    
#     def _extract_project_items(self, text: str) -> List[Dict]:
#         """Extract project entries with bullet points grouped under titles."""
#         projects = []
#         lines = text.split('\n')
        
#         current_project = None
#         description_lines = []
#         technologies = []
        
#         i = 0
#         while i < len(lines):
#             stripped_line = lines[i].strip()
            
#             if not stripped_line:
#                 i += 1
#                 continue
            
#             is_bullet = stripped_line.startswith('•') or stripped_line.startswith('-') or stripped_line.startswith('*')
            
#             if is_bullet and current_project:
#                 clean_line = re.sub(r'^[•\-\*]\s*', '', stripped_line)
#                 description_lines.append(clean_line)
#                 tech_from_line = self._extract_technologies_from_line(clean_line)
#                 technologies.extend(tech_from_line)
#                 i += 1
#                 continue
            
#             has_project_keywords = any(keyword in stripped_line for keyword in [
#                 'App', 'System', 'Platform', 'Website', 'Project', 
#                 'Model', 'Tool', 'Game', 'Car', 'Calculator', 'Interface',
#                 'Portal', 'Dashboard', 'Application', 'Bot', 'Analyzer'
#             ])
            
#             has_link_indicator = '|' in stripped_line or 'http' in stripped_line.lower()
            
#             title_ending_patterns = [
#                 r'\(Ongoing\)$', r'\(In Progress\)$', r'App$', r'System$',
#                 r'Model$', r'Tool$', r'Game$', r'Platform$', r'Website$'
#             ]
            
#             matches_title_pattern = any(re.search(pattern, stripped_line, re.IGNORECASE) for pattern in title_ending_patterns)
#             starts_with_uppercase = stripped_line[0].isupper() if stripped_line else False
            
#             is_likely_title = (
#                 not is_bullet and
#                 starts_with_uppercase and
#                 (has_project_keywords or matches_title_pattern or has_link_indicator) and
#                 len(stripped_line) > 20
#             )
            
#             if len(stripped_line) < 30 and not stripped_line[0].isupper():
#                 is_likely_title = False
            
#             if is_likely_title:
#                 if current_project:
#                     full_description = ' '.join(description_lines).strip()
#                     projects.append({
#                         'title': current_project,
#                         'description': full_description if full_description else None,
#                         'technologies': list(set(technologies)),
#                         'raw_text': full_description if full_description else ''
#                     })
                
#                 current_project = stripped_line
#                 if '|' in current_project:
#                     current_project = current_project.split('|')[0].strip()
#                 current_project = re.sub(r'https?://\S+', '', current_project).strip()
                
#                 description_lines = []
#                 technologies = []
#                 i += 1
#                 continue
            
#             if current_project:
#                 if 'technologies' in stripped_line.lower() or 'tech stack' in stripped_line.lower():
#                     tech_from_line = self._extract_technologies_from_line(stripped_line)
#                     technologies.extend(tech_from_line)
#                 else:
#                     if description_lines:
#                         description_lines[-1] += ' ' + stripped_line
#                     else:
#                         description_lines.append(stripped_line)
            
#             i += 1
        
#         if current_project:
#             full_description = ' '.join(description_lines).strip()
#             projects.append({
#                 'title': current_project,
#                 'description': full_description if full_description else None,
#                 'technologies': list(set(technologies)),
#                 'raw_text': full_description if full_description else ''
#             })
        
#         return projects
    
#     def _extract_experience_items(self, text: str) -> List[Dict]:
#         """Extract experience/internship entries."""
#         experiences = []
#         lines = text.split('\n')
        
#         current_exp = None
#         description_lines = []
        
#         i = 0
#         while i < len(lines):
#             stripped_line = lines[i].strip()
            
#             if not stripped_line:
#                 i += 1
#                 continue
            
#             is_bullet = stripped_line.startswith('•') or stripped_line.startswith('-') or stripped_line.startswith('*')
            
#             # Experience titles often have | separator or dates
#             has_separator = '|' in stripped_line
#             has_date = re.search(r'[A-Za-z]{3}\s+\d{2}\s*-\s*[A-Za-z]{3}\s+\d{2}', stripped_line)
            
#             is_likely_title = (
#                 not is_bullet and
#                 (has_separator or has_date or len(stripped_line) > 30) and
#                 stripped_line[0].isupper()
#             )
            
#             if is_likely_title and not is_bullet:
#                 if current_exp:
#                     full_description = ' '.join(description_lines).strip()
#                     experiences.append({
#                         'title': current_exp,
#                         'description': full_description if full_description else None,
#                         'raw_text': full_description if full_description else ''
#                     })
                
#                 current_exp = stripped_line
#                 description_lines = []
#                 i += 1
#                 continue
            
#             if is_bullet and current_exp:
#                 clean_line = re.sub(r'^[•\-\*]\s*', '', stripped_line)
#                 description_lines.append(clean_line)
#             elif current_exp and not is_bullet:
#                 if description_lines:
#                     description_lines[-1] += ' ' + stripped_line
            
#             i += 1
        
#         if current_exp:
#             full_description = ' '.join(description_lines).strip()
#             experiences.append({
#                 'title': current_exp,
#                 'description': full_description if full_description else None,
#                 'raw_text': full_description if full_description else ''
#             })
        
#         return experiences
    
#     def _extract_list_items(self, text: str, item_type: str) -> List[Dict]:
#         """
#         Extract bullet-pointed items (certifications, achievements, etc.).
#         For responsibilities, groups bullets under their title.
#         """
#         items = []
#         lines = text.split('\n')
        
#         # Special handling for responsibilities (similar to projects)
#         if item_type == 'responsibility':
#             current_resp = None
#             description_lines = []
            
#             i = 0
#             while i < len(lines):
#                 stripped_line = lines[i].strip()
                
#                 if not stripped_line:
#                     i += 1
#                     continue
                
#                 is_bullet = stripped_line.startswith('•') or stripped_line.startswith('-') or stripped_line.startswith('*')
                
#                 # If we have a current responsibility and this is a bullet, it belongs to it
#                 if is_bullet and current_resp:
#                     clean_line = re.sub(r'^[•\-\*]\s*', '', stripped_line)
#                     description_lines.append(clean_line)
#                     i += 1
#                     continue
                
#                 # Check if this looks like a responsibility title
#                 # Titles often have | separator or are substantial non-bullet lines
#                 has_separator = '|' in stripped_line
#                 starts_with_uppercase = stripped_line[0].isupper() if stripped_line else False
                
#                 is_likely_title = (
#                     not is_bullet and
#                     starts_with_uppercase and
#                     (has_separator or len(stripped_line) > 25)
#                 )
                
#                 if is_likely_title:
#                     # Save previous responsibility if exists
#                     if current_resp:
#                         full_description = ' '.join(description_lines).strip()
#                         items.append({
#                             'title': current_resp,
#                             'description': full_description if full_description else None,
#                             'raw_text': full_description if full_description else ''
#                         })
                    
#                     # Start new responsibility
#                     current_resp = stripped_line
#                     description_lines = []
#                     i += 1
#                     continue
                
#                 # If we have a current responsibility and this is not a bullet and not a title,
#                 # it's likely a continuation of the previous bullet point
#                 if current_resp:
#                     if description_lines:
#                         description_lines[-1] += ' ' + stripped_line
#                     else:
#                         description_lines.append(stripped_line)
                
#                 i += 1
            
#             # Save last responsibility
#             if current_resp:
#                 full_description = ' '.join(description_lines).strip()
#                 items.append({
#                     'title': current_resp,
#                     'description': full_description if full_description else None,
#                     'raw_text': full_description if full_description else ''
#                 })
        
#         else:
#             # For certifications and achievements - simple bullet list extraction
#             for line in lines:
#                 stripped = line.strip()
#                 if not stripped:
#                     continue
                
#                 # Remove bullet point if present
#                 is_bullet = stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('*')
#                 if is_bullet:
#                     clean_text = re.sub(r'^[•\-\*]\s*', '', stripped)
#                 else:
#                     clean_text = stripped
                
#                 if clean_text:
#                     # Try to extract name and link/details
#                     if '|' in clean_text:
#                         parts = clean_text.split('|')
#                         name = parts[0].strip()
#                         details = ' | '.join([p.strip() for p in parts[1:]])
                        
#                         items.append({
#                             'name': name,
#                             'details': details,
#                             'raw_text': clean_text
#                         })
#                     else:
#                         items.append({
#                             'name': clean_text,
#                             'details': None,
#                             'raw_text': clean_text
#                         })
        
#         return items
    
#     def _extract_technologies_from_line(self, line: str) -> List[str]:
#         """Extract technology names from a line."""
#         technologies = []
        
#         tech_keywords = [
#             'Kotlin', 'Java', 'Python', 'JavaScript', 'TypeScript', 'C', 'C++', 'Go', 'Rust',
#             'React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'Node.js', 'Express',
#             'Firebase', 'MongoDB', 'MySQL', 'PostgreSQL', 'SQLite', 'Redis', 'Cassandra',
#             'Android', 'iOS', 'Flutter', 'React Native', 'Swift',
#             'HTML', 'CSS', 'XML', 'JSON', 'YAML',
#             'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
#             'Git', 'GitHub', 'GitLab', 'Bitbucket',
#             'TensorFlow', 'PyTorch', 'Scikit-learn',
#             'Android Studio', 'VS Code', 'IntelliJ'
#         ]
        
#         tech_pattern = r'(?:Technologies|Tech Stack|Built with|Using|Tools):\s*(.+?)(?:\.|$)'
#         match = re.search(tech_pattern, line, re.IGNORECASE)
#         if match:
#             tech_text = match.group(1)
#             techs = re.split(r'[,;]|\s+and\s+', tech_text)
#             technologies.extend([t.strip() for t in techs if t.strip()])
        
#         for tech in tech_keywords:
#             if re.search(r'\b' + re.escape(tech) + r'\b', line, re.IGNORECASE):
#                 technologies.append(tech)
        
#         return technologies
    
#     # Legacy methods for backward compatibility
#     def extract_education(self, text: str) -> List[Dict]:
#         """Backward compatible education extraction."""
#         start, end = self._find_section_boundaries(text, 'education')
#         if start == -1:
#             return []
#         section_text = text[start:end].strip()
#         return self._extract_education_items(section_text)
    
#     def extract_projects(self, text: str) -> List[Dict]:
#         """Backward compatible projects extraction."""
#         start, end = self._find_section_boundaries(text, 'projects')
#         if start == -1:
#             return []
#         section_text = text[start:end].strip()
#         return self._extract_project_items(section_text)


# # Maintain backward compatibility
# class ImprovedResumeExtractor(PerfectResumeExtractor):
#     """Alias for backward compatibility."""
#     pass


# class ResumeExtractor(PerfectResumeExtractor):
#     """Alias for backward compatibility."""
#     pass



import re
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class PerfectResumeExtractor:
    """
    Universal extraction service with INTELLIGENT section boundary detection.
    Handles ALL-CAPS headers, formatted text, and ambiguous boundaries.
    """
    
    def __init__(self):
        self.degree_keywords = [
            'btech', 'b.tech', 'bachelor', 'mtech', 'm.tech', 'master',
            'be', 'b.e', 'bs', 'b.s', 'bsc', 'b.sc',
            'me', 'm.e', 'ms', 'm.s', 'msc', 'm.sc',
            'mba', 'mca', 'bca', 'phd', 'ph.d', 'diploma',
            'class 10', 'class 11', 'class 12', 'class x', 'class xi', 'class xii'
        ]
        
        # Comprehensive list of ALL possible section headers
        self.section_keywords = {
            'EDUCATION': ['education', 'academic', 'qualification'],
            'PROJECTS': ['project', 'projects'],
            'EXPERIENCE': ['experience', 'work history', 'employment', 'internship', 'internships'],
            'SKILLS': ['skill', 'skills', 'technical skills', 'core competencies'],
            'CERTIFICATIONS': ['certification', 'certifications', 'certificate', 'certificates', 'training', 'trainings'],
            'ACHIEVEMENTS': ['achievement', 'achievements', 'award', 'awards', 'honors', 'honours'],
            'RESPONSIBILITIES': ['position of responsibility', 'responsibilities', 'leadership', 'leadership activities', 
                                'extra-curricular', 'extracurricular', 'extra curricular'],
            'OBJECTIVE': ['objective', 'career objective'],
            'SUMMARY': ['summary', 'professional summary', 'profile'],
            'VOLUNTEER': ['volunteer', 'volunteering'],
            'LANGUAGES': ['language', 'languages'],
            'INTERESTS': ['interest', 'interests', 'hobbies', 'hobby'],
            'REFERENCES': ['reference', 'references'],
            'PUBLICATIONS': ['publication', 'publications', 'research'],
        }
    
    def _is_section_header(self, line: str) -> tuple[bool, str]:
        """
        Intelligently detect if a line is a section header.
        Returns (is_header, normalized_name)
        """
        line_stripped = line.strip()
        
        if not line_stripped or len(line_stripped) < 3:
            return False, ""
        
        line_lower = line_stripped.lower()
        
        # Check against all known section keywords
        for section_name, keywords in self.section_keywords.items():
            for keyword in keywords:
                # Exact match
                if line_lower == keyword:
                    return True, section_name
                
                # Match with common suffixes/prefixes
                if line_lower == keyword + 's':
                    return True, section_name
                
                # Match ALL-CAPS or Title Case variations
                # Example: "EDUCATION", "Education", "TRAINING", "TRAININGS"
                if line_lower.replace(' ', '') == keyword.replace(' ', ''):
                    return True, section_name
                
                # Handle headers with slashes like "LEADERSHIP/EXTRA-CURRICULAR ACTIVITIES"
                if '/' in line_lower and keyword in line_lower:
                    return True, section_name
                
                # Handle headers with "&" like "ACHIEVEMENTS & AWARDS"
                if '&' in line_lower and keyword in line_lower:
                    return True, section_name
        
        # Additional heuristics for section headers:
        # 1. All uppercase and 3+ words (likely a header)
        words = line_stripped.split()
        if len(words) >= 1 and all(word.isupper() or word in ['&', '/', '-', 'AND', 'OF'] for word in words):
            # This looks like a section header - try to categorize it
            for section_name, keywords in self.section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    return True, section_name
            
            # Unknown section - still a header
            return True, line_stripped.upper()
        
        return False, ""
    
    def _find_all_section_positions(self, text: str) -> List[Dict]:
        """Find all section headers using intelligent detection."""
        sections = []
        lines = text.split('\n')
        
        cumulative_pos = 0
        for i, line in enumerate(lines):
            is_header, section_name = self._is_section_header(line)
            
            if is_header:
                sections.append({
                    'name': line.strip(),
                    'normalized_name': section_name,
                    'start': cumulative_pos + len(line) + 1,  # After the header line
                    'header_start': cumulative_pos,
                    'line_number': i
                })
            
            cumulative_pos += len(line) + 1  # +1 for newline
        
        logger.info(f"Found {len(sections)} sections: {[s['name'] for s in sections]}")
        return sections
    
    def extract_all_sections(self, text: str) -> Dict:
        """
        Extract ALL sections from the resume with smart boundary detection.
        """
        all_sections = self._find_all_section_positions(text)
        
        extracted = {
            'education': [],
            'projects': [],
            'experience': [],
            'certifications': [],
            'achievements': [],
            'responsibilities': [],
            'skills': [],
            'objective': None,
            'summary': None,
            'other_sections': {}
        }
        
        for i, section in enumerate(all_sections):
            section_name = section['normalized_name']
            start = section['start']
            
            # Get end boundary (next section or end of text)
            if i + 1 < len(all_sections):
                end = all_sections[i + 1]['header_start']
            else:
                end = len(text)
            
            section_content = text[start:end].strip()
            
            # Route to appropriate extraction method
            if section_name == 'EDUCATION':
                extracted['education'] = self._extract_education_items(section_content)
            elif section_name == 'PROJECTS':
                extracted['projects'] = self._extract_project_items(section_content)
            elif section_name == 'EXPERIENCE':
                extracted['experience'] = self._extract_experience_items(section_content)
            elif section_name == 'CERTIFICATIONS':
                extracted['certifications'] = self._extract_list_items(section_content, 'certification')
            elif section_name == 'ACHIEVEMENTS':
                extracted['achievements'] = self._extract_list_items(section_content, 'achievement')
            elif section_name == 'RESPONSIBILITIES':
                extracted['responsibilities'] = self._extract_responsibility_items(section_content)
            elif section_name == 'OBJECTIVE':
                extracted['objective'] = section_content
            elif section_name == 'SUMMARY':
                extracted['summary'] = section_content
            elif section_name == 'SKILLS':
                # Store raw skills text in other_sections for reference
                extracted['other_sections'][section_name] = section_content
            else:
                # Store other sections
                extracted['other_sections'][section_name] = section_content
        
        return extracted
    
    def _extract_education_items(self, text: str) -> List[Dict]:
        """Extract education entries."""
        education_entries = []
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            line_lower = line.lower()
            is_education_start = any(keyword in line_lower for keyword in self.degree_keywords)
            
            if is_education_start:
                entry_lines = [line]
                i += 1
                
                # Collect lines until next education entry or empty lines
                while i < len(lines):
                    next_line = lines[i].strip()
                    
                    if not next_line:
                        i += 1
                        # Check if next non-empty is another education entry
                        while i < len(lines) and not lines[i].strip():
                            i += 1
                        if i < len(lines):
                            next_non_empty = lines[i].strip().lower()
                            if any(keyword in next_non_empty for keyword in self.degree_keywords):
                                break
                        continue
                    
                    next_lower = next_line.lower()
                    is_next_education = any(keyword in next_lower for keyword in self.degree_keywords)
                    
                    if is_next_education:
                        break
                    
                    entry_lines.append(next_line)
                    i += 1
                
                entry_text = '\n'.join(entry_lines)
                parsed = self._parse_education_entry(entry_text)
                if parsed:
                    education_entries.append(parsed)
            else:
                i += 1
        
        return education_entries
    
    def _parse_education_entry(self, text: str) -> Optional[Dict]:
        """Parse a single education entry."""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        if not lines:
            return None
        
        degree = lines[0]
        institution = None
        year = None
        
        # Find institution
        for line in lines[1:]:
            if re.search(r'(Institute|University|College|School|Academy)', line, re.IGNORECASE):
                institution = line
                # Remove year from institution if present
                institution = re.sub(r'\s*\d{4}\s*-?\s*\d{0,4}\s*$', '', institution).strip()
                break
        
        # Find year
        full_text = ' '.join(lines)
        year_match = re.search(r'(\d{4})\s*-\s*(\d{4})', full_text)
        if year_match:
            year = f"{year_match.group(1)}-{year_match.group(2)}"
        else:
            year_match = re.search(r'\b(\d{4})\b', full_text)
            if year_match:
                year = year_match.group(1)
        
        # Clean degree
        if institution and institution in degree:
            degree = degree.replace(institution, '').strip()
        if year:
            degree = re.sub(r'\s*\d{4}\s*-?\s*\d{0,4}\s*', '', degree).strip()
        
        return {
            'degree': degree if degree else None,
            'institution': institution,
            'year': year,
            'raw_text': text.strip()
        }
    
    def _extract_project_items(self, text: str) -> List[Dict]:
        """Extract project entries."""
        projects = []
        lines = text.split('\n')
        
        current_project = None
        description_lines = []
        technologies = []
        
        i = 0
        while i < len(lines):
            stripped_line = lines[i].strip()
            
            if not stripped_line:
                i += 1
                continue
            
            is_bullet = stripped_line.startswith('•') or stripped_line.startswith('-') or stripped_line.startswith('*')
            
            # If current project exists and this is a bullet, add to description
            if is_bullet and current_project:
                clean_line = re.sub(r'^[•\-\*]\s*', '', stripped_line)
                description_lines.append(clean_line)
                tech_from_line = self._extract_technologies_from_line(clean_line)
                technologies.extend(tech_from_line)
                i += 1
                continue
            
            # Detect project titles
            has_project_keywords = any(keyword in stripped_line.lower() for keyword in [
                'app', 'system', 'platform', 'website', 'project',
                'model', 'tool', 'game', 'calculator', 'interface',
                'portal', 'dashboard', 'application', 'bot', 'analyzer'
            ])
            
            starts_uppercase = stripped_line[0].isupper() if stripped_line else False
            is_substantial = len(stripped_line) > 20
            
            is_likely_title = (
                not is_bullet and
                starts_uppercase and
                is_substantial and
                has_project_keywords
            )
            
            if is_likely_title:
                # Save previous project
                if current_project:
                    full_description = ' '.join(description_lines).strip()
                    projects.append({
                        'title': current_project,
                        'description': full_description if full_description else None,
                        'technologies': list(set(technologies)),
                        'raw_text': full_description if full_description else ''
                    })
                
                # Start new project
                current_project = stripped_line
                if '|' in current_project:
                    current_project = current_project.split('|')[0].strip()
                current_project = re.sub(r'https?://\S+', '', current_project).strip()
                
                description_lines = []
                technologies = []
                i += 1
                continue
            
            # Add to current project's description
            if current_project and not is_bullet:
                if description_lines:
                    description_lines[-1] += ' ' + stripped_line
                else:
                    description_lines.append(stripped_line)
            
            i += 1
        
        # Save last project
        if current_project:
            full_description = ' '.join(description_lines).strip()
            projects.append({
                'title': current_project,
                'description': full_description if full_description else None,
                'technologies': list(set(technologies)),
                'raw_text': full_description if full_description else ''
            })
        
        return projects
    
    def _extract_experience_items(self, text: str) -> List[Dict]:
        """Extract experience/internship entries with SMART title detection."""
        experiences = []
        lines = text.split('\n')
        
        current_exp = None
        description_lines = []
        
        i = 0
        while i < len(lines):
            stripped_line = lines[i].strip()
            
            if not stripped_line:
                i += 1
                continue
            
            is_bullet = stripped_line.startswith('•') or stripped_line.startswith('-') or stripped_line.startswith('*')
            
            # Detect experience titles
            # Titles often have: dates, company names, OR are longer than 25 chars
            has_date = re.search(r'[A-Za-z]{3}\s+\d{2}\s*-\s*[A-Za-z]{3}\s+\d{2}', stripped_line)
            has_location = any(word in stripped_line for word in ['Kolkata', 'India', 'Bangalore', 'Mumbai', 'Delhi', 'Chennai'])
            is_substantial = len(stripped_line) > 25
            starts_uppercase = stripped_line[0].isupper() if stripped_line else False
            
            # Key experience keywords
            exp_keywords = ['internship', 'programme', 'program', 'training', 'intern', 'engineer', 'developer']
            has_exp_keyword = any(keyword in stripped_line.lower() for keyword in exp_keywords)
            
            is_likely_title = (
                not is_bullet and
                starts_uppercase and
                (has_date or (is_substantial and has_exp_keyword) or has_location)
            )
            
            if is_likely_title:
                # Save previous experience
                if current_exp:
                    full_description = ' '.join(description_lines).strip()
                    experiences.append({
                        'title': current_exp,
                        'description': full_description if full_description else None,
                        'raw_text': full_description if full_description else ''
                    })
                
                # Start new experience
                current_exp = stripped_line
                description_lines = []
                i += 1
                continue
            
            # Add bullets to current experience
            if is_bullet and current_exp:
                clean_line = re.sub(r'^[•\-\*]\s*', '', stripped_line)
                description_lines.append(clean_line)
            elif current_exp and not is_bullet:
                # Continuation of previous line
                if description_lines:
                    description_lines[-1] += ' ' + stripped_line
            
            i += 1
        
        # Save last experience
        if current_exp:
            full_description = ' '.join(description_lines).strip()
            experiences.append({
                'title': current_exp,
                'description': full_description if full_description else None,
                'raw_text': full_description if full_description else ''
            })
        
        return experiences
    
    def _extract_responsibility_items(self, text: str) -> List[Dict]:
        """Extract responsibility/leadership entries."""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Remove bullet if present
            is_bullet = stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('*')
            if is_bullet:
                clean_text = re.sub(r'^[•\-\*]\s*', '', stripped)
            else:
                clean_text = stripped
            
            if clean_text:
                items.append({
                    'title': clean_text,
                    'description': None,
                    'raw_text': clean_text
                })
        
        return items
    
    def _extract_list_items(self, text: str, item_type: str) -> List[Dict]:
        """Extract certification/achievement items."""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Remove bullet
            is_bullet = stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('*')
            if is_bullet:
                clean_text = re.sub(r'^[•\-\*]\s*', '', stripped)
            else:
                clean_text = stripped
            
            if clean_text:
                # Try to split by | or other separators
                if '|' in clean_text:
                    parts = clean_text.split('|')
                    name = parts[0].strip()
                    details = ' | '.join([p.strip() for p in parts[1:]])
                    
                    items.append({
                        'name': name,
                        'details': details,
                        'raw_text': clean_text
                    })
                else:
                    items.append({
                        'name': clean_text,
                        'details': None,
                        'raw_text': clean_text
                    })
        
        return items
    
    def _extract_technologies_from_line(self, line: str) -> List[str]:
        """Extract technology names from a line."""
        technologies = []
        
        tech_keywords = [
            'Kotlin', 'Java', 'Python', 'JavaScript', 'TypeScript', 'C', 'C++', 'Go', 'Rust',
            'React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'Node.js', 'Express',
            'Firebase', 'MongoDB', 'MySQL', 'PostgreSQL', 'SQLite', 'Redis',
            'Android', 'iOS', 'Flutter', 'React Native', 'Swift',
            'HTML', 'CSS', 'XML', 'JSON', 'Tanner', 'Microwind', 'Modelsim', 'FPGA'
        ]
        
        for tech in tech_keywords:
            if re.search(r'\b' + re.escape(tech) + r'\b', line, re.IGNORECASE):
                technologies.append(tech)
        
        return technologies