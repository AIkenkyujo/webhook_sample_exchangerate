# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
API_KEY = 'af306c0289c62fdea2ee87497ba888a6'
api = "http://apilayer.net/api/live?access_key={key}&currencies={currencies}"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "check_rate":
        return {}
    currencies = makeQuery(req)
    print(currencies)
    if currencies is None:
        return {}
    url = api.format(currencies=currencies, key=API_KEY)
    result = urlopen(url).read()
    data = json.loads(result)
    res = makeWebhookResult(data, currencies)
    return res


def makeQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    currency1 = parameters.get("currency1")
    currency2 = parameters.get("currency2")
    if currency1 is None or currency2 is None:
        return None

    return ','.join(currency1, currency2)


def makeWebhookResult(data, currencies):

    currencies = currencies.split(',').split('_')
    rate1 = data["quotes"][currencies[0]]
    rate2 = data["quotes"][currencies[2]]

    speech = "現在の " + currencies[1] + ":" + currencies[3] + \
             "のレートは、" + str(round(rate2/rate1,4)) + "です。"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-rate-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
