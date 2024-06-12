from Agent import Agent
from vanna.remote import VannaDefault

class VannaAgent(Agent):       

    def act (self, query: str, context: str) -> dict:
        
        """
        Getting product information from SQL regarding products and their prices.

        paramter :
         - query (str): The search query (e.g., "tell me price of products")

        response : 
         - returns the result containing data from SQL. 
        
        """
        print("into vanna Query = " +query)
        query = query 
        context = context
        vanna_client = VannaDefault(api_key="2a4c36269aec466593e20027ef8e5975", model='a_i')
        # Connect to the specified SQL Server using the provided ODBC connection string
        odbc_conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=Demo\\SQLDEV2022;DATABASE=nop_commerce;UID=sa;PWD=12345'
        vanna_client.connect_to_mssql(odbc_conn_str=odbc_conn_str)
        generated_sql = vanna_client.generate_sql(question=query, allow_llm_to_see_data=True)
        # Run the generated SQL query
        result = vanna_client.run_sql(sql=generated_sql)
        return result