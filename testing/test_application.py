import requests

def test_get_root_page_check_status_code_equals_200():
     response = requests.get("http://192.168.1.39:8080/")
     assert response.status_code == 200

