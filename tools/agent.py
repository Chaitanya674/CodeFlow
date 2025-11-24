from google.adk.runners import Runner
from google.adk.agents import Agent, SequentialAgent
import uuid
from google.adk.tools import AgentTool, google_search
from google.adk.models.google_llm import Gemini
from tools.tools import github_tools, ask_human_approval
from tools.config import retry_config
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.apps import App, ResumabilityConfig
from tools.prompts import ARCHITECT_SYSTEM_PROMPT, ORCHESTRATOR_PROMPT , CONFLUENCE_DRAFT_PROMPT, REFINER_PROMPT, FLOW_CREATOR_PROMPT

# Optimized model usage
model = Gemini(model="gemini-2.5-pro", retry_options=retry_config)
model_flash = Gemini(model="gemini-2.5-flash", retry_options=retry_config)
model_flash_lite = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)


# --------------------------
# Agent: Normal Chat Agent
# --------------------------
Chat_agent = Agent(
    name="chat_agent", 
    model=model_flash,
    instruction="You are a helpful assistant which can help users with code related queries. you have access to the google_search tool to answer user queries.",
    tools=[google_search],
    description="Analyzes and designs the repository architecture.",
    output_key="chat_response"
)


# --------------------------
# Agent: Repo Architect Agent
# --------------------------
Repo_agent = Agent(
    name="repo_agent",
    model=model_flash,
    instruction=ARCHITECT_SYSTEM_PROMPT,
    tools=[github_tools],
    description="Analyzes and designs the repository architecture.",
    output_key="Repo_Architecture"
)

# --------------------------
# Agent: Flow Creator Agent
# --------------------------
Flow_Creator_Agent = Agent(
    name="flow_creator_agent",
    model=model_flash_lite,
    instruction=FLOW_CREATOR_PROMPT,
    description="Creates MERMAID diagrams based on repository architecture.",
    output_key="Mermaid_Diagram"
)

# --------------------------
# Agent: Confluence Drafter
# --------------------------
Confluence_drafter = Agent(
    name="confluence_agent",
    model=model_flash,
    instruction=CONFLUENCE_DRAFT_PROMPT,
    description="Drafts Confluence documentation based on architecture and mermaid diagrams.",
    output_key="Confluence_Draft"
)

# --------------------------
# Agent: Refiner Agent
# --------------------------
Refiner_agent = Agent(
    name="refiner_agent",
    model=model_flash_lite,
    instruction=REFINER_PROMPT,
    description="Handles approval loop and publishing.",
    tools=[
        ask_human_approval,
    ],
    output_key="Published_document"
)

# --------------------------
# Agent: Confluence Agent
# --------------------------

Data_Agent = SequentialAgent(
   name="Data_agent",
   sub_agents=[Repo_agent, Flow_Creator_Agent],
   description="This is an agent that sequentially executes Repo_agent, Flow_Creator_Agent",
)


# --------------------------
# Agent: Orchestrator Agent
# --------------------------
Orchestrator_Agent = Agent(
    name="orchestrator_agent",
    model=model_flash,
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(Chat_agent),
        AgentTool(Data_Agent),
        AgentTool(Confluence_drafter),
        ask_human_approval
    ],
    description="Orchestrates the workflow between data extraction, documentation drafting, and refinement.",
    output_key="Final_Output"
)



root_agent = Orchestrator_Agent

session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///sessions.db")

app = App(
    root_agent=root_agent,
    name="tools",  # <--- Matches the URL in your logs
    resumability_config=ResumabilityConfig(is_resumable=True)
)
# 3. Initialize Runner correctly
# Note: We do NOT manually create a session here for adk web.
# adk web will create/manage sessions automatically based on the user/browser.
runner = Runner(
    app=app,
    session_service=session_service
)