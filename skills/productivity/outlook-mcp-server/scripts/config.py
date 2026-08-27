"""
Configuration module for Outlook MCP Server.
Handles environment variables and configuration settings.
"""

import os
from pathlib import Path

# Azure AD Configuration
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")

# Microsoft Graph API
GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"
GRAPH_API_SCOPES = [
    "Mail.ReadWrite",
    "Calendars.ReadWrite",
    "Tasks.ReadWrite",
    "Contacts.ReadWrite",
    "Files.ReadWrite",
    "offline_access"
]

# Token cache
TOKEN_CACHE_DIR = Path.home() / ".outlook_mcp_server"
TOKEN_CACHE_FILE = TOKEN_CACHE_DIR / "token_cache.json"

# SharePoint/Excel
SHAREPOINT_SITE_ID = os.getenv("SHAREPOINT_SITE_ID", "")
SHAREPOINT_DRIVE_ID = os.getenv("SHAREPOINT_DRIVE_ID", "")
OUTREACH_WORKBOOK_PATH = os.getenv("OUTREACH_WORKBOOK_PATH", "OutreachTracking.xlsx")
OUTREACH_WORKSHEET_NAME = os.getenv("OUTREACH_WORKSHEET_NAME", "Outreach")

# Default folders
DEFAULT_EMAIL_FOLDER = "inbox"
DEFAULT_TASK_FOLDER = "tasks"
DEFAULT_CONTACT_FOLDER = "contacts"


def ensure_cache_dir():
    """Ensure the token cache directory exists."""
    TOKEN_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_azure_config():
    """Return Azure AD configuration as a dictionary."""
    return {
        "client_id": AZURE_CLIENT_ID,
        "tenant_id": AZURE_TENANT_ID,
        "client_secret": AZURE_CLIENT_SECRET,
        "scopes": GRAPH_API_SCOPES,
        "base_url": GRAPH_API_BASE_URL,
    }


def get_sharepoint_config():
    """Return SharePoint configuration as a dictionary."""
    return {
        "site_id": SHAREPOINT_SITE_ID,
        "drive_id": SHAREPOINT_DRIVE_ID,
        "workbook_path": OUTREACH_WORKBOOK_PATH,
        "worksheet_name": OUTREACH_WORKSHEET_NAME,
    }