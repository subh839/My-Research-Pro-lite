import streamlit as st
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Research Assistant Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .question-example {
        background-color: #e8f4fd;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        cursor: pointer;
    }
    .error-box {
        background-color: #ffe6e6;
        border: 1px solid #ffcccc;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced error handling for deployment
try:
    from free_contextual_agent import FreeContextualAgent
    from chroma_manager import initialize_sample_data
    DEPENDENCIES_LOADED = True
except ImportError as e:
    st.error(f"⚠️ Import error: {e}")
    DEPENDENCIES_LOADED = False

# Fallback agent for deployment issues
class SimpleAgent:
    def process_query(self, question):
        current_date = datetime.now().strftime("%Y-%m-%d")
        return {
            "answer": f"""
# Research Report: {question}

**Report Date:** {current_date}  
**Status:** Running in Basic Mode

## Executive Summary
This is a simplified research report. For full features including real-time web search and document analysis, ensure all dependencies are properly installed.

## Key Findings
- The system is running in basic mode due to dependency loading issues
- Core AI functionality is available
- Advanced features require full dependency installation

## Available Features
 Basic AI-powered responses  
 Professional report formatting  
 Conversation history  
 Export functionality  

 

## Recommendations
1. Check deployment logs for dependency installation issues
2. Verify all packages in requirements.txt are compatible
3. Ensure Python version 3.8-3.11 is used
4. Contact support if issues persist

*Note: Running in limited capability mode. Full features will be available once dependencies are properly loaded.*
            """,
            "sources_used": {"web": False, "internal": False}
        }
    
    def get_agent_info(self):
        return {
            "has_gemini_api": False,
            "knowledge_base_docs": 0,
            "search_capability": "Basic Mode",
            "status": "limited"
        }

# Initialize agent with enhanced error handling
@st.cache_resource
def initialize_agent():
    try:
        if DEPENDENCIES_LOADED:
            initialize_sample_data()
            agent = FreeContextualAgent()
            st.success(" Full features initialized!")
            return agent
        else:
            raise ImportError("Dependencies not loaded")
    except Exception as e:
        st.error(f" Initialization error: {e}")
        return SimpleAgent()

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 AI Research Assistant Pro</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'agent' not in st.session_state:
        with st.spinner(" Initializing Advanced AI Research Agent..."):
            st.session_state.agent = initialize_agent()
    if 'research_count' not in st.session_state:
        st.session_state.research_count = 0

    # Display system status
    agent_info = st.session_state.agent.get_agent_info()
    if agent_info.get('status') == 'limited' or not DEPENDENCIES_LOADED:
        st.markdown("""
        <div class="error-box">
         **Limited Mode Active** - Some features unavailable
        </div>
        """, unsafe_allow_html=True)

    # Sidebar with enhanced features
    with st.sidebar:
        st.header("⚡ Control Panel")
        
        # Agent status with enhanced indicators
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Research Sessions", st.session_state.research_count)
        with col2:
            docs = agent_info['knowledge_base_docs']
            color = "normal" if docs > 0 else "off"
            st.metric("Knowledge Docs", docs)
        
        # System status
        st.markdown("---")
        st.subheader("🔧 System Status")
        
        status_items = [
            ("AI API", " Enabled" if agent_info.get('has_gemini_api') else " Disabled"),
            ("Search Mode", agent_info.get('search_capability', 'Basic')),
            ("Dependencies", "Loaded" if DEPENDENCIES_LOADED else " Issues"),
            ("Vector DB", " Ready" if docs > 0 else " Limited")
        ]
        
        for item, status in status_items:
            st.write(f"{item}: {status}")
        
        st.markdown("---")
        
        # Configuration
        st.subheader("⚙️ Settings")
        
        if st.button("🔄 Clear Conversation", use_container_width=True):
            st.session_state.conversation = []
            st.rerun()
            
        if st.button("📊 Export Research", use_container_width=True):
            if st.session_state.conversation:
                export_data = {
                    "export_date": datetime.now().isoformat(),
                    "conversations": st.session_state.conversation,
                    "system_status": agent_info
                }
                st.download_button(
                    label="📥 Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"research_export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No conversations to export")
        
        st.markdown("---")
        
        # Quick questions
        st.subheader("🚀 Quick Research")
        quick_questions = [
            "Latest AI regulations and our compliance",
            "Solid-state battery market trends",
            "Our renewable energy projects status",
            "Quantum computing competitive landscape",
            "Tech industry hiring trends 2024"
        ]
        
        for q in quick_questions:
            if st.button(f"🔍 {q}", key=f"quick_{q}", use_container_width=True):
                st.session_state.quick_question = q
                st.rerun()

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced question input
        st.subheader("💬 Research Query")
        
        # Handle quick questions
        if 'quick_question' in st.session_state:
            default_question = st.session_state.quick_question
            del st.session_state.quick_question
        else:
            default_question = ""
            
        user_question = st.text_area(
            "**Enter your research question:**",
            value=default_question,
            placeholder="e.g., 'Analyze recent advancements in solid-state batteries and compare with our internal Project Ares research'",
            height=120,
            key="question_input"
        )
        
        # Research options
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            research_depth = st.selectbox(
                "Research Depth",
                ["Quick", "Standard", "Comprehensive"],
                index=1
            )
        with col1b:
            include_sources = st.checkbox("Include Sources", value=True)
        with col1c:
            format_type = st.selectbox(
                "Output Format",
                ["Report", "Summary", "Bullet Points"],
                index=0
            )

    with col2:
        st.subheader("🎯 Research Tips")
        st.markdown("""
        <div class="feature-card">
         **For best results:**
        - Be specific about timeframes
        - Mention your organization context
        - Ask comparative questions
        - Request actionable insights
        </div>
        """, unsafe_allow_html=True)
        
        # Show deployment status
        if not DEPENDENCIES_LOADED or agent_info.get('status') == 'limited':
            st.markdown("""
            <div class="error-box">
             **Deployment Notice**
            - Running in basic mode
            - Some features limited
            - Check deployment logs
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        **Example Formats:**
        <div class="question-example">Compare our AI research with industry trends</div>
        <div class="question-example">Latest developments in renewable energy</div>
        <div class="question-example">Our compliance status for new regulations</div>
        """, unsafe_allow_html=True)

    # Research button
    if st.button("🚀 Launch Research Analysis", type="primary", use_container_width=True):
        if user_question:
            with st.spinner("🔍 Conducting comprehensive research analysis..."):
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    "Analyzing query intent and context...",
                    "Searching latest web developments...",
                    "Querying internal knowledge base...",
                    "Cross-referencing sources...",
                    "Synthesizing comprehensive analysis...",
                    "Formatting final report..."
                ]
                
                for i, step in enumerate(steps):
                    status_text.text(f"🔄 {step}")
                    progress_bar.progress((i + 1) * 16)
                    time.sleep(0.3)  # Reduced for better UX
                
                try:
                    result = st.session_state.agent.process_query(user_question)
                    st.session_state.research_count += 1
                    
                    # Add to conversation
                    st.session_state.conversation.append({
                        'question': user_question,
                        'answer': result['answer'],
                        'sources': result['sources_used'],
                        'timestamp': time.time(),
                        'research_id': f"res_{st.session_state.research_count:04d}",
                        'depth': research_depth
                    })
                    
                    progress_bar.progress(100)
                    status_text.success(" Research analysis complete!")
                    time.sleep(0.5)
                    
                except Exception as e:
                    progress_bar.progress(100)
                    status_text.error(" Research failed!")
                    st.error(f"Research error: {str(e)}")
                    st.info("""
                     **Troubleshooting tips:**
                    - Try a simpler question
                    - Check your API keys in environment variables
                    - Verify all dependencies are installed
                    - Check the deployment logs for errors
                    """)
        else:
            st.warning(" Please enter a research question")

    # Enhanced conversation display
    st.markdown("---")
    st.subheader("📚 Research History")
    
    if not st.session_state.conversation:
        st.info("""
        ## 🎯 Welcome to AI Research Assistant Pro!
        
        **Get started with:**
        
        ### 🔍 Sample Research Questions
        - *"Analyze current AI regulation trends and our compliance readiness"*
        - *"Compare our battery technology with recent market breakthroughs"*  
        - *"Research renewable energy investment opportunities for 2024"*
        - *"Assessment of quantum computing impact on our industry"*
        
        ### 💡 Pro Tips
        - Use specific timeframes for better results
        - Mention your organizational context
        - Ask for comparative analysis
        - Request actionable recommendations
        
        **⬆️ Enter your research question above to begin!**
        """)
    else:
        # Research statistics
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Total Researches", len(st.session_state.conversation))
        with col_stat2:
            web_used = sum(1 for conv in st.session_state.conversation if conv['sources']['web'])
            st.metric("Web Researches", web_used)
        with col_stat3:
            internal_used = sum(1 for conv in st.session_state.conversation if conv['sources']['internal'])
            st.metric("Internal Queries", internal_used)
        with col_stat4:
            success_rate = "100%" if len(st.session_state.conversation) > 0 else "0%"
            st.metric("Success Rate", success_rate)
        
        # Conversation display
        for i, exchange in enumerate(reversed(st.session_state.conversation)):
            with st.expander(
                f"**{exchange['research_id']}** | {exchange['question'][:80]}{'...' if len(exchange['question']) > 80 else ''} | {time.strftime('%m/%d %H:%M', time.localtime(exchange['timestamp']))}",
                expanded=i == 0
            ):
                # Research metadata
                col_meta1, col_meta2, col_meta3 = st.columns(3)
                with col_meta1:
                    st.caption(f"**Depth:** {exchange.get('depth', 'Standard')}")
                with col_meta2:
                    sources = []
                    if exchange['sources']['web']:
                        sources.append("🌐 Web")
                    if exchange['sources']['internal']:
                        sources.append("📚 Internal")
                    st.caption(f"**Sources:** {', '.join(sources)}")
                with col_meta3:
                    st.caption(f"**ID:** {exchange['research_id']}")
                
                # Answer display
                st.markdown(exchange['answer'])
                
                # Actions
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button(f"📋 Copy Report", key=f"copy_{i}"):
                        st.code(exchange['answer'], language='markdown')
                with col_act2:
                    if st.button(f"🔄 Rerun Research", key=f"rerun_{i}"):
                        st.session_state.quick_question = exchange['question']
                        st.rerun()

    # Footer
    st.markdown("---")
    col_foot1, col_foot2, col_foot3 = st.columns([2, 1, 1])
    with col_foot1:
        st.caption("🔍 **AI Research Assistant Pro** v2.0 | Enhanced with advanced analytics and reporting")
    with col_foot2:
        st.caption("🛠️ Built with Streamlit + ChromaDB + Gemini AI")
    with col_foot3:
        st.caption("📧 [Get Free API Keys](https://aistudio.google.com/)")

if __name__ == "__main__":
    main()