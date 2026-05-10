import streamlit as st
import requests
import json
import os
from PIL import Image
import io
import base64

# Page Config
st.set_page_config(
    page_title="VIRALIX AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 16px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ VIRALIX AI</h1>
    <p>Idea Se Viral Tak — Ek Click Mein</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://via.placeholder.com/200x80/667eea/white?text=VIRALIX+AI")
st.sidebar.title("🎯 Features")
feature = st.sidebar.selectbox("Kya karna hai?", [
    "💡 Viral Idea Generator",
    "📝 Script Writer", 
    "🖼️ Image Generator",
    "🎙️ Voice Over Maker",
    "✂️ Viral Clip Cutter",
    "🖼️ Thumbnail Maker",
    "🔍 SEO Generator",
    "🎵 Music Adder",
    "🔇 Background Remover",
    "💧 Watermark Remover"
])

# Groq API
GROQ_API_KEY = st.sidebar.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...")

def call_groq(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                         headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Error: API Key check karo"

def generate_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1280&height=720&nologo=true"
    return url

# Main Content
if feature == "💡 Viral Idea Generator":
    st.header("💡 Viral Idea Generator")
    niche = st.text_input("Apna topic/niche likho:", placeholder="e.g. Technology, Cooking, Travel...")
    language = st.selectbox("Language:", ["Hindi", "English", "Hinglish"])
    
    if st.button("⚡ Viral Idea Generate Karo"):
        if not GROQ_API_KEY:
            st.error("Pehle API Key daalo!")
        elif not niche:
            st.error("Topic likho!")
        else:
            with st.spinner("Viral idea dhundh raha hoon..."):
                prompt = f"""Generate 5 viral YouTube video ideas for niche: {niche}
                Language: {language}
                For each idea provide:
                1. Title (catchy)
                2. Hook (first 10 seconds)
                3. Why it will go viral
                4. Target audience
                Format clearly."""
                result = call_groq(prompt, GROQ_API_KEY)
                st.success("Viral Ideas Ready! 🎉")
                st.write(result)

elif feature == "📝 Script Writer":
    st.header("📝 Script Writer")
    topic = st.text_input("Video topic:", placeholder="e.g. AI tools jo tumhari zindagi badal denge")
    duration = st.selectbox("Video length:", ["1 min", "5 min", "10 min", "20 min", "30 min"])
    language = st.selectbox("Language:", ["Hindi", "English", "Hinglish"])
    
    if st.button("📝 Script Likho"):
        if not GROQ_API_KEY:
            st.error("Pehle API Key daalo!")
        elif not topic:
            st.error("Topic likho!")
        else:
            with st.spinner("Script likh raha hoon..."):
                prompt = f"""Write a complete YouTube video script for:
                Topic: {topic}
                Duration: {duration}
                Language: {language}
                
                Include:
                - Hook (attention grabbing opening)
                - Introduction
                - Main content (scene by scene)
                - Call to action
                - Outro
                
                Make it engaging and viral worthy."""
                result = call_groq(prompt, GROQ_API_KEY)
                st.success("Script Ready! 🎉")
                st.write(result)
                st.download_button("📥 Script Download Karo", result, "viralix_script.txt")

elif feature == "🖼️ Image Generator":
    st.header("🖼️ Image Generator")
    prompt = st.text_area("Image description likho:", placeholder="e.g. Futuristic city at night, neon lights...")
    style = st.selectbox("Style:", ["Realistic", "Cinematic", "Cartoon", "Abstract", "Professional"])
    
    if st.button("🖼️ Image Banao"):
        if not prompt:
            st.error("Description likho!")
        else:
            with st.spinner("Image ban rahi hai..."):
                full_prompt = f"{prompt}, {style} style, high quality, 4k"
                img_url = generate_image(full_prompt)
                st.success("Image Ready! 🎉")
                st.image(img_url, use_column_width=True)
                st.markdown(f"[📥 Image Download Karo]({img_url})")

elif feature == "🎙️ Voice Over Maker":
    st.header("🎙️ Voice Over Maker")
    st.info("🎙️ Voice Over ke liye apna script paste karo")
    script = st.text_area("Script paste karo:", height=200)
    
    st.warning("💡 Voice Over ke liye yeh free tools use karo:")
    st.markdown("""
    - **ElevenLabs.io** - Best quality (free tier available)
    - **TTSMaker.com** - Bilkul free
    - **Murf.ai** - Professional voices
    """)
    
    if st.button("🔗 TTSMaker Open Karo"):
        st.markdown("[TTSMaker.com par jao](https://ttsmaker.com) - Script paste karo aur download karo!")

elif feature == "✂️ Viral Clip Cutter":
    st.header("✂️ Viral Clip Cutter")
    st.info("Long video se viral clips nikalne ke liye")
    
    video_topic = st.text_input("Video ka topic kya hai?")
    video_length = st.number_input("Video kitne minute ki hai?", min_value=1, max_value=180)
    
    if st.button("✂️ Best Clips Dhundho"):
        if not GROQ_API_KEY:
            st.error("Pehle API Key daalo!")
        else:
            with st.spinner("Best moments dhundh raha hoon..."):
                prompt = f"""For a {video_length} minute video about {video_topic},
                suggest the best timestamps for viral short clips.
                Provide:
                1. Top 5 moments with timestamps
                2. Why each moment is viral worthy
                3. Best caption for each clip
                4. Which platform suits each clip (YouTube Shorts/Instagram Reels/TikTok)"""
                result = call_groq(prompt, GROQ_API_KEY)
                st.success("Viral Moments Ready! 🎉")
                st.write(result)

elif feature == "🖼️ Thumbnail Maker":
    st.header("🖼️ Thumbnail Maker")
    title = st.text_input("Video title:", placeholder="e.g. 5 AI Tools Jo Tumhari Zindagi Badal Denge")
    style = st.selectbox("Thumbnail style:", [
        "Shocking/Surprising", "Tutorial", "Listicle", 
        "Before-After", "Question", "Celebrity Style"
    ])
    
    if st.button("🖼️ Thumbnail Banao"):
        if not title:
            st.error("Title likho!")
        else:
            with st.spinner("Thumbnail ban rahi hai..."):
                thumb_prompt = f"YouTube thumbnail for '{title}', {style} style, bold text, bright colors, high contrast, professional, eye-catching"
                img_url = generate_image(thumb_prompt)
                st.success("Thumbnail Ready! 🎉")
                st.image(img_url, use_column_width=True)
                st.markdown(f"[📥 Thumbnail Download Karo]({img_url})")

elif feature == "🔍 SEO Generator":
    st.header("🔍 SEO Generator")
    video_topic = st.text_input("Video topic:", placeholder="e.g. Best AI tools 2024")
    language = st.selectbox("Language:", ["Hindi", "English", "Hinglish"])
    
    if st.button("🔍 SEO Generate Karo"):
        if not GROQ_API_KEY:
            st.error("Pehle API Key daalo!")
        elif not video_topic:
            st.error("Topic likho!")
        else:
            with st.spinner("SEO optimize kar raha hoon..."):
                prompt = f"""Generate complete YouTube SEO for:
                Topic: {video_topic}
                Language: {language}
                
                Provide:
                1. Top 3 Video Titles (with emojis, click-worthy)
                2. Video Description (500 words, keyword rich)
                3. 30 Tags (comma separated)
                4. Best upload time
                5. Thumbnail text suggestions
                6. First comment to pin"""
                result = call_groq(prompt, GROQ_API_KEY)
                st.success("SEO Ready! 🎉")
                st.write(result)
                st.download_button("📥 SEO Download Karo", result, "viralix_seo.txt")

elif feature == "🎵 Music Adder":
    st.header("🎵 Music Adder")
    st.info("Free background music ke liye yeh sources use karo:")
    
    mood = st.selectbox("Video ka mood:", [
        "Motivational", "Calm/Relaxing", "Exciting/Energetic",
        "Sad/Emotional", "Funny", "Mysterious", "Corporate"
    ])
    
    music_sources = {
        "Motivational": "https://pixabay.com/music/search/motivational/",
        "Calm/Relaxing": "https://pixabay.com/music/search/calm/",
        "Exciting/Energetic": "https://pixabay.com/music/search/energetic/",
        "Sad/Emotional": "https://pixabay.com/music/search/emotional/",
        "Funny": "https://pixabay.com/music/search/funny/",
        "Mysterious": "https://pixabay.com/music/search/mysterious/",
        "Corporate": "https://pixabay.com/music/search/corporate/"
    }
    
    st.success(f"✅ {mood} music ke liye:")
    st.markdown(f"[🎵 Free Music Download Karo]({music_sources[mood]})")
    st.markdown("""
    **Other Free Music Sources:**
    - YouTube Audio Library
    - Pixabay Music (No copyright)
    - Bensound.com
    - Mixkit.co
    """)

elif feature == "🔇 Background Remover":
    st.header("🔇 Background Remover")
    uploaded_file = st.file_uploader("Image upload karo:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Original Image", use_column_width=True)
        st.info("Background remove karne ke liye:")
        st.markdown("""
        **Free Background Removers:**
        - [Remove.bg](https://remove.bg) - Best quality
        - [Canva Background Remover](https://canva.com) - Free
        - [Adobe Express](https://express.adobe.com) - Free
        """)

elif feature == "💧 Watermark Remover":
    st.header("💧 Watermark Remover")
    st.info("Watermark remove karne ke liye free tools:")
    st.markdown("""
    **Free Watermark Removers:**
    - [Watermarkremover.io](https://watermarkremover.io) - Automatic AI
    - [Inpaint Online](https://theinpaint.com) - Free
    - [Cleanup.pictures](https://cleanup.pictures) - Free AI
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>⚡ VIRALIX AI — Idea Se Viral Tak | Made with ❤️</p>
</div>
""", unsafe_allow_html=True)
