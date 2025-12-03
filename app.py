import streamlit as st
import requests

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IG Downloader Tool",
    page_icon=":arrow_down:", # Emoji code use kiya hai taaki error na aaye
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. PROFESSIONAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
    }

    .stApp {
        background-color: #fcfcfc;
    }

    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .main-title {
        text-align: center;
        font-weight: 800;
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }

    .stTextInput > div > div > input {
        border: 2px solid #e1e1e1;
        border-radius: 12px;
        padding: 16px;
        font-size: 16px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #833AB4;
        box-shadow: 0 4px 20px rgba(131, 58, 180, 0.15);
    }

    div.stButton > button {
        width: 100%;
        background-color: #0095f6;
        color: white;
        border: none;
        padding: 16px 24px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(0, 149, 246, 0.3);
        transition: transform 0.1s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #0086dd;
        transform: translateY(-2px);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    .result-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #eee;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-top: 20px;
    }

    .custom-footer {
        text-align: center;
        margin-top: 80px;
        padding: 20px;
        font-size: 14px;
        color: #888;
        border-top: 1px solid #eee;
    }
    .custom-footer span {
        color: #000;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION ---
API_KEY = "4772764741msh11a0214873b1c5bp1736fdjsn85b570384ebb" 
API_HOST = "instagram-scraper-stable-api.p.rapidapi.com"

# --- LOGIC ---
def fetch_instagram_data(insta_url):
    url = f"https://{API_HOST}/get_media_data.php"
    querystring = {"reel_post_code_or_url": insta_url}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- UI LAYOUT ---

st.markdown("<div class='main-title'>Instagram Downloader</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Download Video, Reels, Photo & IGTV from Instagram</div>", unsafe_allow_html=True)

url_input = st.text_input("", placeholder="Paste URL Instagram here...")

if st.button("Download"):
    if not url_input:
        st.error("Please paste a valid Instagram link.")
    else:
        with st.spinner("Processing..."):
            data = fetch_instagram_data(url_input)
            
            if "video_url" in data:
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.success("Ready to Download")
                st.video(data["video_url"])
                st.markdown(f"""
                    <a href="{data['video_url']}" target="_blank" style="text-decoration:none;">
                        <button style="background-color:#28a745; color:white; border:none; padding:12px 24px; border-radius:8px; font-size:16px; width:100%; margin-top:10px; cursor:pointer;">
                            Download Video (.mp4)
                        </button>
                    </a>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            elif "display_url" in data:
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.success("Photo Ready")
                st.image(data["display_url"])
                st.markdown(f"""
                    <a href="{data['display_url']}" target="_blank" style="text-decoration:none;">
                        <button style="background-color:#28a745; color:white; border:none; padding:12px 24px; border-radius:8px; font-size:16px; width:100%; margin-top:10px; cursor:pointer;">
                            Download Photo (.jpg)
                        </button>
                    </a>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif "message" in data:
                st.error(f"Server Error: {data['message']}")
            else:
                st.error("Invalid Link or Private Account.")

# Footer me HTML entity use ki hai copyright symbol ki jagah
st.markdown("""
    <div class="custom-footer">
        &copy; 2025 InstaTool. Designed & Developed by <span>Sushi Dahiya</span>.
    </div>
    """, unsafe_allow_html=True)
