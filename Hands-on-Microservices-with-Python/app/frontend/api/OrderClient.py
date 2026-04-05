from flask import session
import requests


class OrderClient:

    @staticmethod
    def get_order():
        headers = {
            'Authorization': 'Basic ' + session.get('user_api_key', '')
        }
        try:
            response = requests.request(method="GET", url='http://order:5010/api/order', headers=headers, timeout=5)
            order = response.json()
            return order
        except requests.exceptions.ConnectionError:
            print("[ERROR] Order Service unavailable")
            return {'result': {'items': {}, 'total': 0}}
        except Exception as e:
            print(f"[ERROR] Get order failed: {str(e)}")
            return {'result': {'items': {}, 'total': 0}}

    @staticmethod
    def update_order(items):
        url = 'http://order:5010/api/order/update'
        headers = {
            'Authorization': 'Basic ' + session.get('user_api_key', '')
        }
        try:
            response = requests.request("POST", url=url, data=items, headers=headers, timeout=5)
            if response:
                order = response.json()
                return order
        except requests.exceptions.ConnectionError:
            print("[ERROR] Order Service unavailable")
            return {'result': {'items': {}, 'total': 0}}
        except Exception as e:
            print(f"[ERROR] Update order failed: {str(e)}")
            return {'result': {'items': {}, 'total': 0}}

    @staticmethod
    def post_add_to_cart(product_id, qty=1):
        payload = {
            'product_id': product_id,
            'qty': qty,
        }
        url = 'http://order:5010/api/order/add-item'
        headers = {
            'Authorization': 'Basic ' + session.get('user_api_key', '')
        }
        try:
            response = requests.request("POST", url=url, data=payload, headers=headers, timeout=5)
            if response:
                order = response.json()
                return order
        except requests.exceptions.ConnectionError:
            print("[ERROR] Order Service unavailable")
            return {'result': {'items': {}, 'total': 0}}
        except Exception as e:
            print(f"[ERROR] Add to cart failed: {str(e)}")
            return {'result': {'items': {}, 'total': 0}}

    @staticmethod
    def post_checkout():
        url = 'http://order:5010/api/order/checkout'
        headers = {
            'Authorization': 'Basic ' + session.get('user_api_key', '')
        }
        try:
            response = requests.request("POST", url=url, data={}, headers=headers, timeout=5)
            order = response.json()
            return order
        except requests.exceptions.ConnectionError:
            print("[ERROR] Order Service unavailable")
            return {'result': {}}
        except Exception as e:
            print(f"[ERROR] Checkout failed: {str(e)}")
            return {'result': {}}

    @staticmethod
    def get_order_from_session():
        default_order = {
            'items': {},
            'total': 0,
        }
        return session.get('order', default_order)


