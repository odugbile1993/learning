import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Page configuration
st.set_page_config(
    page_title="FinanceMaster - Personal Finance Learning",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
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
    .certificate-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .certificate-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        color: #FFF;
    }
    .certificate-name {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1rem 0;
        color: #FFD700;
        text-decoration: underline;
    }
    .certificate-course {
        font-size: 2rem;
        margin: 1rem 0;
        color: #FFF;
    }
    .certificate-date {
        font-size: 1.2rem;
        margin: 1rem 0;
        color: #FFF;
    }
</style>
""", unsafe_allow_html=True)

class CertificateGenerator:
    def __init__(self):
        self.certificate_templates = {
            'basic': {
                'background_color': (139, 69, 19),  # SaddleBrown
                'border_color': (255, 215, 0),      # Gold
                'text_color': (255, 255, 255),      # White
                'accent_color': (255, 215, 0)       # Gold
            },
            'premium': {
                'background_color': (25, 25, 112),  # MidnightBlue
                'border_color': (255, 215, 0),      # Gold
                'text_color': (255, 255, 255),      # White
                'accent_color': (255, 215, 0)       # Gold
            }
        }
    
    def generate_certificate_image(self, student_name, course_name, completion_date, score=None):
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
            except:
                title_font = ImageFont.load_default()
                name_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Draw border
            draw.rectangle([10, 10, width-10, height-10], outline=self.certificate_templates['basic']['border_color'], width=8)
            
            # Draw title
            title = "CERTIFICATE OF COMPLETION"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((width - title_width) // 2, 80), title, fill=self.certificate_templates['basic']['accent_color'], font=title_font)
            
            # Draw subtitle
            subtitle = "This certifies that"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=text_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            draw.text(((width - subtitle_width) // 2, 160), subtitle, fill=self.certificate_templates['basic']['text_color'], font=text_font)
            
            # Draw student name
            name_bbox = draw.textbbox((0, 0), student_name, font=name_font)
            name_width = name_bbox[2] - name_bbox[0]
            draw.text(((width - name_width) // 2, 220), student_name, fill=self.certificate_templates['basic']['accent_color'], font=name_font)
            
            # Draw course completion text
            course_text = f"has successfully completed the course"
            course_bbox = draw.textbbox((0, 0), course_text, font=text_font)
            course_width = course_bbox[2] - course_bbox[0]
            draw.text(((width - course_width) // 2, 290), course_text, fill=self.certificate_templates['basic']['text_color'], font=text_font)
            
            # Draw course name
            course_name_bbox = draw.textbbox((0, 0), course_name, font=name_font)
            course_name_width = course_name_bbox[2] - course_name_bbox[0]
            draw.text(((width - course_name_width) // 2, 340), course_name, fill=self.certificate_templates['basic']['accent_color'], font=name_font)
            
            # Draw score if provided
            if score:
                score_text = f"with a final score of {score}%"
                score_bbox = draw.textbbox((0, 0), score_text, font=text_font)
                score_width = score_bbox[2] - score_bbox[0]
                draw.text(((width - score_width) // 2, 400), score_text, fill=self.certificate_templates['basic']['text_color'], font=text_font)
            
            # Draw date
            date_text = f"Completed on: {completion_date}"
            date_bbox = draw.textbbox((0, 0), date_text, font=small_font)
            date_width = date_bbox[2] - date_bbox[0]
            draw.text(((width - date_width) // 2, 480), date_text, fill=self.certificate_templates['basic']['text_color'], font=small_font)
            
            # Draw signature line
            signature_text = "FinanceMaster Academy"
            signature_bbox = draw.textbbox((0, 0), signature_text, font=text_font)
            signature_width = signature_bbox[2] - signature_bbox[0]
            draw.text(((width - signature_width) // 2, 520), signature_text, fill=self.certificate_templates['basic']['accent_color'], font=text_font)
            
        except Exception as e:
            # Fallback simple text if font loading fails
            draw.text((100, 100), "CERTIFICATE OF COMPLETION", fill=(255, 215, 0))
            draw.text((100, 150), f"Awarded to: {student_name}", fill=(255, 255, 255))
            draw.text((100, 200), f"Course: {course_name}", fill=(255, 255, 255))
            draw.text((100, 250), f"Date: {completion_date}", fill=(255, 255, 255))
            if score:
                draw.text((100, 300), f"Score: {score}%", fill=(255, 255, 255))
        
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
                'certificate_threshold': 70,  # Minimum score to get certificate
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
                ]
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
                    }
                ]
            }
        }
        
        self.achievements = {
            'first_lesson': {'name': 'First Step', 'description': 'Complete your first lesson'},
            'budget_master': {'name': 'Budget Master', 'description': 'Complete Budgeting Basics course'},
            'quiz_champ': {'name': 'Quiz Champion', 'description': 'Score 100% on any quiz'},
            'consistent_learner': {'name': 'Consistent Learner', 'description': 'Complete 5 lessons'},
            'video_watcher': {'name': 'Active Learner', 'description': 'Watch 3 video lessons'},
            'certificate_earner': {'name': 'Certified Learner', 'description': 'Earn your first certificate'}
        }

    def calculate_course_score(self, course_id, user_progress):
        """Calculate average score for a course"""
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

    def award_certificate(self, course_id, user_progress, student_name):
        """Award certificate for course completion"""
        course_score = self.calculate_course_score(course_id, user_progress)
        course = self.courses[course_id]
        
        if course_score >= course['certificate_threshold']:
            certificate_data = {
                'course_id': course_id,
                'course_name': course['title'],
                'student_name': student_name,
                'completion_date': datetime.now().strftime("%B %d, %Y"),
                'score': round(course_score, 1),
                'certificate_id': f"FM-{course_id.upper()}-{datetime.now().strftime('%Y%m%d')}",
                'awarded_at': datetime.now().isoformat()
            }
            
            # Add to certificates list
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

def main():
    st.markdown('<h1 class="main-header">💰 FinanceMaster</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Personal Finance Education Platform</h3>', unsafe_allow_html=True)
    
    # Initialize platform and session state
    platform = FinanceLearningPlatform()
    
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'completed_lessons': [],
            'quiz_scores': {},
            'achievements': [],
            'certificates': [],
            'current_course': None,
            'current_lesson': 0,
            'watched_videos': [],
            'student_name': 'Finance Learner'  # Default name
        }
    
    # Student name input
    if not st.session_state.user_progress.get('student_name_set', False):
        with st.sidebar:
            st.subheader("👤 Your Profile")
            student_name = st.text_input("Enter your name for certificates:", 
                                       value=st.session_state.user_progress['student_name'])
            if student_name and st.button("Save Name"):
                st.session_state.user_progress['student_name'] = student_name
                st.session_state.user_progress['student_name_set'] = True
                st.success("Name saved! You'll see this on your certificates.")
                st.rerun()

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
        
        # Achievements
        st.subheader("🏆 Achievements")
        for achievement in st.session_state.user_progress['achievements']:
            st.markdown(f'<div class="achievement-badge">{achievement}</div>', unsafe_allow_html=True)
        
        # Certificates quick view
        if st.session_state.user_progress.get('certificates'):
            st.subheader("📜 Certificates")
            for cert in st.session_state.user_progress['certificates'][:3]:  # Show latest 3
                st.markdown(f'<div class="certificate-badge">{cert["course_name"]}</div>', unsafe_allow_html=True)

    # Main content area
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "📚 Courses", "🎯 Study", "📊 Progress", "🏆 Certificates"])

    with tab5:  # New Certificates Tab
        st.header("🎓 Your Certificates")
        
        if not st.session_state.user_progress.get('certificates'):
            st.info("Complete courses with passing scores to earn certificates! 🎯")
            
            # Show certificate requirements
            st.subheader("Certificate Requirements:")
            for course_id, course in platform.courses.items():
                st.write(f"**{course['title']}**: Score {course['certificate_threshold']}% or higher on all quizzes")
        else:
            # Display earned certificates
            for certificate in st.session_state.user_progress['certificates']:
                st.markdown("---")
                
                # Certificate display
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="certificate-container">
                        <div class="certificate-title">CERTIFICATE OF COMPLETION</div>
                        <div class="certificate-subtitle">This certifies that</div>
                        <div class="certificate-name">{certificate['student_name']}</div>
                        <div class="certificate-subtitle">has successfully completed</div>
                        <div class="certificate-course">{certificate['course_name']}</div>
                        <div class="certificate-subtitle">with a score of {certificate['score']}%</div>
                        <div class="certificate-date">{certificate['completion_date']}</div>
                        <div class="certificate-subtitle">Certificate ID: {certificate['certificate_id']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.subheader("Download Certificate")
                    
                    # Generate and download certificate image
                    cert_image = platform.certificate_generator.generate_certificate_image(
                        certificate['student_name'],
                        certificate['course_name'],
                        certificate['completion_date'],
                        certificate['score']
                    )
                    
                    # Display certificate preview
                    st.image(cert_image, use_column_width=True)
                    
                    # Download link
                    download_filename = f"FinanceMaster_Certificate_{certificate['course_id']}_{certificate['completion_date'].replace(' ', '_')}.png"
                    st.markdown(
                        platform.certificate_generator.get_certificate_download_link(cert_image, download_filename),
                        unsafe_allow_html=True
                    )
                    
                    # Share options
                    st.write("**Share your achievement:**")
                    st.write("📱 Take a screenshot of your certificate")
                    st.write("💼 Add to your LinkedIn profile")
                    st.write("🎯 Share on social media")

            # Certificate statistics
            st.subheader("📈 Certificate Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Certificates", len(st.session_state.user_progress['certificates']))
            with col2:
                avg_score = sum(c['score'] for c in st.session_state.user_progress['certificates']) / len(st.session_state.user_progress['certificates'])
                st.metric("Average Score", f"{avg_score:.1f}%")
            with col3:
                completed_courses = len(set(c['course_id'] for c in st.session_state.user_progress['certificates']))
                st.metric("Courses Certified", completed_courses)

    # Modified Study Tab to include certificate awarding
    with tab3:
        if st.session_state.user_progress['current_course']:
            course_id = st.session_state.user_progress['current_course']
            lesson_index = st.session_state.user_progress['current_lesson']
            course = platform.courses[course_id]
            lesson = course['lessons'][lesson_index]
            
            # ... (previous study tab content remains the same)
            
            # Enhanced quiz submission to check for certificate eligibility
            if st.button("Submit Quiz", type="primary"):
                correct_answers = sum(1 for user_ans, correct_ans in user_answers if user_ans == correct_ans)
                total_questions = len(lesson['quiz']['questions'])
                quiz_score = (correct_answers / total_questions) * 100
                
                # Update quiz scores
                st.session_state.user_progress['quiz_scores'][quiz_key] = quiz_score
                
                # Mark lesson as completed if quiz passed
                if quiz_score >= 50:
                    if platform.mark_lesson_completed(course_id, lesson['id'], st.session_state.user_progress):
                        st.success(f"🎉 Lesson completed! Quiz score: {quiz_score:.1f}%")
                        
                        # Check if course is completed and award certificate
                        if platform.is_course_completed(course_id, st.session_state.user_progress):
                            certificate = platform.award_certificate(
                                course_id, 
                                st.session_state.user_progress,
                                st.session_state.user_progress['student_name']
                            )
                            if certificate:
                                st.balloons()
                                st.success(f"🎓 Congratulations! You've earned a certificate for {course['title']} with score {certificate['score']}%!")
                                st.info("🎉 Check the 'Certificates' tab to view and download your certificate!")
                    
                    st.rerun()

    # Modified Progress Tab to show certificate progress
    with tab4:
        st.header("📊 Your Learning Progress")
        
        if not st.session_state.user_progress['completed_lessons']:
            st.info("Start learning to see your progress here!")
        else:
            # Certificate progress section
            st.subheader("📜 Certificate Progress")
            for course_id, course in platform.courses.items():
                completed = platform.is_course_completed(course_id, st.session_state.user_progress)
                course_score = platform.calculate_course_score(course_id, st.session_state.user_progress)
                has_certificate = any(c['course_id'] == course_id for c in st.session_state.user_progress.get('certificates', []))
                
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"**{course['title']}**")
                with col2:
                    status = "✅ Certified" if has_certificate else "📖 In Progress" if completed else "⏳ Learning"
                    st.write(status)
                with col3:
                    st.write(f"Score: {course_score:.1f}%")
                with col4:
                    if completed and not has_certificate and course_score >= course['certificate_threshold']:
                        if st.button("🎓 Get Certificate", key=f"cert_{course_id}"):
                            certificate = platform.award_certificate(
                                course_id, 
                                st.session_state.user_progress,
                                st.session_state.user_progress['student_name']
                            )
                            if certificate:
                                st.success("Certificate awarded! Check the Certificates tab.")
                                st.rerun()

if __name__ == "__main__":
    main()
