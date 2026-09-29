import os
def reply(message, user):
    """Provider boundary. Plug an approved API client in here when AI_API_KEY is configured."""
    if os.getenv('AI_API_KEY') and os.getenv('AI_PROVIDER'):
        return 'AI provider integration is configured as an extension point; add the provider client in chatbot/services.py.'
    context=f' Your saved state is {getattr(getattr(user,"farmer_profile",None),"state","") or "not set"}.'
    msg=message.lower()
    if any(w in msg for w in ('fertilizer','soil','npk')): return 'For fertilizer decisions, use a current soil test and follow local extension guidance. The Soil & Fertilizer module can summarize the N-P-K values you enter.'+context
    if any(w in msg for w in ('water','irrigat','moisture')): return 'Match irrigation to crop stage and field moisture; avoid watering saturated soil. Check the Soil module for a simple moisture prompt.'+context
    return 'Development assistant: I can help organise questions about crops, soil, irrigation, expenses, and planning. For field-specific advice, consult your local agricultural extension officer.'+context
