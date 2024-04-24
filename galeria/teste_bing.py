
#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os 
from pprint import pprint
import requests


def testar():

    '''
    This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
    Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    '''

    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
    endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/bing/v7.0/search"

    print('============'+subscription_key)
    print('============'+endpoint)

    url = "https://api.bing.microsoft.com/v7.0/search"
    querystring = {
        "q": "django tutorial",  # Sua consulta de pesquisa aqui
        "mkt": "en-us",
        "count": 10  # Número de resultados desejados
    }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.get(url, headers=headers, params=querystring)
    #search_results = response.json()
    print('**********'+response.text)

    #return render(request, 'search_results.html', {'results': search_results['webPages']['value']})
        