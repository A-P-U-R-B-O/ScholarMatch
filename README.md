# 🎓 ScholarMatch - AI-Powered Scholarship Finder


![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Overview

**ScholarMatch** is an AI-powered scholarship matching platform that helps students discover funding opportunities tailored to their unique profiles. By analyzing academic performance, demographics, interests, and special circumstances, ScholarMatch connects students with scholarships they're most likely to win.

### 💡 The Problem

- **$100+ million in scholarships go unclaimed every year**
- Students spend countless hours searching through irrelevant opportunities
- Many qualified students never find scholarships they're eligible for
- Complex eligibility requirements make matching difficult

### ✨ The Solution

ScholarMatch uses a sophisticated weighted matching algorithm to:
- Scan 60+ diverse scholarships in under 30 seconds
- Calculate personalized match scores (0-100%) for each scholarship
- Prioritize opportunities by fit, deadline urgency, and award amount
- Provide detailed insights on why each scholarship matches your profile

---

## 🎯 Features

### 🧠 Smart Matching Algorithm
- **Multi-factor scoring** based on GPA, major, location, demographics, interests, and special circumstances
- **Weighted evaluation** giving appropriate importance to different criteria
- **Dynamic filtering** to exclude scholarships you don't qualify for

### 📊 Beautiful Visualizations
- Interactive charts showing scholarship distribution by amount and category
- Match score analytics to understand your profile strength
- Deadline urgency indicators (critical/urgent/upcoming)

### ⏰ Deadline Tracking
- Automatic calculation of days until deadline
- Color-coded urgency levels (🚨 < 7 days, ⚠️ < 30 days, 📌 < 90 days)
- Organized deadline calendar view

### 📥 Export & Download
- Download your matches as CSV for offline tracking
- Export filtered results based on category, amount, or deadline

### 🎨 User-Friendly Interface
- Clean, modern design with intuitive navigation
- Mobile-responsive layout
- Step-by-step profile building
- Real-time results

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Web application framework |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive data visualizations |
| **JSON** | Data storage and persistence |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone https://github.com/A-P-U-R-B-O/scholarMatch.git
cd scholarMatch
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
scholarMatch/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/
│   ├── scholarships.json       # Scholarship database (60+ entries)
│   └── users.json              # User profiles storage
├── utils/
│   ├── matcher.py              # Matching algorithm
│   └── database.py             # Database operations
└── exports/                    # Generated export files
```

---

## 🎓 How to Use

### 1. Fill Out Your Profile
Complete the sidebar form with:
- **Personal Info**: Name and email
- **Academic Info**: GPA, grade level, and major
- **Location**: Your state
- **Demographics**: Ethnicity and gender (optional)
- **Interests**: Activities and hobbies
- **Special Circumstances**: First-gen, military family, etc.

### 2. Get Your Matches
Click "🔍 Find My Scholarships!" to:
- Search 60+ scholarships instantly
- Calculate match scores for each
- Rank results by best fit

### 3. Explore Results
Navigate through four tabs:
- **🎯 Top Matches**: Your best 15 opportunities with detailed info
- **📊 Analytics**: Visual insights into your matches
- **📅 Deadlines**: Organized by urgency
- **🔍 All Results**: Full filterable list with CSV export

### 4. Apply & Win!
Use the "Apply Now" links and track your applications offline.

---

## 🧮 Matching Algorithm

ScholarMatch uses a weighted scoring system with 7 factors to determine fit.

### **🚨 Hard Filters (The Non-Negotiables)**

**Before calculating the weighted score, a student must meet the following three hard-filter requirements. Failure on any one of these results in an immediate $\mathbf{0\%}$ match:**

1.  **GPA:** The user's GPA must be greater than or equal to the scholarship's minimum required GPA.
2.  **Grade Level:** The user's current grade level (e.g., College Sophomore) must be explicitly listed in the scholarship's allowed levels.
3.  **Location:** The user's state must be listed in the scholarship's states, unless the scholarship is open to 'All' states.

---

### **Weighted Scoring Factors**

Once the Hard Filters are passed, the total Match Score (out of 100%) is calculated based on the following weights:

| Factor | Weight | Description |
| :--- | :--- | :--- |
| GPA Match | 20% | Meets minimum GPA requirement |
| Major Match | 25% | Field of study alignment |
| Grade Level | 20% | Educational level eligibility |
| Location | 10% | State/national availability |
| Demographics | 10% | Ethnicity, gender preferences |
| Interests | 10% | Extracurricular alignment |
| Special Circumstances | 5% | First-gen, military, etc. |

**Match Score Calculation:**

$$match\_score = \frac{weighted\_sum\_of\_matching\_factors}{max\_possible\_score} \times 100$$

Only scholarships with $\geq40\%$ match are shown to ensure relevance.


---

## 📊 Scholarship Database

Our database includes **64 diverse scholarships** covering:

### Categories
- 🔬 STEM & Engineering (12)
- 💼 Business & Entrepreneurship (8)
- 🎨 Arts & Humanities (7)
- 🏥 Medicine & Healthcare (6)
- 👩‍🏫 Education (5)
- 🌍 Social Sciences (4)
- 🎖️ Military & Veterans (4)
- 🌟 Diversity & Inclusion (12+)

### Award Amounts
- **Range**: $500 - $50,000
- **Average**: ~$6,500
- **Total Available**: $750,000+

### Geographic Coverage
- National scholarships (open to all states)
- State-specific opportunities (CA, TX, NY, FL, IL, PA, OH, GA, MI, NC, VA, WA, AZ, MA, CO, OR)


---

## 🏆 Why ScholarMatch Wins

### ✅ Real-World Impact
- Addresses $100M+ unclaimed scholarship problem
- Directly helps students reduce education costs
- Increases college access and affordability

### ✅ Technical Excellence
- Clean, well-documented code
- Sophisticated matching algorithm
- Beautiful, responsive UI
- Scalable architecture

### ✅ Economic Relevance
- Tackles financial inequality in education
- Democratizes access to funding information
- Data-driven decision making for students

### ✅ Completeness
- Fully functional prototype
- Comprehensive database
- Professional documentation
- Ready for production deployment

---

## 🚀 Future Enhancements

### Phase 1 (Short-term)
- [ ] OpenAI integration for personalized essay assistance
- [ ] Email deadline reminders
- [ ] Application tracker (draft/submitted/awarded)
- [ ] Bookmark favorite scholarships

### Phase 2 (Medium-term)
- [ ] Web scraping to expand database automatically
- [ ] User authentication and saved profiles
- [ ] Community features (reviews, success stories)
- [ ] Mobile app (React Native)

### Phase 3 (Long-term)
- [ ] Partner with scholarship providers for direct applications
- [ ] Machine learning to improve matching accuracy
- [ ] Institutional version for high school counselors
- [ ] API for integration with college planning platforms

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**A-P-U-R-B-O** (Tamzid Ahmed Apurbo)
- GitHub: [@A-P-U-R-B-O](https://github.com/A-P-U-R-B-O)
- Email: [Your email]

---

## 🙏 Acknowledgments

- **Streamlit** for the amazing framework
- **GitHub Copilot** for development assistance
- All the scholarship providers making education accessible

---

## 📞 Support

Found a bug? Have a feature request?
- 🐛 [Open an Issue](https://github.com/A-P-U-R-B-O/scholarMatch/issues)
- 💬 [Start a Discussion](https://github.com/A-P-U-R-B-O/scholarMatch/discussions)

---

<div align="center">

**Built with ❤️ for students everywhere**

⭐ Star this repo if ScholarMatch helped you!


> 📌 Note: Current dataset uses U.S. scholarships to validate the matching engine. In the next phase, we will build the first open, crowdsourced scholarship database for Bangladeshi and Global South students, with scraping + community submissions.
> 

[🚀 Try Live Demo](https://your-streamlit-app-url.streamlit.app) • [📖 Documentation](https://github.com/A-P-U-R-B-O/scholarMatch/wiki) • [🎥 Video Demo](https://youtu.be/your-demo)

</div>
