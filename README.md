# Senegal Jobs API

A FastAPI-based web service that fetches recent job postings in Senegal from LinkedIn (with mock data fallback).

## Features

- **FastAPI** framework with automatic OpenAPI documentation
- **Web scraping** of LinkedIn job listings (Senegal location)
- **Mock data** fallback when scraping is blocked or fails
- **Docker container** ready for deployment
- **RESTful endpoints** for retrieving job information

## Project Structure

```
fastapi-jobs/
├── app.py              # FastAPI application with routes
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── .dockerignore      # Files to exclude from Docker build
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## API Endpoints

### `GET /`
Welcome message.

**Response:**
```json
{"message": "Welcome to Senegal Jobs API. Use /jobs to get recent job postings in Senegal."}
```

### `GET /jobs`
Fetch recent job postings in Senegal.

**Query Parameters:**
- `days` (optional): Number of past days to look for jobs (default: 7)
- `use_mock` (optional): If `true`, returns mock data only (default: `false`)

**Response:**
```json
[
  {
    "title": "Software Engineer",
    "company": "Tech Solutions Senegal",
    "location": "Dakar, Senegal",
    "posted_date": "2025-03-18",
    "link": "https://linkedin.com/jobs/view/12345",
    "description": "Develop and maintain software applications."
  },
  ...
]
```

### `GET /jobs/{job_id}`
Get a specific job by its index in the mock data list (0‑based).

## Setup and Installation

### Using Docker (Recommended)

1. **Build the Docker image:**
   ```bash
   docker build -t senegal-jobs-api .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 senegal-jobs-api
   ```

3. **Access the API:**
   - OpenAPI docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - API root: http://localhost:8000/

### Local Development

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn app:app --reload
   ```

## Configuration

The application attempts to scrape LinkedIn for jobs in Senegal. However, LinkedIn has strong anti‑scraping measures. The scraping function includes:

- A realistic `User‑Agent` header
- Timeout handling
- BeautifulSoup4 for HTML parsing

If scraping fails (due to blocks, network issues, or HTML structure changes), the API automatically falls back to mock data.

## Deployment

### Docker Compose (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
```

Then run:
```bash
docker-compose up
```

### Cloud Platforms

The containerized application can be deployed to:
- **AWS ECS/EKS**
- **Google Cloud Run**
- **Azure Container Instances**
- **Heroku** (with Docker support)
- **Railway** or **Render**

## Limitations

1. **LinkedIn Scraping**: This is a basic demonstration. Production use would require:
   - Official LinkedIn API access
   - Proper authentication
   - Respect for LinkedIn's Terms of Service
   - Robust error handling and rate limiting

2. **Data Freshness**: The mock data is static. Real‑time job listings require continuous scraping or API integration.

3. **Geographic Coverage**: Currently focuses on Senegal; can be extended to other regions by modifying the search parameters.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details (to be added).

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the awesome web framework
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [LinkedIn](https://www.linkedin.com/) for job listings (used with respect to their ToS)

---

**Note**: This project is for educational/demonstration purposes. Always respect website terms of service when scraping data.