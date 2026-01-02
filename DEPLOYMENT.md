# 🚀 IUBAT Bus Management - Deployment Guide

## 📋 Quick Deployment Checklist

### ✅ Pre-Deployment
- [x] Models are production-ready
- [x] 4-actor role system implemented
- [x] Unified login with role-based redirects
- [x] GPS tracking functional
- [x] GPS simulation system working
- [x] API endpoints secured
- [x] Static files configured with WhiteNoise
- [x] Environment variables set up
- [x] Database migrations ready

## 🚢 Deploy to Render (Recommended)

### Step 1: Prepare Repository
```bash
cd d:\Projects\IUBAT_Bus
git add -A
git commit -m "Production ready"
git push origin main
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Connect your repository

### Step 3: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `iubat-bus-db`
3. Plan: Free
4. Click "Create Database"
5. Copy the "Internal Database URL"

### Step 4: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `iubat-bus-system`
   - **Region**: Choose nearest
   - **Branch**: `main`
   - **Root Directory**: `bus_project`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r Requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command**: `gunicorn bus_management_project.wsgi:application --bind 0.0.0.0:$PORT`

### Step 5: Set Environment Variables
In Render dashboard, add these environment variables:

```
SECRET_KEY=your-generated-secret-key-min-50-chars-random
DEBUG=False
ALLOWED_HOSTS=iubat-bus-system.onrender.com,.onrender.com
DATABASE_URL=<paste-internal-database-url-from-step-3>
```

Generate SECRET_KEY:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 6: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for build
3. Service will be live at: `https://iubat-bus-system.onrender.com`

### Step 7: Initialize Data
Run these commands from Render shell:
```bash
python manage.py populate_sample_data
python manage.py create_test_users
```

## 🚂 Deploy to Railway (Alternative)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
railway login
```

### Step 2: Initialize Project
```bash
cd d:\Projects\IUBAT_Bus\bus_project
railway init
```

### Step 3: Add PostgreSQL
```bash
railway add
# Select PostgreSQL
```

### Step 4: Set Environment Variables
```bash
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS="*.railway.app"
```

### Step 5: Deploy
```bash
railway up
```

## 🔧 Post-Deployment Setup

### 1. Create Superuser
```bash
# On Render: use Web Service Shell
# On Railway: railway run python manage.py createsuperuser

python manage.py createsuperuser
```

### 2. Populate Sample Data
```bash
python manage.py populate_sample_data
python manage.py create_test_users
```

### 3. Test All Roles
1. Visit: `https://your-app.onrender.com/buses/login/`
2. Test each role:
   - USER: `testuser` / `user123`
   - DRIVER: `driver1` / `driver123`
   - ADMIN: `admin` / `admin123`
   - AUTHORITY: `authority` / `authority123`

## 🌐 Custom Domain Setup

### On Render
1. Go to Settings → Custom Domain
2. Add your domain: `bus.iubat.edu`
3. Update DNS records as shown
4. Update ALLOWED_HOSTS:
   ```
   ALLOWED_HOSTS=bus.iubat.edu,.onrender.com
   ```

## 🔐 Security Checklist

- ✅ DEBUG=False in production
- ✅ Strong SECRET_KEY (50+ characters)
- ✅ ALLOWED_HOSTS configured
- ✅ HTTPS enabled (automatic on Render/Railway)
- ✅ Database credentials secure
- ✅ CORS configured for API
- ✅ Static files served via WhiteNoise
- ✅ SQLite replaced with PostgreSQL

## 📊 Monitoring

### Check Logs (Render)
```
Dashboard → Your Service → Logs
```

### Check Logs (Railway)
```bash
railway logs
```

### Common Issues

**Issue: Static files not loading**
```bash
python manage.py collectstatic --no-input
```

**Issue: Database connection error**
- Verify DATABASE_URL is set correctly
- Check PostgreSQL database is running

**Issue: ALLOWED_HOSTS error**
- Add your domain to ALLOWED_HOSTS
- Include both `yourdomain.com` and `.onrender.com`

**Issue: 502 Bad Gateway**
- Check build logs for errors
- Verify Start Command is correct
- Ensure all dependencies in Requirements.txt

## 🎯 Production URLs

After deployment, your system will be available at:

- **Login**: `https://your-app.onrender.com/buses/login/`
- **User Map**: `https://your-app.onrender.com/buses/map/`
- **Driver**: `https://your-app.onrender.com/buses/driver/`
- **Admin**: `https://your-app.onrender.com/buses/admin-dashboard/`
- **API**: `https://your-app.onrender.com/api/`
- **Django Admin**: `https://your-app.onrender.com/admin/`

## 💡 Tips

1. **Free Tier Limitations**:
   - Render free tier sleeps after 15 min inactivity
   - First request may take 30-60 seconds
   - Consider upgrading for production use

2. **Database Backups**:
   - Render provides automatic backups on paid plans
   - Export data periodically: `python manage.py dumpdata > backup.json`

3. **Performance**:
   - Enable database connection pooling
   - Use CDN for static files (optional)
   - Monitor response times

4. **Updates**:
   - Push to main branch to auto-deploy
   - Test locally first
   - Monitor logs during deployment

## 📞 Support

For deployment issues:
1. Check Render/Railway documentation
2. Review application logs
3. Verify all environment variables
4. Test database connectivity

---

**Your IUBAT Bus Management System is production-ready!** 🚌✨
