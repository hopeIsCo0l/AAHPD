# 🚀 Railway Deployment Guide

## Quick Start

### Option 1: Automated Script (Recommended)
```bash
# Windows
deploy-railway.bat

# Linux/Mac
chmod +x deploy-railway.sh
./deploy-railway.sh
```

### Option 2: Manual Steps

## Step 1: Login to Railway
```bash
npx @railway/cli login
```
This will open a browser window for authentication.

## Step 2: Initialize Project
```bash
npx @railway/cli init
```
Select your project and follow the prompts.

## Step 3: Add PostgreSQL Database
```bash
npx @railway/cli add postgresql
```

## Step 4: Set Environment Variables
```bash
# Required variables
npx @railway/cli variables set OPENAI_API_KEY=your_openai_key_here
npx @railway/cli variables set JWT_SECRET_KEY=your_jwt_secret_here

# Optional variables
npx @railway/cli variables set PGADMIN_EMAIL=admin@admin.com
npx @railway/cli variables set PGADMIN_PASSWORD=admin
```

## Step 5: Deploy
```bash
npx @railway/cli up
```

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key | `sk-...` |
| `JWT_SECRET_KEY` | Yes | Secret for JWT tokens | `your-secret-key` |
| `POSTGRES_PASSWORD` | Auto | Database password | Auto-generated |
| `PGADMIN_EMAIL` | No | pgAdmin login email | `admin@admin.com` |
| `PGADMIN_PASSWORD` | No | pgAdmin password | `admin` |

## Railway Configuration

Your project includes `railway.json` with the following configuration:
- **Builder**: Dockerfile
- **Dockerfile**: `Dockerfile.production`
- **Start Command**: `docker-compose -f docker-compose.production.yml up`

## Services Deployed

1. **Backend API** - FastAPI application
2. **Frontend** - Nginx serving static files
3. **PostgreSQL** - Database with pgvector
4. **Redis** - Caching service
5. **pgAdmin** - Database management (optional)

## Accessing Your Application

After deployment, Railway will provide you with:
- **Main Application URL** - Your frontend
- **API URL** - Backend API endpoints
- **Database URL** - PostgreSQL connection string
- **pgAdmin URL** - Database management interface

## Monitoring

- **Railway Dashboard**: https://railway.app/dashboard
- **Logs**: Available in Railway dashboard
- **Metrics**: CPU, Memory, Network usage
- **Health Checks**: Automatic health monitoring

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Dockerfile.production
   - Verify all files are committed
   - Check Railway logs

2. **Database Connection Issues**
   - Verify PostgreSQL service is running
   - Check DATABASE_URL environment variable
   - Ensure pgvector extension is installed

3. **Environment Variables Not Set**
   - Use `npx @railway/cli variables` to list all variables
   - Set missing variables with `npx @railway/cli variables set`

4. **Application Not Starting**
   - Check logs in Railway dashboard
   - Verify all required environment variables are set
   - Check if ports are correctly configured

### Useful Commands

```bash
# View logs
npx @railway/cli logs

# View variables
npx @railway/cli variables

# Connect to database
npx @railway/cli connect postgres

# View service status
npx @railway/cli status

# Redeploy
npx @railway/cli up
```

## Cost

- **Free Tier**: $0/month (limited resources)
- **Pro Plan**: $5/month (more resources)
- **Team Plan**: $20/month (team features)

## Security

- All traffic is encrypted with HTTPS
- Environment variables are encrypted
- Database connections are secure
- No sensitive data in logs

## Scaling

Railway automatically handles:
- Load balancing
- Auto-scaling based on traffic
- Health checks and restarts
- Database backups

## Support

- **Railway Docs**: https://docs.railway.app
- **Community**: https://discord.gg/railway
- **GitHub Issues**: For application-specific issues

## Next Steps

1. **Custom Domain**: Add your own domain in Railway dashboard
2. **SSL Certificate**: Automatically provided by Railway
3. **Monitoring**: Set up alerts and monitoring
4. **Backups**: Configure database backups
5. **CI/CD**: Set up automatic deployments from GitHub

Your Academic Assignment Helper is now live on Railway! 🎉
