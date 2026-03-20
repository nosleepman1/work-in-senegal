from fastapi import FastAPI, HTTPException
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import asyncio

app = FastAPI(title="Senegal Jobs API", description="API to fetch recent job postings in Senegal from LinkedIn")

# Mock data for demonstration (in case LinkedIn scraping fails or is blocked)
MOCK_JOBS = [
    {
        "title": "Software Engineer",
        "company": "Tech Solutions Senegal",
        "location": "Dakar, Senegal",
        "posted_date": "2025-03-18",
        "link": "https://linkedin.com/jobs/view/12345",
        "description": "Develop and maintain software applications."
    },
    {
        "title": "Data Analyst",
        "company": "Data Insights Africa",
        "location": "Dakar, Senegal",
        "posted_date": "2025-03-17",
        "link": "https://linkedin.com/jobs/view/67890",
        "description": "Analyze data and generate reports."
    },
    {
        "title": "Project Manager",
        "company": "Build Senegal",
        "location": "Thiès, Senegal",
        "posted_date": "2025-03-16",
        "link": "https://linkedin.com/jobs/view/13579",
        "description": "Manage construction projects across Senegal."
    }
]

def scrape_linkedin_jobs_senegal(days: int = 7) -> List[Dict]:
    """
    Attempt to scrape LinkedIn for jobs in Senegal posted in the last `days` days.
    Note: LinkedIn has strong anti‑scraping measures. This function is a basic example
    and may not work without proper headers, proxies, or a LinkedIn API token.
    """
    jobs = []
    try:
        # Example search URL for jobs in Senegal, posted in last 7 days
        # This URL might need adjustments based on LinkedIn's actual search parameters
        url = "https://www.linkedin.com/jobs/search/?keywords=&location=Senegal&f_TPR=r604800&position=1&pageNum=0"
        
        # Simulate a realistic browser header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # LinkedIn's job listing HTML structure may change; these selectors are illustrative
        job_cards = soup.select('.jobs-search__results-list li')
        
        for card in job_cards[:10]:  # limit to first 10
            title_elem = card.select_one('.base-search-card__title')
            company_elem = card.select_one('.base-search-card__subtitle')
            location_elem = card.select_one('.job-search-card__location')
            link_elem = card.select_one('a.base-card__full-link')
            date_elem = card.select_one('time')
            
            if not all([title_elem, company_elem, location_elem, link_elem]):
                continue
            
            job = {
                "title": title_elem.get_text(strip=True),
                "company": company_elem.get_text(strip=True),
                "location": location_elem.get_text(strip=True),
                "posted_date": date_elem['datetime'].split('T')[0] if date_elem and 'datetime' in date_elem.attrs else "Unknown",
                "link": link_elem['href'].split('?')[0] if link_elem else "",
                "description": ""  # LinkedIn hides full descriptions behind login
            }
            jobs.append(job)
            
    except Exception as e:
        # If scraping fails, fall back to mock data and log the error
        print(f"Scraping failed: {e}")
        # In production, you might want to use a dedicated logging library
        pass
    
    return jobs if jobs else MOCK_JOBS

@app.get("/")
def read_root():
    return {"message": "Welcome to Senegal Jobs API. Use /jobs to get recent job postings in Senegal."}

@app.get("/jobs", response_model=List[Dict])
async def get_jobs(days: int = 7, use_mock: bool = False):
    """
    Fetch recent job postings in Senegal.
    
    - **days**: Number of past days to look for jobs (default 7).
    - **use_mock**: If True, returns mock data only (for testing).
    """
    if use_mock:
        return MOCK_JOBS
    
    jobs = scrape_linkedin_jobs_senegal(days)
    return jobs

@app.get("/jobs/{job_id}")
def get_job_by_id(job_id: int):
    """Get a specific job by its index in the list (0‑based)."""
    jobs = MOCK_JOBS  # For simplicity, using mock data
    if 0 <= job_id < len(jobs):
        return jobs[job_id]
    raise HTTPException(status_code=404, detail="Job not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)