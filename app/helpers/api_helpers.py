from contextlib import redirect_stdout, redirect_stderr
import requests
import json
import io

def execute_api(http_method: str, api_url: str, api_params, access_token: str = None) -> str:
    params_dict = {}
    invalid_params = []
    print("\n\n=========== Access Token ============\n\n")
    print(access_token)
    
    for param in api_params:
        if '=' in param:
            key, value = param.split('=', 1)
            params_dict[key] = value
        else:
            invalid_params.append(param)
    
    output = io.StringIO()
    
    with redirect_stdout(output), redirect_stderr(output):
        if invalid_params:
            print(f"Invalid parameters ignored: {invalid_params}")

        headers = {
            'Content-Type': 'application/json',
        }

        if access_token:
            headers['Authorization'] = f'{access_token}'
        
        print("\n\n=========== Headers ============\n\n")
        print(headers)
        
        print("\n\n=========== Params ============\n\n")
        print(params_dict)
        
        http_method = http_method.lower()
        response = None
        
        try:
            if http_method == 'get':
                #response = requests.get(api_url, headers=headers, params=api_params)
                response = requests.get("https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24?api-key=579b464db66ec23bdd000001b4e6b405f9e145584bff0a3824f781e5&format=json")
            elif http_method == 'post':
                response = requests.post(api_url, headers=headers, json=params_dict)
            elif http_method == 'put':
                response = requests.put(api_url, headers=headers, json=params_dict)
            elif http_method == 'delete':
                response = requests.delete(api_url, headers=headers, json=params_dict)
            else:
                raise ValueError("Invalid HTTP method provided. Use 'GET', 'POST', 'PUT', or 'DELETE'.")
            
            print("\n\n=========== Response Status Code ============\n\n")
            print(response.status_code)
            
            response.raise_for_status()
            
            try:
                json_response = response.json()
                j_response = json.dumps(json_response, indent=4, sort_keys=True)
                print(j_response)
            except ValueError:
                print(f"Response Status Code: {response.status_code}")
                print(f"Response Content: {response.text}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if response:
                print(f"Response Status Code: {response.status_code}")
                print(f"Response Content: {response.content}")
        except Exception as err:
            print(f"Other error occurred: {err}")
    return output.getvalue()
