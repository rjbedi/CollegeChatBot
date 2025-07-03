import streamlit as st
import json
import os
from datetime import datetime
import re

QUESTIONS_FILE = "chatbot_questions.json"

#Questions and answers
DEFAULT_QA = {
    "hello": "Hello! I'm your Team Intel's chatbot. How can I help you today?",
    "hi": "Hi there! Welcome to our Team Intel's chatbot. What would you like to know?",
    "how are you": "I'm doing great! Thank you for asking. How can I assist you?",
    "what is your name": "I'm the Team Intel's Helper Bot, created to assist students with their queries.",
    "bye": "Goodbye! Have a great day and feel free to come back anytime!",
    "thank you": "You're welcome! I'm happy to help. Is there anything else you'd like to know?",
    "help": "I can help you with various college-related queries. Just ask me anything!",
    "courses": "We offer various undergraduate and graduate programs. What specific course are you interested in?",
    "admission": "For admission information, please visit our admissions office or check our website for requirements.",
    "fees": "Fee structure varies by program. Please contact the accounts office for detailed fee information.",
    "library": "Our library is open Monday-Friday 8 AM to 8 PM, and Saturday 9 AM to 5 PM.",
    "campus": "Our campus has modern facilities including labs, library, cafeteria, sports complex, and hostels.",
    "contact": "You can reach us at shruti-manmeet@gmail.com or call our main office at +1234567890."
}


def load_questions():
    """Load questions from JSON file or create default ones"""
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_QA.copy()
    else:
        save_questions(DEFAULT_QA)
        return DEFAULT_QA.copy()

def save_questions(questions):
    """Save questions to JSON file"""
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f, indent=2)

def get_response(user_input, questions):
    """Get response based on user input"""
    user_input = user_input.lower().strip()
    
    if user_input in questions:
        return questions[user_input]
    
    for question, answer in questions.items():
        if question in user_input or user_input in question:
            return answer
    
    for question, answer in questions.items():
        question_words = question.split()
        user_words = user_input.split()
        
        if any(word in question_words for word in user_words):
            return answer
    
    return "I'm sorry, I don't understand that question. Could you please rephrase or ask something else?"

def main():
    st.set_page_config(
        page_title="College Chatbot",
        page_icon="🎓",
        layout="wide"
    )
    
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 30px;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .chat-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        margin: 8px 0;
        margin-left: 20%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        font-weight: 500;
    }
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        margin: 8px 0;
        margin-right: 20%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        font-weight: 500;
    }
    .admin-section {
        background-color: #FFF3E0;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FF9800;
        margin: 10px 0;
    }
    .stTextInput > div > div > input {
        background-color: white;
        color: black;
        border: 2px solid #ddd;
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    .quick-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        margin: 5px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s;
    }
    .quick-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .chat-history-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }
    .welcome-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if 'questions' not in st.session_state:
        st.session_state.questions = load_questions()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.markdown("<h2 class='main-header'>🎓 College Chatbot Assistant</h2>", unsafe_allow_html=True)
    
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["Chatbot", "Admin Panel", "About"])
    
    if page == "Chatbot":
        chatbot_page()
    elif page == "Admin Panel":
        admin_panel()
    else:
        about_page()

