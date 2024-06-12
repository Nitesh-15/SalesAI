import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle

# Sample labeled data
data = {
    'query': [
        "I have birthday party, Suggest me ideas to celebrate it?",
        "product price",
        "add Unicorn Foil Balloons to the cart",
        "hi",
        "party theme for a birthday celebration.",
        "tell me price of Unicorn Coloring Books for Kids",
        "products to the cart",
        "hello", 
        "products available for party celebration",    
        "describe unicorn foil balloons with its price.",               
        "buy products",       
        "how are you",
        "tell me product details",
        "price for products",
        "Add all products in cart",
        "Good Morning",
        "products,themes,details",
        "productId of product,price",
        "Add product in cart having name as ",
        "have a nice day"
    ],
    'label': ['DOC','DB','CART','NLG', 'DOC','DB','CART','NLG', 'DOC', 'DB','CART','NLG','DOC', 'DB','CART','NLG','DOC', 'DB','CART','NLG']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['query'], df['label'], test_size=0.2, random_state=42)

# Print the training and test sets to debug
print("Training data:")
print(X_train)
print(y_train)
print("Test data:")
print(X_test)
print(y_test)

# Create a pipeline with TF-IDF vectorizer and Logistic Regression classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(f"Predicted labels: {y_pred}")
print(f"True labels: {y_test.tolist()}")
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Save the model to a file
with open('classifier_model.pkl', 'wb') as file:
    pickle.dump(pipeline, file)