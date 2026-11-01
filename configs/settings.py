from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

PROMPTS_DIR = ROOT_DIR / "prompts"

MODELS_DIR = ROOT_DIR.parent / "models"

LLM_MODEL = (
    MODELS_DIR
    / "qwen2.5-7b-instruct-q4_k_m.gguf"
)

WHISPER_MODEL = "base"

LLM_CONTEXT = 32768

# -1 = offload all possible layers to Apple Metal
LLM_GPU_LAYERS = -1

LLM_TEMPERATURE = 0.0

LLM_MAX_TOKENS = 4096