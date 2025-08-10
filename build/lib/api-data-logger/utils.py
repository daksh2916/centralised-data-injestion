import time
import json
import uuid
import aioboto3
from fastapi import Request
from startlette.middleware.base import BaseHTTPMiddleware
from typing import Any

class APILoggerMiddleware(BaseHTTPMiddleware):
    def __inti__(self, app, bucket: str, region: str, prefix: str = "api_logs"):
        super().__init__(app)
        self.bucket = bucket
        self.region = region
        self.prefix = prefix
        self.s3_client = aioboto3.client('s3', region_name=self.region)

    async def send_data(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        base_key = f"{self.prefix.rstrip('/')}/{request_id}"
        start_time = time.time()

        request_body = await request.body()
        form_data= await self._safe_parse_form_data(request)

        request_data = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "body": request_body.decode('utf-8') if request_body else None,
            "form_data": form_data,

        }

        responense = await call_next(request)

        response_data = {
            "status_code": responense.status_code,
            "headers": dict(responense.headers),
            "body": await responense.body(),
            "elapsed_time": time.time() - start_time
        }

        async with self.s3_client as s3:
            await s3.put_object(
                Bucket=self.bucket,
                Key=f"{base_key}/request.json",
                Body=json.dumps(request_data).encode('utf-8')
            )

            await s3.put_object(
                Bucket=self.bucket,
                Key=f"{base_key}/response.json",
                Body=json.dumps(response_data).encode('utf-8')
            )

            if form_data and isinstance(form_data, dict):
                for key, value in form_data.items():
                    if hasattr(value, 'filename') and  hasattr(value, 'read'):
                        content = await value.read()
                        await s3.put_object(
                            Bucket=self.bucket,
                            Key=f"{base_key}/request_files/{value.filename}",
                            Body=content
                        )
        return responense
    
    async def _safe_parse_form_data(self, request: Request) -> Any:
        try:
            form_data = await request.form()
            return {key: value for key, value in form_data.items()}
        except Exception as e:
            return {"error": str(e)}








