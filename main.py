from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from transformers import pipeline
from deep_translator import GoogleTranslator
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cross-Lingual Sentiment Analysis API",
    description="Multi-language sentiment analysis service with translation support",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sentiment analysis model
try:
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # CPU
    )
    logger.info("Sentiment model loaded successfully")
except Exception as e:
    logger.error(f"Error loading sentiment model: {e}")
    sentiment_analyzer = None

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
    'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh-CN': 'Chinese',
    'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi',
    'nl': 'Dutch', 'sv': 'Swedish', 'pl': 'Polish', 'tr': 'Turkish'
}

class SentimentRequest(BaseModel):
    text: str = Field(..., description="Text to analyze", min_length=1, max_length=5000)
    source_language: Optional[str] = Field(
        'auto',
        description="Source language code (e.g., 'es', 'fr') or 'auto' for detection"
    )

class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to analyze", max_items=50)
    source_language: Optional[str] = Field('auto', description="Source language code")

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    source_language: str
    translated_text: Optional[str] = None
    processing_time_ms: float
    timestamp: str

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]
    total_processed: int
    processing_time_ms: float

def translate_text(text: str, source_lang: str = 'auto') -> tuple:
    """Translate text to English using Google Translate"""
    try:
        if source_lang == 'auto':
            translator = GoogleTranslator(source='auto', target='en')
        else:
            translator = GoogleTranslator(source=source_lang, target='en')
        
        translated = translator.translate(text)
        detected_lang = source_lang if source_lang != 'auto' else 'auto'
        
        return translated, detected_lang
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

def analyze_sentiment(text: str) -> tuple:
    """Analyze sentiment of English text"""
    try:
        if not sentiment_analyzer:
            raise HTTPException(status_code=503, detail="Sentiment model not available")
        
        result = sentiment_analyzer(text[:512])[0]  # Limit to 512 tokens
        
        # Map model labels to standardized output
        label_map = {
            'POSITIVE': 'positive',
            'NEGATIVE': 'negative',
            'NEUTRAL': 'neutral'
        }
        
        sentiment = label_map.get(result['label'], result['label'].lower())
        confidence = result['score']
        
        return sentiment, confidence
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Cross-Lingual Sentiment Analysis API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "analyze": "/api/v1/sentiment",
            "batch_analyze": "/api/v1/sentiment/batch",
            "health": "/health",
            "languages": "/api/v1/languages"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": sentiment_analyzer is not None,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "supported_languages": SUPPORTED_LANGUAGES,
        "total": len(SUPPORTED_LANGUAGES),
        "auto_detect": True
    }

@app.post("/api/v1/sentiment", response_model=SentimentResponse)
async def analyze_sentiment_endpoint(request: SentimentRequest):
    """
    Analyze sentiment of text in any supported language
    
    - **text**: Text to analyze (required)
    - **source_language**: Language code or 'auto' for automatic detection
    """
    start_time = datetime.utcnow()
    
    try:
        # Translate to English if not already
        if request.source_language == 'en':
            translated_text = request.text
            detected_lang = 'en'
        else:
            translated_text, detected_lang = translate_text(
                request.text,
                request.source_language
            )
        
        # Analyze sentiment
        sentiment, confidence = analyze_sentiment(translated_text)
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return SentimentResponse(
            text=request.text,
            sentiment=sentiment,
            confidence=round(confidence, 4),
            source_language=detected_lang,
            translated_text=translated_text if request.source_language != 'en' else None,
            processing_time_ms=round(processing_time, 2),
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sentiment/batch", response_model=BatchSentimentResponse)
async def batch_analyze_sentiment(request: BatchSentimentRequest):
    """
    Analyze sentiment for multiple texts
    
    - **texts**: List of texts to analyze (max 50)
    - **source_language**: Language code or 'auto' for automatic detection
    """
    start_time = datetime.utcnow()
    results = []
    
    for text in request.texts:
        try:
            individual_start = datetime.utcnow()
            
            # Translate
            if request.source_language == 'en':
                translated_text = text
                detected_lang = 'en'
            else:
                translated_text, detected_lang = translate_text(
                    text,
                    request.source_language
                )
            
            # Analyze
            sentiment, confidence = analyze_sentiment(translated_text)
            
            # Calculate individual processing time
            individual_time = (datetime.utcnow() - individual_start).total_seconds() * 1000
            
            results.append(SentimentResponse(
                text=text,
                sentiment=sentiment,
                confidence=round(confidence, 4),
                source_language=detected_lang,
                translated_text=translated_text if request.source_language != 'en' else None,
                processing_time_ms=round(individual_time, 2),
                timestamp=datetime.utcnow().isoformat()
            ))
        
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            # Continue with other texts
            continue
    
    total_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    
    return BatchSentimentResponse(
        results=results,
        total_processed=len(results),
        processing_time_ms=round(total_time, 2)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
