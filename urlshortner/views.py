from rest_framework import generics
from rest_framework import status
from django.http import JsonResponse,Http404, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import redirect
import json
import traceback

validate = URLValidator()

# Shorten single URL
@csrf_exempt
def CreateShortURL(request):
    response ={}
    try:
        long_url = json.loads(request.body)['long_url']
        u = URL.objects.get(long_url=long_url)
        response = {'short_url':u.short_url,'status':'OK','status_code':[]}
    except URL.DoesNotExist:
        try:
            validate(long_url)
            short_url = settings.SITE_URL  + short_url_generator()
            u = URL(long_url=long_url, short_url=short_url)
            u.save()
            response = {'short_url': short_url, 'status': 'OK', 'status_code': []}
        except ValidationError:
            response = {"status": "FAILED","status_codes": ["INVALID_URLS"]}
    except:
        response = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
    finally:
        return JsonResponse(response)



# Fetch the long URL for a given short URL
@csrf_exempt
def FetchLongURL(request):
    try:
        short_url = json.loads(request.body)['short_url']
        u = URL.objects.get(short_url = short_url)
        response = {'long_url':u.long_url,'status':'OK','status_code':[]}
    except URL.DoesNotExist:
        response = {"status": "FAILED","status_codes": ["SHORT_URLS_NOT_FOUND"]}
    except:
        response = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
    finally:
        return JsonResponse(response)


# Shorten list of URLs
@csrf_exempt
def CreateShortURLs(request):
    response ={"invalid_urls" : [],"status": "","status_codes": []}
    try:
        long_urls = json.loads(request.body)['long_urls']
        valid_urls = []
        invalid_urls = []
        flag = True
        if isinstance(long_urls, list):
            for long_url in long_urls:
                try:
                    valid_urls.append(URL.objects.get(long_url=long_url))
                except URL.DoesNotExist:
                    try:
                        validate(long_url)
                        short_url = settings.SITE_URL + short_url_generator()
                        valid_urls.append(URL(long_url=long_url, short_url=short_url))
                    except ValidationError:
                        invalid_urls.append(long_url)
                        flag = False
            if flag:
                response['short_urls'] = {}
                for valid_url in valid_urls:
                    response['short_urls'][valid_url.long_url] = valid_url.short_url
                    valid_url.save()
                response['status'] = "OK"
            else:
                response['invalid_urls'] = invalid_urls
                response['status'] = "FAILED"
                response['status_codes'] = ["INVALID_URLS"]
        else:
            raise Exception("Not a list")
    except Exception as e:
        print(e)
        response = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
    finally:
        return JsonResponse(response)


# Fetch the long URL for a given short URL
@csrf_exempt
def FetchLongURLs(request):
    response = {"invalid_urls": [], "status": "", "status_codes": []}
    try:
        short_urls = json.loads(request.body)['short_urls']
        valid_urls = []
        invalid_urls = []
        flag = True
        if isinstance(short_urls, list):
            for short_url in  short_urls:
                try:
                    valid_urls.append(URL.objects.get(short_url=short_url))
                except URL.DoesNotExist:
                    flag= False
                    invalid_urls.append(short_url)
            if flag:
                response['long_urls'] = {}
                for valid_url in valid_urls:
                    response['long_urls'][valid_url.short_url] = valid_url.long_url
                response['status'] = "OK"
            else:
                response['invalid_urls'] = invalid_urls
                response['status'] = "FAILED"
                response['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
        else:
            raise Exception("Not a list")
    except Exception as e:
        print(e)
        response = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
    finally:
        return JsonResponse(response)


# Fetch the long URL for a given short URL
@csrf_exempt
def FetchCount(request):
    try:
        short_url = json.loads(request.body)['short_url']
        u = URL.objects.get(short_url = short_url)
        response = {'count':u.count,'status':'OK','status_code':[]}
    except URL.DoesNotExist:
        response = {"status": "FAILED","status_codes": ["SHORT_URLS_NOT_FOUND"]}
    except:
        response = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
    finally:
        return JsonResponse(response)

# Short URL Server
@csrf_exempt
def RedirectURL(request,short_url_hash):
    try:
        short_url = settings.SITE_URL + short_url_hash
        u = URL.objects.get(short_url = short_url)
        u.count = u.count + 1
        u.save()
        return redirect(u.long_url)
    except URL.DoesNotExist:
        response = {"status": "FAILED","status_codes": ["SHORT_URLS_NOT_FOUND"]}
        return JsonResponse(response)
    except Exception as e:
        print(e)
        response = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
        return JsonResponse(response)

# Clean the database for multiple iterations of tests
@csrf_exempt
def CleanURL(request):
    try:
        URL.objects.all().delete()
        response = {"status":"OK"}
    except Exception as e:
        print(e)
        response = {"status":"FAILED"}
    finally:
        return JsonResponse(response)
