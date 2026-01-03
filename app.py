
import streamlit as st
import time
import zipfile
from io import BytesIO
from backend.aipipeline import runbatch_pipeline
import base64
import matplotlib.colors as mcolors

@st.cache_data
def load_color_database():
    # This pulls the 949 colors from matplotlib and cleans the names
    # Example: 'xkcd:sky blue' -> 'Sky Blue'
    return {name.replace('xkcd:', '').title(): hex_val.upper() 
            for name, hex_val in mcolors.XKCD_COLORS.items()}

COLOR_DATABASE = load_color_database()



st.set_page_config(
    page_title="V2 Retail AI", 
    layout='wide', 
    initial_sidebar_state='expanded'
)

if 'focused_idx' not in st.session_state:
    st.session_state['focused_idx'] = None
if 'results' not in st.session_state:
    st.session_state['results'] = None
if 'color_queue' not in st.session_state:
    st.session_state['color_queue'] = []
#--cost tracking-- 
if 'total_images_generated' not in st.session_state:
    st.session_state['total_images_generated'] = 0
if 'usage_history' not in st.session_state:
    st.session_state['usage_history'] = []
    
    
# 2. THE AESTHETIC CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&display=swap');
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] p {
        color: white !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] div {
        color: white !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
    }
    
    /* 1. MANAGE HEADER: Transparent background, keep toggle interactive */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
        color: white !important;
    }

     /* 1. Target the button area and force it to be interactive */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        background-color: #ffffff !important;
        z-index: 999999 !important;
    }

    /* 2. FORCE THE ICON TO WHITE */
    /* This targets the specific icon pointed at by your cursor */
    [data-testid="collapsedControl"] button svg, 
    [data-testid="stHeader"] button svg,
    .st-emotion-cache-p4m0yw svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        stroke: #FFFFFF !important;
        width: 28px !important;
        height: 28px !important;
    }
    /* 3. Handle the 'Collapsed' state specifically */
    button[kind="headerNoPadding"] {
        color: white !important;
    }

    /* 3. Target the button element directly if the SVG selector fails */
    header button {
        color: white !important;
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
selected_names=[]
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

    if 'custom_added' not in st.session_state:
        st.session_state['custom_added'] = {}

    # Merge the 900+ standard colors with user-added custom ones
    all_options = {**COLOR_DATABASE, **st.session_state['custom_added']}

    # 1. Searchable Multiselect (Type 'Teal', 'Sage', etc. here)
    selected_names = st.multiselect(
        "Search & Select Colors:",
        options=list(all_options.keys()),
        placeholder="Type to search 900+ colors..."
    )

    # 2. Rare Occasion: Custom Picker
    with st.expander("➕ Add Rare/Custom Color"):
        c_hex = st.color_picker("Pick Hex:", "#828e5c")
        c_name = st.text_input("Name this color:", placeholder="e.g. Pantone 18-0107")
        if st.button("Add to List"):
            if c_name:
                st.session_state['custom_added'][c_name] = c_hex.upper()
                st.success(f"Added {c_name} to library!")
                st.rerun()

    if st.button("🗑️ Clear Selection"):
        st.session_state['custom_added'] = {}
        st.rerun()
    st.divider()
    st.markdown("## Usage & Billing")
    
    # Retrieve the total from session state (initialized at the top of your script)
    total_imgs = st.session_state.get('total_images_generated', 0)
    
    st.metric("Total Images Created", total_imgs)
    st.metric("Estimated Cost", f"${total_imgs * 0.02:.2f}")# here pls cange the cost peer image acc to the acctual coast

    # Only show the download report button if images have actually been made
    if total_imgs > 0:
        # Create CSV data from the history
        csv_report = "Time,Images,Gender,Frame\n"
        for entry in st.session_state.get('usage_history', []):
            csv_report += f"{entry['Time']},{entry['Count']},{entry['Gender']},{entry['Body']}\n"
        
        st.download_button(
            label="📊 DOWNLOAD USAGE REPORT",
            data=csv_report,
            file_name=f"V2_Retail_Usage_{time.strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
            key="billing_report_btn"
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
        all_results = []
        # Ensure all_options is accessible here (it was defined in your sidebar)
        all_options = {**COLOR_DATABASE, **st.session_state.get('custom_added', {})}
        
        with st.status("🔮 V2 Neural Engine Rendering...", expanded=True) as status:
            
            # Use 'selected_names' which comes from your st.multiselect
            if selected_names:
                for name in selected_names:
                    # Map the readable name (e.g., 'Teal') back to its Hex code
                    hex_val = all_options.get(name)
                    
                    st.write(f"🎨 Rendering Color: **{name}** ({hex_val})...")
                    
                    # Call the pipeline
                    batch_res = runbatch_pipeline(
                        design_files, 
                        gender, 
                        body_type, 
                        pattern_file, 
                        color_name=hex_val
                    )
                    all_results.extend(batch_res)
            
            # FALLBACK: If no colors were selected in the multiselect
            else:
                st.write("✨ Rendering Original Designs (No color override)...")
                batch_res = runbatch_pipeline(
                    design_files, 
                    gender, 
                    body_type, 
                    pattern_file, 
                    color_name=None
                )
            all_results.extend(batch_res)
            generated_count = len(all_results)
            
            # 2. Add to the total grand counter
            st.session_state['total_images_generated'] += generated_count
            
            # 3. Add a line to the history log for the CSV report
            st.session_state['usage_history'].append({
                "Time": time.strftime("%H:%M:%S"), 
                "Count": generated_count, 
                "Gender": gender, 
                "Body": body_type
                })

            # Store results and refresh UI
            st.session_state['results'] = all_results
            st.session_state['focused_idx'] = None 
            status.update(label="✅ Batch Complete!", state="complete", expanded=False) 
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
                st.image(res['output'], use_container_width=True,caption=None)
                if st.button(f"🔍 Zoom {i+1}", key=f"z_{i}"):
                    st.session_state['focused_idx'] = i
                    st.rerun()

    # --- SIDEBAR DOWNLOADS ---
    with st.sidebar:
        st.divider()
        
        
        zip_buffer.seek(0)
        st.download_button("💾 DOWNLOAD ZIP", data=zip_buffer, file_name="batch.zip", mime="application/zip")