import json
from google.adk.tools import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from atlassian import Confluence
from tools.config import CONFLUENCE_API_KEY, CONFLUENCE_DOMAIN, CONFLUENCE_EMAIL, GITHUB_API_KEY

# --------------------------
# Setup: GitHub MCP Server
# --------------------------
github_tools = McpToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer "+ GITHUB_API_KEY,
                    "X-MCP-Toolsets": "all",
                    "X-MCP-Readonly": "true"
                },
            )
)
# --------------------------
# Setup: Confluence Connection
# --------------------------
confluence = Confluence(
    url=CONFLUENCE_DOMAIN,
    username= CONFLUENCE_EMAIL,
    password=CONFLUENCE_API_KEY
)

# --------------------------
# Publishing Tool
# --------------------------
def publish_to_confluence(space_key: str, title: str, content: str) -> str:
    try:
            existing_page = confluence.get_page_by_title(space_key, title)
            
            if existing_page:
                page_id = existing_page['id']
                confluence.update_page(
                    page_id=page_id,
                    title=title,
                    body=content,
                    representation='storage'
                )
                return f"✅ Success! Page '{title}' updated. URL: {CONFLUENCE_DOMAIN}/wiki/spaces/{space_key}/pages/{page_id}"
            else:
                status = confluence.create_page(
                    space=space_key,
                    title=title,
                    body=content,
                    representation='storage'
                )
                page_id = status['id']
                return f"✅ Success! Page '{title}' created. URL: {CONFLUENCE_DOMAIN}/wiki/spaces/{space_key}/pages/{page_id}"

    except Exception as e:
        return f"❌ Error publishing to Confluence: {str(e)}"

# --------------------------
# Human Loop Tool (CORRECTED)
# --------------------------
def ask_human_approval(tool_context: ToolContext, draft: str) -> str:
    """
    Presents the current draft to the human user.
    IMPORTANT: Returns a JSON STRING using json.dumps, never a raw dictionary.
    """
    tool_confirmation = tool_context.tool_confirmation
    
    # 1. Request Confirmation if not yet received
    if not tool_confirmation:
        tool_context.request_confirmation(
            hint="Please review the draft and select APPROVE or REJECT.",
            payload={
                "approve": "",  # Expected values: "APPROVE" or "REJECT"
                "title": "",
                "space_key": "",
                "feedback": ""
            }
        )
        return json.dumps({
            "status": "pending",
            "message": "Waiting for user confirmation"
        })
    
    # 2. Process the User's Response
    # We use str() to be safe, and .get() to pull from the root of the JSON
    is_approved = tool_confirmation.payload["approve"].strip().upper() == "APPROVE"  
    print(" ----====================  User Approval Status:", tool_confirmation.payload["approve"].strip().upper())
    if is_approved:
        try:
            space_key = tool_confirmation.payload["space_key"].strip()
            title = tool_confirmation.payload["title"].strip()
            
            if not space_key or not title:
                return json.dumps({
                    "status": "error",
                    "message": "Missing space_key or title for publishing."
                })
            
            # Publish
            publish_result = publish_to_confluence(space_key, title, draft)
            
            return json.dumps({
                "status": "success",
                "message": publish_result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error publishing to Confluence: {str(e)}"
            })
    else:
        # User Rejected
        feedback = tool_confirmation.payload["feedback"]
        return json.dumps({
            "status": "rejected",
            "message": f"Draft rejected by user. Feedback: {feedback}"
        })