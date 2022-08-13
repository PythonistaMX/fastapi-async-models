#! /usr/bin/env python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", 
                host="0.0.0.0", 
                reload=True, 
                log_level="info")