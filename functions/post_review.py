from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, IndexDefinition, IndexField, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(params):
    authenticator = IAMAuthenticator(
        'LOUSWCCZgIfk-NTulihI_vdxS8zSjxNpGo_W83WcRy2c')
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(
        'https://50ed3f49-f6f4-4293-83c3-66d46f9fb647-bluemix.cloudantnosqldb.appdomain.cloud')
    try:
        response = service.post_document(db='reviews', document=params["review"]).get_result()
    except ApiException as ae: 
         return{"status code": str(ae.code),
               "message": str(ae.message)}
    else:
        return (response)