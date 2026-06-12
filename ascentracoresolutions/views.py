from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import FileResponse, HttpResponse
from sfs.utils import *
from shared_lib.utils import insertions, random

class AdsTxtView(TemplateView):
    template_name = "ads.txt"
    content_type = "text/plain"


class AppAds(TemplateView):
    template_name = "app-ads.txt"
    content_type = "text/plain"

    insertions.insert_activity("gjrijg", version, "app-ads.txt_viewed", "Dgds")


def robots_txt(request):
    content = """
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: YandexBot
Allow: /

User-agent: *
Allow: /

Sitemap: https://ascentracoresolutions.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")

def index(request):

    return render(request, "index.html", {"login": url})


def er_400(request, exception):
    try:
        error_msg = f"400 at {request.path}"


        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "400.html", status=400)



def er_401(request, exception):
    try:
        error_msg = f"401 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "401.html", status=401)


def er_403(request, exception):
    try:
        error_msg = f"403 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "403.html", status=403)


def er_404(request, exception):

    try:
        error_msg = f"404 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "404.html", {"path": request.path}, status=404)



def er_408(request, exception):
    try:
        error_msg = f"408 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "408.html", status=408)


def er_500(request):
    try:
        error_msg = f"500 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "500.html", {"path": request.path}, status=500)


def er_502(request, exception):
    try:
        error_msg = f"502 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "502.html", status=502)


def er_503(request, exception):
    try:
        error_msg = f"503 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "503.html", status=503)


def er_504(request, exception):
    try:
        error_msg = f"504 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "504.html", status=504)


def er_505(request, exception):
    try:
        error_msg = f"505 at {request.path}"

        insertions.insert_error(random.get_client_ip(request), request.session.get('user_id', 'anonymous'), version, error_msg, request.path)
        
    except Exception as e:
        # Log to console or ignore — don’t break the 404 page
        print("Failed to log 404:", e)

    return render(request, "505.html", status=505)


def ads(request):
    file = open('ads.txt')
    return FileResponse(file.read())