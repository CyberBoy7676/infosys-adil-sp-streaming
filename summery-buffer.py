# for run code : c:\users\adilr\anaconda3\python.exe .\buffer-window-memory.py
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain


# Intialize th echat model
chat = ChatGoogleGenerativeAI(
        model = 'gemini-1.5-flash',
        api_key = 'AIzaSyBsk9teXzKWVHeOKHN_PbVBAVZ3CI5oV5k'
    )

# it creates a summary buffer  memory for the conversation
memory = ConversationSummaryBufferMemory(llm=chat,
                                         max_token_limit=20, # maximum number of tokens to keep in memory
                                         ) 


# it creates a conversation chain with the chat model and the memory
conversation = ConversationChain(
    llm = chat,
    memory = memory,
    verbose=True # to see the conversation flow
)

while True:
    # Here we are taking user input
    user_input = input("\nYou (Human) : ")

    # Check for exit command
    if user_input.lower() in ['over','exit', 'bye']:
        print("Khatam-Tata_bye_bye")   

        # Print the conversation history with the summary
        print("\nConversation Summary: ")
        print(conversation.memory.buffer)
        break

    # here we are getting the response from the AI
    response = conversation.predict(input=user_input)
    print("\nAI ( Generated ) : ", response)