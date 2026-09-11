import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Social Media Content Assistant")
st.write("Generate tailored posts, captions, and hashtags in seconds using Groq AI.")

# Sidebar for API Key handling
st.sidebar.header("Configuration")

# Try to get API key from environment secrets first, otherwise ask user
api_key = os.environ.get("GROQ_API_KEY") or st.sidebar.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.info("💡 Please enter your Groq API Key in the sidebar or set it up in Streamlit Secrets to continue.")
    st.markdown("[Get a free Groq API Key here](https://console.groq.com/keys)")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Input Controls
st.header("1. Define Your Post")

col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "TikTok"]
    )
    content_type = st.selectbox(
        "Content Type",
        ["Educational Post", "Promotional / Pitch", "Storytelling", "Thought Leadership", "Quick Tip"]
    )

with col2:
    tone = st.selectbox(
        "Tone",
        ["Professional", "Conversational", "Casual & Fun", "Urgent & Persuasive", "Inspirational"]
    )
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Developers, Small Business Owners")

topic = st.text_area("Topic / Main Message", placeholder="What is your post about?")

# Generation Trigger
if st.button("🚀 Generate Post", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic before generating.")
    else:
        with st.spinner("Crafting your content..."):
            prompt = f"""
            You are an expert social media strategist and content creator.
            Create a complete social media post based on the following specifications:
            
            - Platform: {platform}
            - Content Type: {content_type}
            - Tone: {tone}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Topic: {topic}

            Format your response clearly with the following sections:
            1. **Main Post Content**: The full text formatted with appropriate emojis and line breaks suitable for {platform}.
            2. **Call to Action (CTA)**: A strong closing line to drive engagement.
            3. **Hashtags**: 5 to 10 highly relevant, trending hashtags.
            """

            try:
                # Call Groq API using Llama 3 model
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a professional social media content assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

                generated_content = response.choices[0].message.content

                st.markdown("---")
                st.header("2. Your Generated Content")
                st.markdown(generated_content)

            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")
