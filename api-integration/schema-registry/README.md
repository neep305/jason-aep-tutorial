Use the Schema Registry API to access the Schema Library within Adobe Experience Platform. The registry provides a user interface and RESTful API from which all available library resources are accessible. Programmatically manage all schemas and related Experience Data Model (XDM) resources available to you within Platform. This includes those defined by Adobe, Experience Platform partners, and vendors whose applications you use.

Related documentation:

XDM documentation
Visualize API calls with Postman (a free, third-party software):

Schema Registry API Postman collection on GitHub
Video guide for creating the Postman environment
Steps for importing environments and collections in Postman
API paths:

PLATFORM Gateway URL: https://platform.adobe.io
Base path for this API: /data/foundation/schemaregistry
Example of a complete path for making a call to "/stats": https://platform.adobe.io/data/foundation/schemaregistry/stats
Required headers:

All calls require the headers Authorization, x-gw-ims-org-id, and x-api-key. For more information on how to obtain these values, see the authentication tutorial.
All resources in Experience Platform are isolated to specific virtual sandboxes. All requests to Platform APIs require the header x-sandbox-name whose value is the all-lowercase name of the sandbox the operation will take place in (for example, "prod"). See the sandboxes overview for more information.
All GET requests to the Schema Registry require an Accept header to determine what data is returned by the system. See the section on Accept headers in the Schema Registry developer guide for more information.
All requests with a payload in the request body (such as POST, PUT, and PATCH calls) must include the header Content-Type with a value of application/json.
API error handling:
Refer to the Experience Platform API troubleshooting guide for FAQs, API status codes, and request header errors.

## Generate access token - OAuth
> enerate an access token for quick experimentation, or view the cURL command to learn how to generate access tokens programmatically.
```shell
curl -X POST 'https://ims-na1.adobelogin.com/ims/token/v3' -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=client_credentials&client_id=<client_id>&client_secret=<client_secret>&scope=openid,AdobeID,read_organizations,additional_info.projectedProductContext,session'
```

## API Credential 설정
![Permissions in Adobe Experience Platform](../Permissions%20_%20Adobe%20Experience%20Platform.png)
- API Console에 프로젝트 생성
- Credential 생성
- 생성된 Credential을 프로젝트에 연결:
    - 연결방법: AEP > Administration - Permissions > 샌드박스 선택 > API credentials 탭 > Add API credentials
     
