---
name: azure-ad-app-registration
description: "Set up Azure AD app registration for Microsoft Graph API."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [azure, microsoft, graph-api, oauth, app-registration]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [google-workspace]
---

# Azure AD App Registration for Microsoft Graph API

Guide for setting up an Azure AD app registration to access Microsoft Graph API (Outlook, Calendar, Tasks, Contacts, SharePoint).

## When to Use
- When you need to integrate Microsoft 365 services with Hermes Agent MCP server
- When you want to access Outlook, Calendar, Tasks, Contacts, or SharePoint via API
- When setting up a Microsoft Graph API connection for the first time

## Prerequisites
- A Microsoft 365 account (Work or School account, not personal)
- Access to Azure Portal (https://portal.azure.com)
- Administrator access to your Microsoft 365 tenant (for admin consent)
- Node.js or Python installed (for MCP server)
- Hermes Agent installed and configured

## Step-by-Step Guide

### Step 1: Sign in to Azure Portal
1. Open your web browser and go to https://portal.azure.com
2. Sign in with your Microsoft 365 account (your work email)
3. If prompted, complete multi-factor authentication

### Step 2: Register a New App
1. In the Azure Portal search bar, type "Azure Active Directory" and click on it
2. In the left menu, click "App registrations"
3. Click "New registration"
4. Fill in the form:
   - **Name**: Give your app a descriptive name (e.g., "Hermes Graph API Integration" or "Public Health Outreach Manager")
   - **Supported account types**: Select "Accounts in this organizational directory only (Single tenant)"
   - **Redirect URI**: Select "Web" and enter: `http://localhost:3000/callback` (this is a default; adjust if needed)
5. Click "Register"

### Step 3: Note Your App Details
After registration, you'll see the app overview page. Note these important values:
- **Application (client) ID**: This is your CLIENT_ID
- **Directory (tenant) ID**: This is your TENANT_ID
- **Object ID**: For reference only
- **Redirect URI**: Note this for later

### Step 4: Configure API Permissions
1. In the left menu, click "API permissions"
2. Click "Add a permission"
3. Select "Microsoft Graph"
4. Select "Delegated permissions" (for user-based access)
5. Add the following permissions by searching for each and clicking "Add permissions":
   - **Mail.ReadWrite** (read and write mail)
   - **Calendars.ReadWrite** (read and write calendar events)
   - **Tasks.ReadWrite** (read and write tasks)
   - **Contacts.ReadWrite** (read and write contacts)
   - **Files.ReadWrite** (read and write files in SharePoint/OneDrive)
   - **User.Read** (required for basic user info)
   - **offline_access** (required for refresh tokens)

6. After adding all permissions, click "Grant admin consent for [Your Organization]"
7. Confirm the consent dialog

### Step 5: Create a Client Secret
1. In the left menu, click "Certificates & secrets"
2. Click "New client secret"
3. Give it a description (e.g., "Hermes MCP Server Secret")
4. Set an expiration (6 months to 1 year recommended for security)
5. Click "Add"
6. **IMPORTANT**: Copy the secret value IMMEDIATELY. It will only be shown once!
7. Store this value securely (in a password manager or secure note)

### Step 6: Configure Authentication
1. In the left menu, click "Authentication"
2. Under "Implicit grant and hybrid flows":
   - Check "ID tokens" (for OpenID Connect)
   - Check "Access tokens" (for OAuth 2.0)
3. Click "Save"

### Step 7: Test the Connection
1. Open a terminal or command prompt
2. Test the OAuth2 flow by running the following (example in Python):
   ```python
   import requests
   import webbrowser
   
   CLIENT_ID = "your-client-id"
   TENANT_ID = "your-tenant-id"
   
   auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:3000/callback&scope=Mail.ReadWrite%20Calendars.ReadWrite%20Tasks.ReadWrite%20Contacts.ReadWrite%20Files.ReadWrite%20User.Read%20offline_access"
   
   print(f"Open this URL in your browser:\n{auth_url}")
   webbrowser.open(auth_url)
   ```
3. Copy the authorization code from the redirect URL
4. Exchange it for tokens (see Hermes MCP server documentation)

### Step 8: Add App to Microsoft 365 Tenant (Admin Consent)
If you're not an admin:
1. Contact your IT administrator to grant admin consent
2. Or if you are an admin:
   1. In Azure Portal, go to "Enterprise applications"
   2. Find your app
   3. Click "Permissions"
   4. Click "Grant admin consent for [Your Organization]"
   5. Confirm

### Step 9: Configure Hermes Agent MCP Server
1. Add the following to your Hermes Agent config file (`~/.hermes/config.yaml`):
   ```yaml
   mcp_servers:
     microsoft_graph:
       command: "npx"
       args: ["-y", "@anthropic/mcp-server-msgraph"]
       env:
         AZURE_CLIENT_ID: "your-client-id"
         AZURE_CLIENT_SECRET: "your-client-secret"
         AZURE_TENANT_ID: "your-tenant-id"
         AZURE_REDIRECT_URI: "http://localhost:3000/callback"
       timeout: 120
       connect_timeout: 60
   ```
2. Restart Hermes Agent
3. The MCP server will connect and expose tools like:
   - `mcp_microsoft_graph_send_email`
   - `mcp_microsoft_graph_create_calendar_event`
   - `mcp_microsoft_graph_create_task`
   - `mcp_microsoft_graph_add_contact`
   - `mcp_microsoft_graph_upload_file`

### Step 10: Verify Everything Works
1. In Hermes Agent, ask to:
   - "Send a test email to myself"
   - "Create a calendar event for tomorrow at 10 AM"
   - "List my contacts"
   - "Create a task for Friday"
   - "Upload a file to SharePoint"
2. If any step fails, check:
   - Client ID and secret are correct
   - Permissions are granted (admin consent)
   - Redirect URI matches
   - The MCP server is running

## Important Notes
- **Security**: Keep your client secret secure. Never share it or commit it to code repositories.
- **Admin Consent**: Some permissions require admin consent. If you're not an admin, ask your IT department.
- **Expiration**: Client secrets expire. Set a reminder to renew them before they expire.
- **Rate Limits**: Microsoft Graph API has rate limits. Avoid making too many requests too quickly.
- **Troubleshooting**: If you get errors, check the Azure Portal for app registration status, permissions, and consent.

## Common Issues and Solutions

### "Invalid client secret"
- The client secret may have expired
- The client secret may have been revoked
- Solution: Create a new client secret in Azure Portal

### "Insufficient permissions"
- Admin consent may not have been granted
- Some permissions require admin consent
- Solution: Grant admin consent in Azure Portal

### "Redirect URI mismatch"
- The redirect URI in your app doesn't match what's configured in Azure Portal
- Solution: Update the redirect URI in Azure Portal to match your app

### "Token expired"
- Access tokens expire after 1 hour
- Solution: Use refresh tokens to get new access tokens

## Security Best Practices
1. **Never commit secrets to code repositories**
2. **Use environment variables for secrets**
3. **Rotate client secrets regularly**
4. **Use least-privilege permissions**
5. **Monitor API usage in Azure Portal**
6. **Enable Azure AD Conditional Access policies**
7. **Use multi-factor authentication for all accounts**

## Resources
- Microsoft Graph API Documentation: https://learn.microsoft.com/en-us/graph/
- Azure Portal: https://portal.azure.com
- Microsoft Graph Explorer: https://developer.microsoft.com/graph/graph-explorer
- Azure AD App Registration: https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app