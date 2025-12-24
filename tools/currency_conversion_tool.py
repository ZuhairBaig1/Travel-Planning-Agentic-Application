from utils.currency_convertor import Currencyconvertor
from langchain.tools import tool
from dotenv import load_dotenv
from typing import List
import os

class CurrencyConversionTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.currency_service = Currencyconvertor(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self)-> List:
        """Set up all tools for currency conversion tools"""
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str):
            """Convert amount from one currency to another"""
            return self.currency_service.convert(amount, from_currency, to_currency)
        return [convert_currency]
    
