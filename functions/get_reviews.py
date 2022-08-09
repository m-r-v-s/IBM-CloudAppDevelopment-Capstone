#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, IndexDefinition, IndexField
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, IndexDefinition, IndexField
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys

def main(params):

    authenticator = IAMAuthenticator(
        'LOUSWCCZgIfk-NTulihI_vdxS8zSjxNpGo_W83WcRy2c')
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(
        'https://50ed3f49-f6f4-4293-83c3-66d46f9fb647-bluemix.cloudantnosqldb.appdomain.cloud')
    index_field = IndexField(dealership="asc")
    index = IndexDefinition(
        fields=[index_field]
    )
    
    try:
        idx_response = service.post_index(
            db='reviews',
            ddoc='json-index',
            name='dealershipID_idx',
            index=index,
            type='json'
        ).get_result()
    except ApiException as ae:
            return{ "status code" : str(ae.code),
                    "message" : str(ae.message) }
    
    response = service.post_find(
                db='reviews',
                selector={'dealership': {'$eq': int(params['dealerID'])}},
            ).get_result()
    try: 
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response} 
            }        
        return result
    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
            }