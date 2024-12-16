from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

if __name__ == "__main__":
    # Define the translation prompt template
    summary_prompt = """
    You are a translator. Translate the given input text into the desired language:
    
    Input Text: {input-text}
    Desired Language: {desired-language}
    """

    # Create a prompt template with the new variable names
    prompt_template = PromptTemplate(input_variables=['input-text', 'desired-language'], template=summary_prompt)

    # Initialize the Google Generative AI chat model
    llm = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        api_key = 'AIzaSyBsk9teXzKWVHeOKHN_PbVBAVZ3CI5oV5k'  # Ensure GOOGLE_API_KEY is set as an environment variable
    )

    # Combine the prompt template and LLM into a chain
    chain = prompt_template | llm | StrOutputParser()

    # Take user input for text and desired language
    input_text = input("Enter the text you want to translate: ")
    desired_language = input("Enter the desired language for translation: ")

    # Invoke the chain with user inputs
    res = chain.invoke({"input-text": input_text, "desired-language": desired_language})

    # Display the result
    print("\nTranslated Text:")
    print(res)
