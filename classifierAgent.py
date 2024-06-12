from Agent import Agent 
import pickle

# Load the pre-trained classifier model
with open('classifier_model.pkl', 'rb') as file:
    classifier_model = pickle.load(file)
# Define the classifier agent 
class ClassifierAgent(Agent):
    def classify_query(self, query: str) -> str:
        classification = classifier_model.predict([query])[0]
        print("classification = "+ classification)
        return classification if classification in ['DB', 'DOC', 'CART' ] else 'NLG'

    def act(self, query:str) -> dict:
        # query = agent_input.query
        classification = self.classify_query(query)
        return {"classification": classification, "query": query}