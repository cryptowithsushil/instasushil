import streamlit as st
import requests

# --- 1. PAGE SETUP (Tab ka naam aur icon) ---
st.set_page_config(
    page_title="Insta Downloader Pro",
    page_icon="📸",
    layout="centered"
)

# --- 2. CUSTOM CSS (Design ke liye Jaadu) ---
# Ye code button ko rangeen aur background ko sundar banayega
st.markdown("""
    <style>
    /* Background ka color change karein */
    .stApp {
        background: linear-gradient(to bottom right, #ffffff, #f0f2f6);
    }
    
    /* Input box ka design */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 10px;
    }

    /* Button ko Instagram jaisa banayein */
    div.stButton > button {
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
        color: white;
    }
    
    /* Title ka font style */
    h1 {
        text-align: center;
        color: #bc1888;
        font-family: sans-serif;
    }
    p {
        text-align: center;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION ---
API_KEY = "4772764741msh11a0214873b1c5bp1736fdjsn85b570384ebb" # Apni key yahan rakhein
API_HOST = "instagram-scraper-stable-api.p.rapidapi.com"

# --- LOGIC FUNCTION ---
def fetch_instagram_data(insta_url):
    url = f"https://{API_HOST}/get_media_data.php"
    querystring = {"reel_post_code_or_url": insta_url}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- MAIN UI ---

# Logo / Title area
st.markdown("<h1>📸 Insta Downloader <span style='color:#e6683c'>Pro</span></h1>", unsafe_allow_html=True)
st.markdown("<p>Download Reels, Videos & Photos in High Quality 🚀</p>", unsafe_allow_html=True)

st.write("---") # Ek line khichne ke liye

# Input Section
url_input = st.text_input("🔗 Paste Instagram Link Here:", placeholder="https://www.instagram.com/reel/...")

st.write("") # Thoda gap

# Button
if st.button("🚀 Download Now"):
    if not url_input:
        st.warning("⚠️ Pehle link to daalo bhai!")
    else:
        with st.spinner("🔍 Searching... Please wait..."): # Loading ghumega
            data = fetch_instagram_data(url_input)
            
            # --- RESULT SHOW ---
            if "video_url" in data:
                st.success("✅ Video Mil Gaya!")
                st.video(data["video_url"])
                st.markdown(f"<div style='text-align:center'><a href='{data['video_url']}' target='_blank' style='background-color:#0095f6; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;'>📥 Download Video</a></div>", unsafe_allow_html=True)
            
            elif "display_url" in data:
                st.success("✅ Photo Mil Gayi!")
                st.image(data["display_url"])
                st.markdown(f"<div style='text-align:center'><a href='{data['display_url']}' target='_blank' style='background-color:#0095f6; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;'>📥 Download Photo</a></div>", unsafe_allow_html=True)
            
            elif "edge_sidecar_to_children" in data:
                st.success("✅ Album Found!")
                for item in data["edge_sidecar_to_children"]["edges"]:
                    media = item["node"]
                    if "video_url" in media:
                        st.video(media["video_url"])
                    elif "display_url" in media:
                        st.image(media["display_url"])
            
            elif "message" in data:
                st.error(f"❌ Error: {data['message']}")
            else:
                st.error("❌ Media nahi mila. Link check karein.")

st.write("---")
st.markdown("<p style='color:grey; font-size:12px;'>Made with ❤️ using Python & Streamlit</p>", unsafe_allow_html=True)
