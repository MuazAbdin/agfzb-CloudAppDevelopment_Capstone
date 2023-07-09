const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
  
async function main(params) {
    secret = {
        "COUCH_URL": "https://fe28ffcd-1798-4f8f-9819-06db0f2e4678-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "YGnHmP1y5rKSMeEwZwQ1IjKTDL1_-xkURKhYXYwzuIRt",
        "COUCH_USERNAME": "fe28ffcd-1798-4f8f-9819-06db0f2e4678-bluemix"
    };
    
    const authenticator = new IamAuthenticator({ apikey: secret.IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(secret.COUCH_URL);
    
    try {
        if (params.st) {
            const dbList = await cloudant.postFind({ db: 'dealerships', selector: { st: params.st } });
            const result = dbList.result.docs;
            return {
                statusCode: result.length ? 200 : 404,
                headers: { 'Content-Type': 'application/json' },
                body: result
            };
        } else if (params.id) {
            const dbList = await cloudant.postFind({ db: 'dealerships', selector: { id: parseInt(params.id) } });
            const result = dbList.result.docs;
            return {
                statusCode: result.length ? 200 : 404,
                headers: { 'Content-Type': 'application/json' },
                body: result
            };
        } else {
            const dbList = await cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 });
            const result = dbList.result.rows;
            return {
                statusCode: result.length ? 200 : 404,
                headers: { 'Content-Type': 'application/json' },
                body: result
            };
        }
    } catch (err) {
        console.error(err);
        return {
            statusCode: 500,
            headers: { 'Content-Type': 'application/json' },
            body: { error: 'Internal Server Error' }
        };
    }
}