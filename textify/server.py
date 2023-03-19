from typing import List, Callable, Optional

import uvicorn
import yaml
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from .utils import get_logger


class RequestBody(BaseModel):
    text: List[str]
    lang: str


class ResponseBody(BaseModel):
    text: Optional[List[str]] = None
    success: bool
    message: str


class TextProcessingServer:
    def __init__(self, cleaner: Callable, host: str = '0.0.0.0', port=18899,
                 endpoint: str = "clean_text", auth_token: Optional[str] = "sadkek",
                 logs_dir: str = "logs"):
        self.cleaner = cleaner
        self.host = host
        self.port = port
        self.app = FastAPI()
        self.endpoint = endpoint
        self.auth_token = auth_token
        self.logger = get_logger(logs_dir, logger_name="text-processing")

    def _setup_endpoints(self):
        @self.app.post(f"/{self.endpoint}")
        async def clean_text_endpoint(request: RequestBody,
                                      auth_token: str = Header()) -> ResponseBody:
            self.logger.info(f"received request to clean text: {request.text}")

            if self.auth_token and auth_token != self.auth_token:
                self.logger.info(f"Invalid authorization token, token: {auth_token}, text: {request.text}")
                raise HTTPException(status_code=401, detail="Invalid token")
            lang = request.lang.lower()

            if lang not in {"ar", "en", "neutral"}:
                self.logger.info(f"Invalid lang, lang: {lang}, text: {request.text}")
                raise HTTPException(status_code=400, detail=f"Invalid language: {lang}")

            try:
                clean_text = self.cleaner(request.text, lang)
                self.logger.info(f"original text: {request.text}\t clean text: {clean_text}")
                return ResponseBody(text=clean_text, success=True, message="text cleaned")

            except Exception as e:
                import traceback
                self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
                return ResponseBody(success=False, message=f"{str(e)}")

    def serve(self):
        self.logger.info("Starting up the server")
        self._setup_endpoints()
        self.logger.info("Setup complete")
        uvicorn.run(self.app, host=self.host, port=self.port)


def load_server(cleaner: Callable,
                configs_file: str = r"configs/cleaner_configs.yaml") -> TextProcessingServer:
    with open(configs_file, "r") as f:
        configs = yaml.safe_load(f)['server_configs']
    return TextProcessingServer(cleaner=cleaner, **configs)
