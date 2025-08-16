import argparse

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import rich
from gpt4shell.settings import get_config, create_example_config, SUPPORTED_PROVIDERS


def create_model(config):
    """Create a language model based on the configuration."""
    provider = config.get("provider", "openai").lower()
    
    if provider not in SUPPORTED_PROVIDERS:
        supported_list = ", ".join(SUPPORTED_PROVIDERS)
        raise ValueError(f"Unsupported provider: {provider}. Currently supported providers: {supported_list}")
    
    if provider == "openai":
        model_kwargs = {
            "model": config.get("model", "gpt-3.5-turbo"),
            "temperature": config.get("temperature", 1.0),
        }
        
        # Add optional parameters if specified
        if config.get("max_tokens"):
            model_kwargs["max_tokens"] = config["max_tokens"]
        if config.get("api_base"):
            model_kwargs["openai_api_base"] = config["api_base"]
            
        return ChatOpenAI(**model_kwargs)


def main():
    parser = argparse.ArgumentParser(description='Ask a question to GPT-4')
    parser.add_argument('question', type=str, nargs='?', help='The question to ask GPT-4')
    parser.add_argument('--config-example', action='store_true', 
                       help='Create an example configuration file and exit')
    args = parser.parse_args()

    # Handle config example creation
    if args.config_example:
        create_example_config()
        return 0

    # Ensure question is provided when not creating config example
    if not args.question:
        parser.error("Question is required unless using --config-example")

    # Load configuration
    config = get_config()
    
    # Create prompt template from config
    prompt_template = config.get("prompt_template", 
                                "Answer the question from the user in simple terms:\n{question}")
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Create model from config
    model = create_model(config)
    output_parser = StrOutputParser()

    # Execute the chain
    chain = prompt | model | output_parser
    answer = chain.invoke({"question": args.question})

    rich.print(answer)

