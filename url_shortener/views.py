from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import redirect
from .models import short_url
import uuid
import json


@csrf_exempt
def create_new_short_url(request):
    if request.method == 'GET':
        template = loader.get_template('index.html')
        return HttpResponse(template.render())
    else:
        # method post the user is sending url to be shortened
        # load json data from request body
        data = json.loads(request.body) 
        client_url = data['url']

        # check if the user entered the absolute url or not
        client_url = client_url.replace("https://","")
        client_url = client_url.replace("http://","")

        # get the absolute web address of my site
        current_url = request.build_absolute_uri()

        # check if url is already shortened
        if short_url.objects.filter(url=client_url):
            data = short_url.objects.get(url = client_url)
            existent_url = current_url + "ref/" + data.unique_url
            res = {"already_exists": "url already shortened","existing_url": existent_url}
            response =  JsonResponse(res, status = 200)
            # response["Access-Control-Allow-Origin"] = "*"
            # response["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
            # response["Access-Control-Max-Age"] = "1000"
            # response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
            return response
        try:

            # create a unique 6 character long string using uuid
            # to map it to the url
            unique_short_url = uuid.uuid4().urn
            unique_short_url = unique_short_url[9:15]


            # save the client url and the unique url both into the database
            data_for_db = short_url()
            data_for_db.url = client_url
            data_for_db.unique_url = unique_short_url
            data_for_db.save()

            res = {"short_url": current_url + 'ref/' + unique_short_url}
            response =  JsonResponse(res, status = 200)
            # response["Access-Control-Allow-Origin"] = "*"
            # response["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
            # response["Access-Control-Max-Age"] = "1000"
            # response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

        except Exception as e:
            res = {"error": "there was an error please try again"}
            response =  JsonResponse(res, status = 404)
            # response["Access-Control-Allow-Origin"] = "*"
            # response["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
            # response["Access-Control-Max-Age"] = "1000"
            # response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        
        return response
    



def redirect_user(request, unique_identifier_to_url):
    try:
        data = short_url.objects.get(unique_url = unique_identifier_to_url)

        # add http:// to the url as the url needs to be absolute for redirection
        return HttpResponseRedirect("http://" + data.url)
    except Exception as e:
        # get absolute url to use to redirect user to the home page
        link_to_url_shortener = request.build_absolute_uri()
        index = link_to_url_shortener.index('/ref/')
        link_to_url_shortener = link_to_url_shortener[:index]
        return HttpResponse(f"""<div style=\"display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;\">
                                    <h1>Oops! Looks like this url does not exist in our database</h1>
                                    <a href="{link_to_url_shortener}">click here to shortene the url</a>
                                </div>""")

