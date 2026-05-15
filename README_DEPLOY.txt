CONTENTFORGE PHONE-FIXED VERSION

Upload/replace these files in the root of your GitHub repository:
1) main.py
2) requirements.txt

Render settings:
- Root Directory: leave empty
- Build Command: pip install -r requirements.txt
- Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
