# Cline MCP Configuration

This directory contains the MCP (Model Context Protocol) configuration for Cline.

## Setup Complete ✓

The following MCP server has been configured:

### Knowledge Work Plugins
- **Server**: `@anthropics/knowledge-work-plugins`
- **Command**: `npx -y @anthropics/knowledge-work-plugins`

## How to Use

1. **Open Cline Panel**
   - Click the Cline icon in the VS Code sidebar (usually on the left)
   - Or use Command Palette: `Cmd+Shift+P` → "Cline: Open"

2. **Configure API Key**
   - In the Cline panel, click the settings/gear icon
   - Add your Anthropic API key
   - Select your preferred model (Claude 3.5 Sonnet recommended)

3. **Enable MCP Server**
   - In Cline settings, look for "MCP Servers" section
   - The knowledge-work-plugins server should be listed
   - Ensure it's enabled (not disabled)

4. **Using MCP Tools**
   - When chatting with Cline, it will automatically use available MCP tools
   - The knowledge-work-plugins provide tools for:
     - Sales data analysis
     - CRM integrations
     - Business intelligence queries
     - And more knowledge work tasks

## Available Tools from Knowledge Work Plugins

Once connected, Cline will have access to tools from the knowledge-work-plugins marketplace, including the `sales` plugin you wanted to install.

## Troubleshooting

### If MCP server doesn't connect:
1. Ensure Node.js is installed: `node --version`
2. Check the Cline output panel for errors
3. Restart VS Code after configuration changes

### If tools aren't available:
1. Check that the server is enabled in Cline settings
2. Look at the Cline MCP logs in the output panel
3. Ensure your API key has proper permissions

## Manual Configuration

If you need to configure MCP settings globally (outside this workspace):

```bash
# Edit global Cline MCP settings
~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

## Adding More MCP Servers

To add more MCP servers, edit `mcp_settings.json` and add entries like:

```json
{
  "mcpServers": {
    "knowledge-work-plugins": { ... },
    "another-server": {
      "command": "npx",
      "args": ["-y", "@scope/package-name"],
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Next Steps

1. ✓ Cline installed
2. ✓ MCP configuration created
3. → Open Cline panel and add your API key
4. → Start using the knowledge work plugins in your data analysis!

## Integration with Your Prompts

The prompt files in `.github/prompts/` are designed to work with Cline. You can:
- Use the prompts as context for Cline conversations
- Reference specific stages (data extraction, analysis, etc.)
- Let Cline execute the implementation plans with MCP tool access
