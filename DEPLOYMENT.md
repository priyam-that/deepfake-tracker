# Deployment Guide for Deepfake Tracker

## 🚀 Quick Deployment Steps

### 1️⃣ Deploy Backend to Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
   - Sign up or log in with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `priyam-that/deepfake-tracker`
   - Click "Connect"

3. **Configure Service**
   - **Name**: `deepfake-tracker-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (render.yaml will handle it)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free

4. **Add Environment Variables** (Optional)
   - Click "Advanced" → "Add Environment Variable"
   - `PYTHON_VERSION`: `3.11.0`
   - `ALLOWED_ORIGINS`: (add your Vercel URL after deployment)

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Copy your backend URL (e.g., `https://deepfake-tracker-backend.onrender.com`)

### 2️⃣ Update Frontend Configuration

1. **Add Environment Variable in Vercel**
   - Go to your Vercel project: https://vercel.com/priyam-mannas-projects/deepfake-tracker
   - Go to "Settings" → "Environment Variables"
   - Add new variable:
     - **Name**: `VITE_API_URL`
     - **Value**: `https://your-render-backend-url.onrender.com/api`
     - **Environment**: Production, Preview, Development
   - Click "Save"

2. **Redeploy Frontend**
   - Go to "Deployments" tab
   - Click "..." on latest deployment → "Redeploy"
   - Or push a new commit to trigger automatic deployment

### 3️⃣ Update Backend CORS (Optional)

If you get CORS errors:
1. Go to Render dashboard → Your service
2. Go to "Environment" tab
3. Add environment variable:
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `https://deepfake-tracker.vercel.app,https://deepfake-tracker-priyam-mannas-projects.vercel.app`
4. Save and wait for automatic redeploy

### 4️⃣ Test Your Application

1. Visit your Vercel URL: `https://deepfake-tracker.vercel.app`
2. Try analyzing a URL
3. Check for any errors in:
   - Browser console (F12)
   - Render logs (Render Dashboard → Logs tab)

---

## 🔧 Local Development

To run locally after these changes:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

---

## 📝 Important Notes

### Render Free Tier Limitations:
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 50+ seconds (cold start)
- 750 hours/month free (enough for one service running 24/7)

### Vercel Free Tier:
- 100GB bandwidth/month
- 6000 build minutes/month
- Automatic HTTPS and CDN

### Updating Your App:
1. Push changes to GitHub
2. Vercel redeploys automatically
3. Render redeploys automatically (if auto-deploy enabled)

---

## 🐛 Troubleshooting

### CORS Errors:
- Make sure `VITE_API_URL` is set correctly in Vercel
- Verify Vercel URL is in backend's `allowed_origins`
- Check Render logs for CORS-related errors

### Backend Not Responding:
- Check Render logs for errors
- Verify the service is running (green status)
- Try the health check: `https://your-backend.onrender.com/api/health`

### Build Failures:
- Check that all dependencies are in requirements.txt
- Verify Python version compatibility
- Check Render build logs for specific errors

---

## 🎯 Next Steps

1. ✅ Deploy backend to Render
2. ✅ Get backend URL
3. ✅ Add `VITE_API_URL` to Vercel environment variables
4. ✅ Redeploy frontend
5. ✅ Test the application
6. 🎉 Share your live app!

Your current Vercel deployment: https://vercel.com/priyam-mannas-projects/deepfake-tracker
