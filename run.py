"""Run script for the Banking Transactions API.

This script provides a simple way to start the API server.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.banking_api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
