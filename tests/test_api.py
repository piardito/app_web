import requests
import pytest

data = [
    ("100001",96.46730220712912),
    ("100005",87.8757218023598),
    ("100013",99.02467481480983)

]
@pytest.mark.parametrize("SK_ID_CURR,score",data)
def test_client(SK_ID_CURR,score):
    response = requests.get(f"https://projet7o.herokuapp.com/score/?SK_ID_CURR={SK_ID_CURR}")
    body = response.json()
    assert body["SK_ID_CURR"] == SK_ID_CURR
    assert body["score"] == score


