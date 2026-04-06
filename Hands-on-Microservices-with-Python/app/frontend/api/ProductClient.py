import requests


class ProductClient:

    @staticmethod
    def get_product(slug):
        try:
            response = requests.request(method="GET", url='http://product:5011/api/product/' + slug, timeout=5)
            product = response.json()
            return product
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Product Service unavailable")
            return {'result': {}}
        except Exception as e:
            print(f"[ERROR] Get product failed: {str(e)}")
            return {'result': {}}

    @staticmethod
    def get_products():
        try:
            r = requests.get('http://product:5011/api/products', timeout=5)
            products = r.json()
            return products
        except requests.exceptions.ConnectionError:
            print("[ERROR] Product Service unavailable")
            return {'results': []}
        except Exception as e:
            print(f"[ERROR] Get products failed: {str(e)}")
            return {'results': []}
