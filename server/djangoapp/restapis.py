from unittest import result
import requests
import json
from .models import CarDealer, CarMake, CarModel, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions



def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get("api_key", None)
    if api_key:
        try:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("Network exception occurred")
        else:
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text) 
            return json_data
    else:
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
        except:
            print("Network exception occurred")
        else:
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
            return json_data


def post_request(url, json_payload, **kwargs):
    
    response = requests.post(url = url, json= json_payload, params=kwargs)
    



def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result and kwargs:
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            if( dealer_doc["st"] == kwargs.get("state")):
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
            else: 
                pass
    elif json_result and not kwargs:
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results



def get_dealer_from_cf_by_id(url, dealer_id):
    json_result = get_request(url, dealer_id = dealer_id)
    if json_result:
        dealer_doc = json_result["body"][0]
        dealer = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer



def get_dealer_from_cf_by_state(url, state):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results



def get_dealer_reviews_from_cf(url, dealerID):
    results = []
    json_result = get_request(url, dealerID = dealerID)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for review in reviews:
            if review["purchase"] is True:
                review_obj = DealerReview(dealership_= review["dealership"], name_ = review["name"],
                    purchase_=review["purchase"], review_ = review["review"], purchase_date_= review["purchase_date"], 
                    car_make_= review["car_make"], car_year_= review["car_year"], id_ = review["id"], car_model_ =review["car_model"],
                    sentiment_ = analyze_review_sentiments(review["review"]))
            elif review["purchase"] is False:
                review_obj = DealerReview(dealership_= review["dealership"], name_ = review["name"],
                purchase_=review["purchase"], review_ = review["review"], purchase_date_= None, 
                car_make_= None, car_year_= None, id_ = review["id"], car_model_ = None,
                sentiment_ = analyze_review_sentiments(review["review"]))
            results.append(review_obj)
    return results

def analyze_review_sentiments(dealerreview):
    url ="https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/8f282c81-1fd5-4830-92dd-daab22567857"
    api_key = "qqOljjCnUPMGMMM-xcXOaJcuvXao75ZDXblWY3mdkFYX"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=dealerreview,features=Features(sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
    sentiment = json.dumps(response, indent=2)
    sentiment = response['sentiment']['document']['label']
    return sentiment
