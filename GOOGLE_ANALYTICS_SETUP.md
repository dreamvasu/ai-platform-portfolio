# Google Analytics Setup

## Quick Setup (5 minutes)

### 1. Create Google Analytics 4 Property

1. Go to [Google Analytics](https://analytics.google.com/)
2. Click **Admin** (gear icon, bottom left)
3. Click **Create Property**
4. Enter property name: `Vasu Kapoor Portfolio`
5. Select timezone and currency
6. Click **Next**
7. Select **Industry category**: Technology
8. Select **Business size**: Small
9. Click **Create**
10. Accept Terms of Service

### 2. Set Up Data Stream

1. Select platform: **Web**
2. Enter website URL: `https://www.vasukapoor.com`
3. Enter stream name: `Portfolio Website`
4. Click **Create stream**

### 3. Get Your Measurement ID

You'll see your **Measurement ID** on the next screen:
```
G-XXXXXXXXXX
```

**Copy this ID!**

### 4. Add to Your Website

Open `frontend/index.html` and replace `G-XXXXXXXXXX` with your actual Measurement ID:

```html
<!-- BEFORE -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>

<!-- AFTER (example with real ID) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ABC123DEF4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-ABC123DEF4');
</script>
```

### 5. Deploy

```bash
cd frontend
git add index.html
git commit -m "Add Google Analytics tracking"
git push origin main
```

Vercel will auto-deploy the updated site.

### 6. Verify It's Working

1. Visit your deployed site: https://www.vasukapoor.com
2. Go back to Google Analytics
3. Click **Reports** → **Realtime**
4. You should see yourself as an active user!

---

## What Gets Tracked

Google Analytics will automatically track:

- **Page views**: Which pages users visit
- **Traffic sources**: How users find your site (Google, LinkedIn, direct, etc.)
- **Geography**: Where your visitors are from
- **Devices**: Desktop vs mobile usage
- **Session duration**: How long users stay
- **Bounce rate**: Users who leave immediately

---

## Useful Reports for Your Portfolio

### 1. Traffic Sources (Acquisition → Traffic Acquisition)
See if recruiters are coming from:
- LinkedIn posts
- Job applications
- Google searches
- Direct links

### 2. Popular Pages (Engagement → Pages and screens)
Which case studies get the most views:
- `/case-studies` (most important!)
- `/` (homepage)
- `/kubernetes`, `/gcp`, `/rag` (technical pages)

### 3. User Demographics (User → Demographic details)
- Countries (are you getting views from companies you applied to?)
- Cities (tech hubs like SF, Seattle, NYC?)

---

## Pro Tips

### Add Custom Events

Track specific actions like:
- Case study PDF downloads
- GitHub repo clicks
- Contact form submissions

Add this to your React components:

```javascript
// Example: Track case study view
useEffect(() => {
  if (window.gtag) {
    window.gtag('event', 'case_study_view', {
      'case_study_name': 'Calibra Production Platform',
      'page_path': window.location.pathname
    });
  }
}, []);
```

### Track Outbound Links

```javascript
<a
  href="https://github.com/yourusername"
  onClick={() => {
    if (window.gtag) {
      window.gtag('event', 'click', {
        'event_category': 'outbound',
        'event_label': 'GitHub Profile'
      });
    }
  }}
>
  GitHub
</a>
```

---

## Privacy & GDPR

Since you're tracking basic analytics on a portfolio site, you're generally okay. But if you want to be extra compliant:

1. Add a simple privacy notice in your footer:
```
"This site uses Google Analytics to understand visitor behavior."
```

2. Consider adding a cookie consent banner (optional for portfolio sites)

---

## Common Issues

**"I don't see any data"**
- Wait 24-48 hours for initial data
- Check Realtime reports (shows live data)
- Make sure you deployed the changes
- Verify the Measurement ID is correct

**"Data seems wrong"**
- Filter out your own visits: Admin → Data Settings → Data Filters
- Exclude your IP address from tracking

---

**Status:** Analytics code added to `frontend/index.html` - ready to use once you add your Measurement ID!
