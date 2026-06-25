"""Client for ComfyUI HTTP API.

Sends workflow JSON to ComfyUI server, monitors progress, and retrieves outputs.
Requires a running ComfyUI instance (default: http://127.0.0.1:8188).
"""

import json
import time
import uuid
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Optional


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8188


class ComfyUIClient:
    """Minimal client for ComfyUI's HTTP/WebSocket API."""

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.base_url = f"http://{host}:{port}"
        self.client_id = str(uuid.uuid4())

    def is_running(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/system_stats")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError):
            return False

    def queue_prompt(self, workflow: dict) -> str:
        """Submit a workflow for execution. Returns prompt_id."""
        payload = json.dumps({
            "prompt": workflow,
            "client_id": self.client_id,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{self.base_url}/prompt",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["prompt_id"]

    def get_history(self, prompt_id: str) -> Optional[dict]:
        """Get execution result for a prompt_id."""
        req = urllib.request.Request(f"{self.base_url}/history/{prompt_id}")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get(prompt_id)

    def wait_for_completion(
        self, prompt_id: str, timeout: int = 600, poll_interval: float = 2.0
    ) -> dict:
        """Poll until the prompt completes or times out."""
        start = time.time()
        while time.time() - start < timeout:
            history = self.get_history(prompt_id)
            if history and history.get("status", {}).get("completed", False):
                return history
            if history and history.get("status", {}).get("status_str") == "error":
                raise RuntimeError(
                    f"ComfyUI execution error: {history.get('status', {})}"
                )
            time.sleep(poll_interval)
        raise TimeoutError(f"Prompt {prompt_id} did not complete within {timeout}s")

    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
        """Download a generated image from ComfyUI."""
        params = urllib.parse.urlencode({
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type,
        })
        req = urllib.request.Request(f"{self.base_url}/view?{params}")
        with urllib.request.urlopen(req) as resp:
            return resp.read()

    def generate_and_save(
        self,
        workflow: dict,
        output_path: Path,
        timeout: int = 600,
    ) -> list[Path]:
        """Queue a prompt, wait for completion, save output images."""
        prompt_id = self.queue_prompt(workflow)
        print(f"Queued prompt: {prompt_id}")

        history = self.wait_for_completion(prompt_id, timeout)
        saved_files: list[Path] = []

        outputs = history.get("outputs", {})
        for node_id, node_output in outputs.items():
            images = node_output.get("images", [])
            for img_info in images:
                img_data = self.get_image(
                    img_info["filename"],
                    img_info.get("subfolder", ""),
                    img_info.get("type", "output"),
                )
                if len(images) == 1:
                    save_path = output_path
                else:
                    stem = output_path.stem
                    suffix = output_path.suffix
                    save_path = output_path.parent / f"{stem}_{img_info['filename']}{suffix}"

                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_bytes(img_data)
                saved_files.append(save_path)
                print(f"Saved: {save_path}")

        return saved_files
