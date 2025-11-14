# Local Testing Guide - React/Next.js Frontend

## 🚀 Quick Start

### 1. Install Dependencies (if not done)
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

The app will be available at: **http://localhost:3000**

### 3. Make Sure Backend is Running

For full functionality, start the backend:
```bash
# From project root
docker-compose up -d backend postgres
```

Or check if it's already running:
```bash
docker-compose ps
```

Backend API: **http://localhost:8000**

### 4. Make Sure Figma Desktop is Running

The app uses images from Figma Desktop MCP server at `localhost:3845`. 
Make sure Figma Desktop app is running for images to load properly.

## 🧪 Testing Checklist

### Login/Signup Pages
- [ ] Open http://localhost:3000
- [ ] Should redirect to /login
- [ ] Login page displays with Figma design
- [ ] Gradient mesh background visible
- [ ] Logo and form fields styled correctly
- [ ] Password toggle works
- [ ] Can navigate to signup page

### Dashboard (After Login)
- [ ] Sidebar displays correctly
- [ ] Company logo visible
- [ ] Navigation items work
- [ ] User profile at bottom shows correctly
- [ ] Header with "Upload Assignment" button

### Assignment Analysis
- [ ] Upload area displays correctly
- [ ] Can click to upload file
- [ ] Drag and drop works
- [ ] Analyzing state shows correctly
- [ ] Report view displays after analysis
- [ ] Score cards show with gradient backgrounds
- [ ] Info cards display correctly
- [ ] AI Suggestions card visible
- [ ] Citation Compliance card visible

### Navigation
- [ ] Can switch between pages
- [ ] Active state highlights correctly
- [ ] Logout works

## 🐛 Troubleshooting

### Images Not Loading?
- Make sure Figma Desktop is running
- Check that MCP server is accessible at http://localhost:3845

### API Errors?
- Check backend is running: `docker-compose ps`
- Check backend logs: `docker-compose logs backend`
- Verify API is accessible: http://localhost:8000/health

### Port Already in Use?
- Change port: `PORT=3001 npm run dev`
- Or kill process using port 3000

### Build Errors?
- Clear cache: `rm -rf .next node_modules`
- Reinstall: `npm install`
- Check Node version: `node --version` (should be 18+)

## 📝 Notes

- The frontend runs on port **3000**
- Backend API runs on port **8000**
- Figma images load from port **3845**
- All API calls are proxied through `/api/*` routes

## 🎯 Next Steps

Once testing is complete:
1. Commit changes
2. Push to repository
3. Create PR for React migration
4. Deploy to production

