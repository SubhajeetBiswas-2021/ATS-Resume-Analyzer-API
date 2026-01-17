from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import logging

# Import services
from services.pdf_service import extract_text_from_pdf
from services.skills_service import SkillsAnalyzer
from services.contact_service import ContactInfoChecker
from services.formatting_service import FormattingChecker
from services.grammar_service import GrammarChecker
from services.scoring_service import ATSScorer
from services.extraction_service import PerfectResumeExtractor
from models.response_models import (
    AnalysisResponse, 
    ContactInfo, 
    EducationEntry, 
    ProjectEntry,
    ExperienceEntry,
    ListItem,
    ResponsibilityEntry,
    ExtractedData
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ATS Resume Analyzer API",
    description="Analyze resumes for ATS compatibility with complete data extraction",
    version="4.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "ATS Resume Analyzer API v4.0",
        "status": "running",
        "features": [
            "ATS Score Analysis",
            "Complete Resume Data Extraction",
            "Contact Information",
            "Education (Separate Entries)",
            "Projects (Grouped Bullet Points)",
            "Experience/Internships",
            "Certifications",
            "Achievements & Awards",
            "Position of Responsibility",
            "Skills Matching with Job Description",
            "All Other Resume Sections"
        ],
        "endpoints": {
            "analyze": "/analyze - POST - Analyze resume against job description",
            "health": "/health - GET - API health check"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "4.0.0"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume PDF file"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyze a resume for ATS compatibility and extract ALL structured data.
    
    Returns:
    - ATS score (0-100)
    - Status classification
    - Detailed section scores with warnings
    - Skills analysis
    - Complete extracted data from ALL resume sections:
      * Contact info
      * Education
      * Projects
      * Experience/Internships
      * Certifications
      * Achievements & Awards
      * Position of Responsibility
      * Skills
      * Objective/Summary
      * Any other sections found
    - Actionable recommendations
    """
    try:
        # Validate file type
        if not resume.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        logger.info(f"Analyzing resume: {resume.filename}")
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(resume.file)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Initialize analyzers
        skills_analyzer = SkillsAnalyzer()
        contact_checker = ContactInfoChecker()
        formatting_checker = FormattingChecker()
        grammar_checker = GrammarChecker()
        scorer = ATSScorer()
        extractor = PerfectResumeExtractor()
        
        # Perform all checks
        contact_result = contact_checker.check(resume_text)
        formatting_result = formatting_checker.check(resume_text)
        grammar_result = grammar_checker.check(resume_text)
        skills_result = skills_analyzer.analyze(resume_text, job_description)
        
        # Extract ALL structured data from resume
        all_sections = extractor.extract_all_sections(resume_text)
        
        # Build contact info object
        contact_info = ContactInfo(
            has_email=contact_result['found']['has_email'],
            has_phone=contact_result['found']['has_phone'],
            has_linkedin=contact_result['found']['has_linkedin'],
            has_github=contact_result['found']['has_github'],
            email=contact_result['found'].get('email'),
            phone=contact_result['found'].get('phone'),
            linkedin=contact_result['found'].get('linkedin'),
            github=contact_result['found'].get('github')
        )
        
        # Build education entries
        education_entries = [
            EducationEntry(
                degree=edu.get('degree'),
                institution=edu.get('institution'),
                year=edu.get('year'),
                raw_text=edu.get('raw_text', '')
            ) for edu in all_sections['education']
        ]
        
        # Build project entries
        project_entries = [
            ProjectEntry(
                title=proj.get('title'),
                description=proj.get('description'),
                technologies=proj.get('technologies', []),
                raw_text=proj.get('raw_text', '')
            ) for proj in all_sections['projects']
        ]
        
        # Build experience entries
        experience_entries = [
            ExperienceEntry(
                title=exp.get('title'),
                description=exp.get('description'),
                raw_text=exp.get('raw_text', '')
            ) for exp in all_sections['experience']
        ]
        
        # Build certification entries
        certification_entries = [
            ListItem(
                name=cert.get('name', ''),
                details=cert.get('details'),
                raw_text=cert.get('raw_text', '')
            ) for cert in all_sections['certifications']
        ]
        
        # Build achievement entries
        achievement_entries = [
            ListItem(
                name=ach.get('name', ''),
                details=ach.get('details'),
                raw_text=ach.get('raw_text', '')
            ) for ach in all_sections['achievements']
        ]
        
        # Build responsibility entries
        responsibility_entries = [
            ResponsibilityEntry(
                title=resp.get('title'),
                description=resp.get('description'),
                raw_text=resp.get('raw_text', '')
            ) for resp in all_sections['responsibilities']
        ]
        
        # Build complete extracted data object
        extracted_data = ExtractedData(
            contact_info=contact_info,
            education=education_entries,
            projects=project_entries,
            experience=experience_entries,
            certifications=certification_entries,
            achievements=achievement_entries,
            responsibilities=responsibility_entries,
            skills=skills_result['resume_skills'],
            objective=all_sections.get('objective'),
            summary=all_sections.get('summary'),
            other_sections=all_sections.get('other_sections', {})
        )
        
        # Calculate final score
        final_result = scorer.calculate_score(
            contact_result=contact_result,
            formatting_result=formatting_result,
            grammar_result=grammar_result,
            skills_result=skills_result
        )
        
        # Add extracted data to the result
        final_result['extracted_data'] = extracted_data
        
        # Log extraction summary
        logger.info(f"Analysis complete. Final score: {final_result['ats_score']}")
        logger.info(f"Extracted sections:")
        logger.info(f"  - Education: {len(education_entries)} entries")
        logger.info(f"  - Projects: {len(project_entries)} entries")
        logger.info(f"  - Experience: {len(experience_entries)} entries")
        logger.info(f"  - Certifications: {len(certification_entries)} entries")
        logger.info(f"  - Achievements: {len(achievement_entries)} entries")
        logger.info(f"  - Responsibilities: {len(responsibility_entries)} entries")
        logger.info(f"  - Other sections: {len(all_sections.get('other_sections', {}))}")
        
        return final_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)