"""
Main MCP Server for Outlook Integration.
Provides MCP tools for email, calendar, task, contact, and outreach management.
"""

import json
import logging
from typing import Any, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

from config import get_azure_config
from auth import auth
from graph_client import graph_client

# Import tool modules
from email_tools import (
    get_emails,
    organize_emails,
    create_email,
    search_emails,
    get_mail_folders,
    get_email,
)
from calendar_tools import (
    get_calendar_events,
    get_calendar_event,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
)
from task_tools import (
    get_tasks,
    get_task,
    create_task,
    update_task,
    complete_task,
)
from contact_tools import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
)
from outreach_tools import (
    track_outreach,
    get_outreach_status,
    update_outreach,
    get_outreach_report,
    get_outreach_list,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("outlook-mcp-server")


# ==================== TOOL DEFINITIONS ====================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools."""
    tools = [
        # Email Tools
        Tool(
            name="get_emails",
            description="Read emails from Outlook. Returns a list of emails with subject, sender, date, and preview.",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder": {
                        "type": "string",
                        "description": "Mail folder name or ID (default: 'inbox')",
                        "default": "inbox",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Number of emails to retrieve (default: 10)",
                        "default": 10,
                    },
                    "filter_query": {
                        "type": "string",
                        "description": "OData filter query (optional)",
                    },
                },
            },
        ),
        Tool(
            name="get_email",
            description="Get a specific email by ID with full body content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The ID of the email to retrieve",
                    },
                },
                "required": ["email_id"],
            },
        ),
        Tool(
            name="organize_emails",
            description="Move an email to a specific folder.",
            inputSchema={
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The ID of the email to move",
                    },
                    "folder_id": {
                        "type": "string",
                        "description": "The ID of the destination folder",
                    },
                },
                "required": ["email_id", "folder_id"],
            },
        ),
        Tool(
            name="create_email",
            description="Create and send an email.",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of recipient email addresses",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject",
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body (HTML)",
                    },
                    "cc": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of CC recipient email addresses (optional)",
                    },
                },
                "required": ["to", "subject", "body"],
            },
        ),
        Tool(
            name="search_emails",
            description="Search emails by query string.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                    },
                    "folder": {
                        "type": "string",
                        "description": "Mail folder to search in (default: 'inbox')",
                        "default": "inbox",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_mail_folders",
            description="Get all mail folders in Outlook.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        # Calendar Tools
        Tool(
            name="get_calendar_events",
            description="Get calendar events within a date range.",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in ISO format (e.g., '2024-01-01T00:00:00Z')",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in ISO format (e.g., '2024-01-31T23:59:59Z')",
                    },
                },
                "required": ["start_date", "end_date"],
            },
        ),
        Tool(
            name="get_calendar_event",
            description="Get a specific calendar event by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to retrieve",
                    },
                },
                "required": ["event_id"],
            },
        ),
        Tool(
            name="create_calendar_event",
            description="Create a calendar event.",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Event subject/title",
                    },
                    "start": {
                        "type": "string",
                        "description": "Start time in ISO format (e.g., '2024-01-01T10:00:00Z')",
                    },
                    "end": {
                        "type": "string",
                        "description": "End time in ISO format (e.g., '2024-01-01T11:00:00Z')",
                    },
                    "location": {
                        "type": "string",
                        "description": "Event location (optional)",
                    },
                    "attendees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of attendee email addresses (optional)",
                    },
                },
                "required": ["subject", "start", "end"],
            },
        ),
        Tool(
            name="update_calendar_event",
            description="Update a calendar event.",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to update",
                    },
                    "subject": {
                        "type": "string",
                        "description": "New subject (optional)",
                    },
                    "start": {
                        "type": "string",
                        "description": "New start time in ISO format (optional)",
                    },
                    "end": {
                        "type": "string",
                        "description": "New end time in ISO format (optional)",
                    },
                    "location": {
                        "type": "string",
                        "description": "New location (optional)",
                    },
                },
                "required": ["event_id"],
            },
        ),
        Tool(
            name="delete_calendar_event",
            description="Delete a calendar event.",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to delete",
                    },
                },
                "required": ["event_id"],
            },
        ),
        # Task Tools
        Tool(
            name="get_tasks",
            description="Get tasks from Outlook.",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder": {
                        "type": "string",
                        "description": "Task folder name or ID (default: 'tasks')",
                        "default": "tasks",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Number of tasks to retrieve (default: 10)",
                        "default": 10,
                    },
                },
            },
        ),
        Tool(
            name="get_task",
            description="Get a specific task by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to retrieve",
                    },
                },
                "required": ["task_id"],
            },
        ),
        Tool(
            name="create_task",
            description="Create a new task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Task subject/title",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in ISO format (e.g., '2024-01-01T00:00:00Z')",
                    },
                    "body": {
                        "type": "string",
                        "description": "Task description/body (optional)",
                    },
                },
                "required": ["subject", "due_date"],
            },
        ),
        Tool(
            name="update_task",
            description="Update an existing task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update",
                    },
                    "subject": {
                        "type": "string",
                        "description": "New subject (optional)",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in ISO format (optional)",
                    },
                    "body": {
                        "type": "string",
                        "description": "New description/body (optional)",
                    },
                },
                "required": ["task_id"],
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to mark as complete",
                    },
                },
                "required": ["task_id"],
            },
        ),
        # Contact Tools
        Tool(
            name="get_contacts",
            description="Get contacts from Outlook.",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder": {
                        "type": "string",
                        "description": "Contact folder name or ID (default: 'contacts')",
                        "default": "contacts",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Number of contacts to retrieve (default: 10)",
                        "default": 10,
                    },
                },
            },
        ),
        Tool(
            name="get_contact",
            description="Get a specific contact by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The ID of the contact to retrieve",
                    },
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="create_contact",
            description="Create a new contact.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Contact display name",
                    },
                    "email": {
                        "type": "string",
                        "description": "Contact email address",
                    },
                    "phone": {
                        "type": "string",
                        "description": "Contact phone number (optional)",
                    },
                },
                "required": ["name", "email"],
            },
        ),
        Tool(
            name="update_contact",
            description="Update an existing contact.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The ID of the contact to update",
                    },
                    "name": {
                        "type": "string",
                        "description": "New display name (optional)",
                    },
                    "email": {
                        "type": "string",
                        "description": "New email address (optional)",
                    },
                    "phone": {
                        "type": "string",
                        "description": "New phone number (optional)",
                    },
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="delete_contact",
            description="Delete a contact.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The ID of the contact to delete",
                    },
                },
                "required": ["contact_id"],
            },
        ),
        # Outreach Tools
        Tool(
            name="track_outreach",
            description="Track outreach to an individual.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the individual",
                    },
                    "email": {
                        "type": "string",
                        "description": "Email address of the individual",
                    },
                    "status": {
                        "type": "string",
                        "description": "Outreach status (e.g., 'initial', 'follow_up', 'completed', 'no_response')",
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional notes about the outreach (optional)",
                    },
                },
                "required": ["name", "email", "status"],
            },
        ),
        Tool(
            name="get_outreach_status",
            description="Get the status of outreach to an individual.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the individual to check",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="update_outreach",
            description="Update outreach status for an individual.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the individual",
                    },
                    "status": {
                        "type": "string",
                        "description": "New outreach status (optional)",
                    },
                    "notes": {
                        "type": "string",
                        "description": "New notes (optional)",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="get_outreach_report",
            description="Generate an outreach report with statistics and recent activity.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_outreach_list",
            description="Get a list of all outreach records, optionally filtered by status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status_filter": {
                        "type": "string",
                        "description": "Filter by status (optional)",
                    },
                },
            },
        ),
    ]
    
    return tools


