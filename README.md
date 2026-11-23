# 🚀 EduPilot AI

### Multi-Agent Personalized Learning & Project Research Assistant

**Learn Smarter. Build Better. Research Deeper.**

EduPilot AI is an AI-powered, multi-agent learning and project research platform designed to help students discover quality educational resources, learn new subjects, and transform their project ideas into actionable development roadmaps.

Powered by **LLMs, LangGraph, RAG, and specialized AI agents**, EduPilot AI provides personalized learning recommendations, academic research papers, technical documentation, YouTube resources, and structured project development guidance in one place.

---

## 🌟 Key Features

### 📚 1. AI-Powered Subject Learning Assistant

Enter any subject and let EduPilot AI discover relevant learning resources.

- **YouTube Recommendations:** Discover relevant educational channels, videos, and playlists.
- **Blog Discovery:** Find useful technical blogs, tutorials, and articles.
- **Official Documentation:** Get recommendations for trusted documentation and learning platforms.
- **Personalized Learning Paths:** Receive structured learning roadmaps based on your current knowledge level.
- **Difficulty-Based Recommendations:** Explore beginner, intermediate, and advanced learning materials.

### 💡 2. AI Project Mentor

Have a project idea but don't know where to start?

Simply describe your idea, and EduPilot AI will help you plan its implementation.

- **Project Analysis:** Understand the problem statement, objectives, and expected outcomes.
- **Technology Stack Recommendation:** Identify suitable programming languages, frameworks, libraries, and tools.
- **Development Roadmap:** Generate a structured, step-by-step implementation plan.
- **System Architecture:** Get guidance on components, modules, and system design.
- **Task Breakdown:** Divide complex projects into manageable development phases.
- **GitHub Discovery:** Find relevant open-source repositories and implementation references.

### 📄 3. Academic Research Assistant

Explore existing research before building your project.

- Discover relevant academic research papers.
- Retrieve paper abstracts, authors, publication details, and DOI links.
- Understand research methodologies and technical approaches.
- Compare existing research approaches.
- Explore limitations and potential research directions.
- Build a stronger understanding of the project domain.

### 🤖 4. Multi-Agent AI Architecture

EduPilot AI uses specialized AI agents coordinated through LangGraph.

| AI Agent                | Responsibility                                               |
| ----------------------- | ------------------------------------------------------------ |
| YouTube Research Agent  | Finds educational videos, channels, and playlists.           |
| Web Research Agent      | Discovers blogs, tutorials, and documentation.               |
| Learning Path Agent     | Generates personalized subject-learning roadmaps.            |
| Project Planning Agent  | Converts project ideas into structured implementation plans. |
| Academic Research Agent | Discovers and analyzes relevant research papers.             |
| Response Synthesizer    | Combines agent outputs into structured responses.            |

**Central Orchestrator:** Routes user requests to the appropriate agents using conditional workflows and manages their execution.

---

## 🏗️ System Architecture

```text
                       STUDENT
                          |
                          v
                  REACT DASHBOARD
                          |
                          v
                    FASTAPI BACKEND
                          |
                          v
                 LANGGRAPH ORCHESTRATOR
                          |
                    INTENT ROUTER
                     /         \
                    /           \
               LEARN MODE     BUILD MODE
                   |              |
          +--------+------+   +---+----------+
          |        |      |   |              |
          v        v      v   v              v
       YOUTUBE   WEB   LEARNING PROJECT   ACADEMIC
       AGENT    AGENT   AGENT   AGENT     RESEARCH
          |        |      |   |              |
          +--------+------+   +--------------+
                   |                 |
                   v                 v
              RESOURCE          RESEARCH
              RETRIEVAL         RETRIEVAL
                   |                 |
                   +--------+--------+
                            |
                            v
                   RESPONSE SYNTHESIZER
                            |
                            v
                     FINAL RESPONSE
                            |
                            v
                     REACT DASHBOARD
```

---

## 🛠️ Tech Stack

### Frontend

- React.js
- Tailwind CSS
- Vite
- Axios

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### AI & Agentic Frameworks

