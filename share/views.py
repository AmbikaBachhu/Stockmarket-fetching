from django.shortcuts import redirect, render, Http404, HttpResponse
import json
import traceback
import urllib
from urllib import request
from urllib.request import urlopen, Request
import redis
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from nsetools import Nse
from django.conf import settings
import ast

NIFTY_GAINER_SCRAPPER_URL = settings.SCRAPPER_URL.get('nifty_gainer', '')
NIFTY_LOSER_SCRAPPER_URL = settings.SCRAPPER_URL.get('nifty_loser', '')
POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
r_server = redis.StrictRedis(connection_pool=POOL)
API_TIME_DIFF = settings.API_TIME_DIFF
nse = Nse()
top = nse.get_top_gainers()
bottom = nse.get_top_losers()


def index(request):
    if request.method == "GET":
        gainer_json, loser_json = check_and_save_in_redis()
        return render(request, 'index.html', {'gainer_data': json.dumps(gainer_json),
                                              'loser_data': json.dumps(loser_json)})


def get_data_from_nifty(gainer_flag, loser_flag):
    gainer_json = {}
    loser_json = {}
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                            'Version/12.0 Safari/605.1.15',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'
              }
    if gainer_flag:
        req = urllib.request.Request(NIFTY_GAINER_SCRAPPER_URL, headers=header)
        with urllib.request.urlopen(req) as response:
            gainer_json = response.read()
            gainer_json = json.loads(gainer_json)

    if loser_flag:
        req = urllib.request.Request(NIFTY_LOSER_SCRAPPER_URL, headers=header)
        with urllib.request.urlopen(req) as response:
            loser_json = response.read()
            loser_json = json.loads(loser_json)
    return gainer_json, loser_json


def process_gainer_loser_data(request):
    gainer_json, loser_json = check_and_save_in_redis()
    response_nifty = {}
    response_nifty['gainer_json'] = gainer_json
    response_nifty['loser_json'] = loser_json
    return HttpResponse(json.dumps({'response': 'success',
                                    'response_nifty': response_nifty}))


def check_and_save_in_redis():
    gainer_key = 'gainer_data'
    loser_key = 'loser_data'
    gainer_data = r_server.get(str(gainer_key))
    loser_data = r_server.get(str(loser_key))
    if not gainer_data:
        gainer_data, loser_data = get_data_from_nifty(True, False)
        r_server.set(gainer_key, ast.literal_eval(json.dumps(str(gainer_data))))
    else:
        gainer_data = eval(gainer_data)
        server_time = datetime.strptime(gainer_data.get('time'), '%b %d, %Y %H:%M:%S')
        current_system_time = datetime.now()
        adjusted_time = current_system_time - timedelta(minutes=5)
        if adjusted_time > server_time:
            gainer_data, loser_data = get_data_from_nifty(True, False)
            r_server.set(gainer_key, ast.literal_eval(json.dumps(str(gainer_data))))

    if not loser_data:
        gainer_data_dummy, loser_data = get_data_from_nifty(False, True)
        r_server.set(loser_key, ast.literal_eval(json.dumps(str(loser_data))))
    else:
        loser_data = eval(loser_data)
        server_time = datetime.strptime(loser_data.get('time'), '%b %d, %Y %H:%M:%S')
        current_system_time = datetime.now()
        adjusted_time = current_system_time - timedelta(minutes=5)
        if adjusted_time > server_time:
            gainer_data_dummy, loser_data = get_data_from_nifty(False, True)
            r_server.set(loser_key, ast.literal_eval(json.dumps(str(loser_data))))
    return gainer_data, loser_data


'''Below is another way to appproach NSE data'''




def contain(request):

    return render(request, "show.html", {"recent": top, "recents": bottom})

def contains(request):
    sched = BlockingScheduler()
    # Schedule job_function to be called every twenty seconds
    t = sched.add_job(job_function, 'interval', seconds=40)
    b = sched.add_job(job_function, 'interval', seconds=40)
    sched.start()
    redirect('contain')

def job_function():
    top = nse.get_top_gainers()
    print(top)

def job_functions():
    bot = nse.get_top_losers()
    print(bot)

