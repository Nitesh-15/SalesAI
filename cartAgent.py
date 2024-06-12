from Agent import Agent
from vanna.remote import VannaDefault

class CartAgent(Agent):

    def fetch_product_ids(self,query):
        """
        Fetch product IDs and names based on the user query using VannaAI.

        Parameters:
        - query (str): The search query (e.g., "i want to add balloons").

        Returns:
        - list: A list of product IDs corresponding to the search query.
        """
        print("cart vanna fetch Id")
        # Simulate fetching product data from VannaAI
        # In a real implementation, you would use requests to call the VannaAI API and process the response.
        # This is just a placeholder.
        vanna_client = VannaDefault(api_key="2a4c36269aec466593e20027ef8e5975", model='a_i')
        # Connect to the specified SQL Server using the provided ODBC connection string
        odbc_conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=Demo\\SQLDEV2022;DATABASE=nop_commerce;UID=sa;PWD=12345'
        vanna_client.connect_to_mssql(odbc_conn_str=odbc_conn_str)
        generated_sql = vanna_client.generate_sql(question=query, allow_llm_to_see_data=True)
        # Run the generated SQL query
        response  = vanna_client.run_sql(sql=generated_sql)
        # response = VannaAgent.act(query=query)
        print(response)
        if not response.empty and 'ProductID' in response.columns:
            product_ids = response['ProductID'].tolist()
            print(product_ids)


        # print([product["Name"] for product in response])
        # # Assuming the response is a JSON object with a 'products' key containing a list of products
        # # Each product has 'id' and 'name' keys
        # products = response.json().get('products', [])
        
        # Extract product IDs
        # product_ids = [product['id'] for product in products]
        
        return product_ids

    def generate_add_to_cart_link(self,base_url, product_ids):
        """
        Generate an add to cart URL for nopCommerce.

        Parameters:
        - base_url (str): The base URL of the nopCommerce add to cart page.
        - product_ids (list): A list of product IDs to be added to the cart.

        Returns:
        - str: The full URL for adding the specified products to the cart.
        """
        # Join the product IDs with the pipe character
        products_str = '|'.join(map(str, product_ids))
        
        # Construct the full URL
        full_url = f"{base_url}?products={products_str}"
        print("url = "+full_url)
        return full_url


    def act(self, query: str, context: str):      
        """
            Handle the user query to add products to the cart and generate the add-to-cart link.

            Parameters:
            - query (str): The user query (e.g., "add balloons to cart").
            - base_url (str): The base URL of the nopCommerce add to cart page.

            Returns:
            - str: The full URL for adding the specified products to the cart.
            """
        base_url = "https://nopcommerce.com/addtocart.aspx"
            # Extract the search term from the query (e.g., "balloons")
        search_term = query.replace("add ", "").replace(" to cart", "").strip()
            
            # Fetch product IDs from VannaAI
        product_ids = self.fetch_product_ids(query)
            
            # Generate the add-to-cart link
        add_to_cart_link = self.generate_add_to_cart_link(base_url, product_ids)
            
        return add_to_cart_link