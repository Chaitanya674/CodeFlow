# CodeFlow

CodeFlow is an intelligent, multi-agent AI system designed to automate the documentation process for software projects. It analyzes your GitHub repository, generates architectural diagrams, drafts comprehensive documentation, and publishes it directly to Confluence after human approval.

Built with the **Agent Development Kit (ADK)** and powered by **Google Gemini** models, CodeFlow orchestrates a team of specialized AI agents to ensure your documentation is accurate, visual, and up-to-date.

## 🚀 Features

-   **Automated Repository Analysis**: Scans your GitHub repository to understand the codebase structure and logic.
-   **Architecture Visualization**: Generates Mermaid diagrams to visualize the system architecture.
-   **Confluence Integration**:
    -   Drafts detailed documentation pages.
    -   Embeds architecture diagrams (rendered via Kroki).
    -   Publishes directly to your Confluence space.
-   **Human-in-the-Loop**: Includes an interactive approval workflow. You review the draft and diagrams before anything is published.
-   **Multi-Agent Architecture**:
    -   **Repo Architect**: Analyzes code and designs architecture.
    -   **Flow Creator**: Creates visual diagrams.
    -   **Confluence Drafter**: Writes the documentation content.
    -   **Orchestrator**: Manages the entire workflow.

## 🛠️ Prerequisites

-   Python 3.10+
-   A Google Cloud Project with Gemini API access.
-   A GitHub account and Personal Access Token.
-   An Atlassian (Confluence) account and API Token.

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

-   `tools/agent.py`: Defines the agents (Chat, Repo, Flow Creator, Confluence) and the main application entry point.
-   `tools/tools.py`: Implements the tools for GitHub, Confluence, and diagram generation.
-   `tools/config.py`: Handles configuration and environment variables.
-   `tools/prompts.py`: Contains the system instructions and prompts for each agent.
-   `agents/`: (Directory for additional agent modules).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
