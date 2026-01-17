# import logging
# from typing import Dict, List
# from models.response_models import SectionScore, SkillsAnalysis, SectionWarning

# logger = logging.getLogger(__name__)


# class ATSScorer:
#     """Calculate final ATS score and generate recommendations."""
    
#     def __init__(self):
#         # Score thresholds
#         self.thresholds = {
#             'excellent': 90,
#             'good': 75,
#             'fair': 60,
#             'poor': 45
#         }
    
#     def _get_status(self, score: int) -> str:
#         """Get status classification based on score."""
#         if score >= self.thresholds['excellent']:
#             return "Excellent - Highly ATS Optimized"
#         elif score >= self.thresholds['good']:
#             return "Good - ATS Shortlist Ready"
#         elif score >= self.thresholds['fair']:
#             return "Fair - Needs Minor Improvements"
#         elif score >= self.thresholds['poor']:
#             return "Poor - Needs Significant Improvements"
#         else:
#             return "Very Poor - Likely ATS Rejected"
    
#     def _generate_recommendations(
#         self,
#         contact_result: Dict,
#         formatting_result: Dict,
#         grammar_result: Dict,
#         skills_result: Dict
#     ) -> List[str]:
#         """Generate actionable recommendations based on analysis."""
#         recommendations = []
        
#         # Contact info recommendations (High Priority)
#         if contact_result['score'] < contact_result['max_score']:
#             for issue in contact_result['issues']:
#                 if 'Email' in issue:
#                     recommendations.append("✉️ HIGH PRIORITY: Add a professional email address")
#                 elif 'Phone' in issue:
#                     recommendations.append("📱 HIGH PRIORITY: Include a valid phone number")
#                 elif 'LinkedIn' in issue:
#                     recommendations.append("🔗 Add your LinkedIn profile URL")
#                 elif 'GitHub' in issue and skills_result['total_resume_skills'] > 5:
#                     recommendations.append("💻 Add your GitHub profile")
        
#         # Skills recommendations (Critical Priority)
#         missing_count = len(skills_result.get('missing_skills', []))
#         match_percentage = skills_result.get('match_percentage', 100)
        
#         if match_percentage < 50:
#             recommendations.insert(0, 
#                 f"🚨 CRITICAL: Only {match_percentage:.0f}% skills match - Resume may be auto-rejected!"
#             )
#         elif match_percentage < 70:
#             recommendations.insert(0,
#                 f"⚠️ WARNING: {match_percentage:.0f}% skills match - Add more relevant skills"
#             )
        
#         if missing_count > 0:
#             # Separate technical and general missing skills
#             missing_technical = skills_result.get('missing_technical', [])
#             missing_general = skills_result.get('missing_general', [])
            
#             if missing_technical:
#                 top_missing_tech = missing_technical[:5]
#                 recommendations.append(
#                     f"🎯 Add technical skills: {', '.join(top_missing_tech)}"
#                 )
            
#             if missing_general:
#                 top_missing_general = missing_general[:3]
#                 recommendations.append(
#                     f"📋 Add required keywords/experience: {', '.join(top_missing_general)}"
#                 )
        
#         # Formatting recommendations (High Priority)
#         if formatting_result['score'] < formatting_result['max_score']:
#             for issue in formatting_result['issues']:
#                 if 'Education' in issue:
#                     recommendations.append("🎓 CRITICAL: Add Education section")
#                 elif 'Experience' in issue or 'Projects' in issue:
#                     recommendations.append("💼 CRITICAL: Add Experience or Projects section")
#                 elif 'Skills' in issue:
#                     recommendations.append("⚡ CRITICAL: Add dedicated Skills section")
#                 elif 'bullet' in issue:
#                     recommendations.append("📝 Use bullet points for better ATS parsing")
#                 elif 'dates' in issue:
#                     recommendations.append("📅 Include dates (MM/YYYY) for all experiences")
        
#         # Grammar recommendations (Medium Priority)
#         if grammar_result['score'] < grammar_result['max_score']:
#             error_count = len(grammar_result.get('spelling_errors', []))
#             if error_count > 3:
#                 recommendations.append(
#                     f"✏️ Fix {error_count} spelling errors before submitting"
#                 )
        
#         # General guidance based on total score
#         total_score = (
#             contact_result['score'] +
#             formatting_result['score'] +
#             grammar_result['score'] +
#             skills_result['score']
#         )
        
#         max_total = (
#             contact_result['max_score'] +
#             formatting_result['max_score'] +
#             grammar_result['max_score'] +
#             skills_result['max_score']
#         )
        
