# Codicent CLI Device Authentication Flow

This document describes the device authentication flow implementation in the Codicent CLI.

## Overview

The Codicent CLI now supports OAuth 2.0 Device Authorization Grant flow for authentication, allowing users to securely authenticate without manually managing API tokens. This is especially useful for:

- CLI applications running on headless servers
- Applications without browser access
- Improved security by avoiding long-lived tokens in environment variables

## How It Works

The device flow follows the OAuth 2.0 Device Authorization Grant specification:

1. **Device Authorization Request**: CLI requests a device code and user code
2. **User Authorization**: User visits a URL and enters the code to authorize the device
3. **Token Polling**: CLI polls until user completes authorization
4. **Token Storage**: Access token is securely cached for future use

## Authentication Commands

### Authenticate
```bash
# Authenticate with project prompt
codicent auth

# Authenticate with specific project
codicent auth myproject
```

### Check Status
```bash
codicent status
```

### Logout
```bash
codicent logout
```

## Implementation Details

### Request Format

The CLI makes the following request to initiate device flow:

```bash
curl -X POST https://codicent.com/oauth/device_authorization \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "ClientId=cli-app&Scope=api&Project=myproject"
```

### Response Format

```json
{
  "deviceCode": "1P6H34932RLDJF3HEYKGQL3CCMFJVE5D",
  "userCode": "0NGA-4UCQ", 
  "verificationUri": "https://codicent.com/device",
  "verificationUriComplete": "https://codicent.com/device?user_code=0NGA-4UCQ",
  "expiresIn": 600,
  "interval": 5
}
```

### Token Persistence

- Tokens are stored in `~/.codicent_token`
- File permissions are set to `600` for security
- Includes expiration timestamp for automatic refresh
- Falls back to `CODICENT_TOKEN` environment variable

### User Experience

When authenticating, users see:

```
🔐 Starting device authorization flow...

📱 To authorize this CLI application:
1. Visit: https://codicent.com/device
2. Enter the code: 0NGA-4UCQ

Or visit directly: https://codicent.com/device?user_code=0NGA-4UCQ

⏳ Waiting for authorization (expires in 600 seconds)...
```

## Migration from Environment Variable

Existing users with `CODICENT_TOKEN` can continue using it. The CLI will:

1. Check for cached token first
2. Fall back to `CODICENT_TOKEN` if no cached token
3. Suggest using `codicent auth` for better security

## Security Features

- ✅ Short-lived device codes (10 minutes)
- ✅ Secure token storage with restricted permissions
- ✅ Token expiration handling
- ✅ Project-scoped authentication
- ✅ Error handling for failed authentication
- ✅ Clean logout functionality

## Error Handling

The implementation handles various error conditions:

- Network connectivity issues
- Invalid project names
- Authorization timeouts
- Token expiration
- API rate limiting

## Files Added/Modified

- `auth.py` - New authentication module
- `app.py` - Updated to use device flow
- `setup.py` - Added requests dependency and auth module
- `requirements.txt` - Added requests dependency

This implementation provides a secure, user-friendly authentication experience while maintaining backward compatibility with existing token-based authentication.
