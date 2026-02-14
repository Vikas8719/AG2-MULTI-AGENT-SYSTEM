"""Streamlit UI for AG2 Multi-Agent System"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings, setup_logging
from orchestrator import WorkflowManager
import logging
import shutil
import os
import base64

def create_zip(path, zip_name):
    """Create a zip file from a directory"""
    shutil.make_archive(zip_name, 'zip', path)
    return f"{zip_name}.zip"

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Create a download link for binary file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


# Page config
def main():
    st.set_page_config(
        page_title="AG2 Multi-Agent System",
        page_icon="🤖",
        layout="wide"
    )

    # Initialize
    if 'workflow_manager' not in st.session_state:
        logging_config = setup_logging(settings)
        st.session_state.workflow_manager = WorkflowManager(settings)
        st.session_state.logs = []
        st.session_state.workflow_result = None

    # Title
    st.title("🤖 AG2 Multi-Agent System")
    st.markdown("### Production-Ready Multi-Agent Workflow with Streamlit UI")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        cloud_provider = st.selectbox(
            "Cloud Provider",
            ["aws", "gcp", "azure"],
            help="Select target cloud platform"
        )
        
        st.divider()
        st.markdown("### Agent Status")
        agents = ["Analyzer", "Code Generator", "Code Reviewer", "DevOps", "Validator"]
        for agent in agents:
            st.markdown(f"🔵 {agent}")
        
        st.divider()
        st.markdown("### 🧠 Memory System")
        st.success("Vector DB: Active")

    # Main Input Area
    st.markdown("### 🚀 Create New Project")

    # Tabs for Input Method
    tab_text, tab_csv = st.tabs(["📝 Text Instructions", "📂 Upload CSV"])

    input_data = None
    input_type = "text"

    with tab_text:
        task_description = st.text_area(
            "Describe your project idea in detail",
            height=150,
            placeholder="Example: Create a FastAPI backend for a Todo app with PostgreSQL database, including user authentication and Docker support.",
            help="Be specific about technologies and features you want."
        )
        if task_description:
            input_data = task_description
            input_type = "text"

    with tab_csv:
        uploaded_file = st.file_uploader("Upload Requirements CSV", type=['csv'])
        if uploaded_file:
            # Save uploaded file
            csv_path = Path("uploads") / uploaded_file.name
            csv_path.parent.mkdir(exist_ok=True)
            with open(csv_path, 'wb') as f:
                f.write(uploaded_file.read())
            input_data = str(csv_path)
            input_type = "csv"
            st.success(f"✅ Loaded: {uploaded_file.name}")

    # Advanced Settings
    with st.expander("⚙️ Project Configuration", expanded=True):
        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            project_name = st.text_input("Project Name", "ag2-project", help="Name of the generated project folder")
        with col_conf2:
            # Show selected cloud provider from sidebar
            st.info(f"Target Cloud: **{cloud_provider.upper()}**")

    # Action Area
    st.divider()
    col_action, col_status = st.columns([1, 2])

    with col_action:
        start_btn = st.button("✨ Start Agents", type="primary", use_container_width=True)
        reset_btn = st.button("🔄 Reset", use_container_width=True)

    if reset_btn:
        st.session_state.workflow_result = None
        st.rerun()

    # Execution Logic
    if start_btn:
        if not input_data:
            st.warning("⚠️ Please provide project instructions or upload a CSV.")
        else:
            st.session_state.workflow_result = None
            
            # Status callback function
            def status_update(message, step):
                st.write(message)
                # You can add more complex UI updates here if needed
            
            with st.status("🚀 Agents are working...", expanded=True) as status:
                try:
                    result = st.session_state.workflow_manager.execute_workflow(
                        input_data=input_data,
                        input_type=input_type,
                        cloud_provider=cloud_provider,
                        project_name=project_name,
                        status_callback=status_update
                    )
                    
                    st.session_state.workflow_result = result
                    
                    if result['success']:
                        status.update(label="✅ Workflow Completed Successfully!", state="complete", expanded=False)
                    else:
                        status.update(label="❌ Workflow Failed", state="error", expanded=True)
                        st.error(f"Error: {result.get('error')}")
                
                except Exception as e:
                    status.update(label="❌ Critical Error", state="error")
                    st.error(f"Critical System Error: {str(e)}")

    # Result & Download Section
    if st.session_state.workflow_result:
        result = st.session_state.workflow_result
        
        if result.get('success'):
            st.divider()
            st.success("🎉 Project Generation Complete!")
            
            # Results Columns
            r_col1, r_col2 = st.columns([2, 1])
            
            with r_col1:
                st.markdown("### 📂 Generated Artifacts")
                project_path = result.get('project_path')
                if project_path:
                    st.code(f"Location: {project_path}", language="bash")
                    
                    # Show file structure preview if possible
                    if os.path.exists(project_path):
                        files_count = sum([len(files) for r, d, files in os.walk(project_path)])
                        st.info(f"Generated {files_count} files in project directory.")
            
            with r_col2:
                st.markdown("### 📥 Download")
                if project_path and os.path.exists(project_path):
                    # Robust zip creation
                    project_dir_name = os.path.basename(os.path.normpath(project_path))
                    zip_name = f"{project_dir_name}_v1"
                    zip_path = create_zip(project_path, zip_name)
                    
                    with open(zip_path, "rb") as fp:
                        st.download_button(
                            label=" Download ZIP",
                            data=fp,
                            file_name=f"{project_dir_name}.zip",
                            mime="application/zip",
                            type="primary",
                            use_container_width=True
                        )
                
                if result.get('ready_for_approval'):
                    if st.button(" Deploy to Cloud", use_container_width=True):
                        st.toast("Deployment sequence initiated!", icon="🚀")
        
        # Debug/Log details
        with st.expander("📊 Detailed Agent Logs"):
            st.json(result.get('workflow_state', {}))

    # Footer
    st.markdown("---")
    st.caption("Built with AG2 Framework & Streamlit | 🤖 Multi-Agent System")

if __name__ == "__main__":
    main()

