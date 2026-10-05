from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import OUTPUT_DIR
from .models import GenerateRequest
from .sd_cpp import StableDiffusionCPP


app = FastAPI(
    title="SD.CPP WebUI",
    version="0.1.0",
)


sd_cpp = StableDiffusionCPP()


@app.get("/api/health")
def health():
    return {
        "status": "ok",
    }


@app.get("/api/devices")
def devices():
    try:
        output = sd_cpp.list_devices()

        return {
            "success": True,
            "output": output,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@app.post("/api/generate")
def generate(request: GenerateRequest):
    try:
        output_path = sd_cpp.generate(request)

        return {
            "success": True,
            "image": f"/outputs/{output_path.name}",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUT_DIR),
    name="outputs",
)

app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)