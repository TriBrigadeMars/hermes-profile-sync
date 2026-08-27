---
name: outlook-mcp-server-project
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
description: Build complete Outlook MCP server with full project files
metadata:
  hermes:
    tags: [outlook, mcp, email, calendar, tasks, contacts, outreach]
    description: Complete Outlook MCP server project for Microsoft Graph API integration
---

# Outlook MCP Server Project

This project provides a complete Outlook MCP server for Microsoft Graph API integration.

## Project Structure

All files have been created in the `~/outlook_mcp_server/` directory:

- `requirements.txt` - Dependencies
- `server.py` - Main MCP server
- `auth.py` - Authentication module (MSAL)
- `graph_client.py` - Microsoft Graph API client
- `config.py` - Configuration module
- `tools/` directory containing:
  - `email_tools.py` - Email management tools
  - `calendar_tools.py` - Calendar management tools
  - `task_tools.py` - Task management tools
  - `contact_tools.py` - Contact management tools
  - `outreach_tools.py` - Outreach tracking tools
- `SETUP_GUIDE.md` - Setup guide
- `azure-ad-app-registration-guide.md` - Azure AD app registration guide

## Purpose

Provides Microsoft 365 integration for:
- Email management (read, organize, create, search)
- Calendar management (create, update, delete events)
- Task management (create, update, complete tasks)
- Contact management (create, update, delete contacts)
- Outreach tracking (track follow-ups with SharePoint/Excel)

## Features

Comprehensive MCP server with tools for:

### Email Tools
- `get_emails` - Read emails from Outlook
- `get_email` - Get a specific email by ID
- `organize_emails` - Move emails to folders
- `create_email` - Create and send emails
- `search_emails` - Search emails by query
- `get_mail_folders` - Get all mail folders

### Calendar Tools
- `get_calendar_events` - Get calendar events within a date range
- `get_calendar_event` - Get a specific calendar event
- `create_calendar_event` - Create a calendar event
- `update_calendar_event` - Update a calendar event
- `delete_calendar_event` - Delete a calendar event

### Task Tools
- `get_tasks` - Get tasks from Outlook
- `get_task` - Get a specific task by ID
- `create_task` - Create a new task
- `update_task` - Update an existing task
- `complete_task` - Mark a task as complete

### Contact Tools
- `get_contacts` - Get contacts from Outlook
- `get_contact` - Get a specific contact by ID
- `create_contact` - Create a new contact
- `update_contact` - Update an existing contact
- `delete_contact` - Delete a contact

### Outreach Tools
- `track_outreach` - Track outreach to an individual
- `get_outreach_status` - Get outreach status
- `update_outreach` - Update outreach status
- `get_outreach_report` - Generate outreach report
- `get_outreach_list` - Get outreach list

## Setup

1. Complete Azure AD app registration
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run the server: `python server.py`
5. Integrate with Hermes Agent MCP configuration

## Usage

Ask Hermes Agent to use any of the available tools:

- "Get my recent emails"
- "Create a calendar event for tomorrow at 10am"
- "Track outreach to John Doe"
- "Get my task list"
- "Get my contacts"

## License

MIT License