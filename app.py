
import streamlit as st
import time
import zipfile
from io import BytesIO
from backend.aipipeline import runbatch_pipeline
import base64
from io import BytesIO


st.set_page_config(
    page_title="V2 Retail AI", 
    layout='wide', 
    initial_sidebar_state='expanded'
)

if 'focused_idx' not in st.session_state:
    st.session_state['focused_idx'] = None
if 'results' not in st.session_state:
    st.session_state['results'] = None

# 2. THE AESTHETIC CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&display=swap');
    
    /* 1. MANAGE HEADER: Transparent background, keep toggle interactive */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
        color: white !important;
    }

    /* 2. SIDEBAR TOGGLE: Force visibility and clickability */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        color: white !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 10px 10px 0 !important;
        z-index: 999999 !important;
    }

    /* 3. BACKGROUND & GLOBAL FONT */
    .stApp {
        background: radial-gradient(circle at top right, #34421e, #0f1208);
        color: #f1f8e9;
        font-family: 'Inter', sans-serif;
    }

    /* 4. MAIN TITLE STYLING */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 200;
        letter-spacing: 2px;
        margin-top: -60px; /* Pulls title up since header is transparent */
    }
    .main-subtitle {
        text-align: center;
        opacity: 0.7;
        margin-bottom: 40px;
    }
   

    /* 5. SIDEBAR GLASSMORPHISM */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    /* 6. CENTERED GENERATION BUTTON */
    .stButton>button {
        display: block;
        margin: 0 auto !important;
        background: linear-gradient(90deg, #828e5c, #556b2f) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 45px !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(130, 142, 92, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: Config & Download Zone
with st.sidebar:
    st.markdown("## Configuration")
    
    # Blank first index for dropdowns
    gender = st.selectbox(
        "Model Gender", 
        options=[None, "Female", "Male", "Kid Girl", "Kid Boy"], 
        index=0, 
        format_func=lambda x: "Select Gender" if x is None else x
    )
    body_type = st.selectbox(
        "Frame Type", 
        options=[None, "Full-Body", "Upper-Body", "Lower-Body"], 
        index=0, 
        format_func=lambda x: "Select Frame" if x is None else x
    )
    
    st.divider()
    st.markdown("## 🎨 Select Colors")

    standard_shades = {
    "Olive Green": "#828e5c",
    "Classic Black": "#000000",
    "Pure White": "#FFFFFF",
    "Navy Blue": "#000080",
    "Crimson Red": "#B22222"
    }

# ONLY ONE multiselect here, with a unique key
    selected_colors = st.multiselect(
    "Choose colors to generate:",
    options=list(standard_shades.keys()),
    default=None, 
    placeholder="Choose one or more colors...",
    key="dropdown_colors"  # <--- Unique ID
    )

    st.markdown("---")
    st.markdown("### 🧪 Test: Custom Color Picker")

# Add a key here as well for safety
    custom_color = st.color_picker(
    "Pick a single custom color to test:", 
    "#828e5c", 
    key="manual_color_picker"
    )

    use_custom = st.checkbox(
    "Include this custom color in batch", 
    key="custom_color_toggle"
    )

    
    st.markdown("## Export")
    download_placeholder = st.empty()
    download_placeholder.info("Waiting For Generation")

# 4. MAIN PAGE: Centered Hero
st.markdown('<h1 class="main-title">V2 CREATIVE STUDIO</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">High-Fidelity Fashion Synthesis Engine</p>', unsafe_allow_html=True)

# Upload Zone
col_left, col_right = st.columns(2)
with col_left:
    st.markdown("### 1. Design")
    design_files = st.file_uploader("Upload Cloth Designs (Compulsory) *", type=['png', 'jpg', 'webp'], accept_multiple_files=True)

with col_right:
    st.markdown("### 2. Pattern")
    pattern_file = st.file_uploader("Upload Pattern/Texture (Optional)", type=['png', 'jpg', 'webp'])

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. EXECUTION LOGIC ---
if st.button("✨ START BATCH GENERATION"):
    if not gender or not body_type:
        st.error("⚠️ Please select Gender and Frame Type.")
    elif not design_files:
        st.error("⚠️ Please upload at least one Cloth Design.")
    else:
        # 1. Combine Dropdown Colors + Custom Picker Color
        # We start with the list from your multiselect
        colors_to_process = selected_colors.copy() if selected_colors else []
        
        # 2. If you checked the "Include Custom Color" box, add it to the list
        if use_custom:
            colors_to_process.append(custom_color)
            
        all_results = []
        with st.status("🔮 V2 Neural Engine is rendering...", expanded=True) as status:
            
            # 3. Check if we have ANY colors (Dropdown or Picker)
            if colors_to_process:
                for color_val in colors_to_process:
                    st.write(f"🎨 Rendering {color_val}...")
                    # Pass the name or hex code to the backend
                    batch_res = runbatch_pipeline(design_files, gender, body_type, pattern_file, color_val)
                    all_results.extend(batch_res)
            else:
                # Fallback to original if both are empty
                st.write("✨ Rendering Original Designs...")
                batch_res = runbatch_pipeline(design_files, gender, body_type, pattern_file, None)
                all_results.extend(batch_res)

            st.session_state['results'] = all_results
            st.session_state['focused_idx'] = None 
            status.update(label="✅ Generation Complete!", state="complete", expanded=False)
            st.rerun()
# --- 6. PREVIEW & ZOOM LOGIC (The rest of the logic) ---
if st.session_state.get('results'):
    results = st.session_state['results']
    f_idx = st.session_state.get('focused_idx')

    # Prepare ZIP in background
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a") as zf:
        for i, res in enumerate(results):
            if not isinstance(res['output'], str):
                img_io = BytesIO()
                res['output'].save(img_io, format='PNG') 
                zf.writestr(f"V2_Render_{i+1}.png", img_io.getvalue())

    # --- VIEW TOGGLE ---
    if f_idx is not None:
        # ZOOM VIEW
        res = results[f_idx]
        st.image(res['output'], use_container_width=True)
        if st.button("⬅️ Back to Gallery"):
            st.session_state['focused_idx'] = None
            st.rerun()
    else:
        # GRID VIEW
        grid = st.columns(3)
        for i, res in enumerate(results):
            with grid[i % 3]:
                st.image(res['output'], use_container_width=True)
                if st.button(f"🔍 Zoom {i+1}", key=f"z_{i}"):
                    st.session_state['focused_idx'] = i
                    st.rerun()

    # --- SIDEBAR DOWNLOADS ---
    with st.sidebar:
        st.divider()
        
        
        zip_buffer.seek(0)
        st.download_button("💾 DOWNLOAD ZIP", data=zip_buffer, file_name="batch.zip", mime="application/zip")