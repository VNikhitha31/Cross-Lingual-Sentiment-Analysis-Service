Cross-Lingual Sentiment Analysis Service

A production-ready REST API service that performs sentiment analysis on text written in multiple languages. The service automatically detects the input language, translates non-English text to English, and applies sentiment analysis using state-of-the-art machine learning models.

Features

Multi-Language Support: Analyze sentiment in multiple languages including Spanish, French, German, Chinese, Japanese, Arabic, and more

Auto Language Detection: Automatically detect the source language if not specified

Batch Processing: Analyze multiple texts in a single request

REST API: FastAPI-based service with automatic OpenAPI documentation

Docker Support: Fully containerized using Docker and Docker Compose

Health Monitoring: Built-in health checks and structured logging

High Performance: Optimized for fast inference using Transformer-based models

Supported Languages

English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Russian (ru), Chinese (zh), Japanese (ja), Korean (ko), Arabic (ar), Hindi (hi), Dutch (nl), Swedish (sv), Polish (pl), Turkish (tr)

Architecture
Client Request → FastAPI → Language Detection & Translation → Sentiment Model → JSON Response

Components

FastAPI: High-performance Python web framework for building REST APIs

Transformers: Hugging Face library for Transformer-based sentiment analysis

deep-translator: Translation library leveraging Google Translate backend

DistilBERT: Pre-trained Transformer model fine-tuned for sentiment classification

Prerequisites

Docker and Docker Compose (recommended)

OR Python 3.10+ (for local development)

Quick Start with Docker (Recommended)
1. Build and Start the Service
docker-compose build
docker-compose up -d

2. Verify Service Status
# Health check
curl http://localhost:8000/health

# View logs
docker-compose logs -f

3. Access API Documentation

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Installation (Local Development)
1. Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt

3. Run the Application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

API Endpoints
1. Health Check
GET /health


Returns service health status and model readiness.

2. Get Supported Languages
GET /api/v1/languages


Returns the list of supported languages.

3. Sentiment Analysis (Single Text)
POST /api/v1/sentiment


Request Body

{
  "text": "Your text here",
  "source_language": "auto"
}


Response

{
  "text": "Your text here",
  "sentiment": "positive",
  "confidence": 0.9987,
  "source_language": "en",
  "translated_text": null,
  "processing_time_ms": 145.32,
  "timestamp": "2025-12-24T10:30:00.000Z"
}

4. Sentiment Analysis (Batch)
POST /api/v1/sentiment/batch


Request Body

{
  "texts": [
    "First text",
    "Second text",
    "Third text"
  ],
  "source_language": "auto"
}


Response

{
  "results": [...],
  "total_processed": 3,
  "processing_time_ms": 523.45
}

Sample Usage
Python Example
import requests

url = "http://localhost:8000/api/v1/sentiment"
payload = {
    "text": "¡Este servicio es increíble!",
    "source_language": "auto"
}

response = requests.post(url, json=payload)
print(response.json())


Run test examples:

python test_examples.py

cURL Examples
# English text
curl -X POST http://localhost:8000/api/v1/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"I love this product","source_language":"en"}'

# Auto language detection
curl -X POST http://localhost:8000/api/v1/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"Me encanta este producto","source_language":"auto"}'

# Batch analysis
curl -X POST http://localhost:8000/api/v1/sentiment/batch \
  -H "Content-Type: application/json" \
  -d '{"texts":["Great","Terrible","Okay"],"source_language":"en"}'


Run all cURL tests:

chmod +x curl_examples.sh
./curl_examples.sh

Response Details
Sentiment Labels

positive

negative

neutral

Confidence Score

Range: 0.0 – 1.0

Higher values indicate higher prediction confidence

Configuration
Environment Variables
LOG_LEVEL=INFO
MAX_TEXT_LENGTH=5000
BATCH_SIZE_LIMIT=50

Performance Notes

Cold Start: Initial request may take longer due to model loading

Batch Requests: More efficient for processing multiple texts

Memory Usage: Approximately 1–2 GB RAM depending on workload

Translation Overhead: Translation may add latency depending on input language

Troubleshooting
Service Not Starting
docker-compose down
docker-compose build --no-cache
docker-compose up

Translation Issues

Translation relies on public translation backends

Excessive requests may lead to rate limiting

Consider caching or paid translation APIs for production use

Project Structure
.
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── test_examples.py
├── curl_examples.sh
└── README.md

Security Considerations

Input validation on all endpoints

Text length limits to prevent abuse

CORS enabled (adjust for production)

No authentication implemented (can be added if required)

Future Enhancements

Authentication (JWT / API keys)

Caching (Redis)

Rate limiting

Custom model fine-tuning

GPU acceleration

Database-backed analytics

Streaming inference support

License

This project is provided for evaluation, educational, and demonstration purposes.

Acknowledgments

Hugging Face Transformers

FastAPI

deep-translator

DistilBERT model

Version: 1.0.0
Last Updated: December 2025
Status: Production Ready 