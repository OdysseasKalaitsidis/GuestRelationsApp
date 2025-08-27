# Railway Build Troubleshooting Guide

This guide helps resolve common Railway build issues.

## Issue: Nixpacks Build Failure with "undefined variable 'npm' or 'pip'"

### Problem
```
error: undefined variable 'npm'
error: undefined variable 'pip'
at /app/.nixpacks/nixpkgs-xxx.nix:19:16:
```

### Solution
The issue is that `npm` and `pip` are not separate packages in Nix - they come bundled with their respective runtimes.

**Fixed Configuration:**
```toml
[phases.setup]
nixPkgs = ["nodejs_20", "python311"]
```

**NOT:**
```toml
[phases.setup]
nixPkgs = ["nodejs", "npm", "python311", "pip"]  # ❌ npm and pip are bundled
```

## Alternative Solutions

### Option 1: Use Simple Configuration
If the main `nixpacks.toml` still fails, try using `nixpacks-simple.toml`:

1. Rename `nixpacks.toml` to `nixpacks-backup.toml`
2. Rename `nixpacks-simple.toml` to `nixpacks.toml`
3. Deploy again

### Option 1b: Use Minimal Configuration
If the simple configuration still fails, try `nixpacks-minimal.toml`:

1. Rename `nixpacks.toml` to `nixpacks-backup.toml`
2. Rename `nixpacks-minimal.toml` to `nixpacks.toml`
3. Deploy again

### Option 1c: Use CI Configuration (After Lock File Update)
If you've updated package-lock.json locally, try `nixpacks-ci.toml`:

1. Rename `nixpacks.toml` to `nixpacks-backup.toml`
2. Rename `nixpacks-ci.toml` to `nixpacks.toml`
3. Deploy again

### Option 2: Remove Nixpacks Configuration
If Nixpacks continues to fail:

1. Delete `nixpacks.toml` entirely
2. Railway will auto-detect your project structure
3. It should automatically detect:
   - Node.js for frontend
   - Python for backend

### Option 3: Use Dockerfile Instead
If Nixpacks continues to have issues:

1. Create a `Dockerfile` in your project root
2. Railway will use Docker instead of Nixpacks
3. This gives you full control over the build process

## Common Build Issues

### Node.js Version Issues
- **Issue**: "Vite requires Node.js version 20.19+ or 22.12+"
- **Solution**: Use `nodejs_20` in nixpacks.toml instead of `nodejs`
- **Debug**: Check Node.js version with `node --version`

### Missing Terser Dependency
- **Issue**: "terser not found. Since Vite v3, terser has become an optional dependency"
- **Solution**: Add `"terser": "^5.24.0"` to devDependencies in package.json
- **Debug**: Check if terser is listed in package.json

### NPM CI Lock File Issues
- **Issue**: "Missing: buffer-from@1.1.2 from lock file" or similar lock file errors
- **Solution**: Use `npm install` instead of `npm ci` in nixpacks.toml, or update package-lock.json
- **Debug**: Run `npm install` locally to update the lock file

### Frontend Build Failures
- **Issue**: Frontend build fails during `npm run build`
- **Solution**: Check that all dependencies are in `package.json`
- **Debug**: Add `--verbose` flag to npm commands

### Backend Build Failures
- **Issue**: Python dependencies fail to install
- **Solution**: Check `requirements.txt` for version conflicts
- **Debug**: Use `pip install --no-cache-dir -r requirements.txt`

### Memory Issues
- **Issue**: Build process killed due to memory constraints
- **Solution**: Install dependencies in smaller batches
- **Debug**: Use `--no-cache-dir` flags

## Debugging Steps

1. **Check Build Logs**: View detailed logs in Railway dashboard
2. **Test Locally**: Ensure the app builds locally first
3. **Simplify Configuration**: Start with minimal configuration
4. **Check Dependencies**: Verify all dependencies are correct

## Environment Variables

Ensure these are set in Railway:
```
DATABASE_URL=mysql://...
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
ENVIRONMENT=production
```

## File Structure Requirements

Railway expects:
```
project/
├── frontend/
│   ├── package.json
│   └── src/
├── backend/
│   ├── requirements.txt
│   └── main.py
├── railway.json
├── nixpacks.toml (optional)
└── Procfile (optional)
```

## Getting Help

1. Check Railway documentation: [docs.railway.app](https://docs.railway.app)
2. Join Railway Discord: [discord.gg/railway](https://discord.gg/railway)
3. Check Railway status: [status.railway.app](https://status.railway.app)

## Quick Fixes

### If Build Still Fails:
1. Delete `nixpacks.toml`
2. Let Railway auto-detect
3. If that fails, create a simple `Dockerfile`

### If Dependencies Fail:
1. Check versions in `requirements.txt` and `package.json`
2. Use exact versions instead of ranges
3. Remove any conflicting dependencies

### If Memory Issues:
1. Use `--no-cache-dir` for pip
2. Use `--prefer-offline` for npm
3. Install dependencies in smaller batches
