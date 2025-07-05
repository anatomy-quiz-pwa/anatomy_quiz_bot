# Bridge file for Render deployment
# This file imports the FastAPI app from app_supabase.py
# so that gunicorn app:app works correctly

from app_supabase import app

# The app object is now available for gunicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 