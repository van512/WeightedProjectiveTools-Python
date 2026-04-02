import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath("src"))
os.environ["PYTHONPATH"] = "src"

subprocess.run(["streamlit", "run", "streamlit_app/StreamlitApp.py"])
