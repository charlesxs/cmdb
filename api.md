# 

Client:

    auth:
        request body:
            {
                "key": "xxxxxx",
                "timestamp": "xxxxx",
            }
           or
            {
                "username": "xxxx",
                "password": "xxxx",
                "timestamp": "xxxx" 
            }


Server:
    
    auth:
        repsonse body:
            {
                "code": 200,
                "access_token": "xxxxx",
                "timestamp": "xxxxxx",
                "expires": 60
            }
            or
            {
                "code": 400,
                "reason": "xxxxx"
            }
        

         
        
        
        {
            "serialnum": "xxxx",
            "asset_type": "virtual machine",
            "hostname": ""
        }
        