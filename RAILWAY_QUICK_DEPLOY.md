# 🚀 Quick Railway Deployment

## Your API Key
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Quick Commands (Copy & Paste)

### 1. Login to Railway
```bash
npx @railway/cli login
```

### 2. Initialize Project
```bash
npx @railway/cli init
```

### 3. Add PostgreSQL Database
```bash
npx @railway/cli add postgresql
```

### 4. Set Environment Variables
```bash
npx @railway/cli variables set OPENAI_API_KEY=your_openai_api_key_here
```

```bash
npx @railway/cli variables set JWT_SECRET_KEY=academic-helper-secret-2024
```

### 5. Deploy
```bash
npx @railway/cli up
```

## Alternative: Web Dashboard

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `hopeIsCo0l/AAHPD`
5. Add PostgreSQL service
6. Set environment variables:
   - `OPENAI_API_KEY`: `your_openai_api_key_here`
   - `JWT_SECRET_KEY`: `academic-helper-secret-2024`
7. Deploy!

## What Happens Next

1. Railway will build your Docker containers
2. Set up PostgreSQL database with pgvector
3. Deploy your application
4. Provide you with a live URL
5. Your app will be accessible worldwide!

## Troubleshooting

- **Build fails**: Check Railway logs in dashboard
- **Database issues**: Ensure PostgreSQL service is running
- **Environment variables**: Verify they're set correctly
- **Login issues**: Try `npx @railway/cli logout` then login again

## Success!

Once deployed, you'll have:
- ✅ Live web application
- ✅ Working API endpoints
- ✅ PostgreSQL database
- ✅ File upload functionality
- ✅ AI-powered analysis
- ✅ Plagiarism detection

Your Academic Assignment Helper will be live on the internet! 🌍
