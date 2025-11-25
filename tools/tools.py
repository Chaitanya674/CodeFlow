import json
import base64
import zlib
import markdown
import requests
import re 
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
# Helper: Kroki URL Generator
# --------------------------
def generate_kroki_url(mermaid_code: str) -> str:
    """
    Compresses and encodes the Mermaid code to generate a Kroki GET URL.
    Format: https://kroki.io/mermaid/png/<payload>
    """
    try:
        # 1. Encode to utf-8
        data = mermaid_code.encode('utf-8')
        
        # 2. Compress using zlib
        compressed_data = zlib.compress(data, level=9)
        
        # 3. Base64 encode (URL-safe)
        encoded_data = base64.urlsafe_b64encode(compressed_data).decode('utf-8')
        
        # 4. Construct URL
        return f"https://kroki.io/mermaid/png/{encoded_data}"
    except Exception as e:
        print(f"Error generating Kroki URL: {e}")
        return ""

# --------------------------
# Helper: URL Shortener
# --------------------------
def get_tinyurl(long_url: str) -> str:
    """
    Uses TinyURL API to shorten the long Kroki link.
    """
    try:
        api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"TinyURL failed: {response.status_code}")
            return long_url # Fallback to long URL if shortener fails
    except Exception as e:
        print(f"Error connecting to TinyURL: {e}")
        return long_url

# --------------------------
# Publishing Tool
# --------------------------
def publish_to_confluence(space_key: str, title: str, content: str) -> str:
    try:
        # 1. Get Page ID
        existing_page = confluence.get_page_by_title(space_key, title)
        if existing_page:
            page_id = existing_page['id']
        else:
            status = confluence.create_page(
                space=space_key,
                title=title,
                body="<p>Drafting content...</p>",
                representation='storage'
            )
            page_id = status['id']

        # 2. Process Mermaid Diagrams
        # We find the code block, generate a URL, shorten it, and replace it with an <img> tag.
        mermaid_pattern = r"```\s*mermaid\s*([\s\S]*?)```"
        
        def replace_with_link(match):
            mermaid_code = match.group(1).strip()
            print("Found Mermaid diagram, generating link...")
            
            # Generate the long Kroki URL
            long_url = generate_kroki_url(mermaid_code)
            
            # Shorten it
            final_url = get_tinyurl(long_url)
            
            # Return an HTML image tag
            return f'<img src="{final_url}" alt="Architecture Diagram" />'

        # Regex substitution to swap code blocks for image tags
        content_with_images = re.sub(mermaid_pattern, replace_with_link, content, flags=re.DOTALL)

        # 3. Convert the rest of Markdown to HTML
        final_html = markdown.markdown(content_with_images)

        # 4. Update Page
        confluence.update_page(
            page_id=page_id,
            title=title,
            body=final_html, 
            representation='storage'
        )
        
        return f"✅ Success! Page '{title}' updated with embedded images. URL: {CONFLUENCE_DOMAIN}/wiki/spaces/{space_key}/pages/{page_id}"

    except Exception as e:
        return f"❌ Error publishing to Confluence: {str(e)}"
    

# --------------------------
# Human Loop Tool
# --------------------------
def ask_human_approval(tool_context: ToolContext, draft: str) -> str:
    """
    Presents the current draft to the human user.
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
    is_approved = tool_confirmation.payload["approve"].strip().upper() == "APPROVE"  
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