from app_samples.base_app import BaseLanggraphApp
from langgraph.graph import END, Graph
from app_samples.rag_with_vector_store.graph_nodes import RetrieveNode, GenerateAnswerNode
from app_samples.rag_with_vector_store.document_loader import load_and_split_document
from app_samples.rag_with_vector_store.vector_store import setup_vector_store

class RagWithVectorStoreApp(BaseLanggraphApp):
    
    def create_graph(self):
        chunks = load_and_split_document()
        retriever = setup_vector_store(chunks)


        graph = Graph()
        retrieve_node = RetrieveNode(retriever)
        generate_node = GenerateAnswerNode()
        
        graph.add_node("retrieve", retrieve_node)
        graph.add_node("generate", generate_node)

        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)

        graph.set_entry_point("retrieve")
        
        return graph