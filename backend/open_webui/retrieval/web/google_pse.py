import logging
from typing import Optional
import requests
from open_webui.retrieval.web.main import SearchResult, get_filtered_results
from open_webui.env import SRC_LOG_LEVELS

import asyncio, aiohttp

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])

async def fetch_page(session, url, params):
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()

async def search_google_concurrently(query, search_engine_id, api_key, count, url, headers):
    all_results = []
    tasks = []
    
    async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
        for start_index in range(1, count + 1, 10):
            num_results_this_page = min(count, 10)
            params = {
                "cx": search_engine_id,
                "q": query,
                "key": api_key,
                "num": num_results_this_page,
                "start": start_index,
                "sort": "date"
            }
            tasks.append(fetch_page(session, url, params))
        
        responses = await asyncio.gather(*tasks)
        
        for json_response in responses:
            results = json_response.get("items", [])
            if results:
                all_results.extend(results)
    
    return all_results


def search_google_pse(
    api_key: str,
    search_engine_id: str,
    query: str,
    count: int,
    filter_list: Optional[list[str]] = None,
) -> list[SearchResult]:
    """Search using Google's Programmable Search Engine API and return the results as a list of SearchResult objects.
    Handles pagination for counts greater than 10.

    Args:
        api_key (str): A Programmable Search Engine API key
        search_engine_id (str): A Programmable Search Engine ID
        query (str): The query to search for
        count (int): The number of results to return (max 100, as PSE max results per query is 10 and max page is 10)
        filter_list (Optional[list[str]], optional): A list of keywords to filter out from results. Defaults to None.

    Returns:
        list[SearchResult]: A list of SearchResult objects.
    """

    url = "https://www.googleapis.com/customsearch/v1"
    headers = {"Content-Type": "application/json"}
    all_results = []
    start_index = 1  # Google PSE start parameter is 1-based

    while count > 0:
        num_results_this_page = min(count, 10)  # Google PSE max results per page is 10
        params = {
            "cx": search_engine_id,
            "q": query,
            "key": api_key,
            "num": num_results_this_page,
            "start": start_index,
            "sort": "date"
        }
        response = requests.request("GET", url, headers=headers, params=params)
        response.raise_for_status()
        json_response = response.json()
        print('json_response', json_response)
        results = json_response.get("items", [])
        if results:  # check if results are returned. If not, no more pages to fetch.
            all_results.extend(results)
            count -= len(
                results
            )  # Decrement count by the number of results fetched in this page.
            start_index += 10  # Increment start index for the next page
        else:
            break  # No more results from Google PSE, break the loop

    # """Concurrent request get"""
    # all_results = asyncio.run(search_google_concurrently(query, search_engine_id, api_key, count, url, headers))
        
    if filter_list:
        all_results = get_filtered_results(all_results, filter_list)

    return [
        SearchResult(
            link=result["link"],
            title=result.get("title"),
            snippet=result.get("snippet"),
        )
        for result in all_results
    ]
