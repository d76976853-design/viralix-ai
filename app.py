import streamlit as st
import requests

st.set_page_config(
    page_title="VIRALIX AI",
    page_icon="⚡",
    layout="wide"
)

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
.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>⚡ VIRALIX AI</h1>
    <p>Idea Se Viral Tak — Ek Click Mein</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🎯 Features")
feature = st.sidebar.selectbox("Kya karna hai?", [
    "💡 Viral Idea Generator",
    "📝 Script Writer",
    "🖼️ Image Generator",
    "🎬 Complete Video Maker",
    "🎙️ Voice Over Maker",
    "✂️ Viral Clip Cutter",
    "🖼️ Thumbnail Maker",
    "🔍 SEO Generator",
    "🎵 Music Adder",
    "🔇 Background Remover",
    "💧 Watermark Remover"
])

GROQ_API_KEY = st.sidebar.text_input(
    "🔑 Groq API Key",
    type="password",
    placeholder="gsk_..."
)

def call_groq(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        result = r.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def generate_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1280&height=720&nologo=true"
    return url

# ─── FEATURES ───────────────────────────────────────

if feature == "💡 Viral Idea Generator":
    st.header("💡 Viral Idea Generator")
    niche = st.text_input("Topic/niche likho:", placeholder="Technology, Cooking, Travel...")
    language = st.selectbox("Language:", ["Hindi", "English", "Hinglish"])
    if st.button("⚡ Generate Karo"):
        if not GROQ_API_KEY:
            st.error("API Key daalo!")
        elif not niche:
            st.error("Topic likho!")
        else:
            with st.spinner("Soch raha hoon..."):
                prompt = f"5 viral YouTube ideas for {niche} in {language}. Each with title, hook, why viral, audience."
                st.success("Ideas Ready! 🎉")
                st.write(call_groq(prompt, GROQ_API_KEY))

elif feature == "📝 Script Writer":
    st.header("📝 Script Writer")
    topic = st.text_input("Topic:")
    duration = st.selectbox("Length:", ["1 min","5 min","10 min","20 min","30 min"])
    language = st.selectbox("Language:", ["Hindi","English","Hinglish"])
    if st.button("📝 Script Likho"):
        if not GROQ_API_KEY:
            st.error("API Key daalo!")
        elif not topic:
            st.error("Topic likho!")
        else:
            with st.spinner("Likh raha hoon..."):
                prompt = f"Complete YouTube script. Topic:{topic} Duration:{duration} Language:{language}. Include hook, intro, scenes, CTA, outro."
                result = call_groq(prompt, GROQ_API_KEY)
                st.success("Script Ready! 🎉")
                st.write(result)
                st.download_button("📥 Download", result, "script.txt")

elif feature == "🖼️ Image Generator":
    st.header("🖼️ Image Generator")
    prompt = st.text_area("Description:")
    style = st.selectbox("Style:", ["Realistic","Cinematic","Cartoon","Abstract"])
    if st.button("🖼️ Banao"):
        if not prompt:
            st.error("Description likho!")
        else:
            with st.spinner("Ban rahi hai..."):
                img_url = generate_image(f"{prompt}, {style}, 4k, high quality")
                st.success("Ready! 🎉")
                st.image(img_url, use_column_width=True)
                st.markdown(f"[📥 Download]({img_url})")

elif feature == "🎬 Complete Video Maker":
    st.header("🎬 Complete Video Maker")
    st.success("✅ Yeh feature sab kuch karta hai — Script, Images, Music, Export Plan!")

    topic = st.text_input("Video topic:", placeholder="Top 5 AI Tools jo life badal denge")
    language = st.selectbox("Language:", ["Hindi","English","Hinglish"])
    duration = st.selectbox("Duration:", ["1 min","3 min","5 min","10 min","20 min","30 min"])
    style = st.selectbox("Style:", ["Educational","Entertainment","Motivational","News","Comedy"])
    quality = st.selectbox("Quality:", ["720p","1080p","4K"])

    if st.button("🎬 Complete Video Banao"):
        if not GROQ_API_KEY:
            st.error("API Key daalo!")
        elif not topic:
            st.error("Topic likho!")
        else:
            st.info("Step 1: Script ban rahi hai...")
            with st.spinner("Script likh raha hoon..."):
                script_prompt = f"""
                Complete video production plan:
                Topic: {topic}
                Language: {language}
                Duration: {duration}
                Style: {style}
                Quality: {quality}

                Give me:
                1. VIRAL TITLE (3 options)
                2. COMPLETE SCRIPT (scene by scene with timestamps)
                3. VISUAL DESCRIPTION (for each scene)
                4. MUSIC SUGGESTIONS (mood + free source)
                5. THUMBNAIL IDEA
                6. DESCRIPTION (500 words, SEO optimized)
                7. 30 TAGS
                8. BEST POSTING TIME
                9. EDITING INSTRUCTIONS (cuts, transitions, effects)
                10. EXPORT SETTINGS ({quality}, format MP4)
                """
                result = call_groq(script_prompt, GROQ_API_KEY)

            st.success("✅ Script Ready!")
            st.write(result)
            st.download_button("📥 Poora Plan Download Karo", result, "viralix_video_plan.txt")

            st.markdown("---")
            st.info("Step 2: Scene Images ban rahi hain...")
            col1, col2 = st.columns(2)
            with col1:
                img1 = generate_image(f"{topic} cinematic scene 1, professional, 4k")
                st.image(img1, caption="Scene 1", use_column_width=True)
                st.markdown(f"[📥 Download Scene 1]({img1})")
            with col2:
                img2 = generate_image(f"{topic} cinematic scene 2, professional, 4k")
                st.image(img2, caption="Scene 2", use_column_width=True)
                st.markdown(f"[📥 Download Scene 2]({img2})")

            st.markdown("---")
            st.info("Step 3: Thumbnail...")
            thumb = generate_image(f"YouTube thumbnail {topic}, bold text, bright colors, shocking, viral")
            st.image(thumb, caption="Thumbnail", use_column_width=True)
            st.markdown(f"[📥 Thumbnail Download]({thumb})")

            st.markdown("---")
            st.subheader("Step 4: 🎵 Music")
            st.markdown(f"[🎵 Free Music Download - Pixabay](https://pixabay.com/music/)")

            st.markdown("---")
            st.subheader("Step 5: 🎬 Free Editing Tools")
            st.markdown("""
            | Tool | Link | Best For |
            |------|------|----------|
            | CapCut | [capcut.com](https://capcut.com) | Easy editing |
            | Canva Video | [canva.com](https://canva.com) | Templates |
            | DaVinci Resolve | [blackmagicdesign.com](https://blackmagicdesign.com) | Professional |
            | Clipchamp | [clipchamp.com](https://clipchamp.com) | Quick export |
            """)

            st.markdown("---")
            st.subheader("Step 6: 🎙️ Free Voice Over")
            st.markdown("""
            | Tool | Link |
            |------|------|
            | TTSMaker | [ttsmaker.com](https://ttsmaker.com) |
            | ElevenLabs | [elevenlabs.io](https://elevenlabs.io) |
            | Murf AI | [murf.ai](https://murf.ai) |
            """)

            st.balloons()
            st.success("🎉 Aapka Complete Video Production Plan Ready Hai!")

elif feature == "🎙️ Voice Over Maker":
    st.header("🎙️ Voice Over Maker")
    st.markdown("""
    **Free Voice Over Tools:**
    - [TTSMaker.com](https://ttsmaker.com) - Free
    - [ElevenLabs.io](https://elevenlabs.io) - Best
    - [Murf.ai](https://murf.ai) - Professional
    """)

elif feature == "✂️ Viral Clip Cutter":
    st.header("✂️ Viral Clip Cutter")
    video_topic = st.text_input("Video topic:")
    video_length = st.number_input("Minutes:", min_value=1, max_value=180)
    if st.button("✂️ Dhundho"):
        if not GROQ_API_KEY:
            st.error("API Key daalo!")
        else:
            with st.spinner("Dhundh raha hoon..."):
                prompt = f"{video_length} min video on {video_topic}. Top 5 viral moments with timestamps, why viral, caption, platform."
                result = call_groq(prompt, GROQ_API_KEY)
                st.success("Ready! 🎉")
                st.write(result)

elif feature == "🖼️ Thumbnail Maker":
    st.header("🖼️ Thumbnail Maker")
    title = st.text_input("Title:")
    style = st.selectbox("Style:", ["Shocking","Tutorial","Listicle","Question"])
    if st.button("🖼️ Banao"):
        if not title:
            st.error("Title likho!")
        else:
            with st.spinner("Ban rahi hai..."):
                img_url = generate_image(f"YouTube thumbnail {title}, {style}, bold, bright, viral")
                st.success("Ready! 🎉")
                st.image(img_url, use_column_width=True)
                st.markdown(f"[📥 Download]({img_url})")

elif feature == "🔍 SEO Generator":
    st.header("🔍 SEO Generator")
    video_topic = st.text_input("Topic:")
    language = st.selectbox("Language:", ["Hindi","English","Hinglish"])
    if st.button("🔍 Generate"):
        if not GROQ_API_KEY:
            st.error("API Key daalo!")
        elif not video_topic:
            st.error("Topic likho!")
        else:
            with st.spinner("Optimize kar raha hoon..."):
                prompt = f"YouTube SEO for {video_topic} in {language}. 3 titles, description, 30 tags, upload time, thumbnail text."
                result = call_groq(prompt, GROQ_API_KEY)
                st.success("Ready! 🎉")
                st.write(result)
                st.download_button("📥 Download", result, "seo.txt")

elif feature == "🎵 Music Adder":
    st.header("🎵 Music Adder")
    mood = st.selectbox("Mood:", ["Motivational","Calm","Exciting","Sad","Funny"])
    links = {
        "Motivational": "https://pixabay.com/music/search/motivational/",
        "Calm": "https://pixabay.com/music/search/calm/",
        "Exciting": "https://pixabay.com/music/search/energetic/",
        "Sad": "https://pixabay.com/music/search/emotional/",
        "Funny": "https://pixabay.com/music/search/funny/"
    }
    st.markdown(f"[🎵 Free Music]({links[mood]})")

elif feature == "🔇 Background Remover":
    st.header("🔇 Background Remover")
    st.markdown("""
    - [Remove.bg](https://remove.bg)
    - [Canva](https://canva.com)
    - [Adobe Express](https://express.adobe.com)
    """)

elif feature == "💧 Watermark Remover":
    st.header("💧 Watermark Remover")
    st.markdown("""
    - [Watermarkremover.io](https://watermarkremover.io)
    - [Cleanup.pictures](https://cleanup.pictures)
    - [Inpaint](https://theinpaint.com)
    """)

st.markdown("---")
st.markdown("<div style='text-align:center;color:gray;'>⚡ VIRALIX AI — Idea Se Viral Tak | Made with ❤️</div>", unsafe_allow_html=True)
