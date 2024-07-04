import sys
import os

# Add the src directory to the sys.path so we can import main from there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.main import handler

# Now Netlify can use the handler to process requests