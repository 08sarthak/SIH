import openai
import os
from app.models import model_types
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Fetch OpenAI API key from system environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable.")

# # Load the dataset from a spreadsheet (CSV or Excel)
# def load_dataset(file_path):
#     # Assuming CSV for this example, but can be adapted to Excel with pd.read_excel
#     df = pd.read_csv(file_path)
#     return df

# # Convert the dataset to a format that can be use+d in the prompt
# def format_dataset(df):
#     formatted_data = "industry.csv"
#     for index, row in df.iterrows():
#         formatted_data += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
#     return formatted_data

# # Load and format the dataset
# file_path = 'industry.csv'  # Replace with your file path
# df = load_dataset(file_path)
# formatted_dataset = format_dataset(df)
# Define your dataset as a hardcoded text


# Function to query the chatbot
# def chatbot(query):
#     response = chain.run({"dataset": formatted_dataset, "question": query})
#     return response
def chatbot(query):
    dataset = """
    Question,Answer
    What is the purpose of the app?,
    The app connects farmers directly with buyers, eliminating the middleman, ensuring fair prices and fresh produce.
    How do farmers use the app?,
    Farmers can create a profile, list their products, and set their prices. Buyers can browse and purchase directly from them.
    How can buyers find products on the app?,
    Buyers can search by product, location, or category to find fresh produce from nearby farmers.
    Does the app support bulk orders for buyers?
    ,Yes, buyers can place bulk orders directly with farmers for wholesale purchases.
    What payment methods are available on the app?,
    The app supports various payment methods including credit cards, digital wallets, and direct bank transfers.
    How does the app handle delivery logistics?
    ,Farmers can choose to offer delivery themselves or partner with local delivery services integrated into the app.
    Can farmers track sales and orders?
    ,Yes, the app includes a dashboard for farmers to track their sales, manage orders, and communicate with buyers.
    What kind of products can be sold on the app?
    ,Farmers can sell fresh produce, grains, dairy products, and other farm-related goods.
    How can farmers build trust with buyers?
    ,Farmers can display reviews and ratings from previous buyers, ensuring transparency and building trust.
    Does the app offer any insights or analytics to users?,
    Yes, the app provides insights like popular products, seasonal trends, and price comparisons to help both farmers and buyers make informed decisions..
    1. How can I contact my transport service provider?
    A. You can contact your transport service provider as well as your other partners and fellow users through the messages screen. You can access the messages through the top-right icon on the homepage.
    2. How can I share my bills for a service with others?
    A. You can share your services with a group of people and split the bill based on your usage by going to the aggregation tab from the homepage. Click on the plus sign to add a new group and add details of your usage for the partnered service. You can split the bill by accessing your group from the aggregation tab and clicking on "Split the bill with UPI".
    3. How can I add new items to my inventory?
    A. Add a new item to your inventory by clicking on the PLUS sign from the navigation bar on the homepage. Fill in the details of the product and it will get added to your inventory. The item is removed when it is bought by a customer. 
    4. How can I update the things in my inventory?
    You can update the details of a particular item through the Inventory tab that can be accessed from the homepage. Click on the self-stored or externally stored tabs from the top navigation and select the item you wish to update.
    5. How can I add new items to my inventory?
    Add a new item to your inventory by clicking on the PLUS sign from the navigation bar on the homepage. Fill in the details of the product and it will get added to your inventory. The item is removed when it is bought by a customer.
    ...
    """
    # Prepare the prompt template with the dataset
    template = """
    You are a helpful assistant trained on the following data:
    {dataset}

    Question: {question}
    Answer:"""

    # Create the PromptTemplate object
    prompt = PromptTemplate(
        input_variables=["dataset", "question"],
        template=template,
    )

    # Initialize the OpenAI LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai.api_key)

    # Create a chain using the prompt and LLM
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"dataset": dataset, "question": query})
    return response
    
def price_recommend(data: model_types.CropData):

    dataset = {
    "crop_name":data.cropname,
    "crop_quantity":data.quantity,
    "crop_grade_quality":data.qualitygrade}
    # Prepare the prompt template with the dataset
    template = """
    You are given name of a crop ,its quantity and its quality grade and you have to give the estimated selling price of that crop for that particular quantity according to india,use previous knoweledge for the pricing in indian rupees.
    data:{dataset}
    Question: {question}
    Answer:"""

    # Create the PromptTemplate object
    prompt = PromptTemplate(
        input_variables=["dataset", "question"],
        template=template,
    )

    # Use ChatOpenAI for chat models like gpt-3.5-turbo or gpt-4
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai.api_key)

    # Create a chain using the prompt and LLM
    chain = LLMChain(llm=llm, prompt=prompt)
    query = "what is the estimated selling price  of the yield crop?"

    response = chain.run({"dataset": dataset, "question": query})
    return response
