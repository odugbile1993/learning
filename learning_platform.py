import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
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
</style>
""", unsafe_allow_html=True)

class FinanceLearningPlatform:
    def __init__(self):
        self.courses = {
            'budgeting_basics': {
                'title': '📊 Budgeting Basics',
                'description': 'Learn how to create and maintain a budget',
                'level': 'Beginner',
                'duration': '2 hours',
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
        
        ## Key Concepts:
        - **Income**: Money coming in (salary, business, etc.)
        - **Expenses**: Money going out (rent, food, transport)
        - **Savings**: Money set aside for future use
        - **Emergency Fund**: 3-6 months of expenses saved
        
        ## The 50/30/20 Rule:
        - **50%** for Needs (rent, food, utilities)
        - **30%** for Wants (entertainment, dining out)
        - **20%** for Savings and Debt Repayment
                        """,
                        'video_url': 'https://www.youtube.com/embed/demo_budgeting',
                        'quiz': {
                            'questions': [
                                {
                                    'question': 'What percentage of income should go to needs in the 50/30/20 rule?',
                                    'options': ['30%', '50%', '20%', '40%'],
                                    'correct': 1
                                },
                                {
                                    'question': 'Why is an emergency fund important?',
                                    'options': [
                                        'For vacation planning',
                                        'To cover unexpected expenses',
                                        'For daily shopping',
                                        'To pay for luxury items'
                                    ],
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
        
        2. **Track Expenses**
           - Fixed expenses (rent, loan payments)
           - Variable expenses (food, entertainment)
           - Periodic expenses (insurance, maintenance)
        
        3. **Set Financial Goals**
           - Short-term (1-3 months)
           - Medium-term (3-12 months)
           - Long-term (1+ years)
        
        4. **Monitor and Adjust**
           - Review weekly
           - Adjust categories as needed
                        """,
                        'video_url': 'https://www.youtube.com/embed/demo_budget_creation',
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
                'lessons': [
                    {
                        'id': 1,
                        'title': 'The Power of Compound Interest',
                        'content': """
                        # Compound Interest: Your Best Friend
        
        ## What is Compound Interest?
        Interest earned on both your initial investment AND accumulated interest.
        
        ## The Formula:
        **A = P(1 + r/n)^(nt)**
        - A = Final amount
        - P = Principal amount
        - r = Annual interest rate
        - n = Number of times interest compounds per year
        - t = Number of years
        
        ## Example:
        - Invest $1,000 at 8% annual return
        - After 30 years: $10,062
        - Your money grows 10x!
                        """,
                        'video_url': 'https://www.youtube.com/embed/demo_compound',
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
            },
            'debt_management': {
                'title': '📉 Debt Management',
                'description': 'Strategies to manage and eliminate debt',
                'level': 'Intermediate',
                'duration': '2.5 hours',
                'lessons': [
                    {
                        'id': 1,
                        'title': 'Understanding Different Types of Debt',
                        'content': """
                        # Types of Debt
        
        ## Good Debt vs Bad Debt
        
        **Good Debt:**
        - Student loans (education investment)
        - Mortgages (home ownership)
        - Business loans (income generation)
        
        **Bad Debt:**
        - Credit card debt (high interest)
        - Payday loans (extremely high interest)
        - Car loans (depreciating asset)
        
        ## Interest Rates Matter:
        - Credit cards: 15-25% APR
        - Personal loans: 6-15% APR
        - Mortgages: 3-6% APR
                        """,
                        'video_url': 'https://www.youtube.com/embed/demo_debt',
                        'quiz': {
                            'questions': [
                                {
                                    'question': 'Which is generally considered "good debt"?',
                                    'options': [
                                        'Credit card debt',
                                        'Payday loans',
                                        'Student loans',
                                        'Personal loans for vacation'
                                    ],
                                    'correct': 2
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
            'consistent_learner': {'name': 'Consistent Learner', 'description': 'Complete 5 lessons'}
        }

    def calculate_progress(self, completed_lessons):
        total_lessons = sum(len(course['lessons']) for course in self.courses.values())
        return (len(completed_lessons) / total_lessons) * 100 if total_lessons > 0 else 0

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
            'current_course': None,
            'current_lesson': 0
        }
    
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
        
        # Completed lessons
        st.write(f"**Lessons Completed:** {len(st.session_state.user_progress['completed_lessons'])}")
        
        # Achievements
        st.subheader("🏆 Achievements")
        for achievement in st.session_state.user_progress['achievements']:
            st.markdown(f'<div class="achievement-badge">{achievement}</div>', unsafe_allow_html=True)
        
        # Quick navigation
        st.subheader("📚 Quick Access")
        for course_id, course in platform.courses.items():
            if st.button(f"📖 {course['title']}"):
                st.session_state.user_progress['current_course'] = course_id
                st.session_state.user_progress['current_lesson'] = 0
                st.rerun()

    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📚 Courses", "🎯 Learning Path", "📊 Progress"])

    with tab1:
        st.header("Welcome to FinanceMaster!")
        st.markdown("""
        ### Your Journey to Financial Freedom Starts Here
        
        FinanceMaster is your personal guide to mastering money management. 
        Whether you're just starting out or looking to enhance your financial skills, 
        we have courses designed for every level.
        
        **Why Learn Personal Finance?**
        - 💰 Take control of your money
        - 🏠 Achieve your dream lifestyle
        - 📈 Build wealth over time
        - 🛡️ Protect yourself from financial emergencies
        - 🎯 Reach your life goals faster
        """)
        
        # Featured courses
        st.subheader("🎯 Featured Courses")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            course = platform.courses['budgeting_basics']
            st.markdown(f"""
            <div class="course-card">
                <h3>{course['title']}</h3>
                <p>{course['description']}</p>
                <p><strong>Level:</strong> {course['level']}</p>
                <p><strong>Duration:</strong> {course['duration']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start Learning →", key="budget_start"):
                st.session_state.user_progress['current_course'] = 'budgeting_basics'
                st.session_state.user_progress['current_lesson'] = 0
                st.rerun()
        
        with col2:
            course = platform.courses['saving_investing']
            st.markdown(f"""
            <div class="course-card">
                <h3>{course['title']}</h3>
                <p>{course['description']}</p>
                <p><strong>Level:</strong> {course['level']}</p>
                <p><strong>Duration:</strong> {course['duration']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start Learning →", key="saving_start"):
                st.session_state.user_progress['current_course'] = 'saving_investing'
                st.session_state.user_progress['current_lesson'] = 0
                st.rerun()
        
        with col3:
            course = platform.courses['debt_management']
            st.markdown(f"""
            <div class="course-card">
                <h3>{course['title']}</h3>
                <p>{course['description']}</p>
                <p><strong>Level:</strong> {course['level']}</p>
                <p><strong>Duration:</strong> {course['duration']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start Learning →", key="debt_start"):
                st.session_state.user_progress['current_course'] = 'debt_management'
                st.session_state.user_progress['current_lesson'] = 0
                st.rerun()

    with tab2:
        st.header("📚 All Courses")
        
        for course_id, course in platform.courses.items():
            with st.expander(f"{course['title']} - {course['level']} - {course['duration']}", expanded=True):
                st.write(course['description'])
                
                # Lessons in this course
                st.subheader("Lessons in this Course:")
                for i, lesson in enumerate(course['lessons']):
                    lesson_completed = lesson['id'] in [l['id'] for l in st.session_state.user_progress['completed_lessons'] if l['course'] == course_id]
                    status = "✅" if lesson_completed else "📖"
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{status} {lesson['title']}**")
                    with col2:
                        if st.button("Study", key=f"study_{course_id}_{i}"):
                            st.session_state.user_progress['current_course'] = course_id
                            st.session_state.user_progress['current_lesson'] = i
                            st.rerun()

    with tab3:
        # Learning interface
        if st.session_state.user_progress['current_course']:
            course_id = st.session_state.user_progress['current_course']
            lesson_index = st.session_state.user_progress['current_lesson']
            course = platform.courses[course_id]
            lesson = course['lessons'][lesson_index]
            
            st.header(f"{course['title']} - {lesson['title']}")
            
            # Progress within course
            course_progress = (lesson_index + 1) / len(course['lessons']) * 100
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {course_progress}%"></div>
            </div>
            <p>Progress in this course: {course_progress:.1f}%</p>
            """, unsafe_allow_html=True)
            
            # Lesson content
            st.markdown(lesson['content'])
            
            # Video placeholder
            st.subheader("📺 Video Lesson")
            st.video(lesson['video_url'])
            
            # Quiz section
            st.subheader("🧠 Knowledge Check")
            with st.container():
                st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
                
                quiz_score = 0
                user_answers = []
                
                for i, q in enumerate(lesson['quiz']['questions']):
                    st.write(f"**Q{i+1}: {q['question']}**")
                    answer = st.radio(f"Select your answer:", q['options'], key=f"quiz_{course_id}_{lesson_index}_{i}")
                    user_answers.append((q['options'].index(answer), q['correct']))
                
                if st.button("Submit Quiz", type="primary"):
                    correct_answers = sum(1 for user_ans, correct_ans in user_answers if user_ans == correct_ans)
                    total_questions = len(lesson['quiz']['questions'])
                    quiz_score = (correct_answers / total_questions) * 100
                    
                    st.success(f"🎉 You scored {quiz_score:.1f}%!")
                    
                    # Update progress
                    lesson_key = f"{course_id}_{lesson['id']}"
                    if lesson_key not in st.session_state.user_progress['quiz_scores']:
                        st.session_state.user_progress['quiz_scores'][lesson_key] = quiz_score
                    
                    # Mark lesson as completed
                    completed_lesson = {'course': course_id, 'id': lesson['id']}
                    if completed_lesson not in st.session_state.user_progress['completed_lessons']:
                        st.session_state.user_progress['completed_lessons'].append(completed_lesson)
                    
                    # Award achievements
                    if len(st.session_state.user_progress['completed_lessons']) == 1:
                        st.session_state.user_progress['achievements'].append('First Step')
                    if quiz_score == 100:
                        st.session_state.user_progress['achievements'].append('Quiz Champion')
                    
                    st.balloons()
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if lesson_index > 0:
                    if st.button("← Previous Lesson"):
                        st.session_state.user_progress['current_lesson'] = lesson_index - 1
                        st.rerun()
            with col2:
                if st.button("🏠 Back to Courses"):
                    st.session_state.user_progress['current_course'] = None
                    st.rerun()
            with col3:
                if lesson_index < len(course['lessons']) - 1:
                    if st.button("Next Lesson →"):
                        st.session_state.user_progress['current_lesson'] = lesson_index + 1
                        st.rerun()
                else:
                    if st.button("🎓 Complete Course"):
                        st.session_state.user_progress['achievements'].append('Budget Master')
                        st.success("Congratulations! You've completed this course!")
        else:
            st.info("Select a course from the sidebar or home page to start learning!")

    with tab4:
        st.header("📊 Your Learning Progress")
        
        # Progress metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Courses Started", len(set([l['course'] for l in st.session_state.user_progress['completed_lessons']])))
        with col2:
            st.metric("Lessons Completed", len(st.session_state.user_progress['completed_lessons']))
        with col3:
            avg_quiz_score = np.mean(list(st.session_state.user_progress['quiz_scores'].values())) if st.session_state.user_progress['quiz_scores'] else 0
            st.metric("Average Quiz Score", f"{avg_quiz_score:.1f}%")
        
        # Course completion progress
        st.subheader("Course Completion")
        for course_id, course in platform.courses.items():
            completed_in_course = len([l for l in st.session_state.user_progress['completed_lessons'] if l['course'] == course_id])
            total_in_course = len(course['lessons'])
            progress = (completed_in_course / total_in_course) * 100
            
            st.write(f"**{course['title']}**")
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
            <p>{completed_in_course}/{total_in_course} lessons completed ({progress:.1f}%)</p>
            """, unsafe_allow_html=True)
        
        # Learning statistics
        st.subheader("📈 Learning Statistics")
        if st.session_state.user_progress['completed_lessons']:
            # Create a simple learning timeline
            timeline_data = []
            for i, lesson in enumerate(st.session_state.user_progress['completed_lessons']):
                timeline_data.append({
                    'Lesson': f"Lesson {i+1}",
                    'Course': lesson['course'].replace('_', ' ').title(),
                    'Progress': (i + 1) / len(st.session_state.user_progress['completed_lessons']) * 100
                })
            
            df = pd.DataFrame(timeline_data)
            fig = px.line(df, x='Lesson', y='Progress', title='Your Learning Journey')
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
