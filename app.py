import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, JSON
from sqlalchemy.orm import sessionmaker
import datetime
import sqlalchemy
from cartAgent import CartAgent
from documentAgent import DocumentAgent
from llama3Agent import LLaMA3Agent
from vannaAgent import VannaAgent
from classifierAgent import ClassifierAgent
from langchain_community.llms import Ollama
from langchain.prompts import  PromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate,AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image



# Set up database
DATABASE_URL = "sqlite:///chat_history.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = sqlalchemy.orm.declarative_base()

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    context = Column(JSON)  # To store the conversation context

class ActionState(Base):
    __tablename__ = 'action_state'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    action = Column(String)
    state = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.now())

# Base.metadata.create_all(engine)

# Initialize the LLaMA 3 model
llm = Ollama(model='llama3')

  

# Instantiate agents
classifier_agent = ClassifierAgent()
document_agent = DocumentAgent()
llama3_agent = LLaMA3Agent()
vanna_ai_agent = VannaAgent()  
Cart_agent = CartAgent()


# Create the main agent executor
class MainAgentExecutor():

    def __init__(self):
        """You are a helpful sales agent, who provides information about products and their prices. Being sales person be a good negotiator and pursue user to buy the products"""    
        self.agents = {
            "DB": vanna_ai_agent,
            "DOC": document_agent,
            "NLG": llama3_agent,
            "CART":  Cart_agent
           
        }

    def get_context(self, user_id):
        session = Session()
        history = session.query(ChatHistory).filter_by(user_id=user_id).order_by(ChatHistory.timestamp).all()
        # context = [entry.message for entry in history]
        session.close()
        return history

    def get_action_state(self, user_id):
        session = Session()
        state = session.query(ActionState).filter_by(user_id=user_id).order_by(ActionState.timestamp.desc()).first()
        session.close()
        return state

    def save_action_state(self, user_id, action, state):
        session = Session()
        action_state = ActionState(user_id=user_id, action=action, state=state)
        session.add(action_state)
        session.commit()

    def save_context(self, user_id, message, response):
        session = Session()
        chat_history = ChatHistory(user_id=user_id, message=message, response=response)
        session.add(chat_history)
        session.commit()

    def act(self, query: str, user_id: int) -> dict:

        """
        You are a sales person who will be selling products which will be used to celebrate the parties.
        You should be persuasive while convincing the user to buy the products

        language : English

        response : 
        - Give response with products and their descriptions and usages 
        - Try to sell products to user.
        """        

        # Retrieve the context and action state for the user

        context = self.get_context(user_id)       
        
        classification_result = classifier_agent.act(query)
        classification = classification_result['classification']
        query = classification_result['query']
        action = classification
     

       
        # Route to the appropriate agent using dictionary
        agent = self.agents.get(action)
        if agent is not None:
            response = agent.act(query =query, context = context)
        
            print("response === ")
            print(response)
        systemMessagePrompt = SystemMessagePromptTemplate.from_template("You are a sales person who wants to sell products useful for celebrating a party. You will try to summarize  answer : {answer} for the question - {question} and take reference from history: {history}.You have products like Unicorn Foil Balloons, Rainbow Crepe Paper Streamers, Glitter Unicorn Tablecloth, Pin the Horn on the Unicorn Party Game, Unicorn Colouring Books for Kids, Unicorn Cupcake Toppers and Wrappers, Rainbow Fruit Skewers, Unicorn Headbands, Unicorn Stickers. Highlight the product names when giving answers. Don't mention tools name or source name in the response.Only When {question} is related to adding to the cart, then return the link as it is from {answer} as response.")
        humanMessagePrompt = HumanMessagePromptTemplate.from_template('{question}')
          
        chatPromt = ChatPromptTemplate.from_messages([
                systemMessagePrompt, humanMessagePrompt
            
            ])          

        formattedChatPrompt = chatPromt.format_messages(
                question = query,
                answer = response,
                history = context
            )     
          
        answer = llm.invoke(formattedChatPrompt)       
        # Save the context
        self.save_context(user_id, query, answer)       
        return answer

# Instantiate the main agent executor
main_agent_executor = MainAgentExecutor()

st.sidebar.title("STW Party Planner")
st.sidebar.write("Welcome to our party celebration products app! Dive into a realm of enchanting decorations, engaging activities, tantalizing food and drink options, and delightful party favors. Let our AI guide you through the process and offer valuable suggestions to make your celebrations truly memorable. Explore now and transform ordinary occasions into extraordinary experiences!")


logo = Image.open(r"STW-LOGO.png") 

col1, col2, col3 = st.columns(3)
with col1:
            st.write("")
with col2:
            st.image(logo, caption='STW Services')
with col3:
            st.write("")

user_id = 3
st.session_state.messages = []

if not st.session_state.messages  : 
    history = main_agent_executor.get_context(user_id)
   
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for entry in history :
        st.session_state.messages.append({"role": "user", "content": entry.message})
        st.session_state.messages.append({"role": "assistant","content":entry.response})
        


    # ### Write Message History
for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message(msg["role"], avatar="🧑").write(msg["content"])
        else:
            # print(msg["content"])
            st.chat_message(msg["role"], avatar="🤖").write(msg["content"])            


if prompt := st.chat_input():
        print("into prompt query = "+ prompt)
      
        st.chat_message("user", avatar="🧑").write(prompt)
       
        response = main_agent_executor.act(query  = prompt, user_id=user_id)
        st.chat_message("assistant", avatar="🤖").write(response)     
       