#         normalized_score = int((total_score / max_total) * 100)
        
#         if normalized_score >= 90:
#             recommendations.insert(0, "✅ Excellent! Resume is highly optimized for ATS")
#         elif normalized_score >= 75:
#             recommendations.insert(0, "👍 Good resume! Address minor issues to boost ATS score")
#         elif normalized_score >= 60:
#             recommendations.insert(0, "⚡ Resume needs improvements to pass ATS filters")
#         else:
#             recommendations.insert(0, "⚠️ URGENT: Major improvements needed to avoid auto-rejection")
        
#         # If no specific recommendations, add generic advice
#         if len(recommendations) == 1:  # Only has the overall message
#             recommendations.append("💡 Consider tailoring your resume more closely to this job")
        
#         return recommendations
    
#     def calculate_score(
#         self,
#         contact_result: Dict,
#         formatting_result: Dict,
#         grammar_result: Dict,
#         skills_result: Dict
#     ) -> Dict:
#         """
#         Calculate final ATS score and compile complete analysis.
        
#         Returns:
#             Complete analysis with score, status, and recommendations
#         """
#         # Calculate total score
#         total_score = (
#             contact_result['score'] +
#             formatting_result['score'] +
#             grammar_result['score'] +
#             skills_result['score']
#         )
        
#         max_total = (
#             contact_result['max_score'] +
#             formatting_result['max_score'] +
#             grammar_result['max_score'] +
#             skills_result['max_score']
#         )
        
#         # Normalize to 0-100 scale
#         normalized_score = int((total_score / max_total) * 100)
        
#         # Get status
#         status = self._get_status(normalized_score)
        
#         # Generate recommendations
#         recommendations = self._generate_recommendations(
#             contact_result, formatting_result, grammar_result, skills_result
#         )
        
#         # Build section scores with warnings
#         section_scores = {
#             'contact_info': SectionScore(
#                 score=contact_result['score'],
#                 max_score=contact_result['max_score'],
#                 percentage=contact_result['percentage'],
#                 issues=contact_result['issues'],
#                 warnings=[SectionWarning(**w) for w in contact_result.get('warnings', [])]
#             ),
#             'formatting': SectionScore(
#                 score=formatting_result['score'],
#                 max_score=formatting_result['max_score'],
#                 percentage=formatting_result['percentage'],
#                 issues=formatting_result['issues'],
#                 warnings=[SectionWarning(**w) for w in formatting_result.get('warnings', [])]
#             ),
#             'skills_match': SectionScore(
#                 score=skills_result['score'],
#                 max_score=skills_result['max_score'],
#                 percentage=skills_result['percentage'],
#                 issues=[],
#                 warnings=[]
#             ),
#             'spelling_grammar': SectionScore(
#                 score=grammar_result['score'],
#                 max_score=grammar_result['max_score'],
#                 percentage=grammar_result['percentage'],
#                 issues=grammar_result['issues'],
#                 warnings=[SectionWarning(**w) for w in grammar_result.get('warnings', [])]
#             )
#         }
        
#         # Build skills analysis
#         skills_analysis = SkillsAnalysis(
#             resume_skills=skills_result['resume_skills'],
#             job_skills=skills_result['job_skills'],
#             matched_skills=skills_result['matched_skills'],
#             missing_skills=skills_result['missing_skills'],
#             match_percentage=skills_result['match_percentage']
#         )
        
#         # Additional details
#         details = {
#             'contact_info_found': contact_result['found'],
#             'sections_found': formatting_result.get('sections_found', []),
#             'spelling_errors': grammar_result.get('spelling_errors', []),
#             'skills_categorized': skills_result.get('resume_skills_categorized', {}),
#             'skills_breakdown': {
#                 'matched_technical': skills_result.get('matched_technical', []),
#                 'matched_general': skills_result.get('matched_general', []),
#                 'missing_technical': skills_result.get('missing_technical', []),
#                 'missing_general': skills_result.get('missing_general', []),
#                 'job_general_requirements': skills_result.get('job_general_requirements', [])
#             },
#             'total_score_breakdown': {
#                 'contact': contact_result['score'],
#                 'formatting': formatting_result['score'],
#                 'skills': skills_result['score'],
#                 'grammar': grammar_result['score'],
#                 'total': total_score,
#                 'max_possible': max_total
#             }
#         }
        
#         logger.info(f"Final ATS Score: {normalized_score}/100 - {status}")
        
#         return {
#             'ats_score': normalized_score,
#             'resume_status': status,
#             'section_scores': section_scores,
#             'skills_analysis': skills_analysis,
#             'recommendations': recommendations,
#             'details': details
#         }




