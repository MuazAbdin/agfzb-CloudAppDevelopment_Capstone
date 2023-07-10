import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import time


def get_request(url, **kwargs):
    # print(kwargs)
    # print(f'GET from {url} ')
    api_key = kwargs.get('api_key')

    try:
        if api_key:
            params = {
                'text': kwargs["text"],
                'version': kwargs["version"],
                'features': kwargs["features"],
                'return_analyzed_text': kwargs["return_analyzed_text"]
            }
            requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                         auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
      print("Network exception occurred")

    status_code = response.status_code
    print(f'With status {status_code} ')
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
	try:
		response = requests.post(url, params=kwargs, json=json_payload)
	except:
		print("Network exception occurred")
  
	status_code = response.status_code
	print(f'With status {status_code} ')
	json_data = json.loads(response.text)
	return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    dealers = get_request(url)
    if dealers:
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(id=dealer_doc["id"],
                                   city=dealer_doc["city"],
                                   state=dealer_doc['state'],
                                   st=dealer_doc["st"],
                                   address=dealer_doc["address"],
                                   zip_code=dealer_doc["zip"],
                                   lat=dealer_doc["lat"], longt=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   full_name=dealer_doc["full_name"])
            results.append(dealer_obj)

    return results


def get_dealer_by_id(url, dealer_id):
    results = []
    dealers = get_request(url, id=dealer_id)
    if dealers:
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(id=dealer_doc["id"],
                               city=dealer_doc["city"],
                               state=dealer_doc['state'],
                               st=dealer_doc["st"],
                               address=dealer_doc["address"],
                               zip_code=dealer_doc["zip"],
                               lat=dealer_doc["lat"], longt=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               full_name=dealer_doc["full_name"])
        results.append(dealer_obj)

    return results


def get_dealers_by_state(url, dealer_state):
    results = []
    dealers = get_request(url, st=dealer_state)
    if dealers:
        for dealer_doc in dealers:
            dealer_obj = CarDealer(id=dealer_doc["id"],
                                   city=dealer_doc["city"],
                                   state=dealer_doc['state'],
                                   st=dealer_doc["st"],
                                   address=dealer_doc["address"],
                                   zip_code=dealer_doc["zip"],
                                   lat=dealer_doc["lat"], longt=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   full_name=dealer_doc["full_name"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
  
    results = []
    reviews = get_request(url, id=dealer_id)['data']['docs']
    if reviews:
        for review_doc in reviews:
            review_obj = DealerReview(
                id=review_doc['id'],
                name=review_doc['name'],
                dealership=review_doc['dealership'],
                review=review_doc['review'],
                purchase=review_doc['purchase'],
                purchase_date=review_doc['purchase_date'] if 'purchase_date' in review_doc else '',
                car_make=review_doc['car_make'] if 'car_make' in review_doc else '',
                car_model=review_doc['car_model'] if 'car_model' in review_doc else '',
                car_year=review_doc['car_year'] if 'car_year' in review_doc else '',
                sentiment=analyze_review_sentiments(review_doc['review'])
            )
            results.append(review_obj)
            
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/70cd8a4e-5884-4d3b-a4eb-eab203df46ff"
    api_key = 'nW4ZoO3T_wXR5XKAgfUYqT72ut87g_NP4jNxi1VN0had'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text=text+"hello hello hello", features=Features(
        sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return label
  