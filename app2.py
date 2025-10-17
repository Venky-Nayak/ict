import streamlit as st
import pandas as pd
from datetime import datetime
import os
import warnings

# Suppress specific audio library warnings
warnings.filterwarnings('ignore', category=UserWarning, message='.*PySoundFile failed.*')
warnings.filterwarnings('ignore', category=FutureWarning, message='.*audioread_load.*')

# -----------------------------------------
# Page Config
# -----------------------------------------
st.set_page_config(
    page_title="DataSense — Unstructured Data Explorer",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------------------
# Custom Clean Dark Theme CSS
# -----------------------------------------
st.markdown("""
<style>
/* General layout */
.main {
    background-color: #0e1117;
    color: #e6edf3;
    font-family: "Inter", sans-serif;
    padding: 1.5rem 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(18, 21, 27, 0.95);
    backdrop-filter: blur(10px);
    border-right: 1px solid #30363d;
}

/* Headings */
h1, h2, h3 {
    color: #f0f6fc;
    font-weight: 600;
}
h1 {
    margin-bottom: 1rem;
}
h2, h3 {
    color: #c9d1d9;
}

/* Metrics */
div[data-testid="stMetricValue"] {
    color: #58a6ff;
    font-size: 1.7rem;
    font-weight: 700;
}
div[data-testid="stMetricLabel"] {
    color: #9da7b2;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(22, 27, 34, 0.8);
    border-radius: 8px;
    padding: 0.4rem;
}
.stTabs [data-baseweb="tab"] {
    color: #8b949e;
    border-radius: 6px;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(88, 166, 255, 0.15);
    color: #58a6ff;
}
.stTabs [aria-selected="true"] {
    background-color: #161b22;
    color: #ffffff;
    font-weight: 600;
    border-bottom: none;
}

/* Buttons */
.stButton button, .stDownloadButton button {
    background: #1f6feb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: #388bfd;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: rgba(22,27,34,0.6);
    border-radius: 8px;
    padding: 1rem;
}

/* Text area */
textarea {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
}

/* Info boxes */
.stAlert {
    background-color: rgba(56, 139, 253, 0.1);
    border: 1px solid #388bfd;
    border-radius: 6px;
    color: #e6edf3;
}

/* Cards */
.analysis-card {
    background: rgba(22,27,34,0.8);
    border-radius: 10px;
    padding: 1.5rem;
    border: 1px solid #30363d;
    margin-bottom: 1rem;
}

p, span, div, li {
    color: #e6edf3;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Header
# -----------------------------------------
st.title("🎬 DataSense — Unstructured Data Explorer")
st.caption("Analyze video, text, and audio data with advanced processing and insights.")

# -----------------------------------------
# Sidebar
# -----------------------------------------
with st.sidebar:
    st.header("📂 Data Type")
    data_type = st.radio(
        "Select analysis type:",
        ["🎥 Video Analysis", "📝 Text Analysis", "🎵 Audio Analysis"]
    )
    st.markdown("---")
    st.caption("Upload your unstructured data for comprehensive analysis.")

# -----------------------------------------
# Video Analysis Section
# -----------------------------------------
if data_type == "🎥 Video Analysis":
    st.subheader("🎥 Video Analysis")
    
    # File uploader for video
    video_file = st.file_uploader(
        "Upload a video file",
        type=["mp4", "avi", "mov", "mkv", "webm"],
        help="Supported formats: MP4, AVI, MOV, MKV, WebM"
    )
    
    if video_file:
        # Save uploaded file temporarily
        with open("temp_video.mp4", "wb") as f:
            f.write(video_file.read())
        
        # Display video
        st.markdown("#### 🎬 Video Preview")
        st.video("temp_video.mp4")
        
        # Video metadata
        col1, col2, col3, col4 = st.columns(4)
        file_size = os.path.getsize("temp_video.mp4") / (1024 * 1024)  # MB
        col1.metric("File Size", f"{file_size:.2f} MB")
        col2.metric("Format", video_file.type.split('/')[-1].upper())
        col3.metric("File Name", video_file.name[:20] + "..." if len(video_file.name) > 20 else video_file.name)
        col4.metric("Upload Time", datetime.now().strftime("%H:%M:%S"))
        
        st.markdown("---")
        
        # Analysis options
        st.markdown("#### ⚙️ Analysis Options")
        analysis_tabs = st.tabs(["📊 Basic Info", "🎞️ Frame Analysis", "🔍 Object Detection", "📈 Advanced Metrics"])
        
        with analysis_tabs[0]:
            st.markdown("##### Basic Video Information")
            
            try:
                import cv2
                
                cap = cv2.VideoCapture("temp_video.mp4")
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                duration = frame_count / fps if fps > 0 else 0
                cap.release()
                
                info_col1, info_col2, info_col3 = st.columns(3)
                info_col1.metric("Resolution", f"{width}x{height}")
                info_col2.metric("FPS", f"{fps:.2f}")
                info_col3.metric("Duration", f"{duration:.2f}s")
                
                info_col4, info_col5, info_col6 = st.columns(3)
                info_col4.metric("Total Frames", f"{frame_count:,}")
                info_col5.metric("Aspect Ratio", f"{width/height:.2f}:1")
                info_col6.metric("Bitrate", "Calculating...")
                
                # Video properties table
                st.markdown("##### 📋 Detailed Properties")
                properties_df = pd.DataFrame({
                    'Property': ['File Name', 'Format', 'Resolution', 'FPS', 'Duration', 'Total Frames', 'File Size'],
                    'Value': [
                        video_file.name,
                        video_file.type,
                        f"{width}x{height}",
                        f"{fps:.2f}",
                        f"{duration:.2f}s",
                        f"{frame_count:,}",
                        f"{file_size:.2f} MB"
                    ]
                })
                st.dataframe(properties_df, use_container_width=True, hide_index=True)
                
            except ImportError:
                st.warning("⚠️ OpenCV not installed. Install it with: `pip install opencv-python`")
                st.info("Basic file information only available.")
        
        with analysis_tabs[1]:
            st.markdown("##### 🎞️ Frame Extraction & Analysis")
            
            try:
                import cv2
                import numpy as np
                from PIL import Image
                
                cap = cv2.VideoCapture("temp_video.mp4")
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                num_frames = st.slider("Number of frames to extract", 1, min(20, frame_count), 5)
                
                if st.button("🎬 Extract Frames", key="extract_frames"):
                    with st.spinner("Extracting frames..."):
                        frames = []
                        frame_indices = np.linspace(0, frame_count - 1, num_frames, dtype=int)
                        
                        for idx in frame_indices:
                            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                            ret, frame = cap.read()
                            if ret:
                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                frames.append(frame_rgb)
                        
                        cap.release()
                        
                        # Display extracted frames
                        st.markdown("##### Extracted Frames")
                        cols = st.columns(min(3, num_frames))
                        for i, frame in enumerate(frames):
                            with cols[i % 3]:
                                st.image(frame, caption=f"Frame {frame_indices[i]}", use_container_width=True)
                                
                                # Frame statistics
                                avg_color = frame.mean(axis=(0, 1))
                                st.caption(f"Avg RGB: ({avg_color[0]:.0f}, {avg_color[1]:.0f}, {avg_color[2]:.0f})")
                        
                        st.success(f"✅ Successfully extracted {len(frames)} frames!")
                
            except ImportError:
                st.warning("⚠️ OpenCV and PIL not installed. Install with: `pip install opencv-python pillow`")
        
        with analysis_tabs[2]:
            st.markdown("##### 🔍 Object Detection (Placeholder)")
            st.info("🚧 This feature requires advanced ML models (YOLO, etc.). Coming soon!")
            
            st.markdown("**Planned Features:**")
            st.markdown("""
            - 🎯 Object detection and counting
            - 👤 Face detection and recognition
            - 🚗 Vehicle detection
            - 🏷️ Scene classification
            - 📊 Confidence scores and bounding boxes
            """)
            
            # Simulated object detection
            if st.button("🔮 Simulate Detection", key="simulate_detection"):
                st.markdown("##### Detected Objects (Simulated)")
                simulated_objects = pd.DataFrame({
                    'Object': ['Person', 'Car', 'Tree', 'Building', 'Person'],
                    'Confidence': ['95%', '87%', '92%', '78%', '89%'],
                    'Frame': [45, 120, 230, 340, 450],
                    'Bounding Box': ['(120,80,200,300)', '(300,150,450,280)', '(50,30,150,280)', '(400,50,600,400)', '(180,90,250,320)']
                })
                st.dataframe(simulated_objects, use_container_width=True, hide_index=True)
        
        with analysis_tabs[3]:
            st.markdown("##### 📈 Advanced Video Metrics")
            
            try:
                import cv2
                import numpy as np
                import plotly.graph_objects as go
                
                cap = cv2.VideoCapture("temp_video.mp4")
                
                sample_frames = st.slider("Sample frames for analysis", 10, 100, 30)
                
                if st.button("📊 Analyze Video Metrics", key="analyze_metrics"):
                    with st.spinner("Analyzing video..."):
                        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        frame_indices = np.linspace(0, frame_count - 1, sample_frames, dtype=int)
                        
                        brightness_values = []
                        contrast_values = []
                        
                        for idx in frame_indices:
                            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                            ret, frame = cap.read()
                            if ret:
                                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                brightness = np.mean(gray)
                                contrast = np.std(gray)
                                brightness_values.append(brightness)
                                contrast_values.append(contrast)
                        
                        cap.release()
                        
                        # Plot brightness over time
                        fig_brightness = go.Figure()
                        fig_brightness.add_trace(go.Scatter(
                            x=list(range(len(brightness_values))),
                            y=brightness_values,
                            mode='lines+markers',
                            name='Brightness',
                            line=dict(color='#58a6ff', width=2)
                        ))
                        fig_brightness.update_layout(
                            title='Brightness Variation Over Time',
                            xaxis_title='Sample Frame',
                            yaxis_title='Brightness (0-255)',
                            template='plotly_dark',
                            height=350
                        )
                        st.plotly_chart(fig_brightness, use_container_width=True)
                        
                        # Plot contrast over time
                        fig_contrast = go.Figure()
                        fig_contrast.add_trace(go.Scatter(
                            x=list(range(len(contrast_values))),
                            y=contrast_values,
                            mode='lines+markers',
                            name='Contrast',
                            line=dict(color='#39d353', width=2)
                        ))
                        fig_contrast.update_layout(
                            title='Contrast Variation Over Time',
                            xaxis_title='Sample Frame',
                            yaxis_title='Contrast (Std Dev)',
                            template='plotly_dark',
                            height=350
                        )
                        st.plotly_chart(fig_contrast, use_container_width=True)
                        
                        # Statistics
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Avg Brightness", f"{np.mean(brightness_values):.2f}")
                        col2.metric("Avg Contrast", f"{np.mean(contrast_values):.2f}")
                        col3.metric("Stability Score", f"{100 - np.std(brightness_values):.1f}%")
                
            except ImportError:
                st.warning("⚠️ OpenCV not installed. Install it with: `pip install opencv-python`")
        
        # Cleanup
        st.markdown("---")
        if st.button("🗑️ Clear Video", key="clear_video"):
            if os.path.exists("temp_video.mp4"):
                os.remove("temp_video.mp4")
            st.rerun()
    
    else:
        st.info("👆 Upload a video file to begin analysis.")
        st.markdown("---")
        st.markdown("""
        **Video Analysis Features:**
        - 🎬 Video preview and playback
        - 📊 Metadata extraction (resolution, FPS, duration)
        - 🎞️ Frame extraction and analysis
        - 🔍 Object detection capabilities
        - 📈 Brightness and contrast analysis
        - 🎯 Scene detection and classification
        """)

# -----------------------------------------
# Text Analysis Section
# -----------------------------------------
elif data_type == "📝 Text Analysis":
    st.subheader("📝 Text Analysis")
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["📄 Upload Text File", "✍️ Enter Text Manually"])
    
    text_content = None
    
    if input_method == "📄 Upload Text File":
        text_file = st.file_uploader(
            "Upload a text file",
            type=["txt", "md", "csv", "json", "log"],
            help="Supported formats: TXT, MD, CSV, JSON, LOG"
        )
        
        if text_file:
            text_content = text_file.read().decode('utf-8', errors='ignore')
            st.success(f"✅ Loaded {len(text_content)} characters from {text_file.name}")
    
    else:
        text_content = st.text_area(
            "Enter or paste your text here:",
            height=200,
            placeholder="Type or paste your text for analysis..."
        )
    
    if text_content:
        # Display text
        with st.expander("📖 View Full Text", expanded=False):
            st.text(text_content[:5000] + "..." if len(text_content) > 5000 else text_content)
        
        st.markdown("---")
        
        # Basic metrics
        st.markdown("#### 📊 Text Statistics")
        
        words = text_content.split()
        sentences = text_content.split('.')
        lines = text_content.split('\n')
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Characters", f"{len(text_content):,}")
        col2.metric("Words", f"{len(words):,}")
        col3.metric("Sentences", f"{len(sentences):,}")
        col4.metric("Lines", f"{len(lines):,}")
        col5.metric("Avg Word Length", f"{sum(len(w) for w in words) / len(words):.1f}" if words else "0")
        
        st.markdown("---")
        
        # Analysis tabs
        analysis_tabs = st.tabs(["📈 Word Analysis", "🔤 Character Analysis", "💭 Sentiment", "🏷️ Keywords", "� Text-to-Speech", "�📚 Advanced NLP"])
        
        with analysis_tabs[0]:
            st.markdown("##### 📈 Word Frequency Analysis")
            
            # Word frequency
            from collections import Counter
            import plotly.express as px
            
            # Clean and count words
            clean_words = [w.lower().strip('.,!?;:"()[]{}') for w in words if len(w) > 2]
            word_freq = Counter(clean_words)
            
            # Top words
            top_n = st.slider("Show top N words", 5, 50, 20, key="top_words")
            top_words = word_freq.most_common(top_n)
            
            if top_words:
                # Bar chart
                words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                fig = px.bar(words_df, x='Word', y='Frequency',
                           title=f'Top {top_n} Most Frequent Words',
                           color='Frequency',
                           color_continuous_scale='Blues')
                fig.update_layout(template='plotly_dark', height=400)
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Table
                st.dataframe(words_df, use_container_width=True, hide_index=True)
            
            # Word length distribution
            st.markdown("##### 📏 Word Length Distribution")
            word_lengths = [len(w) for w in words]
            length_dist = Counter(word_lengths)
            
            length_df = pd.DataFrame(sorted(length_dist.items()), columns=['Length', 'Count'])
            fig_length = px.bar(length_df, x='Length', y='Count',
                              title='Distribution of Word Lengths',
                              color='Count',
                              color_continuous_scale='Teal')
            fig_length.update_layout(template='plotly_dark', height=350)
            st.plotly_chart(fig_length, use_container_width=True)
        
        with analysis_tabs[1]:
            st.markdown("##### 🔤 Character Analysis")
            
            # Character frequency
            char_freq = Counter(text_content.lower())
            
            # Filter to letters only
            letters_only = {k: v for k, v in char_freq.items() if k.isalpha()}
            top_chars = sorted(letters_only.items(), key=lambda x: x[1], reverse=True)[:26]
            
            char_df = pd.DataFrame(top_chars, columns=['Character', 'Frequency'])
            
            fig_chars = px.bar(char_df, x='Character', y='Frequency',
                             title='Character Frequency Distribution',
                             color='Frequency',
                             color_continuous_scale='Viridis')
            fig_chars.update_layout(template='plotly_dark', height=400)
            st.plotly_chart(fig_chars, use_container_width=True)
            
            # Special characters
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Letter Statistics")
                uppercase_count = sum(1 for c in text_content if c.isupper())
                lowercase_count = sum(1 for c in text_content if c.islower())
                
                stats_df = pd.DataFrame({
                    'Type': ['Uppercase', 'Lowercase', 'Digits', 'Spaces', 'Special Chars'],
                    'Count': [
                        uppercase_count,
                        lowercase_count,
                        sum(1 for c in text_content if c.isdigit()),
                        sum(1 for c in text_content if c.isspace()),
                        sum(1 for c in text_content if not c.isalnum() and not c.isspace())
                    ]
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("##### Punctuation Frequency")
                punctuation = {k: v for k, v in char_freq.items() if k in '.,!?;:\'"()-'}
                if punctuation:
                    punct_df = pd.DataFrame(sorted(punctuation.items(), key=lambda x: x[1], reverse=True),
                                          columns=['Symbol', 'Count'])
                    st.dataframe(punct_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No punctuation found")
        
        with analysis_tabs[2]:
            st.markdown("##### 💭 Sentiment Analysis")
            
            try:
                from textblob import TextBlob
                
                blob = TextBlob(text_content)
                sentiment = blob.sentiment
                
                # Sentiment metrics
                col1, col2, col3 = st.columns(3)
                
                polarity = sentiment.polarity
                subjectivity = sentiment.subjectivity
                
                # Determine sentiment
                if polarity > 0.1:
                    sentiment_label = "😊 Positive"
                    sentiment_color = "#39d353"
                elif polarity < -0.1:
                    sentiment_label = "😞 Negative"
                    sentiment_color = "#f85149"
                else:
                    sentiment_label = "😐 Neutral"
                    sentiment_color = "#58a6ff"
                
                col1.metric("Sentiment", sentiment_label)
                col2.metric("Polarity", f"{polarity:.3f}")
                col3.metric("Subjectivity", f"{subjectivity:.3f}")
                
                # Visualization
                import plotly.graph_objects as go
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=polarity,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Sentiment Polarity"},
                    delta={'reference': 0},
                    gauge={
                        'axis': {'range': [-1, 1]},
                        'bar': {'color': sentiment_color},
                        'steps': [
                            {'range': [-1, -0.3], 'color': "rgba(248, 81, 73, 0.3)"},
                            {'range': [-0.3, 0.3], 'color': "rgba(88, 166, 255, 0.3)"},
                            {'range': [0.3, 1], 'color': "rgba(57, 211, 83, 0.3)"}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': polarity
                        }
                    }
                ))
                fig.update_layout(template='plotly_dark', height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Explanation
                st.markdown("##### 📖 Understanding the Metrics")
                st.markdown("""
                - **Polarity**: Ranges from -1 (most negative) to +1 (most positive)
                - **Subjectivity**: Ranges from 0 (very objective) to 1 (very subjective)
                """)
                
            except ImportError:
                st.warning("⚠️ TextBlob not installed. Install it with: `pip install textblob`")
                st.info("After installation, run: `python -m textblob.download_corpora`")
        
        with analysis_tabs[3]:
            st.markdown("##### 🏷️ Keyword Extraction")
            
            try:
                from collections import Counter
                import re
                
                # Simple keyword extraction (remove common stop words)
                stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                            'could', 'should', 'may', 'might', 'this', 'that', 'these', 'those',
                            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
                            'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
                            'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
                            'own', 'same', 'so', 'than', 'too', 'very', 'can', 'just', 'now'}
                
                # Clean and filter words
                clean_words = [w.lower().strip('.,!?;:"()[]{}') for w in words 
                              if len(w) > 3 and w.lower() not in stop_words]
                
                keyword_freq = Counter(clean_words)
                top_keywords = keyword_freq.most_common(30)
                
                if top_keywords:
                    keywords_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Frequency'])
                    
                    # Treemap visualization
                    import plotly.express as px
                    fig = px.treemap(keywords_df.head(20), path=['Keyword'], values='Frequency',
                                   title='Top Keywords (Treemap)',
                                   color='Frequency',
                                   color_continuous_scale='Blues')
                    fig.update_layout(template='plotly_dark', height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Table
                    st.dataframe(keywords_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No keywords found")
                
            except Exception as e:
                st.error(f"Error in keyword extraction: {str(e)}")
        
        with analysis_tabs[4]:
            st.markdown("##### � Text-to-Speech Conversion")
            
            st.markdown("Convert your text to speech using Google Text-to-Speech (gTTS)")
            
            # TTS options
            col1, col2 = st.columns(2)
            
            with col1:
                tts_text = st.text_area(
                    "Text to convert to speech:",
                    value=text_content[:500] if len(text_content) > 500 else text_content,
                    height=150,
                    help="Maximum 500 characters recommended for optimal performance"
                )
            
            with col2:
                st.markdown("##### Settings")
                language = st.selectbox(
                    "Language",
                    options=[
                        ("English", "en"),
                        ("Spanish", "es"),
                        ("French", "fr"),
                        ("German", "de"),
                        ("Italian", "it"),
                        ("Portuguese", "pt"),
                        ("Hindi", "hi"),
                        ("Japanese", "ja"),
                        ("Korean", "ko"),
                        ("Chinese", "zh-CN")
                    ],
                    format_func=lambda x: x[0],
                    index=0
                )
                
                slow_speed = st.checkbox("Slow speech", value=False)
                
                st.caption(f"Selected: {language[0]} ({language[1]})")
            
            if st.button("🎤 Generate Speech", key="generate_tts"):
                if not tts_text.strip():
                    st.warning("⚠️ Please enter some text to convert to speech.")
                else:
                    # Try to import gTTS; if missing offer to install it
                    import sys
                    import subprocess

                    try:
                        from gtts import gTTS  # type: ignore
                        gtts_available = True
                    except Exception:
                        gtts_available = False

                    if not gtts_available:
                        st.warning("⚠️ gTTS is not installed.")
                        if st.button("Install gTTS now", key="install_gtts"):
                            with st.spinner("Installing gTTS into the current Python environment..."):
                                try:
                                    # Run pip using the same Python interpreter
                                    proc = subprocess.run([sys.executable, "-m", "pip", "install", "gtts"], capture_output=True, text=True)
                                    if proc.returncode != 0:
                                        st.error("Failed to install gTTS. See output below:")
                                        st.code(proc.stderr[:1000])
                                        raise RuntimeError("pip install failed")
                                    else:
                                        st.success("gTTS installed successfully. Generating speech...")
                                        # attempt import again
                                        from gtts import gTTS  # type: ignore
                                except Exception as e:
                                    st.error(f"Installation failed: {e}")
                                    # stop here; user can re-run after fixing environment
                                    raise st.stop()

                    # If gTTS is available proceed to generate audio
                    try:
                        from gtts import gTTS  # type: ignore
                        with st.spinner("Generating speech..."):
                            tts = gTTS(text=tts_text, lang=language[1], slow=slow_speed)
                            tts_file = "temp_tts_output.mp3"
                            tts.save(tts_file)

                        # Display audio player and download
                        st.success("✅ Speech generated successfully!")
                        st.audio(tts_file)
                        with open(tts_file, "rb") as f:
                            st.download_button(
                                label="📥 Download Audio",
                                data=f,
                                file_name="text_to_speech.mp3",
                                mime="audio/mp3"
                            )

                        # Show stats
                        file_size = os.path.getsize(tts_file) / 1024  # KB
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("Characters", len(tts_text))
                        col_b.metric("Words", len(tts_text.split()))
                        col_c.metric("Audio Size", f"{file_size:.1f} KB")

                    except Exception as e:
                        st.error(f"Error generating speech: {str(e)}")
            
            st.markdown("---")
            st.markdown("##### 📖 About Text-to-Speech")
            st.info("""
            **Google Text-to-Speech (gTTS)** converts text into natural-sounding speech.
            - Supports multiple languages
            - Adjustable speech speed
            - High-quality voice synthesis
            - Ideal for accessibility and content creation
            """)
        
        with analysis_tabs[5]:
            st.markdown("##### �📚 Advanced NLP Features")
            
            st.info("🚧 Advanced NLP features require additional libraries (spaCy, NLTK, transformers)")
            
            st.markdown("**Planned Features:**")
            st.markdown("""
            - 🏷️ Named Entity Recognition (NER)
            - 🌳 Part-of-Speech Tagging
            - 🔗 Dependency Parsing
            - 📊 Text Classification
            - 🌐 Language Detection
            - 📝 Text Summarization
            - 🔄 Text Translation
            """)
            
            # Simulated NER
            if st.button("🔮 Simulate NER", key="simulate_ner"):
                st.markdown("##### Named Entities (Simulated)")
                simulated_entities = pd.DataFrame({
                    'Entity': ['OpenAI', 'San Francisco', 'GPT-4', 'Python', 'USA'],
                    'Type': ['ORGANIZATION', 'LOCATION', 'PRODUCT', 'TECHNOLOGY', 'LOCATION'],
                    'Count': [3, 1, 2, 5, 1]
                })
                st.dataframe(simulated_entities, use_container_width=True, hide_index=True)
        
        # Download analysis
        st.markdown("---")
        
        analysis_report = f"""
TEXT ANALYSIS REPORT
====================

File Statistics:
- Characters: {len(text_content):,}
- Words: {len(words):,}
- Sentences: {len(sentences):,}
- Lines: {len(lines):,}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        st.download_button(
            "📥 Download Analysis Report",
            analysis_report.encode('utf-8'),
            "text_analysis_report.txt",
            "text/plain"
        )
    
    else:
        st.info("👆 Upload a file or enter text to begin analysis.")
        st.markdown("---")
        st.markdown("""
        **Text Analysis Features:**
        - 📊 Comprehensive text statistics
        - 📈 Word frequency analysis
        - 🔤 Character distribution
        - 💭 Sentiment analysis
        - 🏷️ Keyword extraction
        - 📚 Advanced NLP capabilities
        """)

# -----------------------------------------
# Audio Analysis Section
# -----------------------------------------
else:  # Audio Analysis
    st.subheader("🎵 Audio Analysis")
    
    audio_file = st.file_uploader(
        "Upload an audio file",
        type=["mp3", "wav", "ogg", "m4a", "flac"],
        help="Supported formats: MP3, WAV, OGG, M4A, FLAC"
    )
    
    if audio_file:
        # Save audio file
        with open("temp_audio.mp3", "wb") as f:
            f.write(audio_file.read())
        
        # Display audio player
        st.markdown("#### 🎧 Audio Player")
        st.audio("temp_audio.mp3")
        
        # Basic metrics
        file_size = os.path.getsize("temp_audio.mp3") / (1024 * 1024)  # MB
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("File Size", f"{file_size:.2f} MB")
        col2.metric("Format", audio_file.type.split('/')[-1].upper())
        col3.metric("File Name", audio_file.name[:20] + "..." if len(audio_file.name) > 20 else audio_file.name)
        col4.metric("Upload Time", datetime.now().strftime("%H:%M:%S"))
        
        st.markdown("---")
        
        # Analysis tabs
        analysis_tabs = st.tabs(["📊 Audio Info", "🌊 Waveform", "📈 Spectrum", "🎤 Transcription"])
        
        with analysis_tabs[0]:
            st.markdown("##### 📊 Audio Properties")
            
            try:
                import librosa
                import numpy as np
                
                # Load audio
                y, sr = librosa.load("temp_audio.mp3", sr=None)
                duration = len(y) / sr
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Duration", f"{duration:.2f}s")
                col2.metric("Sample Rate", f"{sr:,} Hz")
                col3.metric("Channels", "Mono")
                
                col4, col5, col6 = st.columns(3)
                col4.metric("Total Samples", f"{len(y):,}")
                col5.metric("Bit Depth", "16-bit (estimated)")
                col6.metric("Avg Amplitude", f"{np.mean(np.abs(y)):.4f}")
                
                # Detailed properties
                st.markdown("##### 📋 Detailed Audio Properties")
                props_df = pd.DataFrame({
                    'Property': ['File Name', 'Format', 'Duration', 'Sample Rate', 'Total Samples', 'File Size'],
                    'Value': [
                        audio_file.name,
                        audio_file.type,
                        f"{duration:.2f}s",
                        f"{sr:,} Hz",
                        f"{len(y):,}",
                        f"{file_size:.2f} MB"
                    ]
                })
                st.dataframe(props_df, use_container_width=True, hide_index=True)
                
            except ImportError:
                st.warning("⚠️ Librosa not installed. Install it with: `pip install librosa`")
                st.info("Basic file information only available.")
        
        with analysis_tabs[1]:
            st.markdown("##### 🌊 Waveform Visualization")
            
            try:
                import librosa
                import librosa.display
                import numpy as np
                import plotly.graph_objects as go
                
                # Load audio
                y, sr = librosa.load("temp_audio.mp3", sr=None, duration=60)  # Limit to 60s
                
                # Create time array
                time = np.linspace(0, len(y) / sr, len(y))
                
                # Downsample for plotting
                downsample_factor = max(1, len(y) // 5000)
                time_plot = time[::downsample_factor]
                y_plot = y[::downsample_factor]
                
                # Plot waveform
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=time_plot,
                    y=y_plot,
                    mode='lines',
                    name='Amplitude',
                    line=dict(color='#58a6ff', width=1)
                ))
                fig.update_layout(
                    title='Audio Waveform',
                    xaxis_title='Time (seconds)',
                    yaxis_title='Amplitude',
                    template='plotly_dark',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Max Amplitude", f"{np.max(np.abs(y)):.4f}")
                col2.metric("Min Amplitude", f"{np.min(y):.4f}")
                col3.metric("RMS Energy", f"{np.sqrt(np.mean(y**2)):.4f}")
                col4.metric("Zero Crossings", f"{len(librosa.zero_crossings(y)):,}")
                
            except ImportError:
                st.warning("⚠️ Librosa not installed. Install it with: `pip install librosa`")
        
        with analysis_tabs[2]:
            st.markdown("##### 📈 Frequency Spectrum Analysis")
            
            try:
                import librosa
                import numpy as np
                import plotly.graph_objects as go
                
                # Load audio
                y, sr = librosa.load("temp_audio.mp3", sr=None, duration=30)
                
                # Compute spectrogram
                D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
                
                # Plot spectrogram
                fig = go.Figure(data=go.Heatmap(
                    z=D,
                    colorscale='Viridis',
                    colorbar=dict(title='dB')
                ))
                fig.update_layout(
                    title='Spectrogram',
                    xaxis_title='Time Frame',
                    yaxis_title='Frequency Bin',
                    template='plotly_dark',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Compute spectral features
                spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
                spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Avg Spectral Centroid", f"{np.mean(spectral_centroids):.0f} Hz")
                col2.metric("Avg Spectral Rolloff", f"{np.mean(spectral_rolloff):.0f} Hz")
                col3.metric("Bandwidth", f"{np.std(spectral_centroids):.0f} Hz")
                
                # Plot spectral features over time
                time_frames = np.linspace(0, len(y) / sr, len(spectral_centroids))
                
                fig_features = go.Figure()
                fig_features.add_trace(go.Scatter(
                    x=time_frames,
                    y=spectral_centroids,
                    mode='lines',
                    name='Spectral Centroid',
                    line=dict(color='#58a6ff')
                ))
                fig_features.add_trace(go.Scatter(
                    x=time_frames,
                    y=spectral_rolloff,
                    mode='lines',
                    name='Spectral Rolloff',
                    line=dict(color='#39d353')
                ))
                fig_features.update_layout(
                    title='Spectral Features Over Time',
                    xaxis_title='Time (seconds)',
                    yaxis_title='Frequency (Hz)',
                    template='plotly_dark',
                    height=350
                )
                st.plotly_chart(fig_features, use_container_width=True)
                
            except ImportError:
                st.warning("⚠️ Librosa not installed. Install it with: `pip install librosa`")
        
        with analysis_tabs[3]:
            st.markdown("##### 🎤 Speech-to-Text Transcription")
            
            st.markdown("Convert audio speech to text using Google Speech Recognition")
            
            st.info("ℹ️ Audio files are automatically converted to WAV format for optimal recognition. Supports MP3, WAV, OGG, FLAC, and more!")
            
            # Transcription options
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Transcription Method**")
                transcription_method = st.radio(
                    "Choose recognition engine:",
                    ["Google Speech Recognition (Free)", "Sphinx (Offline)"],
                    help="Google requires internet connection but provides better accuracy"
                )
            
            with col2:
                st.markdown("**Language**")
                lang_code = st.selectbox(
                    "Audio Language",
                    options=[
                        ("English (US)", "en-US"),
                        ("English (UK)", "en-GB"),
                        ("Spanish", "es-ES"),
                        ("French", "fr-FR"),
                        ("German", "de-DE"),
                        ("Hindi", "hi-IN"),
                        ("Japanese", "ja-JP"),
                        ("Chinese", "zh-CN")
                    ],
                    format_func=lambda x: x[0],
                    index=0
                )
            
            if st.button("� Transcribe Audio", key="transcribe_audio"):
                try:
                    import speech_recognition as sr
                    
                    with st.spinner("Transcribing audio... This may take a moment..."):
                        # Initialize recognizer
                        recognizer = sr.Recognizer()
                        
                        # Convert audio to WAV format if needed
                        audio_file_path = "temp_audio.mp3"
                        wav_file_path = "temp_audio_converted.wav"
                        
                        # Load audio file
                        try:
                            from pydub import AudioSegment
                            
                            st.info("🔄 Converting audio to WAV format...")
                            # Load audio file and convert to WAV
                            audio = AudioSegment.from_file(audio_file_path)
                            
                            # Export as WAV with proper settings for speech recognition
                            audio.export(
                                wav_file_path,
                                format="wav",
                                parameters=["-ar", "16000", "-ac", "1"]  # 16kHz, mono
                            )
                            
                            st.info("📖 Reading audio file...")
                            
                            with sr.AudioFile(wav_file_path) as source:
                                # Adjust for ambient noise
                                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                                audio_data = recognizer.record(source)
                                
                                st.info("🔍 Performing speech recognition...")
                                
                                # Perform recognition
                                if "Google" in transcription_method:
                                    transcript = recognizer.recognize_google(
                                        audio_data,
                                        language=lang_code[1]
                                    )
                                else:
                                    transcript = recognizer.recognize_sphinx(audio_data)
                                
                                # Display results
                                st.success("✅ Transcription completed successfully!")
                                
                                st.markdown("##### 📝 Transcription Results")
                                st.text_area(
                                    "Transcribed Text:",
                                    transcript,
                                    height=200,
                                    help="Copy this text for further use"
                                )
                                
                                # Analysis
                                words = transcript.split()
                                col_a, col_b, col_c, col_d = st.columns(4)
                                col_a.metric("Words", len(words))
                                col_b.metric("Characters", len(transcript))
                                col_c.metric("Sentences", transcript.count('.') + transcript.count('!') + transcript.count('?'))
                                col_d.metric("Language", lang_code[0])
                                
                                # Word frequency
                                st.markdown("##### 🏷️ Top Keywords")
                                from collections import Counter
                                word_freq = Counter([w.lower() for w in words if len(w) > 3])
                                top_words = word_freq.most_common(10)
                                
                                if top_words:
                                    keywords_df = pd.DataFrame(top_words, columns=['Keyword', 'Frequency'])
                                    st.dataframe(keywords_df, use_container_width=True, hide_index=True)
                                
                                # Download transcript
                                st.download_button(
                                    label="📥 Download Transcript",
                                    data=transcript,
                                    file_name="audio_transcript.txt",
                                    mime="text/plain"
                                )
                                
                                # Cleanup converted WAV file
                                if os.path.exists(wav_file_path):
                                    os.remove(wav_file_path)
                                
                        except sr.UnknownValueError:
                            st.error("❌ Could not understand the audio. Please ensure the audio contains clear speech.")
                            st.info("💡 Tips: Use clear speech, reduce background noise, and ensure audio quality is good.")
                        except sr.RequestError as e:
                            st.error(f"❌ Could not request results from recognition service: {e}")
                            st.info("💡 Check your internet connection (required for Google Speech Recognition).")
                        except Exception as e:
                            st.error(f"❌ Error processing audio file: {str(e)}")
                            st.info("💡 The audio has been automatically converted to WAV format for processing.")
                        finally:
                            # Cleanup converted file if it exists
                            if os.path.exists(wav_file_path):
                                try:
                                    os.remove(wav_file_path)
                                except:
                                    pass
                
                except ImportError:
                    st.warning("⚠️ SpeechRecognition not installed. Install it with: `pip install SpeechRecognition`")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            st.markdown("---")
            st.markdown("##### 📖 About Speech Recognition")
            st.info("""
            **Speech-to-Text** converts spoken words in audio to written text.
            
            **Available Engines:**
            - **Google Speech Recognition**: High accuracy, requires internet
            - **Sphinx**: Works offline, lower accuracy
            
            **Best Practices:**
            - Use clear, high-quality audio recordings
            - Minimize background noise
            - Use WAV format for best compatibility
            - Select the correct language for better accuracy
            """)
        
        # Cleanup
        st.markdown("---")
        if st.button("🗑️ Clear Audio", key="clear_audio"):
            if os.path.exists("temp_audio.mp3"):
                os.remove("temp_audio.mp3")
            st.rerun()
    
    else:
        st.info("👆 Upload an audio file to begin analysis.")
        st.markdown("---")
        st.markdown("""
        **Audio Analysis Features:**
        - 🎧 Audio playback
        - 📊 Metadata extraction
        - 🌊 Waveform visualization
        - 📈 Spectrum analysis
        - 🎤 Speech-to-text transcription
        - 🎵 Music feature extraction
        - 🔊 Noise reduction
        """)

# Footer
st.markdown("---")
st.caption("🎬 DataSense Unstructured Data Explorer | Built with Streamlit")
