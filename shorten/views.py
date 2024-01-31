from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Links
import validators
import random, string
import json

# This is the homepage for URL Shortener
@csrf_exempt
def homepage(request):
    # Handle request if a URL was given to make it shorter
    if request.method == 'POST':
        # Get URL from json body
        is_json_post = False
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            url = data.get('url')
            is_json_post = True
        else:
            # Get URL from POST
            try:
                url = request.POST['url']
            except Exception:
                return render(request, 'invalid_url.html')

        # Validate the the URL recieved is valid and can be redirected to
        if not validators.url(url):
            return render(request, 'invalid_url.html')
        
        attempts = 0
        max_attempts = 10
        # Try to generate a random short link 10 times before giving up
        while attempts < max_attempts:
            short_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            if not Links.objects.filter(key=short_key).exists():
                break
            attempts += 1

        if attempts >= max_attempts:
            return render(request, 'failed.html')

        # Add URL to database
        link_instance = Links(key=short_key, dest=url)
        link_instance.save()
        short_url = f"{request.scheme}://{request.get_host()}/s/{short_key}"
        if is_json_post: # Handle specific case json 
            return HttpResponse(short_url)
        return render(request, 'success.html', {'shortened_link': short_url})

    # If not, just return the UI
    return render(request, 'index.html')

def short_redirect(request, key):
    try:
        # Redirect if the key is found
        link_instance = Links.objects.get(key=key)
        link_instance.increment_hit_count()
        return HttpResponseRedirect(link_instance.dest)
    except Links.DoesNotExist:
        # Send to 404 if the key is missing
        return render(request, '404.html', status=404)
    