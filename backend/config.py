from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SD_CPP_DIR = Path.home() / "stable-diffusion.cpp"
SD_CLI = SD_CPP_DIR / "build" / "bin" / "sd-cli"

MODELS_DIR = Path.home() / "AI" / "Z-Image" / "models"

DIFFUSION_MODEL = MODELS_DIR / "z-image-turbo-Q6_K.gguf"
TEXT_ENCODER = MODELS_DIR / "Qwen3-4B-Q4_K_M.gguf"
VAE = MODELS_DIR / "ae.safetensors"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

DEFAULT_BACKEND = "diffusion=vulkan0,te=cpu,vae=cpu"

DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_STEPS = 9
DEFAULT_SEED = -1


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)