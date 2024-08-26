import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

"""
Configurec logging to both console and file (monitor logs in real-time &
 retains them for future analysis)
"""
logging.basicConfig(
    level=logging.INFO,  # Set the default log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log"),  # Log to a file
    ],
)

logger = logging.getLogger(__name__)

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        method = request.method
        url = request.url.path
        client_ip = request.client.host
        logger.info(f"DateTime: {request_time}, Method: {method}, URL: {url}, Client IP: {client_ip}")
        # Proceed with the request and capture the response
        response = await call_next(request)
        response_status = response.status_code
        logger.info(f"Response Status: {response_status} for URL: {url}")
        return response
