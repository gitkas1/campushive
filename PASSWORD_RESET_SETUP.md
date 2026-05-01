# 🔐 Password Reset Setup & Troubleshooting

## What Was Fixed

The password reset link generation has been updated with:
1. ✅ Proper `actionCodeSettings` configuration for Firebase
2. ✅ Detailed console logging for debugging
3. ✅ Better error messages and handling
4. ✅ Support for `auth/operation-not-allowed` error code

---

## How Password Reset Works

```
User enters email → Frontend validates → 
Firebase sends reset email → User clicks link in email → 
Password reset page opens → User creates new password
```

---

## Firebase Setup Requirements

### 1. Enable Email/Password Authentication
Your Firebase project needs email/password auth enabled:

**Steps:**
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: `d-cart-66ba5`
3. Click "Authentication" in left menu
4. Click "Get Started" or "Sign-in method"
5. Look for "Email/Password"
6. Make sure it's **ENABLED** (toggle should be ON - blue)
7. If not enabled, click it and toggle ON

✅ Screenshot: Should show "Email/Password" with a blue toggle switch

### 2. Configure Password Reset Email Template
Firebase sends password reset emails using an email template. You need to configure it:

**Steps:**
1. Go to Firebase Console → Your Project
2. Click "Authentication" → "Templates" tab
3. Look for "Password Reset" email template
4. Click the pencil/edit icon
5. Configure:
   - **Subject:** `Reset your password`
   - **From Name:** `CampusHive Support`
   - **Reply-to:** Your support email (if available)
6. Make sure the template includes `%LINK%` (Firebase will replace this with the actual reset link)
7. Click "Save"

✅ Expected Template Content:
```
Hello,

To reset your CampusHive password, click the link below:

%LINK%

If you didn't request this, you can safely ignore this email.

Best regards,
CampusHive Team
```

### 3. Set Your App Domain
Firebase needs to know your app's domain to generate correct reset links:

**Steps:**
1. Go to Firebase Console → Your Project
2. Click "Settings" (gear icon) → "Project Settings"
3. Click "Authentication" tab
4. Scroll down to "Authorized Domains"
5. Add these domains:
   - `localhost`
   - Your actual domain (when deployed)

✅ For development: `localhost` and `localhost:8000` should be listed

---

## Testing Password Reset

### Test Scenario 1: Reset with Valid Email
**Steps:**
1. Open your app in browser (http://localhost:8000)
2. Click "Forgot Password?" link
3. Enter email of an account you created earlier
4. Click "Send Reset Link"

**Expected Results:**
- ✅ Status message: "Password reset link sent to..."
- ✅ Email arrives in your inbox within 1-2 minutes
- ✅ Email contains a clickable link

**Check Browser Console (F12 → Console):**
- Should see: `🔐 Password Reset: Attempting to send reset email to: ...`
- Should see: `✅ Password reset email sent successfully to: ...`

---

### Test Scenario 2: Reset with Non-existent Email
**Steps:**
1. Click "Forgot Password?"
2. Enter email that doesn't exist (e.g., `nonexistent@test.com`)
3. Click "Send Reset Link"

**Expected Results:**
- ✅ Error: "No account found with this email address"
- ✅ Status div shows red background

---

### Test Scenario 3: Click Reset Link from Email
**Steps:**
1. After receiving password reset email
2. Click the link in the email
3. You should be taken to a password reset page

**Expected Results:**
- ✅ Page loads with password reset form
- ✅ Enter new password
- ✅ Password is updated successfully
- ✅ You can login with new password

---

## Troubleshooting

### ❌ Error: "Password reset is not enabled"
**Cause:** Firebase Email/Password auth provider is not enabled

**Fix:**
1. Go to Firebase Console
2. Authentication → Sign-in method
3. Find "Email/Password"
4. Toggle it ON (blue switch)
5. Save

---

### ❌ Error: "Error: undefined"
**Cause:** Missing or incorrect error handling

**Fix:**
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for the error details logged
4. Check if you see: `❌ Password Reset Error: ...`
5. Share the full error message

---

### ❌ Email not arriving
**Cause 1:** Email template not configured in Firebase

**Fix 1:**
1. Go to Firebase Console → Authentication → Templates
2. Find "Password Reset" template
3. Make sure it's configured and contains `%LINK%`
4. Click "Save" if you made changes

**Cause 2:** Email goes to spam folder

**Fix 2:**
1. Check your email spam/junk folder
2. Whitelist the sender: `noreply@d-cart-66ba5.firebaseapp.com`
3. Ask your email provider to not mark Firebase emails as spam

**Cause 3:** Too many requests

**Fix 3:**
- Wait a few minutes before trying again
- Firebase rate-limits to prevent abuse
- Try again after 5 minutes

---

### ❌ Reset link doesn't work
**Cause 1:** Link is expired (only valid for 24 hours)

**Fix 1:**
- Request a new password reset email
- Use the link within 24 hours

**Cause 2:** Link opened in different browser than signup

**Fix 2:**
- Use the same browser where you created your account
- Or clear cookies and try again

---

## Browser Console Debugging

### Open Console
- Press `F12` on your keyboard
- Go to "Console" tab
- Look for messages starting with 🔐

### Good Signs (Success)
```
🔐 Password Reset: Attempting to send reset email to: user@example.com
🔐 Action Code Settings: {url: "...", handleCodeInApp: true}
✅ Password reset email sent successfully to: user@example.com
```

### Bad Signs (Errors)
```
❌ Password Reset Error: [object Object]
Error Code: auth/operation-not-allowed
Error Message: The operation is not allowed...
```

---

## Quick Checklist

Before testing password reset, verify:
- [ ] Firebase project created at [console.firebase.google.com](https://console.firebase.google.com)
- [ ] Email/Password provider is ENABLED in Authentication settings
- [ ] Password Reset email template is configured
- [ ] Your domain is in "Authorized Domains"
- [ ] Backend server is running (if needed)
- [ ] Frontend app is open in browser

---

## Configuration Details for Development

### Current Firebase Config in `index.html`
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyBFc4oHkNcESYOWPRADRES0l1K7VYouUjI",
  authDomain: "d-cart-66ba5.firebaseapp.com",
  projectId: "d-cart-66ba5",
  databaseURL: "https://d-cart-66ba5-default-rtdb.firebaseio.com",
  storageBucket: "d-cart-66ba5.firebasestorage.app",
  messagingSenderId: "1042552533145",
  appId: "1:1042552533145:web:6656094a946e0faf1b4808",
  measurementId: "G-9Q5Z7RF503"
};
```

**Your Auth Domain:** `d-cart-66ba5.firebaseapp.com`

---

## Next Steps

1. **Test Now:** Try the password reset flow following the test scenarios
2. **Check Console:** Press F12 and watch the console messages
3. **Monitor Email:** Check your email for the reset link
4. **Report Issues:** If something doesn't work, check the browser console for error details

---

## Support

If password reset still doesn't work:
1. Open browser console (F12)
2. Try password reset
3. Copy all error messages from console
4. Share the error code and message

Common error codes to look for:
- `auth/user-not-found` - Email doesn't have an account
- `auth/invalid-email` - Email format is wrong
- `auth/too-many-requests` - Too many attempts, wait and retry
- `auth/operation-not-allowed` - Email/Password auth not enabled in Firebase
