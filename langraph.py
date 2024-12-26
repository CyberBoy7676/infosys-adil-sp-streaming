# # sir code 

# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.graph import StateGraph, END
# from langchain.prompts.prompt import PromptTemplate
# from typing import TypedDict

# # Managing the state of the chatbot
# class ChatbotState(TypedDict):
#     history: list

# # Creating a node to generate a response using LLM.
# def llm_node(state: ChatbotState) -> ChatbotState:
#     llm = ChatGoogleGenerativeAI(
#         model='gemini-1.5-flash',
#         api_key = 'AIzaSyBsk9teXzKWVHeOKHN_PbVBAVZ3CI5oV5k'  # Securely fetch the API key
#     )

#     # Get the last user message from history
#     user_message = state["history"][-1]

#     prompt = PromptTemplate(
#         input_variables=["userInput"],
#         template="You are a helpful chatbot. {userInput}"
#     )

#     chain = prompt | llm
#     response = chain.invoke({"userInput": user_message})

#     state["history"].append(response.content)
#     return state

# def create_graph():
#     # Defining the graph
#     graph = StateGraph(ChatbotState)

#     # Add the node
#     graph.add_node("llm_response", llm_node)

#     # Define the flow of the graph
#     graph.set_entry_point("llm_response")  # Starting node
#     graph.add_edge("llm_response", END)   # Ending node

#     return graph

# if __name__ == "__main__":
#     # Building the graph
#     chatbot_graph = create_graph()
#     app = chatbot_graph.compile()

#     # Initialize the chatbot state with an empty history list
#     state: ChatbotState = {"history": []}

#     # Chat loop
#     print("Chatbot: Hello!")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit":
#             print("Chatbot: Goodbye!")
#             break

#         # Update state with user input
#         state["history"].append(user_input)

#         # Run the graph
#         try:
#             state = app.invoke(state)
#             print(f"Chatbot: {state['history'][-1]}")
#         except Exception as e:
#             print(f"Chatbot: Sorry, something went wrong. {e}")



# # updated code 
# import os
# import random
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.graph import StateGraph, END
# from langchain.prompts.prompt import PromptTemplate
# from typing import TypedDict

# # Managing the state of the chatbot
# class ChatbotState(TypedDict):
#     history: list
#     quiz_index: int
#     quiz_answer: str

# # Creating a node to generate a response using LLM.
# def llm_node(state: ChatbotState) -> ChatbotState:
#     llm = ChatGoogleGenerativeAI(
#         model='gemini-1.5-flash',
#         api_key='AIzaSyBsk9teXzKWVHeOKHN_PbVBAVZ3CI5oV5k'  # Securely fetch the API key
#     )

#     # Get the last user message from history
#     user_message = state["history"][-1]

#     prompt = PromptTemplate(
#         input_variables=["userInput"],
#         template="You are a helpful chatbot. {userInput}"
#     )

#     chain = prompt | llm
#     response = chain.invoke({"userInput": user_message})

#     state["history"].append(response.content)
#     return state

# # Greeting Node
# def greeting_node(state: ChatbotState) -> ChatbotState:
#     import datetime
#     hour = datetime.datetime.now().hour
#     if hour < 12:
#         greeting = "Good morning!"
#     elif hour < 18:
#         greeting = "Good afternoon!"
#     else:
#         greeting = "Good evening!"
#     state["history"].append(f"{greeting} Did you know? Honey never spoils!")
#     return state

# # Fun Fact Node
# def fun_fact_node(state: ChatbotState) -> ChatbotState:
#     facts = [
#         "Did you know? Honey never spoils!",
#         "Fun fact: A day on Venus is longer than a year on Venus!",
#         "Did you know? Octopuses have three hearts!",
#         "Fun fact: Bananas are berries, but strawberries aren't!"
#     ]
#     fact = random.choice(facts)
#     state["history"].append(fact)
#     return state

# # Math Solver Node
# def math_solver_node(state: ChatbotState) -> ChatbotState:
#     user_message = state["history"][-1]
#     try:
#         result = eval(user_message)
#         response = f"The answer to your problem is: {result}"
#     except:
#         response = "I can only solve simple math problems. Please try again!"
#     state["history"].append(response)
#     return state

