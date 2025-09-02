# Supabase Client Setup Guide

## Step 1: Environment Variables Setup

You need to configure these environment variables on Render:

### Required Environment Variables

| Key | Value | Description |
|-----|-------|-------------|
| `SUPABASE_URL` | `https://<your-project>.supabase.co` | Your Supabase project URL |
| `SUPABASE_KEY` | `<your-service-or-anon-key>` | Your Supabase API key |
| `PORT` | `10000` | Port for the application |

### How to Set Environment Variables on Render

1. Go to your Render service dashboard
2. Navigate to **Environment** → **Environment Variables**
3. Add each variable exactly as shown above
4. **Important**: No extra spaces or quotes around values

### Example Configuration

```
SUPABASE_URL=https://sjjuaesddqzfcdahutfl.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PORT=10000
```

## Step 2: Key Types

### Service Key vs Anon Key

- **Service Key**: Full access to all tables and operations
- **Anon Key**: Limited access, good for public reads

For your application, use the **Service Key** for full functionality.

## Step 3: Testing

After deployment, the application will automatically test:

1. **Network Connectivity**: Can reach Supabase servers
2. **Authentication**: API key is valid
3. **Database Access**: Can read/write to tables

### Manual Testing

You can test locally with:

```bash
python test_supabase.py
```

## Step 4: Troubleshooting

### Common Issues

1. **"Missing SUPABASE_URL or SUPABASE_KEY"**
   - Check environment variables are set correctly
   - No extra spaces or quotes

2. **"Network error"**
   - Check internet connectivity
   - Verify Supabase URL is correct

3. **"Authentication failed"**
   - Verify API key is correct
   - Check if key has proper permissions

### Success Indicators

✅ `Supabase reachable, status: 200`
✅ `Supabase connection test successful`
✅ `Users table accessible: X records found`
✅ `Cases table accessible: X records found`

## Files Created

- `supabase_client.py` - Main Supabase client configuration
- `user_service_supabase.py` - Example service using Supabase client
- `test_supabase.py` - Testing script
- Updated `startup.py` - Includes connectivity tests
