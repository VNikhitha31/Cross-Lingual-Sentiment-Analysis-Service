#!/bin/bash

# Cross-Lingual Sentiment Analysis API - Sample cURL Requests
BASE_URL="http://localhost:8000"

echo "=================================="
echo "1. HEALTH CHECK"
echo "=================================="
curl -X GET "$BASE_URL/health" | jq '.'
echo -e "\n"

echo "=================================="
echo "2. GET SUPPORTED LANGUAGES"
echo "=================================="
curl -X GET "$BASE_URL/api/v1/languages" | jq '.'
echo -e "\n"

echo "=================================="
echo "3. ENGLISH SENTIMENT (POSITIVE)"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This product is absolutely amazing! I love it!",
    "source_language": "en"
  }' | jq '.'
echo -e "\n"

echo "=================================="
echo "4. SPANISH SENTIMENT (POSITIVE)"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "¡Este producto es increíble! Me encanta mucho.",
    "source_language": "es"
  }' | jq '.'
echo -e "\n"

echo "=================================="
echo "5. FRENCH SENTIMENT (NEGATIVE)"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Je déteste ce service. C'\''est horrible.",
    "source_language": "fr"
  }' | jq '.'
echo -e "\n"

echo "=================================="
echo "6. GERMAN SENTIMENT (POSITIVE)"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Ausgezeichneter Service! Sehr zufrieden.",
    "source_language": "de"
  }' | jq '.'
echo -e "\n"

echo "=================================="
echo "7. AUTO-DETECT LANGUAGE (ITALIAN)"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Questo è fantastico! Molto bene!",
    "source_language": "auto"
  }' | jq '.'
echo -e "\n"

echo "=================================="
echo "8. CHINESE SENTIMENT"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这个产品非常好！我很喜欢。",
    "source_language": "zh-CN"
  }' | jq '.'
echo -e "\n"

echo "=================================="
echo "9. BATCH ANALYSIS (ENGLISH)"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "This is excellent!",
      "I hate this product.",
      "It is okay.",
      "Best experience ever!",
      "Terrible service."
    ],
    "source_language": "en"
  }' | jq '.'
echo -e "\n"

echo "=================================="
echo "10. MIXED LANGUAGE BATCH"
echo "=================================="
curl -X POST "$BASE_URL/api/v1/sentiment/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Excellent product!",
      "C'\''est magnifique!",
      "Esto es terrible.",
      "とても良いです！"
    ],
    "source_language": "auto"
  }' | jq '.'
echo -e "\n"