# # Quiz Node with Fun Facts
# def quiz_node(state: ChatbotState) -> ChatbotState:
#     questions = [
#         {"question": "What is the capital of France?", "options": ["A) Paris", "B) London", "C) Berlin"], "answer": "A"},
#         {"question": "What is 5 + 7?", "options": ["A) 10", "B) 12", "C) 15"], "answer": "B"},
#         {"question": "Which planet is known as the Red Planet?", "options": ["A) Earth", "B) Mars", "C) Jupiter"], "answer": "B"}
#     ]

#     # Initialize quiz state if not already present
#     if "quiz_index" not in state:
#         state["quiz_index"] = 0
#         state["quiz_in_progress"] = True

#     quiz_index = state["quiz_index"]

#     if quiz_index < len(questions):
#         question = questions[quiz_index]
#         state["history"].append(f"{question['question']} {', '.join(question['options'])}")
#         state["quiz_answer"] = question["answer"]
#         state["quiz_index"] += 1
#     else:
#         state["history"].append("Quiz completed! Great job!")
#         state["quiz_index"] = 0  # Reset quiz index for next round
#         state["quiz_in_progress"] = False

#         # Add a fun fact after the quiz
#         fun_facts = [
#             "Did you know? Cats have five toes on their front paws but only four on their back ones!",
#             "Fun fact: Sharks existed before trees!",
#             "Did you know? Wombat poop is cube-shaped to avoid rolling away!"
#         ]
#         state["history"].append(random.choice(fun_facts))
#     return state

# def create_graph():
#     # Defining the graph
#     graph = StateGraph(ChatbotState)

#     # Add nodes
#     graph.add_node("greeting", greeting_node)
#     graph.add_node("llm_response", llm_node)
#     graph.add_node("fun_fact", fun_fact_node)
#     graph.add_node("math_solver", math_solver_node)
#     graph.add_node("quiz", quiz_node)

#     # Define the flow of the graph
#     graph.set_entry_point("greeting")  # Starting node
#     graph.add_edge("greeting", "llm_response")
#     graph.add_edge("llm_response", "fun_fact")
#     graph.add_edge("fun_fact", "math_solver")
#     graph.add_edge("math_solver", "quiz")
#     graph.add_edge("quiz", END)  # Ending node

#     return graph

# if __name__ == "__main__":
#     # Building the graph
#     chatbot_graph = create_graph()
#     app = chatbot_graph.compile()

#     # Initialize the chatbot state with an empty history list
#     state: ChatbotState = {"history": [], "quiz_index": 0, "quiz_answer": ""}

#     # Chat loop
#     print("Chatbot: Hello!")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit":
#             print("Chatbot: Goodbye!")
#             break

#         # Update state with user input
#         state["history"].append(user_input)

#         # Run the graph
#         try:
#             state = app.invoke(state)
#             print(f"Chatbot: {state['history'][-1]}")
#         except Exception as e:
#             print(f"Chatbot: Sorry, something went wrong. {e}")











# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.graph import StateGraph, END
# from langchain.prompts.prompt import PromptTemplate

# from typing import TypedDict

# # Managing the state of the chatbot
# class ChatbotState(TypedDict):
#     history: list

# # New Node: Preprocessing User Input
# def preprocess_input(state: ChatbotState) -> ChatbotState:
#     # Preprocess the user's input
#     user_message = state["history"][-1]
#     cleaned_message = user_message.strip().capitalize()  # Trim whitespace and capitalize the first letter
#     state["history"][-1] = cleaned_message  # Update the last input with cleaned message
#     return state

# # Existing Node: Generate Response using LLM
# def llm_node(state: ChatbotState) -> ChatbotState:
#     llm = ChatGoogleGenerativeAI(
#         model='gemini-1.5-flash',
#         api_key='AIzaSyAcFeg5povb1BkSfXidqsL2a6Ov03zAxx4'
#     )

#     # Get the last user message from history
#     user_message = state["history"][-1]

#     prompt = """
#     You are a helpful chatbot. {userInput}
#     """

#     prompt_template = PromptTemplate(input_variables=["userInput"], template=prompt)
#     chain = prompt_template | llm
#     response = chain.invoke({"userInput": user_message})

#     state["history"].append(response.content)
#     return state

# # New Node: Postprocessing the Response (Fixed)
# def postprocess_response(state: ChatbotState) -> ChatbotState:
#     # Postprocess the LLM response
#     chatbot_response = state["history"][-1]
#     cleaned_response = chatbot_response.strip()  # Remove extra spaces
#     if not cleaned_response.endswith(".") and not cleaned_response.endswith("!") and not cleaned_response.endswith("?"):
#         cleaned_response += "."  # Add a period if no punctuation is present
#     state["history"][-1] = cleaned_response
#     return state


