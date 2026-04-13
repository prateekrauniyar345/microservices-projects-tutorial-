# /app/frontend/api/UserClient.py
from flask import session
import requests
class UserClient:

    @staticmethod
    def post_login(form):
        api_key = False
        payload = {
            'username': form.username.data,
            'password': form.password.data,
        }
        print("login payload is : \n",payload, flush=True) 
        url = 'http://host.docker.internal:5001/api/user/login'
        try:
            response = requests.request("POST", url=url, data=payload, timeout=5)
            print("response for login is : \n",response.text, flush=True)
            if response:
                d = response.json()
                if d.get('api_key') is not None:
                    api_key = d['api_key']
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] User Service unavailable at {url}")
            api_key = False
        except Exception as e:
            print(f"[ERROR] Login failed: {str(e)}", flush=True)
            api_key = False
        return api_key

    @staticmethod
    def does_exist(username):
        url = 'http://host.docker.internal:5001/api/user/'+username+'/exist'
        try:
            response = requests.request("GET", url=url, timeout=5)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] User Service unavailable at {url}", flush=True)
            return False
        except Exception as e:
            print(f"[ERROR] User existence check failed: {str(e)}", flush=True)
            return False

    @staticmethod
    def post_user_create(form):
        user = False
        payload = {
            'email': form.email.data,
            'password': form.password.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'username': form.username.data
        }
        url = 'http://user:5010/api/user/create'
        try:
            response = requests.request("POST", url=url, data=payload, timeout=5)
            if response:
                user = response.json()
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] User Service unavailable at {url}", flush=True)
            user = False
        except Exception as e:
            print(f"[ERROR] User creation failed: {str(e)}", flush=True)
            user = False
        return user

    @staticmethod
    def get_user():
        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        try:
            response = requests.request(method="GET", url='http://user:5010/api/user', headers=headers, timeout=5)
            user = response.json()
            return user
        except requests.exceptions.ConnectionError:
            print("[ERROR] User Service unavailable", flush=True)
            return {'result': {}}
        except Exception as e:
            print(f"[ERROR] Get user failed: {str(e)}", flush=True)
            return {'result': {}}
