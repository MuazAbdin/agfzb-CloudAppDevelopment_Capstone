import sys 
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    secret = {
        "COUCH_URL": "https://fe28ffcd-1798-4f8f-9819-06db0f2e4678-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "YGnHmP1y5rKSMeEwZwQ1IjKTDL1_-xkURKhYXYwzuIRt",
        "COUCH_USERNAME": "fe28ffcd-1798-4f8f-9819-06db0f2e4678-bluemix"
    }
    
    authenticator = IAMAuthenticator(secret["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secret["COUCH_URL"])
    
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
        
    try: 
        # result_by_filter=my_database.get_query_result(selector,raw_result=True) 
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data': response} 
        }        
        return result
    except ApiException:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
        }