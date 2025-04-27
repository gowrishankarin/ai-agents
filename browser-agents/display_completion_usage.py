from dataclasses import dataclass

@dataclass
class CompletionTokensDetails:
    accepted_prediction_tokens: int
    audio_tokens: int
    reasoning_tokens: int
    rejected_prediction_tokens: int

@dataclass
class PromptTokensDetails:
    audio_tokens: int
    cached_tokens: int

@dataclass
class CompletionUsage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: CompletionTokensDetails
    prompt_tokens_details: PromptTokensDetails

def print_usage(usage: CompletionUsage):
    print("🔍 Chat Completion API Usage Summary")
    print("===================================")
    print(f"🧠 Prompt Tokens        : {usage.prompt_tokens}")
    print(f"💬 Completion Tokens    : {usage.completion_tokens}")
    print(f"🧾 Total Tokens         : {usage.total_tokens}")
    print("\n🔍 Prompt Token Details:")
    print(f"  🎵 Audio Tokens       : {usage.prompt_tokens_details.audio_tokens}")
    print(f"  🧊 Cached Tokens      : {usage.prompt_tokens_details.cached_tokens}")
    print("\n✍️ Completion Token Details:")
    print(f"  ✅ Accepted Predictions : {usage.completion_tokens_details.accepted_prediction_tokens}")
    print(f"  ❌ Rejected Predictions : {usage.completion_tokens_details.rejected_prediction_tokens}")
    print(f"  🧠 Reasoning Tokens     : {usage.completion_tokens_details.reasoning_tokens}")
    print(f"  🎧 Audio Tokens         : {usage.completion_tokens_details.audio_tokens}")
    print("===================================")
