# ✅ Firebase Product Persistence - Setup Checklist

## Pre-Flight Checks

### ✅ Backend Setup
- [ ] Navigate to `backend/` folder
- [ ] Verify `backend/config/serviceAccountKey.json` exists (Firebase service account credentials)
- [ ] Verify `requirements.txt` has all dependencies
  - [ ] `firebase-admin`
  - [ ] `flask`
  - [ ] `flask-cors`
  
### ✅ Python Environment
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Install dependencies: 
  ```bash
  cd backend
  pip install -r requirements.txt
  ```

### ✅ Firebase Configuration
- [ ] Service account key exists at `backend/config/serviceAccountKey.json`
- [ ] Firestore database is created in Firebase Console
- [ ] Firebase project is active and accessible

---

## Starting the Application

### 1️⃣ Start Backend Server
```bash
cd backend
python run.py
```

**Expected Output:**
```
✅ Firebase initialized successfully
* Running on http://127.0.0.1:5000
```

### 2️⃣ Open Frontend
```bash
cd ..
# Open index.html in your browser
# Or use a simple HTTP server:
python -m http.server 8000
# Then open http://localhost:8000
```

---

## Testing the Setup

### Test 1: Create a Product
**Steps:**
1. ✅ Login to the app (or signup)
2. ✅ Verify your email (check email for verification link)
3. ✅ Go to "Sell" section
4. ✅ Fill in all product details:
   - Title: "Test Product"
   - Category: "Electronics"
   - Original Price: 500
   - Selling Price: 400
   - Description: "Test product description"
   - Product Condition: "New"
   - Upload at least 1 image
5. ✅ Click "List Product"

**Expected Results:**
- ✅ Success popup appears
- ✅ Product appears in "Browse" section
- ✅ Product appears in "Home" section

### Test 2: Verify Products Persist
**Steps:**
1. ✅ After creating product, refresh the page (Ctrl+R)
2. ✅ Product should still be visible in "Browse"

**Expected Results:**
- ✅ Product is still there after refresh
- ✅ No "add to cart" needed

### Test 3: Cross-Device Testing
**Steps:**
1. ✅ Create product on Device A
2. ✅ Open app on Device B (different device/browser)
3. ✅ Navigate to "Browse" section

**Expected Results:**
- ✅ Product created on Device A visible on Device B
- ✅ Same product appears for all users

### Test 4: Delete Product
**Steps:**
1. ✅ Go to Dashboard/My Products
2. ✅ Find a product you created
3. ✅ Click "Delete Product"
4. ✅ Confirm deletion

**Expected Results:**
- ✅ Product disappears from Dashboard
- ✅ Product disappears from Browse/Home sections
- ✅ After refresh, product is still gone

### Test 5: Firebase Verification
**Steps:**
1. ✅ Go to [Firebase Console](https://console.firebase.google.com)
2. ✅ Open your project
3. ✅ Go to Firestore Database
4. ✅ Look for `products` collection

**Expected Results:**
- ✅ `products` collection exists
- ✅ Documents in collection match created products
- ✅ Each document has fields: `id`, `name`, `price`, `seller_id`, etc.

---

## Troubleshooting

### ❌ "Cannot POST /api/products/create"
**Problem:** Backend API not running
**Solution:**
1. Check if backend server is running (`python run.py`)
2. Verify port 5000 is not in use
3. Check terminal for errors
4. Try: `netstat -ano | findstr :5000` (Windows)

### ❌ "Error: Products loaded: undefined"
**Problem:** API is not returning products
**Solutions:**
1. Check backend console for errors
2. Verify Firebase service account key exists
3. Check Firebase Firestore has `products` collection
4. Verify user is authenticated

### ❌ "Email Not Verified!" when creating product
**Problem:** User hasn't verified email
**Solution:**
1. Go to email inbox
2. Click verification link from Firebase
3. Wait for email verification
4. Try creating product again

### ❌ Products showing "Seller: Seller" instead of actual name
**Problem:** Seller name not stored in Firebase
**Note:** This is expected - only seller_id is stored
**Future Enhancement:** Fetch seller name from Firestore `sellers` collection

### ❌ "Failed to fetch" error
**Problem:** CORS or connection error
**Solutions:**
1. Ensure backend is running on `http://localhost:5000`
2. Check if API_BASE in `api-integration.js` is correct
3. Check network tab in browser DevTools for all requests

---

## Browser Console Debugging

### Check Console (Press F12 → Console tab)

**Expected messages:**
```
✅ Firebase ready, loading products...
📥 Loading products from Firebase...
✅ Loaded 3 products from Firebase
```

**Error patterns to watch for:**
```
❌ Error loading products: ...
❌ [401] Unauthorized
❌ CORS error
❌ Firebase not initialized
```

### Check Network Tab (Press F12 → Network)

**Look for these API calls:**
- `GET /api/products/all` - Should return 200 with products
- `POST /api/products/create` - Should return 201 with product_id
- `DELETE /api/products/{id}` - Should return 200

---

## Quick Reference Commands

### Backend
```bash
# Start backend
cd backend && python run.py

# Check if running
curl http://localhost:5000/api/products/all

# View logs
# Check terminal where you ran python run.py
```

### Frontend
```bash
# Simple HTTP server (in project root)
python -m http.server 8000
# Then open http://localhost:8000

# On Windows:
python -m http.server 8000
```

### Firebase CLI (Optional)
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Deploy if needed
firebase deploy
```

---

## Success Indicators ✅

After completing setup, you should see:

1. ✅ Products created in "Sell" section appear immediately in "Browse"
2. ✅ Refreshing page doesn't lose products
3. ✅ Opening app from different device shows same products
4. ✅ Deleting product removes it from all views
5. ✅ Firebase Console shows products in `products` collection
6. ✅ No errors in browser console when creating/viewing products

---

## Next Steps (Optional)

1. 🚀 Deploy backend to cloud (Heroku, Google Cloud, etc.)
2. 🚀 Set up image storage in Firebase Storage
3. 🚀 Add seller profile information display
4. 🚀 Implement product search
5. 🚀 Add real-time product updates

---

## Support

If products still don't persist:
1. Check browser console (F12) for errors
2. Check backend console for API errors
3. Verify Firebase credentials in `serviceAccountKey.json`
4. Verify Firestore database is active in Firebase Console
5. Check network requests in DevTools

