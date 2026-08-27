# Complete Outlook MCP Server Setup Guide

This document provides comprehensive setup instructions for the Outlook MCP server project.

## Project Overview

This MCP server integrates Microsoft Outlook with Hermes Agent, providing tools for email, calendar, task, contact, and outreach management through the Microsoft Graph API.

## Prerequisites

1. **Microsoft 365 Account** - You need a Microsoft 365 account with Outlook
2. **Azure AD App Registration** - You need to register an app in Azure AD
3. **Python 3.10+** - Python 3.10 or higher
4. **Hermes Agent** - Hermes Agent installed and configured

## Step 1: Register Azure AD App

### Detailed Azure AD App Registration Guide

Follow these steps to create your Azure AD application:

1. **Sign in to Azure Portal**
   - Go to [https://portal.azure.com](https://portal.azure.com)
   - Sign in with your Microsoft 365 account

2. **Create New App Registration**
   - Search for "Azure Active Directory" and click on it
   - In the left menu, click "App registrations"
   - Click "New registration"
   - Fill in the form:
     - **Name**: Enter a descriptive name (e.g., "Hermes Outlook MCP Server")
     - **Supported account types**: Select "Accounts in this organizational directory only (Single tenant)"
     - **Redirect URI**: Leave blank (we'll use client credentials flow)
   - Click "Register"

3. **Note Your App Details**
   - **Application (client) ID**: This is your CLIENT_ID
   - **Directory (tenant) ID**: This is your TENANT_ID
   - Copy these values - you'll need them later

4. **Configure API Permissions**
   - In your app registration, go to "API permissions"
   - Click "Add a permission"
   - Select "Microsoft Graph"
   - Select "Application permissions" (for server-to-server communication)
   - Add the following permissions:
     - `Mail.ReadWrite`
     - `Calendars.ReadWrite`
     - `Tasks.ReadWrite`
     - `Contacts.ReadWrite`
     - `Files.ReadWrite`
     - `Sites.ReadAll` (for SharePoint access)
   - Click "Grant admin consent" (requires admin approval)

5. **Create a Client Secret**
   - In your app registration, go to "Certificates & secrets"
   - Click "New client secret"
   - Give it a description (e.g., "Hermes MCP Server Secret")
   - Set an expiration (6 months to 1 year recommended)
   - Click "Add"
   - **IMPORTANT**: Copy the secret value immediately - it will only be shown once!

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements.txt file contains:
- `msal>=1.20.0` - Microsoft Authentication Library
- `requests>=2.31.0` - HTTP library
- `mcp>=0.15.0` - Model Context Protocol library
- `python-dotenv>=1.0.0` - Environment variables

## Step 3: Configure Environment Variables

Create a `.env` file in the project directory with the following variables:

```bash
# Azure AD Configuration
AZURE_CLIENT_ID=your-client-id-here
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_SECRET=your-client-secret-here

# SharePoint Configuration (optional but recommended)
SHAREPOINT_SITE_ID=your-site-id-here
SHAREPOINT_DRIVE_ID=your-drive-id-here
OUTREACH_WORKBOOK_PATH=OutreachTracking.xlsx
OUTREACH_WORKSHEET_NAME=Outreach
```

**Important Security Notes:**
- Never commit your .env file to version control
- Store your client secret securely (password manager recommended)
- Use environment variables in production

## Step 4: Set Up the Project Structure

The project has the following structure:

```
outlook_mcp_server/
├── requirements.txt                    # Dependencies
├── server.py                           # Main MCP server
├── auth.py                             # Authentication module
├── graph_client.py                     # Graph API client
├── config.py                           # Configuration module
├── tools/                              # Tool modules
│   ├── email_tools.py                  # Email management
│   ├── calendar_tools.py               # Calendar management
│   ├── task_tools.py                   # Task management
│   ├── contact_tools.py                # Contact management
│   └── outreach_tools.py                # Outreach tracking
├── SETUP_GUIDE.md                      # This guide
└── azure-ad-app-registration-guide.md   # Azure AD registration guide
```

## Step 5: Configure Hermes Agent MCP Server

Add the Outlook MCP server to your Hermes Agent configuration:

1. Edit your Hermes Agent config file (`~/.hermes/config.yaml`)
2. Add the MCP server configuration:

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

3. Restart Hermes Agent:

```bash
hermes
```

## Step 6: Test the Integration

After setup, test the integration by asking Hermes Agent:

- "Get my recent emails"
- "Create a calendar event for tomorrow at 10am"
- "What are my tasks for this week?"
- "Show my contacts"
- "Track outreach to John Doe"

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check that client ID, tenant ID, and client secret are correct
   - Ensure admin consent was granted
   - Verify app registration permissions

2. **Missing Permissions**
   - Go to Azure Portal > Azure Active Directory > App registrations
   - Select your app > API permissions
   - Ensure all required permissions are present and granted

3. **SharePoint Integration Issues**
   - Verify SharePoint site ID and drive ID
   - Ensure `Sites.ReadAll` permission is granted
   - Check SharePoint workbook exists and is accessible

4. **Tool Not Found**
   - Ensure the MCP server is running
   - Verify Hermes Agent configuration
   - Restart Hermes Agent after changes

### Debugging Steps

1. **Check Server Logs**
   ```bash
   # Run server with debug output
   python server.py
   ```

2. **Verify Environment Variables**
   ```python
   import os
   print("AZURE_CLIENT_ID:", os.getenv("AZURE_CLIENT_ID"))
   print("AZURE_TENANT_ID:", os.getenv("AZURE_TENANT_ID"))
   ```

3. **Test Authentication**
   ```python
   from auth import OutlookAuth
   auth = OutlookAuth()
   print("Is authenticated:", auth.is_authenticated())
   ```

## Security Best Practices

1. **Never hardcode credentials** - always use environment variables
2. **Use least privilege permissions** - only grant permissions needed
3. **Regular secret rotation** - update client secrets periodically
4. **Monitor API usage** - check Azure Portal for usage statistics
5. **Use HTTPS in production** - ensure secure communication
6. **Implement proper error handling** - don't expose sensitive error messages

## Advanced Configuration

### Custom Folders

Modify `config.py` to customize default folders:

```python
DEFAULT_EMAIL_FOLDER = "inbox"
DEFAULT_TASK_FOLDER = "tasks"
DEFAULT_CONTACT_FOLDER = "contacts"
```

### SharePoint Integration

For advanced SharePoint scenarios:
- Use different workbook templates
- Configure multiple worksheets for different data types
- Implement data validation and error handling

### Performance Optimization

- Enable token caching for better performance
- Use connection pooling
- Implement batch operations where possible
- Consider using Azure AD conditional access

## License

MIT License

## Support

For issues or questions:
1. Check the documentation
2. Review Azure Portal logs
3. Verify Microsoft Graph API documentation
4. Check Hermes Agent MCP server documentation

## Next Steps

1. Complete Azure AD app registration
2. Install dependencies
3. Configure environment variables
4. Test the integration
5. Customize for your specific needs

This setup guide should get you started with the Outlook MCP server. Once authenticated, you'll have full access to Outlook, SharePoint, and Microsoft Graph API capabilities through Hermes Agent.