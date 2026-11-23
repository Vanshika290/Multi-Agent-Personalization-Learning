"""Project Architect & Research Mentor Agent.
Analyzes project ideas, generates comprehensive technical roadmaps, recommended file structures,
starter boilerplate code, and live academic research papers from ArXiv.
"""

import urllib.parse
from typing import Dict, Any, List
from utils.gemini_client import GeminiClient
from agents.arxiv_service import fetch_arxiv_papers

class ProjectMentorAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def create_project_roadmap(
        self,
        project_idea: str,
        domain: str = "Artificial Intelligence & Machine Learning",
        timeframe: str = "4-6 Weeks (Semester Project)",
        max_papers: int = 4
    ) -> Dict[str, Any]:
        """
        End-to-end project mentorship:
        1. Fetch real academic papers from ArXiv.
        2. Prompt Gemini for a comprehensive, structured project blueprint
           with architecture, file tree, starter code, research synthesis,
           and viva defense questions.
        """
        papers = fetch_arxiv_papers(project_idea, max_results=max_papers)

        if not self.client.is_configured():
            mock_roadmap = self._generate_offline_roadmap(project_idea, domain, timeframe, papers)
            return {
                "roadmap_markdown": mock_roadmap,
                "papers": papers
            }

        # Format papers context for the Gemini prompt
        papers_context = ""
        if papers:
            papers_context = "Here are the top academic papers retrieved from ArXiv for this project:\n"
            for i, p in enumerate(papers, 1):
                papers_context += f"{i}. Title: {p['title']}\n   Authors: {', '.join(p['authors'])}\n   Abstract: {p['summary'][:320]}...\n   PDF URL: {p['pdf_url']}\n\n"

        prompt = f"""
You are a Principal Software Architect and Academic Project Mentor.
A student wants to build the following project:
**Project Idea:** {project_idea}
**Target Domain:** {domain}
**Timeframe:** {timeframe}

{papers_context}

Generate an exhaustive, world-class Project Engineering Blueprint formatted in clean GitHub-flavored Markdown. Ensure the explanations are crystal clear, practical, and highly impressive. Follow this structure:

# 🚀 Complete Project Blueprint: {project_idea}

## 🎯 1. Executive Summary & Problem Formulation
- **The Core Problem:** Exactly what problem does this project solve, and why do existing solutions fall short?
- **Target Users & Real-World Impact:** Who benefits and how?
- **Key Innovation:** What makes this project stand out on a resume or to graduate evaluators?

## 🏗️ 2. System Architecture & Component Design
Explain how data flows through the system, and provide a detailed Mermaid flowchart:
```mermaid
graph TD
    User([Client / User Interface]) --> Gateway[API Gateway / Router]
    Gateway --> Service[Core Business Logic / Pipeline]
    Service --> Storage[(Database / Vector Store)]
    Service --> Engine[AI Engine / Analytics Model]
    Engine --> Output([Processed Output / Visualization])
```
*(Customize this mermaid chart specifically to match the real components of "{project_idea}")*

## 📁 3. Production Repository & Folder Structure
Provide the recommended clean directory tree for this project:
```
project-root/
├── src/
│   ├── api/
│   ├── core/
│   ├── models/
│   └── utils/
├── tests/
├── config.py
├── requirements.txt
├── Dockerfile
└── README.md
```
*(Tailor this file structure with brief 1-line annotations explaining what goes inside each key file/folder)*

## 🛠️ 4. Recommended Tech Stack & Alternatives
Provide a clear breakdown:
| Layer | Recommended Choice | Industry Alternative | Why This Is Best For This Project |
| :--- | :--- | :--- | :--- |
| **Frontend / UI** | ... | ... | ... |
| **Backend / API** | ... | ... | ... |
| **Database / Storage** | ... | ... | ... |
| **AI / ML / Core Engine** | ... | ... | ... |
| **DevOps / Deployment** | ... | ... | ... |

## 📅 5. Phased Implementation Roadmap ({timeframe})
Break this into 4 actionable phases with concrete deliverables:
- **Phase 1: Environment Setup, Data Pipeline & Architecture (Week 1)**
  - Tasks: ...
  - Deliverable: ...
- **Phase 2: Minimum Viable Product (MVP) Core Logic (Week 2-3)**
  - Tasks: ...
  - Deliverable: ...
- **Phase 3: Advanced Optimization, Edge Cases & Polish (Week 4)**
  - Tasks: ...
  - Deliverable: ...
- **Phase 4: Benchmarking, Automated Tests & Deployment (Final Week)**
  - Tasks: ...
  - Deliverable: ...

## 💻 6. Starter Boilerplate Code
Provide a copy-pasteable, functional Python (or relevant language) baseline starter script (e.g., `main.py` or `pipeline.py`) that sets up the core classes, configuration, and a mock execution loop so the student can start coding immediately.

## 📄 7. Academic Research Deep-Dive & How to Apply Papers
Analyze the research papers provided above:
For each paper:
- **Paper Title & Direct Link**
- **Core Breakthrough / Theory:** (In simple terms)
- **Code Implementation Blueprint:** How the student should translate this paper's math, loss function, or algorithm into actual code.
- **📥 Direct PDF Link**

## ⚠️ 8. Common Pitfalls, Edge Cases & How to Fix Them
- Identify 3 major technical bugs, bottlenecks, or data leakage traps students face in this specific project and how to prevent them.

## 🎓 9. Viva / Interview Defense & Resume Impact
- **Top 3 Tough Viva / Technical Interview Questions:** Anticipate questions professors or recruiters will ask about this project, along with winning sample answers.
- **Quantified Resume Bullet Points:** 3 high-impact resume lines formatted with Google's X-Y-Z formula.
"""

        system_instruction = "You are EduAgent Project Architect, guiding students with rigorous engineering standards, production architecture, and academic depth."
        roadmap_text = self.client.generate(prompt, system_instruction=system_instruction)

        return {
            "roadmap_markdown": roadmap_text,
            "papers": papers
        }

    def _generate_offline_roadmap(self, project_idea: str, domain: str, timeframe: str, papers: List[Dict[str, Any]]) -> str:
        """Curated fallback response when running without an API key."""
        papers_md = ""
        if papers:
            papers_md = "## 📄 Real-Time Academic Research Papers (via ArXiv)\n"
            for i, p in enumerate(papers, 1):
                papers_md += f"""
### {i}. [{p['title']}]({p['arxiv_url']})
- **Authors:** {', '.join(p['authors'])} ({p['published']})
- **Category:** `{p['primary_category']}`
- **Abstract Summary:** {p['summary'][:300]}...
- **📥 Direct PDF:** [Download Paper PDF]({p['pdf_url']})
- **💡 Practical Code Application:** Implement the baseline model proposed in Section 3 of this paper, using their loss function and parameter initialization to benchmark against standard baselines.

---
"""

        return f"""
# 🚀 Complete Project Blueprint: {project_idea}
*(Running in instant preview mode. Connect your Gemini API Key in the sidebar for personalized deep-dives)*

## 🎯 1. Executive Summary & Problem Formulation
- **Project Concept:** {project_idea}
- **Engineering Domain:** {domain}
- **Target Timeframe:** {timeframe}
- **Core Problem:** Current standard implementations lack modularity, end-to-end latency optimization, and real-time observability.
- **Key Innovation:** This project integrates modern asynchronous pipelining, modular architecture, and research-backed algorithmic baselines.

---

## 🏗️ 2. System Architecture & Data Flow
```mermaid
graph TD
    User([Student / Client UI]) --> API[API Gateway / Endpoints]
    API --> Pipeline[Core Processing Pipeline]
    Pipeline --> Cache[(Redis / In-Memory Cache)]
    Pipeline --> Storage[(PostgreSQL / Vector DB)]
    Pipeline --> Engine[Model / Processing Engine]
    Engine --> Metrics[Benchmark & Telemetry]
```

---

## 📁 3. Production Repository & Folder Structure
```
{project_idea.lower().replace(' ', '_')[:24]}/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # REST/WebSocket endpoints
│   ├── core/
│   │   ├── config.py         # Environment variables & constants
│   │   └── pipeline.py       # Core orchestration logic
│   ├── models/
│   │   └── processor.py      # AI/ML algorithms & inference
│   └── utils/
│       └── helpers.py        # Formatting & data transformations
├── tests/
│   ├── test_api.py           # Endpoint integration tests
│   └── test_pipeline.py      # Unit tests for core logic
├── .env.example              # Sample environment variables
├── Dockerfile                # Containerization specification
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation & setup guide
```

---

## 🛠️ 4. Recommended Tech Stack
| Layer | Recommended Choice | Industry Alternative | Why This Is Best |
| :--- | :--- | :--- | :--- |
| **Frontend / UI** | `Streamlit` or `React + Tailwind` | `Next.js` | Fast development with high responsiveness |
| **Backend / API** | `Python FastAPI` | `Express.js / Go` | Native async support and seamless ML integration |
| **Database** | `PostgreSQL` + `ChromaDB` | `MongoDB` | Strong consistency with vector search support |
| **Compute / AI** | `PyTorch` / `Gemini API` | `HuggingFace` | High throughput and state-of-the-art accuracy |
| **Deployment** | `Docker` + `Render / AWS` | `Vercel` | Reproducible builds with zero dependency drift |

---

## 💻 6. Starter Boilerplate Code (`src/core/pipeline.py`)
```python
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectEngine:
    # Core processing engine for this project

    def __init__(self, config=None):
        self.config = config or dict()
        logger.info("Initializing project engine...")

    def execute_pipeline(self, input_data):
        # Process input data through the end-to-end pipeline
        logger.info("Processing input payload...")
        
        # 1. Validation & Preprocessing
        processed = self._preprocess(input_data)
        
        # 2. Core Model Inference / Business Logic
        result = self._infer(processed)
        
        # 3. Post-processing & Output Structuring
        return dict(status="success", result=result)

    def _preprocess(self, data):
        return dict(cleaned=data)

    def _infer(self, data):
        return dict(prediction="Output generated based on baseline")

if __name__ == "__main__":
    engine = ProjectEngine()
    output = engine.execute_pipeline(dict(query="Sample test payload"))
    print("Execution output:", output)
```

---

{papers_md}

## ⚠️ 8. Common Pitfalls & Edge Cases
1. **Unbounded Latency:** Failure to implement asynchronous timeouts and retries on external API/model calls.
2. **Data Leakage & Overfitting:** Testing algorithms on unrepresentative datasets without cross-validation.
3. **Hardcoded Secrets:** Storing API keys or credentials directly in source files instead of using `.env`.

---

## 🎓 9. Viva / Interview Defense & Resume Bullets
- **Q1: Why did you choose this architecture over a monolithic approach?**
  - *Answer:* The modular design separates API routing from compute-heavy inference, ensuring that failures in model execution don't crash the web service.
- **Q2: How do you evaluate and benchmark the system's performance?**
  - *Answer:* We track throughput (requests/sec), latency (p95 response time), and model precision/recall against standard benchmarks.
- **Resume Impact:**
  - *Architected `{project_idea}` utilizing modern asynchronous design, reducing end-to-end latency by 35%.*
  - *Integrated peer-reviewed research methodologies from ArXiv, ensuring production compliance and benchmark validation.*
"""
