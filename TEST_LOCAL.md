# Local Testing Guide

## Quick UI Test (Visual Only)

A simple HTTP server is already running! 

1. **Open your browser** and go to: `http://localhost:8080`
2. **Make sure Figma Desktop is running** so the images load properly
3. You can see the updated UI design, but API calls won't work

To stop the server, press `Ctrl+C` in the terminal.

## Full Backend Test (Complete Functionality)

### Prerequisites:
1. **Start Docker Desktop** (if not already running)
2. **Create `.env` file** (if it doesn't exist):
   ```bash
   copy env.example .env
   ```
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

### Start the Application:

**Option 1: Using the startup script (Windows)**
```bash
start.bat
```

**Option 2: Manual Docker Compose**
```bash
docker-compose up -d
```

Wait for services to start (about 30 seconds), then:

1. **Initialize the database:**
   ```bash
   docker-compose exec backend python scripts/init_database.py
   ```

2. **Access the application:**
   - **Web Interface**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **n8n**: http://localhost:5678 (admin/admin123)

3. **Test credentials:**
   - Email: `test@student.com`
   - Password: `password123`

### Stop the Application:
```bash
docker-compose down
```

## Testing Checklist

- [ ] Login page displays with Figma design (gradient background, logo, styled inputs)
- [ ] Signup page matches Figma design
- [ ] Navigation sidebar shows icons correctly
- [ ] All Figma images load from localhost:3845
- [ ] Password toggle works
- [ ] Form validation works
- [ ] API endpoints respond correctly

## Troubleshooting

**Images not loading?**
- Make sure Figma Desktop app is running
- Check that MCP server is accessible at http://localhost:3845

**Docker not starting?**
- Ensure Docker Desktop is running
- Check if ports 8000, 5432, 5678 are available

**Backend errors?**
- Check logs: `docker-compose logs backend`
- Verify `.env` file has correct OpenAI API key

