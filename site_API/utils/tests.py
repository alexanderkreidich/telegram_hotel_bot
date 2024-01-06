import pytest
from unittest.mock import patch, MagicMock

from site_API.utils.requests.site_api_requests import make_response, get_locations_json, get_hotel_info_json, \
    get_hotels_json

# Mocks for secrets
site = MagicMock()
site.api_key.get_secret_value.return_value = "your_api_key"
site.host_api.get_secret_value.return_value = "your_host_api"


# Mock for requests module
@patch("your_module.requests.request")
async def test_make_response(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"mock_data": "mock_value"}
    mock_request.return_value = mock_response

    url = "https://example.com"
    params = {"param1": "value1", "param2": "value2"}
    result = await make_response(url, params)

    assert result == {"mock_data": "mock_value"}
    mock_request.assert_called_once_with(
        method="GET",
        url=url,
        headers={
            "X-RapidAPI-Key": "your_api_key",
            "X-RapidAPI-Host": "your_host_api",
        },
        params=params,
        timeout=10,
    )


# Test for get_locations_json
async def test_get_locations_json():
    with patch("your_module.make_response") as mock_make_response:
        mock_make_response.return_value = {"location_data": "mock_value"}

        result = await get_locations_json("City", "en_US", "example.com")

        assert result == {"location_data": "mock_value"}
        mock_make_response.assert_called_once_with(
            url="https://hotels-com-provider.p.rapidapi.com/v2/regions",
            params={"locale": "en_US", "query": "City", "domain": "example.com"},
        )


# Test for get_hotel_info_json
async def test_get_hotel_info_json():
    with patch("your_module.make_response") as mock_make_response:
        mock_make_response.return_value = {"hotel_info": "mock_value"}

        result = await get_hotel_info_json("example.com", "en_US", "12345")

        assert result == {"hotel_info": "mock_value"}
        mock_make_response.assert_called_once_with(
            url="https://hotels-com-provider.p.rapidapi.com/v2/hotels/details",
            params={"domain": "example.com", "locale": "en_US", "hotel_id": "12345"},
        )


# Test for get_hotels_json
async def test_get_hotels_json():
    with patch("your_module.make_response") as mock_make_response:
        mock_make_response.return_value = {"hotels_data": "mock_value"}

        result = await get_hotels_json(
            "example.com",
            "asc",
            "en_US",
            "2023-01-01",
            "123",
            "2",
            "2022-12-31",
        )

        assert result == {"hotels_data": "mock_value"}
        mock_make_response.assert_called_once_with(
            url="https://hotels-com-provider.p.rapidapi.com/v2/hotels/search",
            params={
                "domain": "example.com",
                "sort_order": "asc",
                "locale": "en_US",
                "checkout_date": "2023-01-01",
                "region_id": "123",
                "adults_number": "2",
                "checkin_date": "2022-12-31",
                "lodging_type": "HOTEL",
            },
        )


if __name__ == "__main__":
    pytest.main()
