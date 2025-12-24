import os
from utils.place_info_search import TavilySearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.tavily_api_key=os.environ.get("TAVILY_API_KEY")
        self.tavily_place_search=TavilySearchTool(self.tavily_api_key)
        self.place_search_tool_list=self._setup_tools()

    def _setup_tools(self)->List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(place:str)->str:
            """Setup attractions of a place"""
            tavily_result=self.tavily_place_search.tavily_search_attractions(place)
            return f"Following are the attracions of {place} as suggested by tavily:" + "\n".join(tavily_result)
        @tool
        def search_restaurants(place:str)->str:
            """Setup restaurants of a place"""
            tavily_result=self.tavily_place_search.tavily_search_restaurants(place)
            return f"Following are the restaurants of {place} as suggested by tavily:" + "\n".join(tavily_result)
        @tool
        def search_activities(place:str)->str:
            """Setup activities of a place"""
            tavily_result=self.tavily_place_search.tavily_search_activities(place)
            return f"Following are the activities in and around {place} as suggested by tavily:" + "\n".join(tavily_result)
        
        @tool
        def search_transportation(place:str)->str:
            """Setup transportation of a place"""
            tavily_result=self.tavily_place_search.tavily_search_transportation(place)
            return f"Following are the transportation in {place} as suggested by tavily:" + "\n".join(tavily_result)
        
        return [search_attractions,search_restaurants,search_activities,search_transportation]
    
    