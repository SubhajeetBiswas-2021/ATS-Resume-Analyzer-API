# ATS Resume Analyzer API
**Version 4.0**

A production-grade ATS (Applicant Tracking System) Resume Analyzer built using **FastAPI**.
It evaluates resumes the way real ATS systems do, using structured parsing, weighted scoring,
and job-specific skill matching.

---

## Features

- ATS Score (0–100) with realistic normalization
- Job-specific skills matching (technical and general)
- Intelligent resume section extraction
- Resume-safe grammar and spelling analysis
- Priority-based actionable recommendations
- OpenAPI / Swagger documentation

---

## ATS Scoring Overview

### Total ATS Score: 100 Points

Internally, the system calculates a raw score out of **85 points** and normalizes it to a **0–100 scale**.

```python
normalized_score = int((total_score / max_total) * 100)    
```
## Score Distribution (Raw Score: 85 Points)

| Component                | Points | Weight |
| ------------------------ | ------ | ------ |
| Contact Information      | 15     | 17.6%  |
| Formatting and Structure | 25     | 29.4%  |
| Spelling and Grammar     | 10     | 11.8%  |
| Skills Matching          | 35     | 41.2%  |
| Total                    | 85     | 100%   |

## Contact Information (15 Points – Critical)

Missing essential contact details results in immediate ATS penalties.

| Field    | Penalty | Priority                          |
| -------- | ------- | --------------------------------- |
| Email    | -5      | Critical                          |
| Phone    | -5      | Critical                          |
| LinkedIn | -3      | Recommended                       |
| GitHub   | -2      | Recommended for technical resumes |


## Formatting and Structure (25 Points)

Evaluates whether the resume follows an ATS-friendly structure.

• Education section missing: -7

• Both Experience and Projects missing: -8

• Skills section missing: -6

• No bullet points detected: -2

• Missing dates or timeline: -2

At least one of Experience or Projects must be present.


## Spelling and Grammar (10 Points)

Grammar analysis is resume-safe and context-aware.
| Errors Found     | Score           |
| ---------------- | --------------- |
| 0–2 errors       | 10 (no penalty) |
| 3–5 errors       | 8               |
| 6 or more errors | 7               |

• Maximum grammar penalty is capped at -3 points

• Technical terms, acronyms, URLs, emails, and dates are ignored

## Skills Matching (35 Points – Most Critical)

Skills are matched directly against the job description, not generic keyword lists.

Match Percentage to Score Mapping
| Match Percentage | Score |
| ---------------- | ----- |
| 90% or higher    | 35    |
| 75–89%           | 29    |
| 60–74%           | 24    |
| 40–59%           | 17    |
| 20–39%           | 10    |
| Below 20%        | 5     |

Skills matching contributes the highest weight to the total ATS score.

## Smart Skills Detection

The system prevents common ATS false positives:

• Strict boundary detection for short skills such as C, Go, and R

• Context-aware matching (Go is not equal to going)

• Separation of technical skills and general job requirements

• Multi-word phrase detection such as system design and team leadership

## Resume Section Extraction

The analyzer intelligently extracts all resume sections, including:

• Contact Information

• Education

• Projects

• Experience and Internships

• Certifications

• Achievements and Awards

• Positions of Responsibility

• Skills

• Objective and Summary

• Custom or unknown sections

Supported formats:

• ALL CAPS headers

• Slash-based headers such as LEADERSHIP / ACTIVITIES

• Mixed and non-standard formatting

## ATS Score Classification
| Score Range | Status                                |
| ----------- | ------------------------------------- |
| 90–100      | Excellent – Highly ATS Optimized      |
| 75–89       | Good – ATS Shortlist Ready            |
| 60–74       | Fair – Needs Minor Improvements       |
| 45–59       | Poor – Needs Significant Improvements |
| 0–44        | Very Poor – Likely ATS Rejected       |

## Maximum Achievable Score

To achieve a perfect ATS score of 100 / 100, a resume must meet:

• Contact Information: 15 / 15

• Formatting and Structure: 25 / 25

• Spelling and Grammar: 10 / 10

• Skills Match (90% or higher): 35 / 35

Raw Score: 85 / 85
Final ATS Score: 100 / 100

## API Usage
Analyze Resume

## POST  
```API
/analyze
```
Form Data

• resume – PDF file

• job_description – text

Response Includes

• ATS score and status

• Section-wise score breakdown

• Skills match analysis

• Extracted resume data

• Actionable recommendations

## Local Development

Install dependencies:
```python
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Run the server:
```python
uvicorn main:app --reload
```

API documentation:
```TestingSite Swagger
http://localhost:8000/docs
```
## Tech Stack

• FastAPI

• Pydantic v2

• pdfplumber

• PySpellChecker

• Regex-based NLP

• spaCy (optional)

## Use Cases

• ATS simulation and research

• Resume optimization platforms

• Job portals

## Final Note

This ATS Resume Analyzer is logic-driven, explainable, and realistic.
It reflects how real ATS systems silently reject resumes and explains why.

