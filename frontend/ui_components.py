"""
Frontend UI Components with Enhanced Styling
"""
import streamlit as st
from pathlib import Path

def inject_custom_css():
    """Inject custom CSS for better styling"""
    st.markdown("""
        <style>
        /* Main container */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Tool card styling */
        .tool-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .tool-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        /* Category section */
        .category-section {
            margin: 20px 0;
        }
        
        /* Hero section */
        .hero-section {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .hero-title {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .hero-subtitle {
            font-size: 1.2em;
            opacity: 0.95;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            height: 60px;
            font-size: 16px;
            font-weight: 500;
            border: 1px solid #e0e0e0;
            background: white;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background: #f0f0f0;
            border-color: #667eea;
            transform: translateY(-1px);
        }
        
        /* File uploader */
        .uploadedFile {
            border-radius: 8px;
            background: #f8f9fa;
        }
        
        /* Success/Error messages */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
            margin-top: 50px;
        }
        
        /* Tool interface card */
        .tool-interface {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #667eea;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
        }
        
        /* Category filters */
        .category-filter {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def render_hero_section():
    """Render hero section at the top of the page"""
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">📄 Every tool you need to work with PDFs</div>
            <div class="hero-subtitle">
                Merge, split, compress, convert, rotate, unlock and watermark PDFs with just a few clicks.
                <br>All tools are 100% FREE and easy to use!
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_category_tabs(tools_data):
    """Render category tabs for navigation"""
    tab_names = ["All Tools"] + list(tools_data.keys())
    tabs = st.tabs(tab_names)
    
    return tabs, tab_names

def render_tool_card(category, tool_data, tool_key):
    """Render a tool as a card with icon and description"""
    col1, col2 = st.columns([1, 20])
    
    with col1:
        st.markdown(f"<div style='font-size: 2em;'>{tool_data['icon']}</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button(
            tool_data['name'],
            key=f"btn_{tool_key}",
            use_container_width=True,
            help=tool_data['description']
        ):
            return True
    
    return False

def render_tool_interface(category, tool_data, tools_data):
    """Render the tool interface with file upload and options"""
    st.markdown(f"""
        <div class="tool-interface">
            <h2>{tool_data['icon']} {tool_data['name']}</h2>
            <p style='color: #666; font-size: 1.1em;'>{tool_data['description']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    return tool_data

def render_stats_section(stats):
    """Render statistics section"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3>31+</h3>
                <p>PDF Tools</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3>100%</h3>
                <p>Free to Use</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3>Secure</h3>
                <p>Files Auto-Deleted</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card">
                <h3>Fast</h3>
                <p>Instant Processing</p>
            </div>
        """, unsafe_allow_html=True)

def render_footer(logo_path: Path = None):
    """Render enhanced footer"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if logo_path and logo_path.exists():
            st.image(str(logo_path), width=100)
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <p style='color: #666; font-size: 16px; margin-bottom: 10px;'>
                    <strong>All rights reserved © Shivam IT Solutions</strong>
                </p>
                <p style='color: #999; font-size: 14px;'>
                    Professional PDF Tools | Secure & Fast Processing
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pass

def show_processing_animation(message: str = "Processing..."):
    """Show processing animation"""
    with st.spinner(message):
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
        return progress_bar

def show_success_message(tool_name: str, filename: str, additional_info: dict = None):
    """Show success message with file info"""
    st.success(f"✅ **{tool_name}** completed successfully!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📄 **File:** {filename}")
    
    if additional_info:
        with col2:
            for key, value in additional_info.items():
                st.info(f"**{key}:** {value}")

def show_error_message(error_msg: str):
    """Show error message"""
    st.error(f"❌ **Error:** {error_msg}")

def render_feature_grid(features: list):
    """Render features in a grid layout"""
    cols = st.columns(3)
    
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="tool-card">
                    <h3>{feature['icon']} {feature['title']}</h3>
                    <p>{feature['description']}</p>
                </div>
            """, unsafe_allow_html=True)
