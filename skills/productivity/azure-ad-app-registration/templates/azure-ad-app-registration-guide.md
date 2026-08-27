# Azure AD App Registration Guide for Microsoft Graph API
## A Step-by-Step Guide for Public Health Educators

> **Purpose**: This guide will help you set up an Azure AD app registration so you can connect your Hermes Agent MCP server to Microsoft 365 services like Outlook, Calendar, Tasks, Contacts, and SharePoint. This is for non-technical users — no coding experience required.

---

## Table of Contents
- [What You'll Need](#what-youll-need)
- [Step 1: Sign in to Azure Portal](#step-1-sign-in-to-azure-portal)
- [Step 2: Register a New App](#step-2-register-a-new-app)
- [Step 3: Note Your App Details](#step-3-note-your-app-details)
- [Step 4: Configure API Permissions](#step-4-configure-api-permissions)
- [Step 5: Create a Client Secret](#step-5-create-a-client-secret)
- [Step 6: Configure Authentication](#step-6-configure-authentication)
- [Step 7: Test the Connection](#step-7-test-the-connection)
- [Step 8: Add App to Microsoft 365 Tenant (Admin Consent)](#step-8-add-app-to-microsoft-365-tenant-admin-consent)
- [Step 9: Configure Hermes Agent MCP Server](#step-9-configure-hermes-agent-mcp-server)
- [Step 10: Verify Everything Works](#step-10-verify-everything-works)
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Security Best Practices](#security-best-practices)
- [Resources](#resources)

---

## What You'll Need

Before you start, make sure you have:

- [ ] **A Microsoft 365 work account** (your organization email, like `you@yourorg.onmicrosoft.com`)
- [ ] **Admin access** to your organization's Azure AD (if you don't have this, your IT department can help)
- [ ] **Internet connection** and a web browser (Chrome, Edge, or Firefox)
- [ ] **A text editor** (like Notepad) to save important values
- [ ] **Hermes Agent installed** on your Windows 11 computer (you're using the Hermes Desktop app)

> **Important**: If you don't have admin access to your organization's Azure AD, you'll need to ask your IT department to help with this setup. You can still follow along to understand what's happening, but they'll need to complete some steps.

---

## Step 1: Sign in to Azure Portal

The Azure Portal is where you manage your Microsoft cloud services. Think of it as a control panel for your Microsoft 365 account.

1. **Open your web browser** (Chrome, Edge, or Firefox)
2. **Go to**: https://portal.azure.com
3. **Sign in** with your Microsoft 365 work email (e.g., `you@yourorg.onmicrosoft.com`)
4. If prompted, **complete multi-factor authentication** (this might be a code sent to your phone or an authenticator app)

> **Tip**: If you're not sure if you have access, try signing in. If you can't access the Azure Portal, contact your IT department.

---

## Step 2: Register a New App

This step creates a new "app registration" in Azure AD. Think of this as creating a "key" that your Hermes Agent can use to access your Microsoft 365 data.

1. **In the Azure Portal search bar** (at the top), type **"Azure Active Directory"** and click on it
2. In the left menu, click **"App registrations"**
3. Click **"New registration"** (blue button at the top)
4. Fill in the form:

   | Field | What to Enter | Example |
   |-------|---------------|---------|
   | **Name** | Give your app a descriptive name | "Hermes Graph API Integration" or "Public Health Outreach Manager" |
   | **Supported account types** | Select "Accounts in this organizational directory only (Single tenant)" | This means only people in your organization can use it |
   | **Redirect URI** | Select "Web" from the dropdown, then enter: `http://localhost:3000/callback` | This is where the app will redirect after you sign in |

5. Click **"Register"**

> **What is a Redirect URI?** It's like a "return address" — after you sign in, Microsoft will send you back to this URL with a code. The `http://localhost:3000/callback` URL is a default that works for most setups.

---

## Step 3: Note Your App Details

After you register the app, you'll see an "Overview" page with important information. **Write these down or save them in a secure place** (like a password manager or a secure note):

| Information | Where to Find It | What It's Used For |
|-------------|------------------|--------------------|
| **Application (client) ID** | On the Overview page | This is like your app's "username" |
| **Directory (tenant) ID** | On the Overview page | This is like your organization's "ID" |
| **Redirect URI** | On the Overview page (or under Authentication) | This tells Microsoft where to send you back after signing in |

> **Important**: Keep these values safe! You'll need them later when configuring Hermes Agent.

---

## Step 4: Configure API Permissions

Permissions tell Microsoft what your app is allowed to do. Since you want to access Outlook, Calendar, Tasks, Contacts, and SharePoint, you need to add specific permissions.

### 4.1: Add Permissions

1. In the left menu, click **"API permissions"**
2. Click **"Add a permission"**
3. Select **"Microsoft Graph"** (this is the main API for Microsoft 365)
4. Select **"Delegated permissions"** (this means the app will act on behalf of the user, not as a service)
5. Add the following permissions by searching for each and clicking **"Add permissions"**:

   | Permission | What It Does |
   |------------|--------------|
   | **Mail.ReadWrite** | Read and send emails |
   | **Calendars.ReadWrite** | Read and create calendar events |
   | **Tasks.ReadWrite** | Read and create tasks |
   | **Contacts.ReadWrite** | Read and add contacts |
   | **Files.ReadWrite** | Read and upload files to SharePoint/OneDrive |
   | **User.Read** | Get basic user information (required) |
   | **offline_access** | Keep access after closing the app (required for refresh tokens) |

6. After adding all permissions, click **"Grant admin consent for [Your Organization]"**
7. Click **"Yes"** to confirm

> **What are permissions?** They're like "keys" that let your app do specific things. For example, `Mail.ReadWrite` lets your app read and send emails, but not delete them (that would need a different permission).

> **Why "Delegated permissions"?** These permissions mean the app will act on behalf of you (the user), not as a service. This is important because you want your app to access YOUR emails, calendar, etc.

---

## Step 5: Create a Client Secret

A client secret is like a password for your app. It proves that your app is who it says it is.

1. In the left menu, click **"Certificates & secrets"**
2. Click **"New client secret"** (blue button at the top)
3. Give it a description (e.g., "Hermes MCP Server Secret")
4. Set an expiration (choose **6 months to 1 year** — shorter is more secure, but you'll need to update it more often)
5. Click **"Add"**
6. **IMPORTANT**: Copy the secret value **IMMEDIATELY**. It will only be shown once!
7. Store this value securely (in a password manager or secure note)

> **Warning**: If you lose this secret, you'll need to create a new one. You can't recover the old one.

> **Security tip**: Never share this secret with anyone. Never write it in an email or chat. Never save it in a plain text file on your computer.

---

## Step 6: Configure Authentication

This step tells Microsoft how your app should authenticate (sign in).

1. In the left menu, click **"Authentication"**
2. Under **"Implicit grant and hybrid flows"**:
   - Check **"ID tokens"** (for OpenID Connect — this helps verify who you are)
   - Check **"Access tokens"** (for OAuth 2.0 — this lets your app access your data)
3. Click **"Save"**

> **What is Implicit Grant?** It's a way for your app to get tokens directly. It's simpler than other methods, which is why we're using it here.

---

## Step 7: Test the Connection

Before configuring Hermes Agent, let's test that the app registration is working correctly.

### Option 1: Use the Microsoft Graph Explorer (Easiest)

1. Go to https://developer.microsoft.com/graph/graph-explorer
2. Sign in with your Microsoft 365 account
3. Try running a query like `https://graph.microsoft.com/v1.0/me` — this should return your user information

### Option 2: Use a Simple Test Script (If You're Comfortable with Code)

If you have Python installed, you can run a simple test:

```python
import requests
import webbrowser

# Replace these with your actual values
CLIENT_ID = "your-client-id"  # From Step 3
TENANT_ID = "your-tenant-id"  # From Step 3

# Build the authorization URL
auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:3000/callback&scope=Mail.ReadWrite%20Calendars.ReadWrite%20Tasks.ReadWrite%20Contacts.ReadWrite%20Files.ReadWrite%20User.Read%20offline_access"

print(f"Open this URL in your browser:\n{auth_url}")
webbrowser.open(auth_url)

# After you sign in, you'll be redirected to a URL with a code
# Copy the code from the URL and use it to get tokens
```

> **Note**: If you're not comfortable with code, you can skip this step and proceed to Step 9. The Microsoft Graph Explorer is the easiest way to test.

---

## Step 8: Add App to Microsoft 365 Tenant (Admin Consent)

Some permissions require admin consent (approval from your IT department). This is a security measure to prevent apps from accessing data without permission.

### If You're an Admin:

1. In Azure Portal, go to **"Enterprise applications"** (search for it in the top bar)
2. Find your app by name
3. Click on it
4. Click **"Permissions"**
5. Click **"Grant admin consent for [Your Organization]"**
6. Click **"Yes"** to confirm

### If You're NOT an Admin:

1. Contact your IT administrator
2. Ask them to grant admin consent for your app registration
3. Provide them with the app name and client ID

> **Why is admin consent needed?** It's a security feature. Your IT department needs to approve that your app can access sensitive data like emails and calendar events.

---

## Step 9: Configure Hermes Agent MCP Server

Now that you've registered the app, you need to configure Hermes Agent to use it.

### 9.1: Find Your Config File

Your Hermes Agent config file is located at:
- **Windows**: `C:\Users\cruzmars\.hermes\config.yaml`
- Or if you're using a custom path: `~/.hermes/config.yaml`

### 9.2: Add the MCP Server Configuration

Open the config file in a text editor (like Notepad or VS Code) and add the following section:

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

**Replace the following values with your actual values from Step 3 and Step 5:**
- `your-client-id` → Your Application (client) ID
- `your-client-secret` → Your Client Secret (from Step 5)
- `your-tenant-id` → Your Directory (tenant) ID

> **Important**: Make sure the YAML indentation is correct. Use spaces, not tabs. Each level of indentation should be 2 spaces.

### 9.3: Save and Restart

1. Save the config file
2. Restart Hermes Agent (close and reopen it, or use the restart command)
3. The MCP server will connect automatically when Hermes starts

---

## Step 10: Verify Everything Works

Now let's test that everything is working correctly.

### 10.1: Test Basic Connection

Ask Hermes Agent to do some simple tasks:

1. **Send a test email to yourself**:
   - Say: "Send a test email to myself with the subject 'Test Email' and body 'This is a test'"
   - If it works, you'll see the email in your inbox

2. **Create a calendar event**:
   - Say: "Create a calendar event for tomorrow at 10 AM with the subject 'Team Meeting'"
   - If it works, you'll see the event in your calendar

3. **List your contacts**:
   - Say: "List my contacts"
   - If it works, you'll see a list of your contacts

4. **Create a task**:
   - Say: "Create a task for Friday with the subject 'Submit report'"
   - If it works, you'll see the task in your Microsoft To-Do app

5. **Upload a file to SharePoint**:
   - Say: "Upload the file C:\Users\cruzmars\Documents\report.pdf to SharePoint"
   - If it works, you'll see the file in your SharePoint library

### 10.2: Troubleshooting

If something doesn't work, check:

| Issue | Solution |
|-------|----------|
| "Client ID not found" | Make sure you entered the correct Client ID in the config file |
| "Client secret is invalid" | Make sure you copied the secret correctly and it hasn't expired |
| "Permission denied" | Make sure admin consent was granted for all permissions |
| "Redirect URI mismatch" | Make sure the redirect URI in your config matches the one in Azure Portal |
| "Token expired" | Access tokens expire after 1 hour; the app should automatically refresh them |

---

## Common Issues and Solutions

### "Invalid client secret"
- The client secret may have expired
- The client secret may have been revoked
- **Solution**: Create a new client secret in Azure Portal (Step 5)

### "Insufficient permissions"
- Admin consent may not have been granted
- Some permissions require admin consent
- **Solution**: Grant admin consent in Azure Portal (Step 8)

### "Redirect URI mismatch"
- The redirect URI in your app doesn't match what's configured in Azure Portal
- **Solution**: Update the redirect URI in Azure Portal to match your app

### "Token expired"
- Access tokens expire after 1 hour
- **Solution**: Use refresh tokens to get new access tokens (Hermes Agent should handle this automatically)

### "MCP server not connecting"
- The MCP server may not be installed
- **Solution**: Make sure Node.js is installed and the MCP server package is available

---

## Security Best Practices

1. **Never commit secrets to code repositories** — keep your client secret in a secure location
2. **Use environment variables for secrets** — don't hardcode them in files
3. **Rotate client secrets regularly** — set a reminder to renew them before they expire
4. **Use least-privilege permissions** — only add the permissions you actually need
5. **Monitor API usage in Azure Portal** — check the "Usage" section to see if your app is being used
6. **Enable Azure AD Conditional Access policies** — this adds extra security
7. **Use multi-factor authentication for all accounts** — this protects your accounts from unauthorized access

---

## Resources

- **Microsoft Graph API Documentation**: https://learn.microsoft.com/en-us/graph/
- **Azure Portal**: https://portal.azure.com
- **Microsoft Graph Explorer**: https://developer.microsoft.com/graph/graph-explorer
- **Azure AD App Registration**: https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app
- **Hermes Agent Documentation**: https://hermes-agent.nousresearch.com/docs

---

## Quick Reference Card

| Item | Value |
|------|-------|
| **App Name** | (Your chosen name) |
| **Client ID** | (From Azure Portal Overview) |
| **Tenant ID** | (From Azure Portal Overview) |
| **Client Secret** | (From Step 5 — keep secure!) |
| **Redirect URI** | http://localhost:3000/callback |
| **Permissions** | Mail.ReadWrite, Calendars.ReadWrite, Tasks.ReadWrite, Contacts.ReadWrite, Files.ReadWrite, User.Read, offline_access |
| **MCP Server** | @anthropic/mcp-server-msgraph |

---

## Need Help?

If you're stuck at any step, contact your IT department or refer to the resources above. You can also ask Hermes Agent for help — it can guide you through the process!

---

*This guide was created for public health educators using Hermes Agent to integrate Microsoft 365 with their workflow. Last updated: August 18, 2026.*