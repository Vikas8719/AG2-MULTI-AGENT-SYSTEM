"""
AG2 Multi-Agent System - Main Entry Point for Streamlit Deployment
This file serves as the main entry point for Streamlit Cloud deployment.
"""

import sys
from pathlib import Path


# Add project root to path if not present
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Import and run the Streamlit app
try:
    from ui.streamlit_app import main
except Exception as e:
    import streamlit as st
    st.error(f"Critical Error during import: {str(e)}")
    sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import streamlit as st
        st.error(f"Application Error: {str(e)}")
        # Print traceback to console as well
        import traceback
        traceback.print_exc()
