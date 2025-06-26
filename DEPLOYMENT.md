# Deployment Guide

## 🚀 Deploying to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- Git installed locally

### Step-by-Step Deployment

#### 1. Prepare Repository
```bash
# Clone or fork the repository
git clone https://github.com/novalbahri17/hungarian.git
cd hungarian

# Make sure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Deploy to Vercel

**Option A: Using Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your repository
5. Vercel will auto-detect the configuration
6. Click "Deploy"

**Option B: Using Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

#### 3. Configuration
The project includes `vercel.json` with optimal settings:
```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### Environment Variables
No additional environment variables required for basic functionality.

### Custom Domain (Optional)
1. Go to your project dashboard on Vercel
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## 🐳 Alternative: Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app/main.py"]
```

### Build and Run
```bash
# Build image
docker build -t hungarian-app .

# Run container
docker run -p 5001:5001 hungarian-app
```

## 🌐 Other Deployment Options

### Heroku
1. Create `Procfile`:
   ```
   web: python app/main.py
   ```
2. Deploy using Heroku CLI or GitHub integration

### Railway
1. Connect GitHub repository
2. Railway will auto-detect Python app
3. Deploy automatically

### DigitalOcean App Platform
1. Create new app from GitHub
2. Configure build and run commands
3. Deploy

## 🔧 Troubleshooting

### Common Issues

**Build Fails**
- Check `requirements.txt` for compatibility
- Ensure Python version compatibility
- Verify all imports are available

**Runtime Errors**
- Check Vercel function logs
- Verify file paths are correct
- Ensure no local file dependencies

**Static Files Not Loading**
- Verify static file paths
- Check Vercel routing configuration

### Performance Optimization

1. **Minimize Dependencies**
   - Only include necessary packages in `requirements.txt`
   - Use lightweight alternatives when possible

2. **Optimize Code**
   - Minimize cold start time
   - Cache expensive operations
   - Use efficient algorithms

3. **Monitor Performance**
   - Use Vercel Analytics
   - Monitor function execution time
   - Track memory usage

## 📊 Monitoring

### Vercel Analytics
- Enable in project settings
- Monitor page views and performance
- Track user engagement

### Error Tracking
- Check Vercel function logs
- Set up error notifications
- Monitor application health

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit secrets to repository
   - Use Vercel environment variables for sensitive data

2. **Input Validation**
   - Validate all user inputs
   - Sanitize file uploads
   - Implement rate limiting

3. **HTTPS**
   - Vercel provides HTTPS by default
   - Ensure all external resources use HTTPS

---

**Need help?** Open an issue on GitHub or check Vercel documentation.