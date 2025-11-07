import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import numpy as np

# Page configuration
st.set_page_config(
    page_title="OPENFRAUDLABS - Finance Learning",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (No changes, but included for completeness)
st.markdown("""
<style>
    /* ... (Your existing CSS is kept as-is) ... */
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .course-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    .course-card:hover {
        transform: translateY(-5px);
    }
    .lesson-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .lesson-card:hover {
        background-color: #e9ecef;
        transform: translateX(5px);
    }
    .lesson-card.completed {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .progress-bar {
        background-color: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 1rem 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #28a745, #20c997);
        height: 100%;
        transition: width 0.5s ease;
    }
    .quiz-card {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        margin: 1rem 0;
    }
    .exam-card {
        background-color: #fffaf0;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #ffc107;
        margin: 1rem 0;
    }
    .achievement-badge {
        background: linear-gradient(135deg, #ffd89b, #19547b);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
    .certificate-badge {
        background: linear-gradient(135deg, #ff6b6b, #c0392b);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        display: inline-block;
        margin: 0.5rem;
        font-size: 1rem;
        font-weight: bold;
        border: 3px solid gold;
    }
    .video-container {
        position: relative;
        padding-bottom: 56.25%;
        height: 0;
        overflow: hidden;
        border-radius: 10px;
        margin: 2rem 0;
    }
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }
    .certificate-container {
        background: linear-gradient(135deg, #8B4513, #D2691E);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        border: 15px solid #FFD700;
        position: relative;
    }
</style>
""", unsafe_allow_html=True)

class CertificateGenerator:
    def __init__(self):
        self.certificate_templates = {
            'basic': {
                'background_color': (139, 69, 19),  # SaddleBrown
                'border_color': (255, 215, 0),     # Gold
                'text_color': (255, 255, 255),       # White
                'accent_color': (255, 215, 0)        # Gold
            }
        }
    
    def generate_certificate_image(self, student_name, course_name, completion_date, score=None, organization_name="OPENFRAUDLABS"):
        """Generate a certificate image using PIL"""
        # Create a blank certificate image
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color=self.certificate_templates['basic']['background_color'])
        draw = ImageDraw.Draw(image)
        
        try:
            # Try to use a fancy font, fall back to default if not available
            try:
                title_font = ImageFont.truetype("arialbd.ttf", 40)
                name_font = ImageFont.truetype("arialbd.ttf", 36)
                text_font = ImageFont.truetype("arial.ttf", 24)
                small_font = ImageFont.truetype("arial.ttf", 18)
                org_font = ImageFont.truetype("arialbd.ttf", 28)
            except:
                # Fallback to default font
                title_font = ImageFont.load_default()
                name_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
                org_font = ImageFont.load_default()
            
            # Draw border
            draw.rectangle([10, 10, width-10, height-10], outline=self.certificate_templates['basic']['border_color'], width=8)
            
            # *** NEW: Draw Organization Name at Top ***
            org_bbox = draw.textbbox((0, 0), organization_name, font=org_font)
            org_width = org_bbox[2] - org_bbox[0]
            draw.text(((width - org_width) // 2, 40), organization_name, fill=self.certificate_templates['basic']['text_color'], font=org_font)
            
            # Draw title
            title = "CERTIFICATE OF COMPLETION"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((width - title_width) // 2, 100), title, fill=self.certificate_templates['basic']['accent_color'], font=title_font)
            
            # Draw subtitle
            subtitle = "This certifies that"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=text_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            draw.text(((width - subtitle_width) // 2, 180), subtitle, fill=self.certificate_templates['basic']['text_color'], font=text_font)
            
            # Draw student name
            name_bbox = draw.textbbox((0, 0), student_name, font=name_font)
            name_width = name_bbox[2] - name_bbox[0]
            draw.text(((width - name_width) // 2, 240), student_name, fill=self.certificate_templates['basic']['accent_color'], font=name_font)
            
            # Draw course completion text
            course_text = f"has successfully completed the course"
            course_bbox = draw.textbbox((0, 0), course_text, font=text_font)
            course_width = course_bbox[2] - course_bbox[0]
            draw.text(((width - course_width) // 2, 310), course_text, fill=self.certificate_templates['basic']['text_color'], font=text_font)
            
            # Draw course name
            course_name_bbox = draw.textbbox((0, 0), course_name, font=name_font)
            course_name_width = course_name_bbox[2] - course_name_bbox[0]
            draw.text(((width - course_name_width) // 2, 360), course_name, fill=self.certificate_templates['basic']['accent_color'], font=name_font)
            
            # Draw score if provided
            if score:
                score_text = f"with a final exam score of {score}%"
                score_bbox = draw.textbbox((0, 0), score_text, font=text_font)
                score_width = score_bbox[2] - score_bbox[0]
                draw.text(((width - score_width) // 2, 420), score_text, fill=self.certificate_templates['basic']['text_color'], font=text_font)
            
            # Draw date
            date_text = f"Completed on: {completion_date}"
            date_bbox = draw.textbbox((0, 0), date_text, font=small_font)
            date_width = date_bbox[2] - date_bbox[0]
            draw.text(((width - date_width) // 2, 480), date_text, fill=self.certificate_templates['basic']['text_color'], font=small_font)
            
            # *** MODIFIED: Draw signature line with Organization Name ***
            signature_text = organization_name
            signature_bbox = draw.textbbox((0, 0), signature_text, font=text_font)
            signature_width = signature_bbox[2] - signature_bbox[0]
            draw.text(((width - signature_width) // 2, 530), signature_text, fill=self.certificate_templates['basic']['accent_color'], font=text_font)
            
        except Exception as e:
            # Fallback simple text if anything fails
            draw.text((100, 50), f"{organization_name}", fill=(255, 255, 255))
            draw.text((100, 100), "CERTIFICATE OF COMPLETION", fill=(255, 215, 0))
            draw.text((100, 150), f"Awarded to: {student_name}", fill=(255, 255, 255))
            draw.text((100, 200), f"Course: {course_name}", fill=(255, 255, 255))
            draw.text((100, 250), f"Date: {completion_date}", fill=(255, 255, 255))
            if score:
                draw.text((100, 300), f"Score: {score}%", fill=(255, 255, 255))
            draw.text((100, 350), f"Issued by: {organization_name}", fill=(255, 215, 0))
        
        return image
    
    def get_certificate_download_link(self, image, filename="certificate.png"):
        """Generate a download link for the certificate"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:image/png;base64,{img_str}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; font-size: 16px; margin: 10px 0;">📄 Download Certificate</a>'
        return href

class FinanceLearningPlatform:
    def __init__(self):
        self.certificate_generator = CertificateGenerator()
        self.courses = {
            'budgeting_basics': {
                'title': '📊 Budgeting Basics',
                'description': 'Learn how to create and maintain a budget',
                'level': 'Beginner',
                'duration': '2 hours',
                'certificate_threshold': 70, # Score needed on FINAL EXAM
                'lessons': [
                    {
                        'id': 1,
                        'title': 'What is Budgeting?',
                        'content': """
                        # Understanding Budgeting

A budget is a plan for your money. It helps you:
- Track income and expenses
- Achieve financial goals
- Avoid debt
- Save for the future
                        """,
                        'video_id': '6X024dlVguA',
                        'video_title': 'Budgeting Basics for Beginners',
                        'duration': '8:30',
                        'quiz': {
                            'questions': [
                                {
                                    'question': 'What is the primary purpose of a budget?',
                                    'options': ['To restrict spending', 'To plan and track income/expenses', 'To get rich quick', 'To impress friends'],
                                    'correct': 1
                                },
                                {
                                    'question': 'What percentage of income should go to needs in the 50/30/20 rule?',
                                    'options': ['30%', '50%', '20%', '40%'],
                                    'correct': 1
                                }
                            ]
                        }
                    },
                    {
                        'id': 2,
                        'title': 'Creating Your First Budget',
                        'content': """
                        # Creating Your First Budget
        
## Step-by-Step Guide:
        
1. **Calculate Monthly Income**
   - List all income sources
   - Use net income (after taxes)
2. **List Monthly Expenses**
   - Fixed (rent, car payment)
   - Variable (groceries, gas)
3. **Subtract Expenses from Income**
   - Positive result = Good!
   - Negative result = Adjust expenses!
                        """,
                        'video_id': 'yY3IUVBiPx4',
                        'video_title': 'How to Create a Budget',
                        'duration': '10:15',
                        'quiz': {
                            'questions': [
                                {
                                    'question': 'What should you use for budgeting calculations?',
                                    'options': [
                                        'Gross income',
                                        'Net income',
                                        'Yearly income',
                                        'Expected income'
                                    ],
                                    'correct': 1
                                }
                            ]
                        }
                    }
                ],
                # *** NEW: Final Exam for the whole course ***
                'final_quiz': {
                    'title': 'Budgeting Basics Final Exam',
                    'questions': [
                        {
                            'question': 'What is a "zero-based" budget?',
                            'options': ['A budget with no income', 'A budget where Income - Expenses = 0', 'A budget for people with zero debt', 'A budget with zero savings'],
                            'correct': 1
                        },
                        {
                            'question': 'Which of these is a "variable" expense?',
                            'options': ['Rent', 'Car Insurance', 'Groceries', 'Loan Payment'],
                            'correct': 2
                        },
                        {
                            'question': 'The 50/30/20 rule allocates 20% to...',
                            'options': ['Needs', 'Wants', 'Savings & Debt Repayment', 'Taxes'],
                            'correct': 2
                        }
                    ]
                }
            },
            'saving_investing': {
                'title': '💸 Saving & Investing',
                'description': 'Build wealth through smart saving and investing strategies',
                'level': 'Intermediate',
                'duration': '3 hours',
                'certificate_threshold': 75,
                'lessons': [
                    {
                        'id': 1,
                        'title': 'The Power of Compound Interest',
                        'content': """
                        # Compound Interest: Your Best Friend
        
## What is Compound Interest?
Interest earned on both your initial investment AND accumulated interest.
                        """,
                        'video_id': 'wf91rEGs88Y',
                        'video_title': 'The Power of Compound Interest',
                        'duration': '9:20',
                        'quiz': {
                            'questions': [
                                {
                                    'question': 'What makes compound interest powerful?',
                                    'options': [
                                        'Earning interest on interest',
                                        'High risk investments',
                                        'Government guarantees',
                                        'Daily trading'
                                    ],
                                    'correct': 0
                                }
                            ]
                        }
                    },
                    {
                        'id': 2,
                        'title': 'Stocks vs. Bonds',
                        'content': """
                        # Stocks vs. Bonds: The Basics

* **Stocks (Equities):** You own a small piece (share) of a company. Higher potential returns, higher risk.
* **Bonds (Debt):** You are lending money to a company or government. Lower returns, lower risk.
                        """,
                        'video_id': 'rs1md3e4a-4',
                        'video_title': 'Stocks vs Bonds Explained',
                        'duration': '7:45',
                        'quiz': {
                            'questions': [
                                {
                                    'question': 'If you buy a stock, you own:',
                                    'options': ['A loan', 'A piece of the company', 'A guaranteed return', 'A bond'],
                                    'correct': 1
                                }
                            ]
                        }
                    }
                ],
                # *** NEW: Final Exam for the whole course ***
                'final_quiz': {
                    'title': 'Saving & Investing Final Exam',
                    'questions': [
                        {
                            'question': 'What is "diversification" in investing?',
                            'options': ['Putting all money in one stock', 'Spreading investments across different assets', 'Only buying bonds', 'Only buying stocks'],
                            'correct': 1
                        },
                        {
                            'question': 'Generally, which is considered higher risk?',
                            'options': ['Stocks', 'Bonds', 'A savings account', 'All are equal'],
                            'correct': 0
                        },
                        {
                            'question': 'Compound interest works best over a...?',
                            'options': ['Short period', 'Long period', 'It does not depend on time', 'Period of high risk'],
                            'correct': 1
                        }
                    ]
                }
            }
        }
        
        self.achievements = {
            'first_lesson': {'name': 'First Step', 'description': 'Complete your first lesson'},
            'quiz_champ': {'name': 'Quiz Champion', 'description': 'Score 100% on any quiz'},
            'certificate_earner': {'name': 'Certified Learner', 'description': 'Earn your first certificate'}
        }

    def calculate_progress(self, completed_lessons):
        """Calculate overall progress percentage"""
        total_lessons = sum(len(course['lessons']) for course in self.courses.values())
        return (len(completed_lessons) / total_lessons) * 100 if total_lessons > 0 else 0

    def is_lesson_completed(self, course_id, lesson_id, user_progress):
        """Check if a specific lesson is completed"""
        return any(lesson['course'] == course_id and lesson['id'] == lesson_id 
                   for lesson in user_progress['completed_lessons'])

    def mark_lesson_completed(self, course_id, lesson_id, user_progress):
        """Mark a lesson as completed"""
        if not self.is_lesson_completed(course_id, lesson_id, user_progress):
            user_progress['completed_lessons'].append({
                'course': course_id, 
                'id': lesson_id,
                'completed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return True
        return False

    def calculate_course_score(self, course_id, user_progress):
        """Calculate average *lesson quiz* score for a course"""
        quiz_scores = []
        for lesson in self.courses[course_id]['lessons']:
            quiz_key = f"{course_id}_{lesson['id']}"
            if quiz_key in user_progress['quiz_scores']:
                quiz_scores.append(user_progress['quiz_scores'][quiz_key])
        
        return sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0

    def is_course_completed(self, course_id, user_progress):
        """Check if all lessons in course are completed"""
        course_lessons = [lesson['id'] for lesson in self.courses[course_id]['lessons']]
        completed_lessons = [lesson['id'] for lesson in user_progress['completed_lessons'] if lesson['course'] == course_id]
        return len(completed_lessons) == len(course_lessons)

    # *** MODIFIED: Award certificate based on FINAL EXAM score ***
    def award_certificate(self, course_id, user_progress, student_name, final_score):
        """Award certificate for course completion"""
        course = self.courses[course_id]
        
        if final_score >= course['certificate_threshold']:
            certificate_data = {
                'course_id': course_id,
                'course_name': course['title'],
                'student_name': student_name,
                'completion_date': datetime.now().strftime("%B %d, %Y"),
                'score': round(final_score, 1),
                'certificate_id': f"FM-{course_id.upper()}-{datetime.now().strftime('%Y%m%d')}",
                'awarded_at': datetime.now().isoformat()
            }
            
            # Initialize certificates list if it doesn't exist
            if 'certificates' not in user_progress:
                user_progress['certificates'] = []
            
            # Check if certificate already exists
            existing_cert = next((c for c in user_progress['certificates'] if c['course_id'] == course_id), None)
            if not existing_cert:
                user_progress['certificates'].append(certificate_data)
                
                # Award certificate achievement
                if 'Certified Learner' not in user_progress['achievements']:
                    user_progress['achievements'].append('Certified Learner')
                
                return certificate_data
        return None

def display_video_lesson(video_id, video_title):
    """Display YouTube video in a responsive container"""
    st.markdown(f"""
    <div class="video-container">
        <iframe src="https://www.youtube.com/embed/{video_id}" 
                title="{video_title}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all required session state variables"""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'completed_lessons': [],  # Tracks completed lessons
            'quiz_scores': {},        # Tracks *lesson* quiz scores
            'final_quiz_scores': {},  # *** NEW: Tracks *final exam* scores ***
            'achievements': [],
            'certificates': [],
            'current_course': None,
            'current_lesson': 0,
            'watched_videos': [],     # *** NEW: Tracks watched videos ***
            'student_name': 'Finance Learner',
            'student_name_set': False
        }

def main():
    # *** MODIFIED: Added Organization Name to Title ***
    st.markdown('<h1 class="main-header">💰 FinanceMaster by OPENFRAUDLABS</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Personal Finance Education Platform</h3>', unsafe_allow_html=True)
    
    # Initialize platform and session state
    platform = FinanceLearningPlatform()
    initialize_session_state()
    
    # Student name input
    if not st.session_state.user_progress['student_name_set']:
        st.info("👋 Welcome! Please set up your profile to get started.")
        col1, col2 = st.columns([2, 1])
        with col1:
            student_name = st.text_input(
                "Enter your name for certificates:",
                placeholder="Enter your full name",
                key="name_input"
            )
        with col2:
            st.write("") 
            st.write("") 
            if st.button("Save Name", type="primary"):
                if student_name and student_name.strip():
                    st.session_state.user_progress['student_name'] = student_name.strip()
                    st.session_state.user_progress['student_name_set'] = True
                    st.success(f"Welcome, {student_name.strip()}! 🎉")
                    st.rerun()
                else:
                    st.error("Please enter your name")
        st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎓 Your Learning Dashboard")
        
        # Progress
        progress = platform.calculate_progress(st.session_state.user_progress['completed_lessons'])
        st.subheader(f"Overall Progress: {progress:.1f}%")
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Completed lessons and certificates
        st.write(f"**Lessons Completed:** {len(st.session_state.user_progress['completed_lessons'])}")
        st.write(f"**Certificates Earned:** {len(st.session_state.user_progress.get('certificates', []))}")
        
        # Student info
        if st.session_state.user_progress['student_name_set']:
            st.write(f"**Student:** {st.session_state.user_progress['student_name']}")
        
        # Achievements
        if st.session_state.user_progress['achievements']:
            st.subheader("🏆 Achievements")
            for achievement in st.session_state.user_progress['achievements']:
                st.markdown(f'<div class="achievement-badge">{achievement}</div>', unsafe_allow_html=True)

    # Main content area
    if not st.session_state.user_progress['student_name_set']:
        # Show only basic info until name is set
        st.info("🔐 Please set your name above to unlock all features")
        
        # Show course preview without interaction
        st.subheader("Available Courses")
        for course_id, course in platform.courses.items():
            with st.expander(f"{course['title']} - {course['level']}"):
                st.write(course['description'])
                st.write(f"📚 {len(course['lessons'])} lessons • ⏱️ {course['duration']}")
        
    else:
        # Full app experience when name is set
        # *** MODIFIED: Changed last tab name ***
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "📚 Courses", "🎯 Study", "📊 Progress", "🎓 Exams & Certificates"])

        with tab1:
            st.header(f"Welcome, {st.session_state.user_progress['student_name']}! 👋")
            st.markdown("""
            ### Your Journey to Financial Freedom Starts Here
            
            **Why Learn Personal Finance?**
            - 💰 Take control of your money
            - 🏠 Achieve your dream lifestyle
            - 📈 Build wealth over time
            - 🛡️ Protect yourself from financial emergencies
            """)
            
            # Quick stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Courses Available", len(platform.courses))
            with col2:
                st.metric("Your Progress", f"{progress:.1f}%")
            with col3:
                st.metric("Certificates", len(st.session_state.user_progress.get('certificates', [])))

        with tab2:
            st.header("📚 All Courses")
            for course_id, course in platform.courses.items():
                with st.expander(f"{course['title']} - {course['level']} - {course['duration']}", expanded=True):
                    st.write(course['description'])
                    st.write(f"**Certificate Requirement:** Pass a final exam with {course['certificate_threshold']}% or higher.")
                    
                    # Lessons list
                    for i, lesson in enumerate(course['lessons']):
                        is_completed = platform.is_lesson_completed(course_id, lesson['id'], st.session_state.user_progress)
                        status = "✅" if is_completed else "📖"
                        if st.button(f"{status} {lesson['title']} - {lesson['duration']}", 
                                     key=f"study_{course_id}_{i}",
                                     use_container_width=True):
                            st.session_state.user_progress['current_course'] = course_id
                            st.session_state.user_progress['current_lesson'] = i
                            # Switch to study tab (This is an improvement, but st.tabs doesn't support programmatic switching. st.rerun() is the best we can do)
                            st.rerun()

        with tab3:
            if st.session_state.user_progress['current_course']:
                course_id = st.session_state.user_progress['current_course']
                lesson_index = st.session_state.user_progress['current_lesson']
                course = platform.courses[course_id]
                lesson = course['lessons'][lesson_index]
                
                st.header(f"{course['title']}")
                st.subheader(f"Lesson: {lesson['title']}")
                
                # Progress
                completed_in_course = len([l for l in st.session_state.user_progress['completed_lessons'] if l['course'] == course_id])
                total_in_course = len(course['lessons'])
                course_progress = (completed_in_course / total_in_course) * 100
                
                st.markdown(f"""
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {course_progress}%"></div>
                </div>
                <p>Course Progress: {completed_in_course}/{total_in_course} lessons ({course_progress:.1f}%)</p>
                """, unsafe_allow_html=True)
                
                # Video lesson
                st.subheader("🎥 Video Lesson")
                display_video_lesson(lesson['video_id'], lesson['video_title'])
                
                # *** NEW: Video watch tracking logic ***
                video_watched_key = f"{course_id}_{lesson['id']}"
                is_video_watched = video_watched_key in st.session_state.user_progress['watched_videos']
                
                if not is_video_watched:
                    if st.button("Mark Video as Watched", type="primary"):
                        st.session_state.user_progress['watched_videos'].append(video_watched_key)
                        st.rerun()
                
                # Lesson content
                st.subheader("📖 Lesson Content")
                st.markdown(lesson['content'])
                
                # Quiz
                st.subheader("🧠 Knowledge Check")
                
                # *** NEW: Quiz is locked until video is watched ***
                if is_video_watched:
                    with st.container():
                        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
                        
                        user_answers = []
                        quiz_key = f"{course_id}_{lesson['id']}"
                        
                        # Check if quiz was already passed
                        if quiz_key in st.session_state.user_progress['quiz_scores'] and st.session_state.user_progress['quiz_scores'][quiz_key] >= 50:
                             st.info(f"You have already passed this quiz with a score of {st.session_state.user_progress['quiz_scores'][quiz_key]:.1f}%.")
                        
                        for i, q in enumerate(lesson['quiz']['questions']):
                            st.write(f"**Q{i+1}: {q['question']}**")
                            answer = st.radio(f"Select your answer:", q['options'], key=f"quiz_{quiz_key}_{i}")
                            user_answers.append((q['options'].index(answer), q['correct']))
                        
                        if st.button("Submit Quiz", type="primary"):
                            correct_answers = sum(1 for user_ans, correct_ans in user_answers if user_ans == correct_ans)
                            total_questions = len(lesson['quiz']['questions'])
                            quiz_score = (correct_answers / total_questions) * 100
                            
                            # Store the score regardless
                            st.session_state.user_progress['quiz_scores'][quiz_key] = quiz_score
                            
                            if quiz_score >= 50:
                                if platform.mark_lesson_completed(course_id, lesson['id'], st.session_state.user_progress):
                                    st.success(f"🎉 Lesson completed! Score: {quiz_score:.1f}%")
                                    
                                    # *** NEW: Check for course completion and guide user ***
                                    if platform.is_course_completed(course_id, st.session_state.user_progress):
                                        st.balloons()
                                        st.success(f"🎓 Awesome! You've completed all lessons for {course['title']}.")
                                        st.info("Head to the 'Exams & Certificates' tab to take your final exam!")
                                else:
                                    st.info(f"Score: {quiz_score:.1f}% - Lesson already completed")
                            else:
                                st.warning(f"Score: {quiz_score:.1f}% - Try again (need 50%+ to pass lesson)")
                            
                            st.rerun()
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("Mark the video as watched to unlock the quiz.")
                
                # Navigation
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if lesson_index > 0 and st.button("← Previous Lesson"):
                        st.session_state.user_progress['current_lesson'] = lesson_index - 1
                        st.rerun()
                with col2:
                    if st.button("🏠 Back to Courses"):
                        st.session_state.user_progress['current_course'] = None
                        st.rerun()
                with col3:
                    if lesson_index < len(course['lessons']) - 1 and st.button("Next Lesson →"):
                        st.session_state.user_progress['current_lesson'] = lesson_index + 1
                        st.rerun()
            else:
                st.info("Select a lesson from the Courses tab to start studying!")
                # Replaced placeholder with a more relevant image query
                st.markdown("", unsafe_allow_html=True)


        with tab4:
            st.header("📊 Your Learning Progress")
            
            if not st.session_state.user_progress['completed_lessons']:
                st.info("Start learning to see your progress here!")
            else:
                # Progress metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Lessons Completed", len(st.session_state.user_progress['completed_lessons']))
                with col2:
                    courses_started = len(set([l['course'] for l in st.session_state.user_progress['completed_lessons']]))
                    st.metric("Courses Started", courses_started)
                with col3:
                    avg_score = np.mean(list(st.session_state.user_progress['quiz_scores'].values())) if st.session_state.user_progress['quiz_scores'] else 0
                    st.metric("Avg. Lesson Quiz Score", f"{avg_score:.1f}%")
                
                # Course progress
                st.subheader("Course Progress")
                for course_id, course in platform.courses.items():
                    completed = len([l for l in st.session_state.user_progress['completed_lessons'] if l['course'] == course_id])
                    total = len(course['lessons'])
                    progress_pct = (completed / total) * 100
                    
                    st.write(f"**{course['title']}**")
                    st.markdown(f"""
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {progress_pct}%"></div>
                    </div>
                    <p>{completed}/{total} lessons ({progress_pct:.1f}%)</p>
                    """, unsafe_allow_html=True)

        # *** NEW: Rebuilt Tab 5 for Exams & Certificates ***
        with tab5:
            st.header("🎓 Exams & Certificates")
            
            certificates = st.session_state.user_progress.get('certificates', [])
            
            if not platform.courses:
                st.info("No courses are available yet.")
                
            for course_id, course in platform.courses.items():
                st.markdown("---")
                st.subheader(f"{course['title']}")
                
                all_lessons_done = platform.is_course_completed(course_id, st.session_state.user_progress)
                final_quiz_key = f"final_{course_id}"
                final_score = st.session_state.user_progress['final_quiz_scores'].get(final_quiz_key)
                cert = next((c for c in certificates if c['course_id'] == course_id), None)

                if cert:
                    # User has certificate, display it
                    st.success(f"Congratulations! You earned a certificate for this course on {cert['completion_date']}.")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        # Display the HTML preview
                        st.markdown(f"""
                        <div class="certificate-container">
                            <div style="font-size: 1.5rem; font-weight: bold; color: white; margin-bottom: 1rem;">OPENFRAUDLABS</div>
                            <div style="font-size: 2.5rem; font-weight: bold; color: #FFD700; margin-bottom: 1rem;">CERTIFICATE OF COMPLETION</div>
                            <div style="font-size: 1.2rem; margin-bottom: 1rem;">This certifies that</div>
                            <div style="font-size: 2rem; font-weight: bold; color: #FFD700; margin: 1rem 0; text-decoration: underline;">{cert['student_name']}</div>
                            <div style="font-size: 1.2rem; margin-bottom: 1rem;">has successfully completed</div>
                            <div style="font-size: 1.8rem; font-weight: bold; color: white; margin: 1rem 0;">{cert['course_name']}</div>
                            <div style="font-size: 1.2rem; margin-bottom: 1rem;">with a final exam score of {cert['score']}%</div>
                            <div style="font-size: 1rem; margin: 1rem 0;">Completed on: {cert['completion_date']}</div>
                            <div style="font-size: 0.9rem; margin-top: 2rem;">Certificate ID: {cert['certificate_id']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Generate and offer download
                        cert_image = platform.certificate_generator.generate_certificate_image(
                            cert['student_name'],
                            cert['course_name'],
                            cert['completion_date'],
                            cert['score'],
                            organization_name="OPENFRAUDLABS"
                        )
                        st.image(cert_image, use_column_width=True, caption="Your Official Certificate")
                        download_filename = f"Certificate_{cert['course_name'].replace(' ', '_')}.png"
                        st.markdown(
                            platform.certificate_generator.get_certificate_download_link(cert_image, download_filename),
                            unsafe_allow_html=True
                        )

                elif all_lessons_done:
                    # All lessons done, but no cert yet. Show Final Exam.
                    st.info("You've completed all lessons! Pass the final exam to earn your certificate.")
                    
                    with st.container():
                        st.markdown('<div class="exam-card">', unsafe_allow_html=True)
                        st.subheader(f"Final Exam: {course['title']}")
                        
                        final_quiz_data = course['final_quiz']
                        
                        with st.form(f"final_quiz_form_{course_id}"):
                            final_user_answers = []
                            for i, q in enumerate(final_quiz_data['questions']):
                                st.write(f"**Q{i+1}: {q['question']}**")
                                answer = st.radio(f"Select your answer:", q['options'], key=f"final_quiz_{course_id}_{i}")
                                final_user_answers.append((q['options'].index(answer), q['correct']))
                            
                            submitted = st.form_submit_button("Submit Final Exam", type="primary")
                        
                            if submitted:
                                correct_answers = sum(1 for user_ans, correct_ans in final_user_answers if user_ans == correct_ans)
                                total_questions = len(final_quiz_data['questions'])
                                score = (correct_answers / total_questions) * 100
                                
                                st.session_state.user_progress['final_quiz_scores'][final_quiz_key] = score
                                
                                if score >= course['certificate_threshold']:
                                    st.balloons()
                                    st.success(f"🎉 You passed! Final Score: {score:.1f}%")
                                    # Award the certificate
                                    platform.award_certificate(
                                        course_id, 
                                        st.session_state.user_progress, 
                                        st.session_state.user_progress['student_name'], 
                                        score
                                    )
                                else:
                                    st.error(f"Your score was {score:.1f}%. You need {course['certificate_threshold']}% to pass. Please review the material and try again.")
                                
                                st.rerun()
                                
                        st.markdown('</div>', unsafe_allow_html=True)
                
                else:
                    # Lessons are not yet complete
                    st.warning(f"Complete all {len(course['lessons'])} lessons in this course to unlock the final exam.")
                    
                    # Show progress
                    completed = len([l for l in st.session_state.user_progress['completed_lessons'] if l['course'] == course_id])
                    total = len(course['lessons'])
                    progress_pct = (completed / total) * 100
                    st.progress(progress_pct / 100, text=f"{completed}/{total} lessons completed")


if __name__ == "__main__":
    main()
