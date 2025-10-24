import os

rits_api_key = os.environ['RITS_API_KEY']
ibm_litellm_api_key=os.environ['IBM_LITELLM_API_KEY']

model_config = {
    "openrouter": {
        "api_key": "Your OpenRouter API Key",
        "base_url": "https://openrouter.ai/api/v1",
    },
    "rits": 
    {
        "base_url": "https://inference-3scale-apicast-production.apps.rits.fmaas.res.ibm.com/gpt-oss-120b/v1", 
        "api_key": rits_api_key,
    },
    "openai": {
        "api_key": "Your OpenAI API Key",
        "base_url": "Your Base URL",
    },
}

# model_config = {
#     #"model_name": {"base_url": "YOUR_API_URL", "api_key": "YOUR_API_KEY"},
#     "gemini": {"base_url": "YOUR_API_URL", "api_key": "YOUR_API_KEY"},
#     "GCP/claude-4-sonnet": {"base_url": "https://ete-litellm.bx.cloud9.ibm.com/v1", "api_key": ibm_litellm_api_key},
#     "GCP/claude-3-7-sonnet": {"base_url": "https://ete-litellm.bx.cloud9.ibm.com/v1", "api_key": ibm_litellm_api_key},
#     "gcp/claude-sonnet-4-5": {"base_url": "https://ete-litellm.bx.cloud9.ibm.com/v1", "api_key": ibm_litellm_api_key},
#     "openai/gpt-oss-120b": {"base_url": "https://inference-3scale-apicast-production.apps.rits.fmaas.res.ibm.com/gpt-oss-120b", "api_key": rits_api_key},
# }