# # Create the StateGraph
# def create_graph():
#     # Define the graph
#     graph = StateGraph(ChatbotState)

#     # Add nodes to the graph
#     graph.add_node("preprocess_input", preprocess_input)  # Preprocess user input
#     graph.add_node("llm_response", llm_node)             # Generate response using LLM
#     graph.add_node("postprocess_response", postprocess_response)  # Postprocess chatbot response

#     # Define the flow of the graph
#     graph.set_entry_point("preprocess_input")  # Starting node
#     graph.add_edge("preprocess_input", "llm_response")  # Preprocessing → LLM response generation
#     graph.add_edge("llm_response", "postprocess_response")  # LLM response → Postprocessing
#     graph.add_edge("postprocess_response", END)  # Postprocessing → End

#     return graph

# if __name__ == "__main__":
#     # Build the graph
#     chatbot_graph = create_graph()
#     app = chatbot_graph.compile()

#     # Initialize the chatbot state with an empty history list
#     state: ChatbotState = {"history": []}

#     # Chat loop
#     print("Chatbot: Hello!")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit":
#             print("Chatbot: Goodbye!")
#             print(f"Chatbot: {state['history']}")
#             break

#         # Update state with user input
#         state["history"].append(user_input)

#         # Run the graph
#         state = app.invoke(state)

#         # Print the last response
#         print(f"Chatbot: {state['history'][-1]}")











import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langchain.prompts.prompt import PromptTemplate
from typing import TypedDict

# Managing the state of the chatbot
class ChatbotState(TypedDict):
    history: list

# Preprocessing User Input Node
def preprocess_input(state: ChatbotState) -> ChatbotState:
    user_message = state["history"][-1]
    cleaned_message = user_message.strip().capitalize()
    state["history"][-1] = cleaned_message
    return state

# Generate Response using LLM Node
def llm_node(state: ChatbotState) -> ChatbotState:
    llm = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        api_key='AIzaSyAcFeg5povb1BkSfXidqsL2a6Ov03zAxx4'
    )

    user_message = state["history"][-1]
    prompt = f"You are a helpful chatbot. {user_message}"

    prompt_template = PromptTemplate(input_variables=["userInput"], template=prompt)
    chain = prompt_template | llm
    response = chain.invoke({"userInput": user_message})

    state["history"].append(response.content)
    return state

# Fun Fact Node
def fun_fact_node(state: ChatbotState) -> ChatbotState:
    fun_facts = [
        "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible.",
        "Fun fact: The shortest war in history lasted only 38 to 45 minutes. It was between Britain and Zanzibar on August 27, 1896.",
        "Did you know? Octopuses have three hearts, and two of them stop beating when they swim.",
        "Fun fact: A day on Venus is longer than a year on Venus!",
        "Did you know? Bananas are berries, but strawberries aren't."
    ]
    fact = random.choice(fun_facts)
    state["history"].append(fact)
    return state

# Postprocessing Response Node
def postprocess_response(state: ChatbotState) -> ChatbotState:
    chatbot_response = state["history"][-1]
    cleaned_response = chatbot_response.strip()
    if not cleaned_response.endswith((".", "!", "?")):
        cleaned_response += "."
    state["history"][-1] = cleaned_response
    return state

# Create the StateGraph
def create_graph():
    graph = StateGraph(ChatbotState)

    # Add nodes
    graph.add_node("preprocess_input", preprocess_input)
    graph.add_node("llm_response", llm_node)
    graph.add_node("fun_fact_node", fun_fact_node)
    graph.add_node("postprocess_response", postprocess_response)

    # Define flow
    graph.set_entry_point("preprocess_input")
    graph.add_edge("preprocess_input", "llm_response")
    graph.add_edge("llm_response", "postprocess_response")
    graph.add_edge("postprocess_response", "fun_fact_node")
    graph.add_edge("fun_fact_node", END)

    return graph

if __name__ == "__main__":
    # Build the graph
    chatbot_graph = create_graph()
    app = chatbot_graph.compile()

    # Initialize chatbot state
    state: ChatbotState = {"history": []}

    # Chat loop
    print("Chatbot: Hello! Ask me anything, or type 'exit' to leave.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            print(f"Chatbot: {state['history']}")
            break

        # Update state with user input
        state["history"].append(user_input)

        # Run the graph
        state = app.invoke(state)

        # Print the last response
        print(f"Chatbot: {state['history'][-1]}")
