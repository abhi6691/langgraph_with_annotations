from framework import initialize, entrypoint, application
from app_samples.rag_with_vector_store.rag_with_vector_store_app import RagWithVectorStoreApp

@application
class MyApp:
    def __init__(self):
        self.graph = None
    
    @initialize
    def setup_graph(self):
        self.graph = RagWithVectorStoreApp().create_graph()

    @entrypoint
    def handle_query(self, event):
        # Process the query
        initial_state = {"query": event.get("query")}
        app = self.graph.compile()
        result = app.invoke(initial_state)
        print(result)
        return result["response"]

