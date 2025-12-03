import streamlit as st
import requests

# --- CONFIGURATION ---
API_KEY = "4772764741msh11a0214873b1c5bp1736fdjsn85b570384ebb"
API_HOST = "instagram-scraper-stable-api.p.rapidapi.com"

# --- MAIN FUNCTION ---
def fetch_instagram_data(insta_url):
    """
    RapidAPI se data fetch karta hai.
    Endpoint: /get_media_data.php (Screenshot se liya gaya)
    """
    url = f"https://{API_HOST}/get_media_data.php"
    
    # Screenshot ke hisab se parameter ka naam 'reel_post_code_or_url' hai
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

# --- STREAMLIT APP UI ---
st.set_page_config(page_title="Insta Downloader", page_icon="??")

st.title("?? Insta Downloader (Final)")
st.write("Instagram Reel ya Photo ka link yahan dalein:")

# Input Box
url_input = st.text_input("Paste Link Here", placeholder="https://www.instagram.com/reel/...")

if st.button("Download Now"):
    if not url_input:
        st.warning("Please paste a link first!")
    else:
        st.info("Searching video... Please wait...")
        
        # API Call
        data = fetch_instagram_data(url_input)
        
        # --- DEBUGGING (Agar future me koi dikkat aaye to ise hatakar check karein) ---
        # st.json(data) 

        # --- RESULT LOGIC ---
        # Check karte hain ki response me video hai ya photo
        
        if "video_url" in data:
            st.success("? Video Found!")
            st.video(data["video_url"])
            st.markdown(f"### [?? Download Video]({data['video_url']})")
            
        elif "display_url" in data:
            st.success("? Photo Found!")
            st.image(data["display_url"])
            st.markdown(f"### [?? Download Photo]({data['display_url']})")
            
        # Kabhi kabhi API data 'edges' ke andar deti hai (Carousel posts ke liye)
        elif "edge_sidecar_to_children" in data:
            st.success("? Album Found!")
            st.write("Is post me ek se zyada photos/videos hain:")
            for item in data["edge_sidecar_to_children"]["edges"]:
                media = item["node"]
                if "video_url" in media:
                     st.video(media["video_url"])
                elif "display_url" in media:
                     st.image(media["display_url"])
        
        # Agar koi error message aaye API se
        elif "message" in data:
            st.error(f"API Error: {data['message']}")
            
        else:
            st.error("Media nahi mila. Link check karein ya API ka response badal gaya hai.")
            with st.expander("Show Technical Data"):
                st.json(data)