import logging
from typing import Dict, List
from models.response_models import SectionScore, SkillsAnalysis, SectionWarning

logger = logging.getLogger(__name__)


class ATSScorer:
    """Calculate final ATS score and generate recommendations."""
    
    def __init__(self):
        # Score thresholds
        self.thresholds = {
            'excellent': 90,
            'good': 75,
            'fair': 60,
            'poor': 45
        }
    
    def _get_status(self, score: int) -> str:
        """Get status classification based on score."""
        if score >= self.thresholds['excellent']:
            return "Excellent - Highly ATS Optimized"
        elif score >= self.thresholds['good']:
            return "Good - ATS Shortlist Ready"
        elif score >= self.thresholds['fair']:
            return "Fair - Needs Minor Improvements"
        elif score >= self.thresholds['poor']:
            return "Poor - Needs Significant Improvements"
        else:
            return "Very Poor - Likely ATS Rejected"
    
    def _convert_warnings_to_strings(self, warnings_data):
        """Convert warnings to string list for SectionScore."""
        if not warnings_data:
            return []
        
        result = []
        for w in warnings_data:
            try:
                if isinstance(w, SectionWarning):
                    # Convert SectionWarning object to string message
                    result.append(w.message)
                elif isinstance(w, dict):
                    # Convert dict to string (use message field if exists)
                    result.append(w.get('message', str(w)))
                elif isinstance(w, str):
                    # Already a string
                    result.append(w)
                else:
                    # Convert anything else to string
                    logger.warning(f"Invalid warning data type: {type(w)}, converting to string")
                    result.append(str(w))
            except Exception as e:
                logger.error(f"Error converting warning to string: {e}, warning data: {w}")
                # Skip this warning if conversion fails
                continue
        return result
    
    def _generate_recommendations(
        self,
        contact_result: Dict,
        formatting_result: Dict,
        grammar_result: Dict,
        skills_result: Dict
    ) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # Contact info recommendations (High Priority)
        if contact_result['score'] < contact_result['max_score']:
            for issue in contact_result['issues']:
                if 'Email' in issue:
                    recommendations.append("✉️ HIGH PRIORITY: Add a professional email address")
                elif 'Phone' in issue:
                    recommendations.append("📱 HIGH PRIORITY: Include a valid phone number")
                elif 'LinkedIn' in issue:
                    recommendations.append("🔗 Add your LinkedIn profile URL")
                elif 'GitHub' in issue and skills_result['total_resume_skills'] > 5:
                    recommendations.append("💻 Add your GitHub profile")
        
        # Skills recommendations (Critical Priority)
        missing_count = len(skills_result.get('missing_skills', []))
        match_percentage = skills_result.get('match_percentage', 100)
        
        if match_percentage < 50:
            recommendations.insert(0, 
                f"🚨 CRITICAL: Only {match_percentage:.0f}% skills match - Resume may be auto-rejected!"
            )
        elif match_percentage < 70:
            recommendations.insert(0,
                f"⚠️ WARNING: {match_percentage:.0f}% skills match - Add more relevant skills"
            )
        
        if missing_count > 0:
            # Separate technical and general missing skills
            missing_technical = skills_result.get('missing_technical', [])
            missing_general = skills_result.get('missing_general', [])
            
            if missing_technical:
                top_missing_tech = missing_technical[:5]
                recommendations.append(
                    f"🎯 Add technical skills: {', '.join(top_missing_tech)}"
                )
            
            if missing_general:
                top_missing_general = missing_general[:3]
                recommendations.append(
                    f"📋 Add required keywords/experience: {', '.join(top_missing_general)}"
                )
        
        # Formatting recommendations (High Priority)
        if formatting_result['score'] < formatting_result['max_score']:
            for issue in formatting_result['issues']:
                if 'Education' in issue:
                    recommendations.append("🎓 CRITICAL: Add Education section")
                elif 'Experience' in issue or 'Projects' in issue:
                    recommendations.append("💼 CRITICAL: Add Experience or Projects section")
                elif 'Skills' in issue:
                    recommendations.append("⚡ CRITICAL: Add dedicated Skills section")
                elif 'bullet' in issue:
                    recommendations.append("📝 Use bullet points for better ATS parsing")
                elif 'dates' in issue:
                    recommendations.append("📅 Include dates (MM/YYYY) for all experiences")
        
        # Grammar recommendations (Medium Priority)
        if grammar_result['score'] < grammar_result['max_score']:
            error_count = len(grammar_result.get('spelling_errors', []))
            if error_count > 3:
                recommendations.append(
                    f"✏️ Fix {error_count} spelling errors before submitting"
                )
        
        # General guidance based on total score
        total_score = (
            contact_result['score'] +
            formatting_result['score'] +
            grammar_result['score'] +
            skills_result['score']
        )
        
        max_total = (
            contact_result['max_score'] +
            formatting_result['max_score'] +
            grammar_result['max_score'] +
            skills_result['max_score']
        )
        
        normalized_score = int((total_score / max_total) * 100)
        
        if normalized_score >= 90:
            recommendations.insert(0, "✅ Excellent! Resume is highly optimized for ATS")
        elif normalized_score >= 75:
            recommendations.insert(0, "👍 Good resume! Address minor issues to boost ATS score")
        elif normalized_score >= 60:
            recommendations.insert(0, "⚡ Resume needs improvements to pass ATS filters")
        else:
            recommendations.insert(0, "⚠️ URGENT: Major improvements needed to avoid auto-rejection")
        
        # If no specific recommendations, add generic advice
        if len(recommendations) == 1:  # Only has the overall message
            recommendations.append("💡 Consider tailoring your resume more closely to this job")
        
        return recommendations
    
    def calculate_score(
        self,
        contact_result: Dict,
        formatting_result: Dict,
        grammar_result: Dict,
        skills_result: Dict
    ) -> Dict:
        """
        Calculate final ATS score and compile complete analysis.
        
        Returns:
            Complete analysis with score, status, and recommendations
        """
        # Calculate total score
        total_score = (
            contact_result['score'] +
            formatting_result['score'] +
            grammar_result['score'] +
            skills_result['score']
        )
        
        max_total = (
            contact_result['max_score'] +
            formatting_result['max_score'] +
            grammar_result['max_score'] +
            skills_result['max_score']
        )
        
        # Normalize to 0-100 scale
        normalized_score = int((total_score / max_total) * 100)
        
        # Get status
        status = self._get_status(normalized_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            contact_result, formatting_result, grammar_result, skills_result
        )
        
        # Build section scores - CONVERT WARNINGS TO STRINGS
        section_scores = {
            'contact_info': SectionScore(
                score=contact_result['score'],
                max_score=contact_result['max_score'],
                percentage=contact_result['percentage'],
                issues=contact_result['issues'],
                warnings=self._convert_warnings_to_strings(contact_result.get('warnings', []))
            ),
            'formatting': SectionScore(
                score=formatting_result['score'],
                max_score=formatting_result['max_score'],
                percentage=formatting_result['percentage'],
                issues=formatting_result['issues'],
                warnings=self._convert_warnings_to_strings(formatting_result.get('warnings', []))
            ),
            'skills_match': SectionScore(
                score=skills_result['score'],
                max_score=skills_result['max_score'],
                percentage=skills_result['percentage'],
                issues=[],
                warnings=[]
            ),
            'spelling_grammar': SectionScore(
                score=grammar_result['score'],
                max_score=grammar_result['max_score'],
                percentage=grammar_result['percentage'],
                issues=grammar_result['issues'],
                warnings=self._convert_warnings_to_strings(grammar_result.get('warnings', []))
            )
        }
        
        # Build skills analysis
        skills_analysis = SkillsAnalysis(
            resume_skills=skills_result['resume_skills'],
            job_skills=skills_result['job_skills'],
            matched_skills=skills_result['matched_skills'],
            missing_skills=skills_result['missing_skills'],
            match_percentage=skills_result['match_percentage']
        )
        
        # Additional details
        details = {
            'contact_info_found': contact_result['found'],
            'sections_found': formatting_result.get('sections_found', []),
            'spelling_errors': grammar_result.get('spelling_errors', []),
            'skills_categorized': skills_result.get('resume_skills_categorized', {}),
            'skills_breakdown': {
                'matched_technical': skills_result.get('matched_technical', []),
                'matched_general': skills_result.get('matched_general', []),
                'missing_technical': skills_result.get('missing_technical', []),
                'missing_general': skills_result.get('missing_general', []),
                'job_general_requirements': skills_result.get('job_general_requirements', [])
            },
            'total_score_breakdown': {
                'contact': contact_result['score'],
                'formatting': formatting_result['score'],
                'skills': skills_result['score'],
                'grammar': grammar_result['score'],
                'total': total_score,
                'max_possible': max_total
            }
        }
        
        logger.info(f"Final ATS Score: {normalized_score}/100 - {status}")
        
        return {
            'ats_score': normalized_score,
            'resume_status': status,
            'section_scores': section_scores,
            'skills_analysis': skills_analysis,
            'recommendations': recommendations,
            'details': details
        }