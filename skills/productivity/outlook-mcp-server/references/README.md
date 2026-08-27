# Outlook MCP Server

A comprehensive MCP server for integrating Microsoft Outlook with Hermes Agent.

## Features

- **Email Management** - Read, organize, create, and search emails
- **Calendar Management** - Create, update, and delete calendar events
- **Task Management** - Create, update, and complete tasks
- **Contact Management** - Create, update, and delete contacts
- **Outreach Tracking** - Track outreach to individuals with SharePoint/Excel integration

## Quick Start

1. Register an Azure AD app with required permissions
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run the server: `python server.py`

## Documentation

See the [Setup Guide](references/setup-guide.md) for detailed instructions.

## File Structure

```
outlook-mcp-server/
├── requirements.txt      # Dependencies
├── server.py            # Main MCP server
├── auth.py              # Authentication module (MSAL)
├── graph_client.py      # Microsoft Graph API client
├── config.py            # Configuration module
└── tools/
    ├── email_tools.py   # Email management tools
    ├── calendar_tools.py # Calendar management tools
    ├── task_tools.py    # Task management tools
    ├── contact_tools.py # Contact management tools
    └── outreach_tools.py # Outreach tracking tools
```

## License

MIT License