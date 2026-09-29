def language(request):
    return {'site_language': request.session.get('site_language', 'en')}
