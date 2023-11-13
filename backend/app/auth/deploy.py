import logging
from fastapi import APIRouter, Depends, HTTPException, status

logging.basicConfig(level=logging.DEBUG)
from fastapi import  HTTPException, Depends
from fastapi.security import APIKeyHeader
from subprocess import run



# Example API key for authentication
API_KEY = "your_secret_api_key"

# API key security
api_key_header = APIKeyHeader(name="X-API-Key")

deployment_router = APIRouter()

# Dependency to validate API key
def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Invalid API key")

# Redeployment endpoint
@deployment_router.post("/redeploy", response_model=dict)
async def redeploy(api_key: str = Depends(get_api_key)):
    """
    Trigger redeployment of Docker container.
    """
    try:
        # Execute your redeployment script or Docker commands
        result = run(["./redeployment_script.sh"], check=True)
        return {"status": "success", "message": "Redeployment triggered successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error triggering redeployment: {str(e)}"}
