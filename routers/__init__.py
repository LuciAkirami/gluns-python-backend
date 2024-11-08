from .ai_api import router as ai_router
from .bigdata_api import router as bigdata_router

__all__ = [
    'ai_router',
    'bigdata_router'
]