import subprocess
import uuid
from pathlib import Path

from .config import (
    SD_CLI,
    DIFFUSION_MODEL,
    TEXT_ENCODER,
    VAE,
    DEFAULT_BACKEND,
    OUTPUT_DIR,
)
from .models import GenerateRequest


class StableDiffusionCPP:
    def __init__(self) -> None:
        self.sd_cli = SD_CLI

    def _check_file(self, path: Path, name: str) -> None:
        if not path.exists():
            raise FileNotFoundError(f"{name} not found: {path}")

        if not path.is_file():
            raise RuntimeError(f"{name} is not a file: {path}")

    def check_installation(self) -> None:
        self._check_file(self.sd_cli, "sd-cli")
        self._check_file(DIFFUSION_MODEL, "Diffusion model")
        self._check_file(TEXT_ENCODER, "Text encoder")
        self._check_file(VAE, "VAE")

    def list_devices(self) -> str:
        self._check_file(self.sd_cli, "sd-cli")

        result = subprocess.run(
            [str(self.sd_cli), "--list-devices"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"sd-cli --list-devices failed:\n{result.stderr}"
            )

        return result.stdout

    def build_command(self, request: GenerateRequest, output_path: Path) -> list[str]:
        return [
            str(self.sd_cli),

            "--diffusion-model",
            str(DIFFUSION_MODEL),

            "--vae",
            str(VAE),

            "--llm",
            str(TEXT_ENCODER),

            "--backend",
            DEFAULT_BACKEND,

            "-p",
            request.prompt,

            "-W",
            str(request.width),

            "-H",
            str(request.height),

            "--steps",
            str(request.steps),

            "--seed",
            str(request.seed),

            "-o",
            str(output_path),
        ]

    def generate(self, request: GenerateRequest) -> Path:
        self.check_installation()

        output_name = f"{uuid.uuid4().hex}.png"
        output_path = OUTPUT_DIR / output_name

        command = self.build_command(request, output_path)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "stable-diffusion.cpp failed.\n\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )

        if not output_path.exists():
            raise RuntimeError(
                "stable-diffusion.cpp finished successfully, "
                "but output image was not created.\n\n"
                f"STDOUT:\n{result.stdout}"
            )

        return output_path