def chatbot_page():
    """Main chatbot interface"""
    st.markdown("### 💬 Chat with our College Bot")
    
    if not st.session_state.chat_history:
        st.markdown("""
        <div class='welcome-message'>
            👋 Welcome to the College Chatbot! 
            <br>Ask me anything about admissions, courses, facilities, or college life.
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        st.markdown("#### 💬 Chat History")
        with st.container():
            st.markdown("<div class='chat-history-container'>", unsafe_allow_html=True)
            for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
                st.markdown(f"<div class='user-message'>👤 {user_msg}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='bot-message'>🤖 {bot_msg}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    st.markdown("#### 💭 Send a Message")
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input("", key="user_input", placeholder="Type your message here... (e.g., 'What courses do you offer?')")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
            send_button = st.button("Send 📤", type="primary")
    
    if send_button and user_input:
        bot_response = get_response(user_input, st.session_state.questions)
        
        st.session_state.chat_history.append((user_input, bot_response))
        
        st.rerun()
    
    st.markdown("#### 🚀 Quick Questions")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 15px; margin: 10px 0;'>
        <p style='color: white; margin: 0; text-align: center; font-weight: 500;'>
            Click any button below for instant answers! 👇
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎓 Admission Info", use_container_width=True):
            bot_response = get_response("admission", st.session_state.questions)
            st.session_state.chat_history.append(("🎓 Admission Info", bot_response))
            st.rerun()
    
    with col2:
        if st.button("📚 Courses", use_container_width=True):
            bot_response = get_response("courses", st.session_state.questions)
            st.session_state.chat_history.append(("📚 Courses", bot_response))
            st.rerun()
    
    with col3:
        if st.button("📖 Library Hours", use_container_width=True):
            bot_response = get_response("library", st.session_state.questions)
            st.session_state.chat_history.append(("📖 Library Hours", bot_response))
            st.rerun()
    
    with col4:
        if st.button("📞 Contact Info", use_container_width=True):
            bot_response = get_response("contact", st.session_state.questions)
            st.session_state.chat_history.append(("📞 Contact Info", bot_response))
            st.rerun()
    
    # Additional quick buttons
    st.markdown("---")
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        if st.button("💰 Fees", use_container_width=True):
            bot_response = get_response("fees", st.session_state.questions)
            st.session_state.chat_history.append(("💰 Fees", bot_response))
            st.rerun()
    
    with col6:
        if st.button("🏫 Campus", use_container_width=True):
            bot_response = get_response("campus", st.session_state.questions)
            st.session_state.chat_history.append(("🏫 Campus", bot_response))
            st.rerun()
    
    with col7:
        if st.button("❓ Help", use_container_width=True):
            bot_response = get_response("help", st.session_state.questions)
            st.session_state.chat_history.append(("❓ Help", bot_response))
            st.rerun()
    
    with col8:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()

def admin_panel():
    """Admin panel for managing questions and answers"""
    st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Admin Panel - Manage Questions & Answers")
    
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter admin password:", type="password")
        if st.button("Login"):
            if password == "admin123":  # You can change this password
                st.session_state.admin_authenticated = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid password!")
        st.info("💡 Default password: admin123")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Admin interface
    st.success("Welcome to the Admin Panel!")
    
    # Add new question/answer
    st.markdown("#### Add New Question & Answer")
    col1, col2 = st.columns(2)
    
    with col1:
        new_question = st.text_input("Question/Keyword:", placeholder="Enter question or keyword...")
    
    with col2:
        new_answer = st.text_area("Answer:", placeholder="Enter the response...")
    
    if st.button("Add Question"):
        if new_question and new_answer:
            question_key = new_question.lower().strip()
            st.session_state.questions[question_key] = new_answer
            save_questions(st.session_state.questions)
            st.success(f"Added: '{new_question}' -> '{new_answer}'")
            st.rerun()
        else:
            st.error("Please fill in both question and answer fields.")
    
    st.markdown("#### Existing Questions & Answers")
    
    if st.session_state.questions:
        search_term = st.text_input("Search questions:", placeholder="Search existing questions...")
        
        questions_to_show = st.session_state.questions
        if search_term:
            questions_to_show = {k: v for k, v in st.session_state.questions.items() 
                                if search_term.lower() in k.lower() or search_term.lower() in v.lower()}
        
        for i, (question, answer) in enumerate(questions_to_show.items()):
            with st.expander(f"Q: {question.title()}"):
                st.write(f"**Answer:** {answer}")
                
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_q = st.text_input(f"Edit question:", value=question, key=f"edit_q_{i}")
                
                with col2:
                    new_a = st.text_area(f"Edit answer:", value=answer, key=f"edit_a_{i}")
                
                with col3:
                    st.write("")  
                    if st.button("Update", key=f"update_{i}"):
                        if new_q and new_a:
                            # Remove old question
                            del st.session_state.questions[question]
                            # Add updated question
                            st.session_state.questions[new_q.lower().strip()] = new_a
                            save_questions(st.session_state.questions)
                            st.success("Updated successfully!")
                            st.rerun()
                    
                    if st.button("Delete", key=f"delete_{i}"):
                        del st.session_state.questions[question]
                        save_questions(st.session_state.questions)
                        st.success("Deleted successfully!")
                        st.rerun()
    
    # Bulk operations
    st.markdown("#### Bulk Operations")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Questions"):
            st.download_button(
                label="Download JSON",
                data=json.dumps(st.session_state.questions, indent=2),
                file_name=f"chatbot_questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("Import Questions", type=['json'])
        if uploaded_file is not None:
            try:
                imported_questions = json.load(uploaded_file)
                st.session_state.questions.update(imported_questions)
                save_questions(st.session_state.questions)
                st.success("Questions imported successfully!")
                st.rerun()
            except:
                st.error("Invalid JSON file!")
    
    with col3:
        if st.button("Reset to Default"):
            st.session_state.questions = DEFAULT_QA.copy()
            save_questions(st.session_state.questions)
            st.success("Reset to default questions!")
            st.rerun()
    
    # Statistics
    st.markdown("#### Statistics")
    st.info(f"Total Questions: {len(st.session_state.questions)}")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def about_page():
    """About page with project information"""
    st.markdown("### 📚 About This Chatbot")
    
    st.markdown("""
    This is a Team Intel's chatbot created by Shruti Chawla [23BCA10625] & Manmeet Singh [23BCA10805]. Here are its features:
    
    **Features:**
    - Interactive chat interface
    - Keyword-based response matching
    - Admin panel for managing questions and answers
    - Persistent data storage using JSON
    - Responsive design with Streamlit
    
    **Technologies Used:**
    - **Python**: Core programming language
    - **Streamlit**: Web framework for creating the interface
    - **JSON**: Data storage for questions and answers
    - **Regular Expressions**: For text matching and processing
    
    **How to Use:**
    1. **Chat**: Use the main chatbot interface to ask questions
    2. **Admin Panel**: Add, edit or delete questions and answers
    3. **Quick Buttons**: Use predefined buttons for common queries
    
    **Admin Panel Features:**
    - Password protection (default: admin123)
    - Add new questions and answers
    - Edit existing content
    - Delete unwanted entries
    - Search functionality
    - Export/Import questions
    - Reset to default questions
    
    **Project Structure:**
    ```
    college_chatbot.py          # Main application file
    chatbot_questions.json      # Questions and answers database
    ```
    
    **Future Enhancements:**
    - Integration with actual college databases
    - Natural Language Processing for better understanding
    - Multi-language support
    - Voice interaction capabilities
    - Analytics dashboard
    """)
    
    st.markdown("---")
    st.markdown("**Created for Intel AI Internship Project** 🎓")

if __name__ == "__main__":
    main()
