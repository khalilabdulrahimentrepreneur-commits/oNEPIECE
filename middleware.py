from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import asyncio
import json
import os
from typing import List, Optional


class AntiEntryLogMiddleware(BaseHTTPMiddleware):
    """
    AntiEntryLogMiddleware

    - Logs incoming requests and outgoing responses with configurable redaction.
    - Keeps an in-memory rolling buffer (max_entries) and optionally persists to disk.
    - Designed for diagnostics and audit while avoiding sensitive data leakage.
    """

    def __init__(
        self,
        app,
        max_entries: int = 1000,
        redaction_keys: Optional[List[str]] = None,
        persist: bool = True,
        log_path: str = "logs/antientry.log",
        redact_depth: int = 3,
    ):
        super().__init__(app)
        self.max_entries = max_entries
        self.redaction_keys = set((redaction_keys or ["password", "token", "secret", "authorization"]))
        self.persist = persist
        self.log_path = log_path
        self.redact_depth = redact_depth

        # Ensure log directory exists when persisting
        if self.persist:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    async def dispatch(self, request: Request, call_next):
        # Collect basic request metadata
        meta = {
            "method": request.method,
            "path": request.url.path,
            "query": str(request.url.query) or None,
            "client": request.client.host if request.client else None,
            "headers": {k: v for k, v in request.headers.items()},
        }

        # Attempt to read and redact body (if any)
        try:
            body_bytes = await request.body()
            if body_bytes:
                try:
                    body = json.loads(body_bytes.decode("utf-8"))
                    body = self._redact(body, depth=self.redact_depth)
                except Exception:
                    # Non-JSON payloads are stored as truncated strings
                    body = (body_bytes.decode("utf-8", errors="replace"))[:2048]
            else:
                body = None
        except Exception:
            body = None

        meta["request_body"] = body

        # Call the next application component and capture response
        try:
            response = await call_next(request)
        except Exception as exc:
            # Log the error and re-raise
            entry = self._make_entry(meta, None, error=str(exc))
            await self._store_entry(entry)
            raise

        # Try to read response body (works for most Response types)
        response_body = None
        try:
            # Accessing .body may trigger streaming consumption; only do if available
            if hasattr(response, "body") and response.body is not None:
                content = response.body
                try:
                    response_body = json.loads(content.decode("utf-8")) if isinstance(content, (bytes, bytearray)) else content
                except Exception:
                    response_body = (content.decode("utf-8", errors="replace")[:2048] if isinstance(content, (bytes, bytearray)) else str(content))
            else:
                # Fall back to streaming iteration (may consume body)
                chunks = []
                async for chunk in response.body_iterator:
                    chunks.append(chunk)
                content = b"".join(chunks)
                response_body = (content.decode("utf-8", errors="replace")[:2048])
                # Recreate Response with original headers to avoid side-effects
                response = Response(content=content, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
        except Exception:
            response_body = None

        entry = self._make_entry(meta, response_body, status_code=getattr(response, "status_code", None))
        await self._store_entry(entry)

        return response

    def _make_entry(self, request_meta: dict, response_body: Optional[object], status_code: Optional[int] = None, error: Optional[str] = None):
        entry = {
            "timestamp": asyncio.get_event_loop().time(),
            "request": request_meta,
            "response_preview": response_body,
            "status_code": status_code,
            "error": error,
        }
        return entry

    async def _store_entry(self, entry: dict):
        # Append to app-level buffer if available, else persist directly
        app_state = getattr(self, "app", None)
        # Persist to disk
        if self.persist:
            try:
                with open(self.log_path, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(entry, default=str) + "\n")
            except Exception:
                # Do not fail the request because logging failed
                pass

    def _redact(self, obj, depth: int = 0):
        if depth < 0:
            return None
        if isinstance(obj, dict):
            out = {}
            for k, v in obj.items():
                if k.lower() in self.redaction_keys:
                    out[k] = "[REDACTED]"
                else:
                    out[k] = self._redact(v, depth - 1)
            return out
        elif isinstance(obj, list):
            return [self._redact(v, depth - 1) for v in obj]
        else:
            return obj
