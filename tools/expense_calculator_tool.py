from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator_tool_list = self._setup_tools()
    
    def _setup_tools(self):
        """Setup all tools for the calculator tool"""    
        @tool
        def estimate_total_hotel_cost(price_per_night:float, total_days:float)->float:
            """
            Calculates the total hotel cost. 
            IMPORTANT: Arguments must be raw numbers ONLY. 
            Do NOT pass expressions like '3*10'.
            """
            return price_per_night*total_days
        
        @tool
        def calculate_total_expense(costs: List[float])->float:
             """
             Calculates the sum of a list of expenses. 
             Input MUST be a list of floats (e.g., [10.0, 20.5]). 
             DO NOT include currency symbols or math formulas in the list.
             """
             return sum(costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int)->float:
             """
             Calculates daily budget by dividing total cost by number of days.
             Args: total_cost (float), days (int).
             """
             return total_cost/days
        
        return [estimate_total_hotel_cost,calculate_total_expense,calculate_daily_expense_budget]



