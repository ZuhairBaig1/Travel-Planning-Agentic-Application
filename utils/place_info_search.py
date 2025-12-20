from tavily import TavilyClient

class TavilySearchTool:
    def __init__(self, api_key:str):
        self.place_tool = TavilyClient(api_key=api_key)

    def tavily_search_attractions(self, places:str)->dict:
        """Searches for attractions in the specified places using Tavily API"""
        tavily_results = self.place_tool.search(f"top attractive places in and around {places}")
        summary = []
        for result in tavily_results.get('results',[])[:6]:
            summary.append(f"- {result.get('title')}: {result.get('content')[:100]}...")
        return summary
    
    def tavily_search_restaurants(self, places: str)-> dict:
        """Searches for available restaurants on the specified place using Tavily API"""
        tavily_results = self.place_tool.search(f"what are the 10 restaurants and eateries in and around {places}?")
        summary = []
        for result in tavily_results.get('results',[])[:6]:
            summary.append(f"- {result.get('title')}: {result.get('content')[:100]}...")
        return summary
    
    def tavily_search_activities(self, places: str)-> dict:
        """Search for popular activities in the specified places using Tavily API"""
        tavily_results = self.place_tool.search(f"Activities in and around {places}")
        summary = []
        for result in tavily_results.get('results',[])[:6]:
            summary.append(f"- {result.get('title')}: {result.get('content')[:100]}...")
        return summary
    
    def tavily_search_transportation(self, places: str)-> dict:
        """Search for transportation in the specified places using tavily API"""
        tavily_results = self.place_tool.search(f"What are the different transportations available in {places}")
        summary = []
        for result in tavily_results.get('results',[])[:6]:
            summary.append(f"- {result.get('title')}: {result.get('content')[:100]}...")
        return summary
