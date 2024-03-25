import argparse

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import rich


def main():
    parser = argparse.ArgumentParser(description='Ask a question to GPT-4')
    parser.add_argument('question', type=str, help='The question to ask GPT-4')
    args = parser.parse_args()

    prompt = ChatPromptTemplate.from_template(
        "Answer the question from the user in simple terms:\n{question}"
    )
    model = ChatOpenAI(model="gpt-3.5-turbo")
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    answer = chain.invoke({"question": args.question})

    rich.print(answer)


if __name__ == "__main__":
    raise SystemExit(main())
