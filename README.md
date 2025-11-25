Codeflow 🚀
===========

**Bridging the Gap Between Code, Product, and People.**

> _Automated Technical Documentation, Architecture Visualization, and Knowledge Base Management powered by AI Agents._

🎯 The Mission
--------------

In fast-paced engineering teams, a silent disconnect often grows between the **Code** (what exists) and the **Business** (what is understood).

*   **Managers & Product Owners** struggle to get deep technical insights without interrupting developers.
    
*   **New Hires** waste days or weeks in repetitive "Knowledge Transfer" (KT) sessions just to set up their environment.
    
*   **Open Source Contributors** shy away from complex repositories because the learning curve is too steep.
    

**Codeflow** solves this by treating **Documentation as Code**. It employs a swarm of AI agents to reverse-engineer your repository, visualize its architecture, and publish professional, living documentation directly to Confluence.

💡 Key Features
---------------

### 1\. 🔍 Automated Repo Analysis & Visualization

Codeflow scans your entire repository structure to extract:

*   **Barebone Structure**: File trees and class hierarchies.
    
*   **Execution Flow**: Logic paths (Caller $\\rightarrow$ Callee).
    
*   **Architecture Diagrams**: Automatically generates complex **Mermaid.js** charts (Flowcharts, Sequence diagrams) and renders them as high-quality images.
    

### 2\. 📄 One-Click Confluence Pages

Stop writing docs manually. Codeflow drafts comprehensive Confluence pages including:

*   System Overviews.
    
*   Technical Architecture.
    
*   Step-by-step Logic Flows.
    
*   Embedded Diagrams.
    

### 3\. 🔄 Smart Updates & Changelogs

Documentation goes stale the moment it's written—unless it updates itself.

*   **Changelog Agent**: Scans git history to generate human-readable "Release Notes" (Features vs. Fixes).
    
*   **Smart Updater**: Intelligently appends new sections (like "Updated Features" or "New Features") to _existing_ pages without overwriting current content.
    

### 4\. 🛡️ Human-in-the-Loop Approval

AI drafts it; You own it.

*   Codeflow presents a draft before publishing.
    
*   **Refinement Loop**: Don't like the tone? Want more detail? Just ask the agent to "Redraft," and it refines the content until you click **APPROVE**.
    

🏗️ System Architecture
-----------------------

Codeflow runs on a multi-agent orchestration architecture powered by **Google Gemini 2.5**.

<img width="695" height="864" alt="Screenshot from 2025-11-26 00-29-54" src="https://github.com/user-attachments/assets/e83fc685-773f-423e-8b99-576e4196008c" />


### The Agent Squad

*   **Orchestrator**: The brain. Routes requests (Create vs. Update vs. Chat).

*   **Repo Agent**: Has Github MCP connected to answer repo related queries.    

*   **Repo Architect**: Reverse-engineers code structure.
    
*   **Flow Creator**: Writes Mermaid.js syntax for visualizations.
    
*   **Confluence Drafter**: Formats text into professional documentation.
    
*   **Updater Agent**: Merges new insights into existing live pages.
    
*   **Refiner Agent**: Handles your feedback loop.
    

🚀 Getting Started
------------------

## Prerequisites

*   Python 3.10+
    
*   Google Cloud Project (for Gemini API)
    
*   Atlassian Confluence Account (API Key + Email + Confluence Domain URL)
    
*   GitHub Copilot MCP (Model Context Protocol) Access Token
    

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd CodeFlow
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    You can install the required dependencies using the provided `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  **Environment Variables:**
    Create a `.env` file in the `tools/` directory (or the root, depending on how you run it, but `tools/config.py` looks in `tools/`).
    
    ```bash
    touch tools/.env
    ```

2.  **Add the following variables to `tools/.env`:**

    ```env
    # Google Gemini API Key
    # Note: The current config expects this specific variable name
    KAGGLE_SECRET_GEMINI_API_KEY=your_google_api_key_here

    # GitHub Configuration
    GITHUB_API_KEY=your_github_personal_access_token

    # Confluence Configuration
    CONFLUENCE_API_KEY=your_atlassian_api_token
    CONFLUENCE_EMAIL=your_email@example.com
    CONFLUENCE_DOMAIN=https://your-domain.atlassian.net
    ```

    > **Note:** To generate an Atlassian API Token, go to [Atlassian Account Settings > Security > Create and manage API tokens](https://id.atlassian.com/manage-profile/security/api-tokens).

## 🏃‍♂️ How to Run

CodeFlow is built as an ADK application. You can run it using the `adk` CLI.

1.  **Navigate to the project root:**
    ```bash
    cd CodeFlow
    ```

2.  **Run the Agent:**
    ```bash
    adk web .
    ```
    This command points `adk` to the current directory (which should contain `tools/agent.py` or be the parent of the module). If that doesn't work, try:
    ```bash
    adk web tools/agent.py
    ```

3.  **Interact with the Agent:**
    -   Open your browser and navigate to the URL provided by the `adk` output (usually `http://localhost:8000` or similar).
    -   Start a chat with the agent.
    -   Ask it to "Analyze and Create a Confluence Page for this repo : https://<link-to-any-repo>".
    -   The agent will guide you through the process, asking for approval before publishing.

## 📂 Project Structure

-   `tools/agent.py`: Defines the agents (Chat, Repo, Flow Creator, Confluence etc.) and the main application entry point.
-   `tools/tools.py`: Implements the tools for GitHub, Confluence, and diagram generation etc.
-   `tools/config.py`: Handles configuration and environment variables.
-   `tools/prompts.py`: Contains the system instructions and prompts for each agent.
-   `agents/`: (Directory for additional agent modules).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