- LangGraph
- LangChain
- Google Gemini API
- Sentence Transformers

### RAG & Vector Database

- ChromaDB
- Embeddings
- Semantic Search

### External APIs & Integrations

- YouTube Data API v3
- Tavily Search API
- Semantic Scholar API
- OpenAlex API
- arXiv API
- GitHub REST API

### Database & Deployment

- PostgreSQL
- Vercel
- Render

---

## 📁 Project Structure

```text
EduPilot-AI/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── orchestrator.py
│   │   │   ├── youtube_agent.py
│   │   │   ├── web_agent.py
│   │   │   ├── learning_agent.py
│   │   │   ├── project_agent.py
│   │   │   ├── research_agent.py
│   │   │   └── synthesizer.py
│   │   │
│   │   ├── workflows/
│   │   │   ├── learning_workflow.py
│   │   │   └── project_workflow.py
│   │   │
│   │   ├── tools/
│   │   │   ├── youtube_tool.py
│   │   │   ├── web_search_tool.py
│   │   │   ├── academic_tool.py
│   │   │   └── github_tool.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── learning_schema.py
│   │   │   └── project_schema.py
│   │   │
│   │   ├── services/
│   │   │   ├── llm_service.py
│   │   │   └── resource_service.py
│   │   │
│   │   ├── database/
│   │   │   ├── db.py
│   │   │   └── models.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have installed:

- Python 3.11+
- Node.js and npm
- Git
- PostgreSQL (when enabling database functionality)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/EduPilot-AI.git

cd EduPilot-AI
```

### 2. Backend Setup

```bash
cd backend

python -m venv env
```

Activate the environment:

**Windows PowerShell:**

```powershell
.\env\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file inside the backend directory.

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
YOUTUBE_API_KEY=your_youtube_api_key
DATABASE_URL=your_postgresql_connection_string
GITHUB_TOKEN=your_github_token
```

Obtain API credentials:

- [Google AI Studio](https://aistudio.google.com/apikey)
- [Tavily](https://app.tavily.com/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [GitHub Developer Settings](https://github.com/settings/tokens)

Never commit your API keys or `.env` file to GitHub.

### 4. Run the Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 🔌 API Endpoints

Planned backend endpoints:

| Method | Endpoint                | Description                           |
| ------ | ----------------------- | ------------------------------------- |
| POST   | `/api/learn`            | Generate subject learning resources.  |
| POST   | `/api/learn/roadmap`    | Generate personalized learning paths. |
| POST   | `/api/build`            | Generate project roadmaps.            |
| POST   | `/api/build/research`   | Retrieve relevant research papers.    |
| POST   | `/api/build/github`     | Discover GitHub repositories.         |
| POST   | `/api/papers/summarize` | Summarize academic papers.            |
| GET    | `/api/history`          | Retrieve user activity history.       |
| POST   | `/api/save-resource`    | Save useful learning resources.       |

---

## 🔮 Future Enhancements

- [ ] AI-powered personalized study plans.
- [ ] Research paper summarization and comparison.
- [ ] Research Gap Analyzer.
- [ ] Chat with uploaded research papers using RAG.
- [ ] Project progress tracking and task management.
- [ ] GitHub repository analysis.
- [ ] AI-generated project architecture diagrams.
- [ ] Knowledge gap detection.
- [ ] Student learning analytics.
- [ ] Persistent conversational memory.

---

## 🎯 Project Objectives

EduPilot AI aims to:

1. Simplify the process of finding reliable educational resources.
2. Provide personalized learning recommendations.
3. Help students convert ideas into implementable projects.
4. Make academic research more accessible.
5. Demonstrate practical applications of multi-agent AI systems, LLMs, and RAG.

---

## 👩‍💻 Author

**Vanshika Saxena**

B.Tech – Computer Science Engineering (AI/ML & IoT)

Interested in Artificial Intelligence, Generative AI, Agentic AI, and Backend Development.

- GitHub: [Vanshika290](https://github.com/Vanshika290)

---

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub!

**EduPilot AI – Turning Learning Goals and Project Ideas into Action.**
