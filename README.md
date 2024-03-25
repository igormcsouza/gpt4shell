# GPT for Shell

[![Publish on Docker Hub](https://github.com/igormcsouza/gpt4shell/actions/workflows/publish.yml/badge.svg)](https://github.com/igormcsouza/gpt4shell/actions/workflows/publish.yml)

A chat for terminal with preatty response

## How to use?

Set the `OPENAI_API_KEY` environment variable (go to the OPENAI to fetch that key). Then run the following command:

```bash
docker run -e OPENAI_API_KEY -it igormcsouza/gptforshell:0.1.0 "<Your question here>"
```

And gpt will answer your question.