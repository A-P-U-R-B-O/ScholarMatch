"""
ScholarMatch - AI-Powered Scholarship Matching Platform
Author: A-P-U-R-B-O
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Import custom modules
from utils.matcher import match_scholarships, get_scholarship_statistics, filter_scholarships
from utils.database import (
    load_scholarships, 
    save_user_profile, 
    get_categories, 
    search_scholarships,
    get_statistics,
    update_scholarship_deadlines
)

# Page configuration
st.set_page_config(
    page_title="ScholarMatch - AI Scholarship Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .scholarship-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .match-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .match-high {
        background: #10b981;
        color: white;
    }
    .match-medium {
        background: #f59e0b;
        color: white;
    }
    .match-low {
        background: #ef4444;
        color: white;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .deadline-critical {
        background: #fee2e2;
        border-left: 4px solid #dc2626;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .deadline-warning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .deadline-info {
        background: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'scholarships_loaded' not in st.session_state:
    st.session_state.scholarships_loaded = False

# Load scholarships (cached)
@st.cache_data
def load_scholarship_data():
    scholarships = load_scholarships()
    scholarships = update_scholarship_deadlines(scholarships)
    return scholarships

# Main app header
st.markdown('<p class="main-header">🎓 ScholarMatch</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Scholarship Matching • Unlock Your Educational Funding</p>', unsafe_allow_html=True)

# Sidebar - User Profile Form
st.sidebar.title("📝 Build Your Profile")
st.sidebar.markdown("Fill out your information to find matching scholarships!")

with st.sidebar.form("profile_form"):
    st.markdown("### 👤 Personal Information")
    name = st.text_input("Full Name *", placeholder="John Doe")
    email = st.text_input("Email *", placeholder="john@example.com")
    
    st.markdown("### 📚 Academic Information")
    gpa = st.slider("GPA (4.0 scale)", 0.0, 4.0, 3.5, 0.1)
    
    grade_level = st.selectbox("Grade Level *", [
        "High School Freshman",
        "High School Sophomore", 
        "High School Junior",
        "High School Senior",
        "College Freshman",
        "College Sophomore",
        "College Junior",
        "College Senior",
        "Graduate Student"
    ])
    
    major = st.selectbox("Field of Study *", [
        "STEM",
        "Engineering",
        "Business",
        "Arts & Humanities",
        "Social Sciences",
        "Medicine",
        "Education",
        "Undecided"
    ])
    
    st.markdown("### 📍 Location")
    state = st.selectbox("State *", [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
        "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
        "West Virginia", "Wisconsin", "Wyoming"
    ])
    
    st.markdown("### 🌈 Demographics (Optional)")
    ethnicity = st.multiselect("Ethnicity", [
        "African American",
        "Hispanic/Latino",
        "Asian American",
        "Native American",
        "Pacific Islander",
        "White",
        "Other"
    ])
    
    gender = st.selectbox("Gender", [
        "Prefer not to say",
        "Male",
        "Female",
        "Other"
    ])
    
    st.markdown("### 🎯 Interests & Activities")
    interests = st.multiselect("Select all that apply", [
        "Sports",
        "Community Service",
        "STEM Clubs",
        "Arts/Music",
        "Student Government",
        "Entrepreneurship",
        "Writing",
        "Debate"
    ])
    
    st.markdown("### ⭐ Special Circumstances")
    special_circumstances = st.multiselect("Select if applicable", [
        "First Generation College Student",
        "Military Family",
        "Financial Need",
        "Disability",
        "None"
    ])
    
    submit_button = st.form_submit_button("🔍 Find My Scholarships!", use_container_width=True)

# Main content area
if submit_button:
    # Validate required fields
    if not name or not email:
        st.error("⚠️ Please fill in your name and email!")
    elif "@" not in email:
        st.error("⚠️ Please enter a valid email address!")
    else:
        # Create user profile
        user_profile = {
            "name": name,
            "email": email,
            "gpa": gpa,
            "grade_level": grade_level,
            "major": major,
            "state": state,
            "ethnicity": ethnicity,
            "gender": gender,
            "interests": interests,
            "special_circumstances": special_circumstances
        }
        
        # Save to session state
        st.session_state.user_profile = user_profile
        
        # Save to database
        save_user_profile(user_profile)
        
        # Load scholarships
        with st.spinner("🔍 Searching through 60+ scholarships..."):
            scholarships = load_scholarship_data()
            
            # Match scholarships
            matches = match_scholarships(user_profile, scholarships, min_match_threshold=40)
            st.session_state.matches = matches
        
        st.success(f"✅ Found {len(matches)} scholarships matching your profile, {name}!")
        st.balloons()

# Display results if matches exist
if st.session_state.matches:
    matches = st.session_state.matches
    
    # Top statistics
    st.markdown("---")
    st.markdown("## 📊 Your Match Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <p class="stat-number">{len(matches)}</p>
                <p class="stat-label">Total Matches</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_value = sum([s.get('amount', 0) for s in matches[:10] if isinstance(s.get('amount'), (int, float))])
        st.markdown(f"""
            <div class="stat-box">
                <p class="stat-number">${total_value:,}</p>
                <p class="stat-label">Potential Value (Top 10)</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_match = sum([s.get('match_score', 0) for s in matches]) / len(matches) if matches else 0
        st.markdown(f"""
            <div class="stat-box">
                <p class="stat-number">{int(avg_match)}%</p>
                <p class="stat-label">Avg Match Score</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        urgent = len([s for s in matches if s.get('deadline_days', 999) < 30])
        st.markdown(f"""
            <div class="stat-box">
                <p class="stat-number">{urgent}</p>
                <p class="stat-label">Urgent Deadlines</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Top Matches", "📊 Analytics", "📅 Deadlines", "🔍 All Results"])
    
    with tab1:
        st.markdown("### 🏆 Your Best Scholarship Matches")
        st.markdown("These scholarships are ranked by how well they match your profile!")
        
        # Display top 15 matches
        for idx, scholarship in enumerate(matches[:15], 1):
            match_score = scholarship.get('match_score', 0)
            
            # Determine match quality
            if match_score >= 80:
                badge_class = "match-high"
                emoji = "🟢"
            elif match_score >= 60:
                badge_class = "match-medium"
                emoji = "🟡"
            else:
                badge_class = "match-low"
                emoji = "🟠"
            
            with st.expander(f"{emoji} **#{idx} - {scholarship['name']}** - {match_score}% Match"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**💰 Amount:** ${scholarship.get('amount', 'Varies'):,}" if isinstance(scholarship.get('amount'), (int, float)) else f"**💰 Amount:** {scholarship.get('amount', 'Varies')}")
                    st.markdown(f"**📅 Deadline:** {scholarship.get('deadline', 'Rolling')}")
                    st.markdown(f"**📝 Category:** {scholarship.get('category', 'General')}")
                    st.markdown(f"**📖 Description:** {scholarship.get('description', 'No description available')}")
                    
                    st.markdown("**✅ Requirements:**")
                    for req in scholarship.get('requirements', ['See website for details']):
                        st.markdown(f"• {req}")
                
                with col2:
                    # Match score progress bar
                    st.markdown(f"**Match Score**")
                    st.progress(match_score / 100)
                    st.markdown(f"<span class='match-badge {badge_class}'>{match_score}%</span>", unsafe_allow_html=True)
                    
                    st.markdown("**Why You Match:**")
                    for reason in scholarship.get('match_reasons', [])[:5]:
                        st.markdown(f"{reason}")
                    
                    # Deadline urgency
                    days_left = scholarship.get('deadline_days', 999)
                    if days_left < 7:
                        st.error(f"⚠️ Due in {days_left} days!")
                    elif days_left < 30:
                        st.warning(f"⏰ Due in {days_left} days")
                    else:
                        st.info(f"📅 Due in {days_left} days")
                    
                    if scholarship.get('url'):
                        st.link_button("Apply Now →", scholarship['url'], use_container_width=True)
    
    with tab2:
        st.markdown("### 📈 Scholarship Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Amount distribution
            amounts = [s.get('amount', 0) for s in matches[:30] if isinstance(s.get('amount'), (int, float))]
            if amounts:
                fig = px.histogram(
                    amounts, 
                    nbins=10, 
                    title="Scholarship Amount Distribution (Top 30)",
                    labels={'value': 'Amount ($)', 'count': 'Number of Scholarships'},
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category breakdown pie chart
            categories = {}
            for s in matches[:30]:
                cat = s.get('category', 'General')
                categories[cat] = categories.get(cat, 0) + 1
            
            fig2 = px.pie(
                values=list(categories.values()), 
                names=list(categories.keys()),
                title="Scholarships by Category (Top 30)",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Match score distribution
        st.markdown("#### Match Score Distribution")
        match_scores = [s.get('match_score', 0) for s in matches]
        fig3 = px.histogram(
            match_scores,
            nbins=10,
            title="How Well Scholarships Match Your Profile",
            labels={'value': 'Match Score (%)', 'count': 'Number of Scholarships'},
            color_discrete_sequence=['#f59e0b']
        )
        fig3.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Top categories table
        st.markdown("#### Category Breakdown")
        category_df = pd.DataFrame([
            {"Category": cat, "Count": count, "Avg Amount": f"${sum([s.get('amount', 0) for s in matches if s.get('category') == cat and isinstance(s.get('amount'), (int, float))]) // max(count, 1):,}"}
            for cat, count in categories.items()
        ]).sort_values('Count', ascending=False)
        st.dataframe(category_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 📅 Upcoming Deadlines")
        st.markdown("Stay on track with these important dates!")
        
        # Sort by deadline
        deadline_sorted = sorted(
            [s for s in matches if s.get('deadline_days') is not None],
            key=lambda x: x.get('deadline_days', 999)
        )
        
        # Group by urgency
        critical = [s for s in deadline_sorted if s.get('deadline_days', 999) < 7]
        urgent = [s for s in deadline_sorted if 7 <= s.get('deadline_days', 999) < 30]
        upcoming = [s for s in deadline_sorted if 30 <= s.get('deadline_days', 999) < 90]
        
        if critical:
            st.markdown("#### 🚨 Critical - Due This Week!")
            for s in critical:
                st.markdown(f"""
                    <div class="deadline-critical">
                        <strong>{s['name']}</strong><br>
                        💰 ${s.get('amount', 'Varies'):,} • ⏰ {s.get('deadline_days', '?')} days left • Due: {s.get('deadline', 'TBD')}
                    </div>
                """, unsafe_allow_html=True)
        
        if urgent:
            st.markdown("#### ⚠️ Urgent - Due This Month")
            for s in urgent:
                st.markdown(f"""
                    <div class="deadline-warning">
                        <strong>{s['name']}</strong><br>
                        💰 ${s.get('amount', 'Varies'):,} • ⏰ {s.get('deadline_days', '?')} days left • Due: {s.get('deadline', 'TBD')}
                    </div>
                """, unsafe_allow_html=True)
        
        if upcoming:
            st.markdown("#### 📌 Upcoming - Next 3 Months")
            for s in upcoming[:10]:
                st.markdown(f"""
                    <div class="deadline-info">
                        <strong>{s['name']}</strong><br>
                        💰 ${s.get('amount', 'Varies'):,} • ⏰ {s.get('deadline_days', '?')} days left • Due: {s.get('deadline', 'TBD')}
                    </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🔍 All Matched Scholarships")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = ['All'] + sorted(list(set([s.get('category', 'General') for s in matches])))
            category_filter = st.selectbox("Filter by Category", categories)
        
        with col2:
            min_amount = st.number_input("Min Amount ($)", min_value=0, value=0, step=500)
        
        with col3:
            deadline_filter = st.selectbox("Deadline", ["All", "This Week", "This Month", "This Quarter"])
        
        # Apply filters
        filtered_matches = matches.copy()
        
        if category_filter != 'All':
            filtered_matches = [s for s in filtered_matches if s.get('category') == category_filter]
        
        if min_amount > 0:
            filtered_matches = [s for s in filtered_matches if isinstance(s.get('amount'), (int, float)) and s.get('amount', 0) >= min_amount]
        
        if deadline_filter == "This Week":
            filtered_matches = [s for s in filtered_matches if s.get('deadline_days', 999) < 7]
        elif deadline_filter == "This Month":
            filtered_matches = [s for s in filtered_matches if s.get('deadline_days', 999) < 30]
        elif deadline_filter == "This Quarter":
            filtered_matches = [s for s in filtered_matches if s.get('deadline_days', 999) < 90]
        
        st.markdown(f"**Showing {len(filtered_matches)} scholarships**")
        
        # Display as table
        if filtered_matches:
            table_data = []
            for s in filtered_matches:
                table_data.append({
                    "Scholarship": s['name'],
                    "Amount": f"${s.get('amount', 0):,}" if isinstance(s.get('amount'), (int, float)) else str(s.get('amount', 'Varies')),
                    "Match": f"{s.get('match_score', 0)}%",
                    "Deadline": s.get('deadline', 'Rolling'),
                    "Days Left": s.get('deadline_days', '?'),
                    "Category": s.get('category', 'General')
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="scholarMatch_results.csv",
                mime="text/csv"
            )

else:
    # Landing page (before form submission)
    st.markdown("## 💰 Billions in Scholarships Go Unclaimed Every Year")
    st.markdown("**Don't leave money on the table!** ScholarMatch uses AI to find scholarships perfectly matched to YOUR profile.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(...)
