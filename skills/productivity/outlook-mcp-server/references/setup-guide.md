# Outlook MCP Server Setup Guide

## Overview

This MCP server integrates Microsoft Outlook with Hermes Agent, providing tools for email, calendar, task, contact, and outreach management.

## Prerequisites

1. **Microsoft 365 Account** - You need a Microsoft 365 account with Outlook
2. **Azure AD App Registration** - You need to register an app in Azure AD
3. **Python 3.10+** - Python 3.10 or higher
4. **Hermes Agent** - Hermes Agent installed on your system

## Step 1: Register Azure AD App

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in the details:
   - **Name**: `Outlook MCP Server` (or any name you prefer)
   - **Supported account types**: Choose "Accounts in this organizational directory only"
   - **Redirect URI**: Leave blank (we'll use client credentials)
5. Click **Register**
6. Copy the **Application (client) ID** - you'll need this later

## Step 2: Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph** > **Application permissions**
4. Add the following permissions:
   - `Mail.ReadWrite`
   - `Calendars.ReadWrite`
   - `Tasks.ReadWrite`
   - `Contacts.ReadWrite`
   - `Files.ReadWrite`
5. Click **Grant admin consent** (requires admin approval)

## Step 3: Create Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Enter a description and expiration period
4. Click **Add**
5. Copy the **Client secret value** - you'll need this later

## Step 4: Configure Environment Variables

Create a `.env` file in the project directory with the following variables:

```bash
# Azure AD Configuration
AZURE_CLIENT_ID=your-client-id-here
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_SECRET=your-client-secret-here

# SharePoint/Excel Configuration (optional)
SHAREPOINT_SITE_ID=your-site-id-here
SHAREPOINT_DRIVE_ID=your-drive-id-here
OUTREACH_WORKBOOK_PATH=OutreachTracking.xlsx
OUTREACH_WORKSHEET_NAME=Outreach
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Configure Hermes Agent

Add the MCP server to your Hermes Agent configuration. Edit `~/.hermes/config.yaml` and add:

```yaml
mcp_servers:
  outlook:
    command: "python"
    args: ["path/to/outlook_mcp_server/server.py"]
    env:
      AZURE_CLIENT_ID: "your-client-id-here"
      AZURE_TENANT_ID: "your-tenant-id-here"
      AZURE_CLIENT_SECRET: "your-client-secret-here"
```

## Step 7: Restart Hermes Agent

```bash
hermes
```

## Step 8: Test the Integration

Ask Hermes Agent to use the Outlook tools:

- "Get my recent emails"
- "Create a calendar event for tomorrow at 10am"
- "Track outreach to John Doe"
- "Get my task list"

## Troubleshooting

### Authentication Issues
- Ensure your Azure AD app has the correct permissions
- Verify that admin consent was granted for the app permissions
- Check that the client secret hasn't expired

### Connection Issues
- Verify that the MCP server is running
- Check that the environment variables are correctly set
- Ensure that the Python environment has all dependencies installed

### Tool Not Found
- Ensure the MCP server is listed in the Hermes configuration
- Restart Hermes Agent after adding the server
- Check that the server name matches what's in the configuration

## Security Notes

- Never commit your Azure AD credentials to version control
- Use environment variables or a `.env` file for credentials
- Regularly rotate your client secrets
- Review the permissions granted to the app and remove any unused ones

## Customization

### Adding Custom Folders
You can customize the default folders by modifying the `config.py` file:

```python
DEFAULT_EMAIL_FOLDER = "inbox"
DEFAULT_TASK_FOLDER = "tasks"
DEFAULT_CONTACT_FOLDER = "contacts"
```

### Custom SharePoint Integration
If you need to use a different SharePoint site or workbook, update the SharePoint configuration in `config.py`.

## API Reference

### Email Tools
- `get_emails(folder, top, filter)` - Read emails from Outlook
- `get_email(email_id)` - Get a specific email
- `organize_emails(email_id, folder_id)` - Move emails to folders
- `create_email(to, subject, body, cc)` - Create and send emails
- `search_emails(query, folder)` - Search emails by query
- `get_mail_folders()` - Get all mail folders

### Calendar Tools
- `get_calendar_events(start_date, end_date)` - Get calendar events
- `get_calendar_event(event_id)` - Get a specific calendar event
- `create_calendar_event(subject, start, end, location, attendees)` - Create calendar event
- `update_calendar_event(event_id, subject, start, end, location)` - Update calendar event
- `delete_calendar_event(event_id)` - Delete a calendar event

### Task Tools
- `get_tasks(folder, top)` - Get tasks
- `get_task(task_id)` - Get a specific task
- `create_task(subject, due_date, body)` - Create a task
- `update_task(task_id, subject, due_date, body)` - Update a task
- `complete_task(task_id)` - Mark task as complete

### Contact Tools
- `get_contacts(folder, top)` - Get contacts
- `get_contact(contact_id)` - Get a specific contact
- `create_contact(name, email, phone)` - Create a contact
- `update_contact(contact_id, name, email, phone)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact

### Outreach Tools
- `track_outreach(name, email, status, notes)` - Track outreach
- `get_outreach_status(name)` - Get outreach status
- `update_outreach(name, status, notes)` - Update outreach status
- `get_outreach_report()` - Generate outreach report
- `get_outreach_list(status_filter)` - Get outreach list

## License

MIT License - See LICENSE file for details.