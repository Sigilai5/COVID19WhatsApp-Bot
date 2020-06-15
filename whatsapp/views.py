from django.shortcuts import render
from django.http import HttpResponse
from flask import request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def whatsapp(request):
    if request.method == "POST":
        # add webhook logic here and return a response
        incoming_msg = request.POST.get('Body', '').lower()
        resp = MessagingResponse()
        msg = resp.message()
        # msg.body('this is the response text')
        # msg.media('https://example.com/path/image.jpg')

        url = "https://coronavirus-map.p.rapidapi.com/v1/summary/region"

        querystring = {"region": incoming_msg}

        headers = {
            'x-rapidapi-host': "coronavirus-map.p.rapidapi.com",
            'x-rapidapi-key': "5fee8291b9msh7f3c48582f3b2f6p105d31jsn6a44bdd5d8ff"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        json_response = response.json()
        parsed_data = json_response['data']['summary']
        total_cases = str(parsed_data['total_cases'])
        active_cases = str(parsed_data['active_cases'])
        deaths = str(parsed_data['deaths'])
        recovered = str(parsed_data['recovered'])
        change_parsed_data = json_response['data']['change']
        change_total_cases = str(change_parsed_data['total_cases'])
        change_deaths = str(change_parsed_data['deaths'])


        msg.body(
            '🔴️' +' '+'*Active Cases:* ' + active_cases + '\n' +
            '⚰️' +' '+ '*Deaths:* '+  deaths + '\n' +
            '⚕️️' +' '+ '*Recovered:* ' + recovered  + '\n' +
            '*Total Cases:* ' + total_cases + '\n\n\n' +
            '*Today*' + '\n\n' +
            '🔴️' +' '+'*New Cases:* ' + change_total_cases + '\n' +
            '⚰️' +' '+ '*Deaths:* ' + change_deaths
        )
        print(response)


        return HttpResponse(resp)

        # "data": {
        #     "summary": {
        #         "total_cases": 867882,
        #         "active_cases": 355352,
        #         "deaths": 43389,
        #         "recovered": 469141,
        #         "critical": 370925,
        #         "tested": 204,
        #         "death_ratio": 0.04999412362510111,
        #         "recovery_ratio": 0.5405585091060766
        #     },
        #     "change": {
        #         "total_cases": 0,
        #         "active_cases": -298,
        #         "deaths": 0,
        #         "recovered": 298,
        #         "critical": -16056,
        #         "tested": 0,
        #         "death_ratio": 0,
        #         "recovery_ratio": 0.00034336465095485824
        #     }
        # }



        # responded = True

        # if 'quote' in incoming_msg:
        #     # return a quote
        #     r = requests.get('https://api.quotable.io/random')
        #     if r.status_code == 200:
        #         data = r.json()
        #         quote = data.get('content') + '-' + '*' + data.get('author') + '*'
        #     else:
        #         quote = 'I could not retrieve a quote at this time,sorry.'
        #     msg.body(quote)
        #     responded = True
        # if 'video' in incoming_msg:
        #     # return a cat pic
        #     msg.media(
        #         'https://sqika.com/media/uploads/videos/d06305b0-8110-4959-9df6-9eac747fa056/d06305b0-8110-4959-9df6-9eac747fa056.mp4')
        #     responded = True
        #
        # if not responded:
        #     respo = "Thanks for not smoking!"
        #
        #     msg.body(respo)
        # return HttpResponse(resp)
