# /app/frontend/api/ProductClient.py
import requests
class ProductClient:

    @staticmethod
    def get_product(code):
        try:
            response = requests.request(method="GET", url='http://host.docker.internal:5002/api/product/' + str(code), timeout=5)
            product = response.json()
            print("product retrieved : ", product, flush=True)
            return product
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Product Service unavailable", flush=True)
            return {'result': {}}
        except Exception as e:
            print(f"[ERROR] Get product failed: {str(e)}", flush=True)
            return {'result': {}}

    @staticmethod
    def get_products():
        try:
            r = requests.get('http://host.docker.internal:5002/api/products', timeout=5)
            products = r.json()
            return products
        except requests.exceptions.ConnectionError:
            print("[ERROR] Product Service unavailable", flush=True)
            return {'results': []}
        except Exception as e:
            print(f"[ERROR] Get products failed: {str(e)}", flush=True)
            return {'results': []}
