# 🚀 EduPilot AI

### Multi-Agent Personalized Learning & Project Research Assistant

**Learn Smarter. Build Better. Research Deeper.**

EduPilot AI is an AI-powered, multi-agent learning and project research platform designed to help students discover quality educational resources, learn new subjects, and transform their project ideas into actionable development roadmaps.

Powered by **LLMs, LangGraph, Streamlit/Aspira UI, and specialized AI agents**, EduPilot AI provides personalized learning recommendations, academic research papers, technical documentation, YouTube resources, and structured project development guidance in one place.

---

## 🌟 Key Features

### 📚 1. AI-Powered Subject Learning Assistant

Enter any subject and let EduPilot AI discover relevant learning resources:
- **YouTube Recommendations:** Discover relevant educational channels, videos, and playlists with direct watch links.
- **Blog Discovery:** Find useful technical blogs, tutorials, and articles from GeeksforGeeks, Medium, Towards Data Science, and official documentation.
- **Personalized Learning Paths:** Receive structured 4-phase milestone checklists based on your knowledge level.
- **Self-Check Flashcards:** Interactive conceptual and interview questions with collapsible answers.

### 💡 2. AI Project Mentor & Architecture Designer

Have a project idea but don't know where to start? Describe your idea, and EduPilot AI will plan its implementation:
- **Phased Implementation Roadmap:** Detailed milestone breakdown (Phase 1 Setup, Phase 2 MVP, Phase 3 Optimization, Phase 4 Deployment).
- **System Architecture:** Interactive Mermaid flowcharts representing data flow between UI, API gateway, cache, database, and models.
- **Production Directory Tree:** Clean repository file structure (`src/api`, `src/core`, `src/models`, `tests/`).
- **Starter Boilerplate Code:** Copy-pasteable and downloadable Python starter template (`main.py`).
- **Technology Stack Comparison:** Rationale for choosing specific frameworks and libraries over alternatives.

### 📄 3. Academic Research Assistant (ArXiv Integration)

Explore existing research before building your project:
- Discover relevant academic research papers via **ArXiv & Semantic Scholar API** in real time (zero API key needed!).
- Retrieve paper abstracts, authors, publication dates, and direct PDF download links.
- Practical guidance on translating research papers' algorithms, loss functions, and methodologies into project code.
- Viva defense questions and Google X-Y-Z formula resume bullet points.

### 🤖 4. Multi-Agent AI Architecture

EduPilot AI uses specialized AI agents:

| AI Agent | Responsibility |
| :--- | :--- |
| **Subject Study Agent** | Curates educational YouTube channels, tutorials, blogs, and syllabi. |
| **Project Architect Agent** | Converts project ideas into roadmaps, system architectures, and starter code. |
| **Academic Research Agent** | Fetches and analyzes real-time peer-reviewed research papers from ArXiv. |
| **AI Tutor (Gemini)** | Conversational mentor for doubts, conceptual explanations, and viva prep. |

---

## 🎨 Aspira Dark-Violet UI

EduPilot AI includes a modern, responsive web dashboard inspired by **Aspira**:
- **7-Day Streak & Daily Study Goal Widget** (interactive hour logging with celebration animations).
- **Dynamic Category Filter Pills** (`All`, `Data Science`, `Web Development`, `Design`, `Computer Science`, `Cloud Computing`).
- **One-Click Quick Topic & Project Prompt Chips**.
- **Interactive Saved Library (Bookmarks)** to revisit pinned guides anytime.

---

## ⚙️ Quickstart & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Vanshika290/Multi-Agent-Personalization-Learning.git
cd Multi-Agent-Personalization-Learning
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration (Optional)

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Get a free key from [Google AI Studio](https://aistudio.google.com/). You can also input the key directly inside the dashboard sidebar at runtime!)*

### 4. Run the Application

Launch the interactive dashboard:

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 📁 Repository Structure

```text
Multi-Agent-Personalization-Learning/
├── app.py                     # Streamlit frontend & Aspira interactive dashboard
├── config.py                  # Model preferences & configuration loader
├── requirements.txt           # Python dependencies
├── .env.example               # Sample environment variables
├── .gitignore                 # Excludes cache, virtual environments, and secrets
├── README.md                  # Comprehensive documentation
├── agents/
│   ├── __init__.py
│   ├── subject_agent.py       # Subject Study Companion logic
│   ├── project_agent.py       # Project Roadmap & Architecture Mentor
│   └── arxiv_service.py       # ArXiv & Semantic Scholar research paper service
└── utils/
    ├── __init__.py
    └── gemini_client.py       # Unified Gemini API client (google-genai / google-generativeai)
```

---

## 👩‍💻 Author

**Vanshika Saxena**

B.Tech – Computer Science Engineering (AI/ML & IoT)  
Interested in Artificial Intelligence, Generative AI, Agentic AI, and Backend Development.

- GitHub: [@Vanshika290](https://github.com/Vanshika290)

---

## ⭐ Support

If you find this project helpful, please give this repository a ⭐ on GitHub!
