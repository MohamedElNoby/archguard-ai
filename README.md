\# 🛡️ ArchGuard AI



> \*\*An AI-powered Software Architecture Review \& Adversarial Defense Platform\*\*  

> Evaluates software architecture diagrams using Gemini Vision, orchestrates real-time multi-agent jury debates, and benchmarks engineer defenses with automated Mermaid.js remediation.



\---



\## 🌟 Key Features



\- \*\*Multimodal Architecture Ingestion:\*\* Uses Gemini Vision to parse components, network links, protocols, and topology directly from uploaded diagrams.

\- \*\*Automated Risk Discovery:\*\* Uncovers single points of failure (SPOF), cascading failures, sync chaining, and insecure edge relays.

\- \*\*Adversarial Multi-Agent Jury:\*\* Real-time debate simulating three specialized engineering perspectives:

&#x20; - \*\*CyberSec:\*\* Attack surface, blast radius, encryption, and zero-trust segmentation.

&#x20; - \*\*SRE:\*\* Availability calculations ($A\_{total} = \\prod A\_i$), error budgets, retries, and cascading stalls.

&#x20; - \*\*FinOps:\*\* Idle resource lockups, auto-scaling thrashing, and unthrottled bandwidth costs.

\- \*\*Interactive Defense Arena:\*\* Allows engineers to submit targeted architectural refactorings within strict constraints.

\- \*\*Dynamic Scoring \& Mermaid Remediation:\*\* Evaluates defenses across a 5-pillar rubric and dynamically outputs a clean, interactive Mermaid flowchart representing the resilient topology.

\- \*\*Full Localization:\*\* Complete bilingual support (English \& Arabic) with real-time RTL toggling.



\---



\## 🏗️ Architecture Stack



\- \*\*Frontend:\*\* React, Vite, Tailwind CSS, Lucide Icons, Mermaid.js

\- \*\*Backend:\*\* FastAPI, Python 3.11, Google GenAI SDK (Gemini 2.5 Flash / Pro)

\- \*\*State \& Communication:\*\* REST API, client-side progressive reveal simulations



\---



\## 🚀 Quick Start



\### 1. Prerequisites

\- Python 3.11+

\- Node.js 18+ \& npm

\- Google Gemini API Key



\### 2. Backend Setup

```bash

cd backend

python -m venv venv

\# Windows:

venv\\Scripts\\activate

\# Linux/macOS:

source venv/bin/activate



pip install -r requirements.txt

cp .env.example .env

\# Set your GEMINI\_API\_KEY in .env



uvicorn app.main:app --reload --port 8000

