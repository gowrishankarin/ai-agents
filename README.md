# ai-agents
AI Agents 

## Prerequisites
Install uv from here https://docs.astral.sh/uv/getting-started/installation/

### Python Environment
```
uv --version
uv venv .venv
source .venv/bin/activate
uv pip install -r <(uv pip compile pyproject.toml)
uv pip install -U crewai_tools
jupyter lab
```


### Environment Variables
Create a .env file in the root folder of the notebooks with the following environment variables
```
OPENAI_API_KEY=
SERPER_API_KEY=
```