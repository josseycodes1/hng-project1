# Dynamic Profile API

A Django REST Framework API that returns profile information with dynamic cat facts.

## Features

- GET `/me` endpoint returns profile data
- Dynamic cat facts from external API
- Proper error handling and fallbacks
- UTC timestamp in ISO 8601 format
- Comprehensive test suite

## API Endpoint

### GET /me
Returns profile information with a dynamic cat fact.

**Response:**
```json
{
  "status": "success",
  "user": {
    "email": "adewumijosephine1@gmail.com",
    "name": "Adewumi Josephine",
    "stack": "Python/Django/DRF"
  },
  "timestamp": "2024-01-15T10:30:00.123Z",
  "fact": "Cats can jump up to 6 times their height."
}