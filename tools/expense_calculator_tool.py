from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator_tool_list = self._setup_tools()
    
    def _setup_tools(self):
        """Setup all tools for the calculator tool"""    
        @tool
        def estimate_total_hotel_cost(price_per_night:float, total_days:float)->float:
            """Calculate total hotel cost"""
            return price_per_night*total_days
        
        @tool
        def calculate_total_expense(costs: List[float])->float:
             """Calculate total expense of the trip"""
             return sum(costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int)->float:
             """Calculate daily expense"""
             return total_cost/days
        
        return [estimate_total_hotel_cost,calculate_total_expense,calculate_daily_expense_budget]




