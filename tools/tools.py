from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
import os

def get_profile_url_tavily(name:str):
    """
    Given a name, return the LinkedIn profile URL using Tavily Search.
    """
    # Initialize the TavilySearchResults tool
    tavily_search = TavilySearch(
        search_type="linkedin",
        search_results_class=TavilySearchResults,
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        search_depth="advanced",
        max_results=5
    )
    
    # Perform the search using the tool
    results = tavily_search.run(f"{name}")
    return results
    
