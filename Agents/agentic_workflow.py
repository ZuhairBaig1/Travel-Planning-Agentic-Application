from utils.model_loaders import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from prompt_library.reflection_agent_prompt import REFLECTION_PROMPT
from langchain_core.messages import HumanMessage

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConversionTool

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition



class GraphBuilder():
    def __init__(self):
        self.model_loader = ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.tools = []
        self.weather_tool = WeatherInfoTool()
        self.place_search_tool = PlaceSearchTool()
        self.calculator_tool = CalculatorTool()
        self.currency_converter_tool=CurrencyConversionTool()
        self.tools.extend([* self.weather_tool.weather_tool_list,
                           * self.place_search_tool.place_search_tool_list,
                           * self.calculator_tool.calculator_tool_list,
                           * self.currency_converter_tool.currency_converter_tool_list])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.graph = None
        self.system_prompt = SYSTEM_PROMPT
        self.reflection_prompt = REFLECTION_PROMPT

    def agent_function(self,state: MessagesState):
        """Main agent function"""
        user_question=state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages":[response]}

    
    def reflection_agent(self,state: MessagesState):
        """reflection agent"""
        travel_plan = state["messages"][-1].content
        if isinstance(travel_plan, str):
            travel_plan_input = [self.reflection_prompt] + [HumanMessage(content = travel_plan)]
            refined_travel_plan = self.llm.invoke(travel_plan_input)
            return {"messages":[refined_travel_plan]}
        elif isinstance(travel_plan, list):
            text_parts = []
            for block in travel_plan:
                # Check for the dictionary structure Gemini uses
                if isinstance(block, dict) and "text" in block:
                    text_parts.append(block["text"])
                # Sometimes elements in the list are just strings
                elif isinstance(block, str):
                    text_parts.append(block)
            travel_plan_gemini= "".join(text_parts)
            travel_plan_input = [self.reflection_prompt] + [HumanMessage(content = travel_plan_gemini)]
            refined_travel_plan = self.llm.invoke(travel_plan_input)
            return {"messages":[refined_travel_plan]}


    def build_graph(self):
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent",self.agent_function)
        graph_builder.add_node("tools",ToolNode(tools=self.tools))
        graph_builder.add_node("reflection_agent",self.reflection_agent)
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent","reflection_agent")
        graph_builder.add_edge("reflection_agent",END)

        self.graph=graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()