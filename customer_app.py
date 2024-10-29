# customer_app.py

from framework import initialize, entrypoint, application

@application
class MyApp:
    def __init__(self):
        self.graph = None
    
    @initialize
    def setup_graph(self):
        # Import necessary LangGraph classes
        from langgraph.graph import END, Graph
        from langchain_core.runnables import Runnable

        # Define a simple query node
        class QueryNode(Runnable):
            def invoke(self, input, config, **kwargs):
                query = input.get("query")
                return {"response": f"Processed query: {query}."}

        # Set up the graph
        self.graph = Graph()
        self.graph.add_node("query_node", QueryNode())
        self.graph.add_edge("query_node", END)
        self.graph.set_entry_point("query_node")

        print("Graph setup complete.")

    @entrypoint
    def handle_query(self, event):
        # Process the query
        initial_state = {"query": event.get("query")}
        app = self.graph.compile()
        result = app.invoke(initial_state)
        print(result)
        return result["response"]

