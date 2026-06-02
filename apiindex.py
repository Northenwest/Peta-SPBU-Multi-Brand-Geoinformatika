import os
import sys
import streamlit.web.cli as stcli

def handler(request):
    # Mengarahkan argumen untuk menjalankan app.py Anda
    sys.argv = ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    stcli.main()