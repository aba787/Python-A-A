
from .responder import ChatResponder
import logging

logger = logging.getLogger(__name__)

class RequestRouter:
    def __init__(self):
        self.responder = ChatResponder()
    
    def route_request(self, request_data: dict) -> dict:
        """Route incoming requests to appropriate handlers"""
        try:
            message = request_data.get('message', '').strip()
            
            if not message:
                return {
                    "response": "Please provide a message.",
                    "type": "error",
                    "confidence": 0
                }
            
            # Log the request
            logger.info(f"Processing message: {message}")
            
            # Get response from responder
            result = self.responder.find_response(message)
            
            # Log the response
            logger.info(f"Generated response type: {result.get('type', 'unknown')}")
            
            return result
            
        except Exception as e:
            logger.exception(f"Error routing request: {e}")
            return {
                "response": "An error occurred while processing your request.",
                "type": "error",
                "confidence": 0,
                "error": str(e)
            }
