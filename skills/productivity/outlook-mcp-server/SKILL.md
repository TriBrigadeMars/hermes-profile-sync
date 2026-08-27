---
name: outlook-mcp-server
description: "Outlook MCP server for email, calendar, tasks, contacts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [outlook, mcp, email, calendar, tasks, contacts, outreach, microsoft-365]
---

# Outlook MCP Server

A comprehensive MCP server for integrating Microsoft Outlook with Hermes Agent.

## When to Use
Use when the user needs to integrate Outlook, calendar, tasks, contacts, or outreach tracking with Hermes Agent via MCP.

## Files
- `requirements.txt` - Dependencies
- `server.py` - Main MCP server
- `auth.py` - Authentication module (MSAL)
- `graph_client.py` - Microsoft Graph API client
- `config.py` - Configuration module
- `tools/email_tools.py` - Email management tools
- `tools/calendar_tools.py` - Calendar management tools
- `tools/task_tools.py` - Task management tools
- `tools/contact_tools.py` - Contact management tools
- `tools/outreach_tools.py` - Outreach tracking tools
- `references/SETUP_GUIDE.md` - Complete setup guide
- `references/azure-ad-app-registration-guide.md` - Azure AD app registration guide

## Setup
1. Register Azure AD app with required permissions
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run: `python server.py`
5. Review SETUP_GUIDE.md for detailed instructions
6. Review azure-ad-app-registration-guide.md for Azure AD setup