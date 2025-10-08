# 🚀 Hosting Guide for Academic Assignment Helper

## 📋 Application Overview

Your application consists of:
- **Frontend**: HTML/CSS/JavaScript (static files)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with pgvector extension
- **Services**: n8n, pgAdmin, Redis
- **Containerized**: Docker Compose

## 🎯 Hosting Requirements

- Python 3.8+ runtime
- PostgreSQL database with pgvector extension
- Docker support (recommended)
- File storage for uploads
- Environment variables for API keys
- Minimum 1GB RAM, 1 CPU core

## 💰 Hosting Options

### 1. 🆓 FREE OPTIONS

#### A. Railway (Recommended for Free Tier)
**Best for**: Quick deployment with minimal setup
**Cost**: Free tier available
**Pros**: Easy Docker deployment, built-in PostgreSQL
**Cons**: Limited resources on free tier

**Steps**:
1. Sign up at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add PostgreSQL service
4. Set environment variables
5. Deploy

#### B. Render
**Best for**: Simple deployment
**Cost**: Free tier available
**Pros**: Easy setup, automatic deployments
**Cons**: Limited free tier resources

**Steps**:
1. Sign up at [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Add PostgreSQL database
5. Configure environment variables

#### C. Heroku
**Best for**: Traditional PaaS deployment
**Cost**: Limited free tier (now paid)
**Pros**: Mature platform, good documentation
**Cons**: No longer has free tier

### 2. 💵 PAID OPTIONS

#### A. DigitalOcean App Platform
**Cost**: $5-25/month
**Pros**: Simple deployment, good performance
**Cons**: Requires paid plan

#### B. AWS (ECS + RDS)
**Cost**: $10-50/month
**Pros**: Highly scalable, enterprise-grade
**Cons**: Complex setup, can be expensive

#### C. Google Cloud Platform
**Cost**: $10-40/month
**Pros**: Good free credits, scalable
**Cons**: Complex pricing

### 3. 🏠 SELF-HOSTED OPTIONS

#### A. VPS (Virtual Private Server)
**Providers**: DigitalOcean, Linode, Vultr, AWS EC2
**Cost**: $5-20/month
**Pros**: Full control, cost-effective
**Cons**: Requires server management

#### B. University Server
**Cost**: Free (if available)
**Pros**: Free, secure
**Cons**: May have restrictions

## 🚀 Recommended Deployment: Railway

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if not already done)
2. **Add these files to your repository**:

```bash
# .railwayignore
node_modules/
__pycache__/
*.pyc
.env
uploads/
```

3. **Create railway.json**:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "docker-compose up",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy on Railway

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** and select your repository
3. **Add PostgreSQL service**:
   - Go to your project
   - Click "New Service" → "Database" → "PostgreSQL"
4. **Set environment variables**:
   ```
   POSTGRES_DB=academic_helper
   POSTGRES_USER=student
   POSTGRES_PASSWORD=your_secure_password
   OPENAI_API_KEY=your_openai_key
   JWT_SECRET_KEY=your_jwt_secret
   ```
5. **Deploy** your application

### Step 3: Configure Domain (Optional)

1. Go to your service settings
2. Add custom domain
3. Update CORS settings in your backend

## 🐳 Alternative: Docker Deployment

### For VPS/Cloud Server:

1. **Set up a VPS** (DigitalOcean, Linode, etc.)
2. **Install Docker and Docker Compose**:
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Clone your repository**:
   ```bash
   git clone https://github.com/yourusername/academic-assignment-helper.git
   cd academic-assignment-helper
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   nano .env  # Edit with your values
   ```

5. **Deploy**:
   ```bash
   docker-compose up -d
   ```

6. **Set up reverse proxy** (Nginx):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🔧 Environment Variables

Create a `.env` file with these variables:

```env
# Database
POSTGRES_DB=academic_helper
POSTGRES_USER=student
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://student:your_secure_password@localhost:5432/academic_helper

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Application
N8N_WEBHOOK_URL=http://localhost:5678/webhook/assignment
REDIS_URL=redis://localhost:6379

# File Storage
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB
```

## 📊 Cost Comparison

| Option | Monthly Cost | Setup Difficulty | Scalability |
|--------|-------------|------------------|-------------|
| Railway (Free) | $0 | Easy | Limited |
| Railway (Paid) | $5-20 | Easy | Good |
| Render | $7-25 | Easy | Good |
| DigitalOcean VPS | $5-20 | Medium | Good |
| AWS | $10-50+ | Hard | Excellent |
| Self-hosted | $0-10 | Hard | Limited |

## 🎯 Recommended Path

**For beginners**: Start with Railway free tier
**For production**: Use DigitalOcean App Platform or VPS
**For enterprise**: Use AWS or Google Cloud

## 🔒 Security Considerations

1. **Use HTTPS** (most platforms provide this automatically)
2. **Set strong passwords** for database and JWT
3. **Limit file upload sizes**
4. **Implement rate limiting**
5. **Regular security updates**

## 📈 Monitoring & Maintenance

1. **Set up monitoring** (Uptime Robot, Pingdom)
2. **Regular backups** of database
3. **Log monitoring** for errors
4. **Performance monitoring**

## 🆘 Troubleshooting

### Common Issues:

1. **Database connection errors**: Check environment variables
2. **File upload issues**: Check file permissions and size limits
3. **CORS errors**: Update CORS settings in backend
4. **Memory issues**: Upgrade to higher tier plan

### Getting Help:

1. Check platform documentation
2. Check application logs
3. Test locally first
4. Use platform support channels

## 🚀 Quick Start Commands

```bash
# Test locally
docker-compose up

# Deploy to Railway
railway login
railway link
railway up

# Deploy to Render
# Connect GitHub repo in Render dashboard

# Deploy to VPS
git clone your-repo
cd your-repo
docker-compose up -d
```

Choose the option that best fits your needs and budget! 🎉
