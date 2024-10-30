from app_samples.simple_langgraph_app import SimpleLanggraphApp
from framework import initialize, entrypoint, application

@application
class MyApp:
    def __init__(self):
        self.graph = None
    
    @initialize
    def setup_graph(self):
        self.graph = SimpleLanggraphApp().create_graph()

    @entrypoint
    def handle_query(self, event):
        # Process the query
        initial_state = {"query": event.get("query")}
        app = self.graph.compile()
        result = app.invoke(initial_state)
        print(result)
        return result["response"]

