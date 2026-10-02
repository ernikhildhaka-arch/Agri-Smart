import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings


def _fallback(message, user, reason=None):
    context = f' Your saved state is {getattr(getattr(user, "farmer_profile", None), "state", "") or "not set"}.'
    msg = message.lower()
    if any(word in msg for word in ('fertilizer', 'soil', 'npk')):
        answer = (
            'For fertilizer decisions, use a current soil test and follow local extension '
            'guidance. The Soil & Fertilizer module can summarize the N-P-K values you enter.'
        )
    elif any(word in msg for word in ('water', 'irrigat', 'moisture')):
        answer = (
            'Match irrigation to crop stage and field moisture; avoid watering saturated soil. '
            'Check the Soil module for a simple moisture prompt.'
        )
    else:
        answer = (
            'I can help organise questions about crops, soil, irrigation, expenses, and planning. '
            'For field-specific advice, consult your local agricultural extension officer.'
        )
    if reason:
        answer += f' (AI provider unavailable: {reason})'
    return answer + context


def _gemini_reply(message):
    api_key = getattr(settings, 'AI_API_KEY', '') or os.getenv('AI_API_KEY', '').strip()
    if not api_key:
        return None, 'no API key configured'
    model = getattr(settings, 'AI_MODEL', 'gemini-2.0-flash')
    endpoint = (
        f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        f'?key={api_key}'
    )
    body = {
        'contents': [{'parts': [{'text': (
            'You are a careful agricultural planning assistant. Give concise, practical advice, '
            'state uncertainty, and recommend local agronomists for high-stakes decisions. '
            f'User question: {message}'
        )}]}],
        'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 500},
    }
    request = Request(
        endpoint,
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        method='POST',
    )
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
        text = payload['candidates'][0]['content']['parts'][0]['text'].strip()
        return text, None
    except (KeyError, IndexError, TypeError, ValueError):
        return None, 'provider returned an unexpected response'
    except (HTTPError, URLError, TimeoutError, OSError):
        return None, 'request failed'


def reply(message, user):
    """Return a provider response, with a transparent local fallback."""
    provider = getattr(settings, 'AI_PROVIDER', os.getenv('AI_PROVIDER', 'gemini')).lower()
    if provider == 'gemini':
        answer, error = _gemini_reply(message)
        if answer:
            return answer
        return _fallback(message, user, error)
    return _fallback(message, user, f'unsupported provider "{provider}"')
