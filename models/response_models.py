from pydantic import BaseModel
from typing import List, Optional, Dict


class ContactInfo(BaseModel):
    has_email: bool
    has_phone: bool
    has_linkedin: bool
    has_github: bool
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class EducationEntry(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    raw_text: str


class ProjectEntry(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = []
    raw_text: str


class ExperienceEntry(BaseModel):
    """Model for work experience/internship entries."""
    title: Optional[str] = None
    description: Optional[str] = None
    raw_text: str


class ListItem(BaseModel):
    """Model for certifications and achievements."""
    name: str
    details: Optional[str] = None
    raw_text: str


class ResponsibilityEntry(BaseModel):
    """Model for position of responsibility entries (similar to projects)."""
    title: Optional[str] = None
    description: Optional[str] = None
    raw_text: str


class ExtractedData(BaseModel):
    contact_info: ContactInfo
    education: List[EducationEntry] = []
    projects: List[ProjectEntry] = []
    experience: List[ExperienceEntry] = []
    certifications: List[ListItem] = []
    achievements: List[ListItem] = []
    responsibilities: List[ResponsibilityEntry] = []
    skills: List[str] = []
    objective: Optional[str] = None
    summary: Optional[str] = None
    other_sections: Dict[str, str] = {}


class SectionWarning(BaseModel):
    """Model for section warnings with point deductions."""
    message: str
    points_deducted: int


class SectionScore(BaseModel):
    score: int
    max_score: int
    percentage: float
    issues: List[str] = []
    warnings: List[str] = []


class SkillsAnalysis(BaseModel):
    resume_skills: List[str]
    job_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float


class AnalysisResponse(BaseModel):
    ats_score: int
    resume_status: str
    section_scores: Dict[str, SectionScore]
    skills_analysis: SkillsAnalysis
    recommendations: List[str]
    extracted_data: ExtractedData
    details: Dict