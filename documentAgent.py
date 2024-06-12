from Agent import Agent
import os
from gradientai import Gradient



os.environ['GRADIENT_WORKSPACE_ID']='da7d6671-828b-483e-8198-bd5a243ce5ae_workspace'
os.environ['GRADIENT_ACCESS_TOKEN']='IAvSEN94BDWr7Ivb5m1JQdamE35caBpb'
# Define the Document Processing agent
class DocumentAgent(Agent): 
    def act(self, query: str, context: str) -> dict:
        """
       
        Retrieving data from documents related to party celebration themes, party products .

        Parameters:
        - query (str): The search query (e.g., "I want theme for a party").
        - context(str): previous chat history.This will be usefull for answering the current question 

        Returns:
        - response got from document retrival model.
       
        """

        gradient = Gradient()        
        print("document query ================")
        print(query)
        query_with_context = f"Context:\n{context}\n\nUser: {query}"
        response= gradient.answer(
                question=query_with_context,
                source ={
                "type": "rag",
              "collectionId": "242b6ade-448b-4bc9-abca-79e6ce0028af_rag_config" })['answer']
        return response