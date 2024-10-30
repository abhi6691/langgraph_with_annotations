import os
from app_samples.base_app import BaseLanggraphApp
from langgraph.graph import END, Graph
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class SimpleLanggraphApp(BaseLanggraphApp):

    def create_graph(self):
        # Import necessary LangGraph classes

        # Define a simple query node
        class QueryNode(Runnable):
            def invoke(self, input, config, **kwargs):
                query = input.get("query")
                model = ChatOpenAI(model="gpt-3.5-turbo",
                        api_key=os.getenv("OPENAI_API_KEY"))
                
                prompt = f"Answer the following question: {query}"

                response = model.invoke([HumanMessage(content=prompt)]).content
                return {"response": response}

        # Set up the graph
        graph = Graph()
        graph.add_node("query_node", QueryNode())
        graph.add_edge("query_node", END)
        graph.set_entry_point("query_node")

        print("Graph setup complete.")
        return graph