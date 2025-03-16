# ai-agents
AI Agents 

## Python Environment
```
uv --version
uv venv .venv
source .venv/bin/activate
uv pip install -r <(uv pip compile pyproject.toml)
jupyter lab
```


## Environment Variables
Create a .env file in the root folder of the notebooks with the following environment variables
```
OPENAI_API_KEY=
SERPER_API_KEY=
```