# ==================== TOOL HANDLERS ====================

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "get_emails":
            result = get_emails(
                folder=arguments.get("folder", "inbox"),
                top=arguments.get("top", 10),
                filter_query=arguments.get("filter_query"),
            )
        elif name == "get_email":
            result = get_email(email_id=arguments["email_id"])
        elif name == "organize_emails":
            result = organize_emails(
                email_id=arguments["email_id"],
                folder_id=arguments["folder_id"],
            )
        elif name == "create_email":
            result = create_email(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"],
                cc=arguments.get("cc"),
            )
        elif name == "search_emails":
            result = search_emails(
                query=arguments["query"],
                folder=arguments.get("folder", "inbox"),
            )
        elif name == "get_mail_folders":
            result = get_mail_folders()
        elif name == "get_calendar_events":
            result = get_calendar_events(
                start_date=arguments["start_date"],
                end_date=arguments["end_date"],
            )
        elif name == "get_calendar_event":
            result = get_calendar_event(event_id=arguments["event_id"])
        elif name == "create_calendar_event":
            result = create_calendar_event(
                subject=arguments["subject"],
                start=arguments["start"],
                end=arguments["end"],
                location=arguments.get("location", ""),
                attendees=arguments.get("attendees"),
            )
        elif name == "update_calendar_event":
            result = update_calendar_event(
                event_id=arguments["event_id"],
                subject=arguments.get("subject"),
                start=arguments.get("start"),
                end=arguments.get("end"),
                location=arguments.get("location"),
            )
        elif name == "delete_calendar_event":
            result = delete_calendar_event(event_id=arguments["event_id"])
        elif name == "get_tasks":
            result = get_tasks(
                folder=arguments.get("folder", "tasks"),
                top=arguments.get("top", 10),
            )
        elif name == "get_task":
            result = get_task(task_id=arguments["task_id"])
        elif name == "create_task":
            result = create_task(
                subject=arguments["subject"],
                due_date=arguments["due_date"],
                body=arguments.get("body", ""),
            )
        elif name == "update_task":
            result = update_task(
                task_id=arguments["task_id"],
                subject=arguments.get("subject"),
                due_date=arguments.get("due_date"),
                body=arguments.get("body"),
            )
        elif name == "complete_task":
            result = complete_task(task_id=arguments["task_id"])
        elif name == "get_contacts":
            result = get_contacts(
                folder=arguments.get("folder", "contacts"),
                top=arguments.get("top", 10),
            )
        elif name == "get_contact":
            result = get_contact(contact_id=arguments["contact_id"])
        elif name == "create_contact":
            result = create_contact(
                name=arguments["name"],
                email=arguments["email"],
                phone=arguments.get("phone"),
            )
        elif name == "update_contact":
            result = update_contact(
                contact_id=arguments["contact_id"],
                name=arguments.get("name"),
                email=arguments.get("email"),
                phone=arguments.get("phone"),
            )
        elif name == "delete_contact":
            result = delete_contact(contact_id=arguments["contact_id"])
        elif name == "track_outreach":
            result = track_outreach(
                name=arguments["name"],
                email=arguments["email"],
                status=arguments["status"],
                notes=arguments.get("notes", ""),
            )
        elif name == "get_outreach_status":
            result = get_outreach_status(name=arguments["name"])
        elif name == "update_outreach":
            result = update_outreach(
                name=arguments["name"],
                status=arguments.get("status"),
                notes=arguments.get("notes"),
            )
        elif name == "get_outreach_report":
            result = get_outreach_report()
        elif name == "get_outreach_list":
            result = get_outreach_list(
                status_filter=arguments.get("status_filter"),
            )
        else:
            return CallToolResult(
                content=[TextContent(text=f"Unknown tool: {name}")],
                isError=True,
            )
        
        return CallToolResult(
            content=[TextContent(text=result)],
            isError=False,
        )
    
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return CallToolResult(
            content=[TextContent(text=json.dumps({"error": str(e)}))],
            isError=True,
        )


# ==================== SERVER STARTUP ====================

async def main():
    """Run the MCP server."""
    logger.info("Starting Outlook MCP Server...")
    
    # Verify authentication
    config = get_azure_config()
    if not config["client_id"] or not config["tenant_id"]:
        logger.warning("Azure AD credentials not configured. Please set AZURE_CLIENT_ID and AZURE_TENANT_ID.")
    
    logger.info("Outlook MCP Server started successfully.")
    
    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())