"""Subject Study Companion Agent.
Curates top YouTube channels, blogs, interactive documentation, structured syllabi,
and self-check flashcards for any academic or technical subject.
"""

import urllib.parse
from typing import Dict, Any, List
from utils.gemini_client import GeminiClient

class SubjectStudyAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def get_youtube_search_url(self, query: str) -> str:
        """Generate safe direct YouTube search link."""
        encoded = urllib.parse.quote_plus(query)
        return f"https://www.youtube.com/results?search_query={encoded}"

    def get_web_search_url(self, query: str, platform: str = "") -> str:
        """Generate safe direct web search link for documentation / blogs."""
        full_query = f"{query} {platform}".strip()
        encoded = urllib.parse.quote_plus(full_query)
        return f"https://www.google.com/search?q={encoded}"

    def curate_subject(self, subject: str, level: str = "Beginner to Intermediate", goal: str = "Comprehensive Understanding") -> str:
        """
        Analyze subject and generate complete learning package:
        YouTube channels, curated blogs/books, syllabus checklist, and interview flashcards.
        """
        if not self.client.is_configured():
            return self._generate_offline_subject_guide(subject, level, goal)

        prompt = f"""
You are an expert Senior Academic & Technical Educator. A student wants to master the subject: "{subject}".
Their current level is: {level}.
Their primary goal is: {goal}.

Generate an in-depth, high-value study guide in clean, beautifully structured GitHub-flavored Markdown. Follow this exact structure:

# 📚 Study Companion: {subject}

## 🎯 Executive Overview & What You Will Master
- A crisp 2-3 sentence overview explaining what {subject} is and why it's critical in the real world.
- Key prerequisites before diving in.

## 📺 Recommended YouTube Channels & Video Playlists
For this subject, recommend at least 4-5 of the best, most reputable YouTube channels (e.g., 3Blue1Brown, freeCodeCamp, MIT OpenCourseWare, StatQuest, Computerphile, Traversy Media, Hussein Nasser, NeetCode, CS50, or relevant domain-specific creators).
For each channel, use this format:
- **[Channel Name](https://www.youtube.com/results?search_query={urllib.parse.quote_plus(subject)}+channel)** (Level: Beginner / Intermediate / Advanced)
  - **Specialty / Style:** (e.g., Visual animations, proof-based, project-driven hands-on coding)
  - **Recommended Playlist / Series:** Name of the specific course or playlist on their channel.
  - **Why Watch:** Why this creator is ideal for this topic.

## ✍️ Curated Blogs, Documentation & Free Textbooks
Recommend 4-5 top reading resources (e.g., GeeksforGeeks, Towards Data Science, Medium publication, official docs, Stanford/MIT lecture notes, free online books like 'Eloquent JavaScript', 'OS Three Easy Pieces', etc.).
For each, provide:
- **[Resource Name / Site](https://www.google.com/search?q={urllib.parse.quote_plus(subject)}+tutorial+blog)**:
  - **Publisher / Author:** (e.g., GeeksforGeeks, Mozilla MDN, Towards Data Science, Official Docs)
  - **Type:** (e.g., Interactive Guide, In-depth Technical Blog, Free Textbook)
  - **Key Focus:** What specific concepts are best learned here.

## 🗺️ Step-by-Step Topic Syllabus & Milestone Checklist
Provide a logical topic progression (4 distinct milestones) with actionable checkboxes so the student can track their progress:
- [ ] **Milestone 1: Foundations & Core Terminology** (List 3-4 key subtopics)
- [ ] **Milestone 2: Intermediate Architecture & Mechanics** (List 3-4 key subtopics)
- [ ] **Milestone 3: Advanced Concepts & Optimization** (List 3-4 key subtopics)
- [ ] **Milestone 4: Real-World Applications & Industry Standards** (List 3-4 key subtopics)

## 💡 Quick Concept Self-Check (Test Your Understanding)
Provide 3 thought-provoking interview / conceptual questions with collapsible details:
<details>
<summary><b>Q1: Key Conceptual Question?</b></summary>
<b>Answer & Explanation:</b> Clear, intuitive explanation.
</details>

<details>
<summary><b>Q2: Common Practical / Edge Case Question?</b></summary>
<b>Answer & Explanation:</b> Clear, intuitive explanation.
</details>

<details>
<summary><b>Q3: Architectural / Why does it work this way Question?</b></summary>
<b>Answer & Explanation:</b> Clear, intuitive explanation.
</details>

Provide authentic, high-quality, actionable advice without generic filler.
"""
        system_instruction = "You are EduAgent, a world-class educational AI mentor specializing in curriculum curation, learning roadmaps, and learning resource synthesis."
        return self.client.generate(prompt, system_instruction=system_instruction)

    def _generate_offline_subject_guide(self, subject: str, level: str, goal: str) -> str:
        """Curated fallback response when running without an API key."""
        encoded = urllib.parse.quote_plus(subject)
        yt_search = f"https://www.youtube.com/results?search_query={encoded}"
        blog_search = f"https://www.google.com/search?q={encoded}+guide+tutorial+blog"
        
        return f"""
# 📚 Study Companion: {subject}
*(Running in instant preview mode. Connect your Gemini API Key in the sidebar for personalized deep-dives)*

## 🎯 Executive Overview & What You Will Master
- **Subject:** {subject}
- **Current Level Target:** {level}
- **Learning Objective:** {goal}
- **Focus:** Building deep conceptual mastery and practical intuition through top-tier video lectures, industry documentation, and milestone tracking.

---

## 📺 Recommended YouTube Channels & Video Playlists
Explore the top verified educators for **{subject}**:

1. **[MIT OpenCourseWare / Stanford Online]({yt_search}+MIT+OCW)** (Beginner to Advanced)
   - **Specialty:** Rigorous academic foundations, mathematical rigor, and university-grade lectures.
   - **Why Watch:** Gold standard for deep first-principles comprehension.

2. **[freeCodeCamp.org / Traversy Media]({yt_search}+freeCodeCamp)** (Beginner to Intermediate)
   - **Specialty:** Comprehensive zero-to-hero full courses, hands-on implementations.
   - **Why Watch:** Great for seeing end-to-end practical walkthroughs in single multi-hour sessions.

3. **[StatQuest with Josh Starmer / 3Blue1Brown]({yt_search}+visual+guide)** (All Levels)
   - **Specialty:** Crystal-clear visual intuition, breaking down complex math and mechanisms step-by-step.
   - **Why Watch:** Best for building mental models without getting lost in jargon.

4. **[NeetCode / Hussein Nasser / Computerphile]({yt_search}+computerphile)** (Intermediate to Advanced)
   - **Specialty:** Systems-level engineering, performance trade-offs, and industry interview preparation.
   - **Why Watch:** Understand how real production systems and architectures function.

👉 **[Click here to search all top YouTube courses for "{subject}"]({yt_search})**

---

## ✍️ Curated Blogs, Documentation & Free Textbooks

1. **[GeeksforGeeks & TutorialsPoint]({blog_search}+geeksforgeeks)**
   - **Type:** Structured Reference & Code Snippets
   - **Best For:** Fast lookup of syntax, standard algorithms, and interview definitions.

2. **[Towards Data Science & Medium Publications]({blog_search}+towardsdatascience)**
   - **Type:** Real-World Engineering Case Studies
   - **Best For:** Applied implementations, system benchmarks, and modern best practices.

3. **[Official Documentation & Dev.to Community]({blog_search}+official+documentation)**
   - **Type:** Authoritative Specs & Community Tips
   - **Best For:** The most up-to-date APIs, configurations, and common gotchas.

👉 **[Click here to search all verified blogs & articles for "{subject}"]({blog_search})**

---

## 🗺️ Step-by-Step Topic Syllabus & Milestone Checklist
- [ ] **Milestone 1: Fundamentals & Essential Terminology**
  - Core definitions, historical context, and primary abstractions.
  - Development/environment setup and basic tooling.
- [ ] **Milestone 2: Mechanics & Core Architecture**
  - Data structures, algorithmic operations, and internal workflows.
  - Hands-on exercises and intermediate problem-solving.
- [ ] **Milestone 3: Advanced Optimization & Edge Cases**
  - Performance profiling, memory/complexity trade-offs, and scale.
  - Handling concurrency, distributed states, or security boundaries.
- [ ] **Milestone 4: Capstone & Portfolio Application**
  - Building a real-world project applying the mastered principles.
  - Documenting findings, creating unit tests, and writing benchmarks.

---

## 💡 Quick Concept Self-Check
<details>
<summary><b>Q1: What is the primary problem {subject} solves compared to traditional alternatives?</b></summary>
<b>Insight:</b> It abstracts low-level complexities, optimizes resource utilization, and provides modular architectures that scale reliably under production workloads.
</details>

<details>
<summary><b>Q2: What is the most common pitfall beginners encounter in {subject}?</b></summary>
<b>Insight:</b> Skipping first-principles fundamentals to jump directly into high-level frameworks without understanding the underlying data flow and constraints.
</details>
"""
