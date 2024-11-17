from urllib.parse import parse_qs, urlparse

import requests


def get_result(url: str) -> str:
    """
    Prompts the user for a Winsplits URL, extracts the databaseId and categoryId,
    constructs the API URL, makes a GET request to the API, and returns the XML response.
    Args:
        url (str): The Winsplits URL containing the databaseId and categoryId.
    Returns:
        str: The XML content returned by the API.

    Raises:
        ValueError: If the URL is missing databaseId or categoryId.
        requests.exceptions.RequestException: If the API request fails.
    """

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    eventId = query_params.get("databaseId", [None])[0]
    # There seems to be a bug in the API where the classId is off by one
    classId = str(int(query_params.get("categoryId", [None])[0]) + 1)
    if not eventId or not classId:
        raise ValueError("Invalid URL: Missing databaseId or categoryId")

    api_url = f"http://obasen.orientering.se/winsplits/api/events/{eventId}/classes/{classId}/resultlist/xml"
    response = requests.get(api_url)

    if response.status_code == 200:
        xml_content = response.text
        return xml_content
    else:
        response.raise_for_status()


# Example usage
if __name__ == "__main__":
    try:
        result = get_result(
            "http://obasen.orientering.se/winsplits/online/sv/default.asp?page=table&databaseId=100310&categoryId=1"
        )
    except Exception as e:
        print(f"An error occurred: {e}")
