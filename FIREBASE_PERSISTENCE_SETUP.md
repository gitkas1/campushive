# Firebase Product Persistence Setup

## Overview
✅ **Products are now stored in Firebase Firestore** instead of localStorage, so they persist across devices and users.

## Problem Solved
Previously:
- ❌ Products were stored only in browser localStorage
- ❌ Products disappeared when accessing the app from another device
- ❌ Products disappeared after clearing browser cache

Now:
- ✅ Products are saved to Firebase Firestore database
- ✅ Products persist across all devices
- ✅ Products are linked to user accounts via seller_id
- ✅ Products are automatically loaded from database on each visit

---

## Architecture

### Backend (Python/Flask)
**File**: `backend/app/models/product.py`

The backend already had full Firebase Firestore integration:
- `Product.create()` - Creates a new product in Firestore
- `Product.get_by_id()` - Retrieves a single product
- `Product.update()` - Updates product details
- `Product.delete()` - Soft deletes (marks as inactive)
- `Product.get_by_seller()` - Gets all products from a seller
- `Product.get_all()` - Gets all active products with filters

**Firestore Collection**: `products`

Product fields stored:
```
{
  id: string (unique product ID),
  seller_id: string (Firebase user ID),
  name: string,
  description: string,
  category: string,
  price: float,
  original_price: float,
  image_url: string,
  images: array,
  stock: integer,
  condition: string (new, like-new, used),
  tags: array,
  created_at: timestamp,
  updated_at: timestamp,
  views: integer,
  wishlist_count: integer,
  cart_count: integer,
  rating: float,
  review_count: integer,
  is_active: boolean,
  discount_percentage: float,
  delivery_days: integer,
  return_period_days: integer
}
```

### Frontend (JavaScript)
**API Integration File**: `api-integration.js`

New API functions added:
1. `createProduct(productData)` - Creates a product via API
2. `deleteProductFromFirebase(productId)` - Deletes a product via API
3. `getAllProducts()` - Fetches all products from Firebase
4. `filterByCategory(category)` - Filters products by category

**Main File**: `index.html`

Changes made:
1. Removed `localStorage.removeItem('products')` on page load
2. Added `loadProductsFromFirebase()` function
3. Updated `listProduct()` to call `createProduct()` API instead of localStorage
4. Updated `deleteProduct()` to call `deleteProductFromFirebase()` API
5. Updated product rendering functions to handle Firebase format
6. Products array now loaded from Firebase instead of localStorage

---

## How It Works

### 1. **Creating a Product** (When user lists a product)
```
User fills form → listProduct() → createProduct() API call 
→ Backend creates in Firestore → Success modal shows 
→ loadProductsFromFirebase() reloads all products
```

### 2. **Loading Products** (When page loads)
```
Page loads → loadProductsFromFirebase() 
→ getAllProducts() API call → Backend queries Firestore 
→ Products array updated → renderProducts() displays them
```

### 3. **Deleting a Product** (When seller deletes)
```
User clicks delete → deleteProduct() 
→ deleteProductFromFirebase() API call 
→ Backend marks product is_active=false in Firestore 
→ loadProductsFromFirebase() reloads updated list
```

---

## API Endpoints

### Create Product
```
POST /api/products/create
Authorization: Bearer {firebase_token}
Body: {
  name: string,
  description: string,
  category: string,
  price: float,
  original_price: float,
  image_url: string,
  images: array,
  stock: integer,
  condition: string,
  tags: array,
  discount_percentage: float,
  delivery_days: integer,
  return_period_days: integer
}
Returns: { success: true, product_id: string }
```

### Get All Products
```
GET /api/products/all?category={category}&limit=50&offset=0
Returns: { 
  success: true, 
  products: array, 
  count: integer 
}
```

### Get Product Details
```
GET /api/products/{product_id}
Returns: { success: true, product: object }
```

### Delete Product
```
DELETE /api/products/{product_id}
Authorization: Bearer {firebase_token}
Returns: { success: true, message: string }
```

---

## Setup Instructions

### 1. Firebase Service Account Key
✅ Already in place at `backend/config/serviceAccountKey.json`

### 2. Backend Requirements
All Python dependencies already in `backend/requirements.txt`:
- firebase-admin
- flask
- python-dotenv
- etc.

Install with:
```bash
pip install -r backend/requirements.txt
```

### 3. Start Backend Server
```bash
cd backend
python run.py
```

The API will run at `http://localhost:5000`

### 4. Frontend Configuration
✅ API base URL already configured in `api-integration.js`:
```javascript
const API_BASE = 'http://localhost:5000/api';
```

### 5. Load index.html
✅ Open `index.html` in your browser
✅ Products will automatically load from Firebase on page load

---

## Testing

### Test Creating a Product
1. Login to the app
2. Go to "Sell" section
3. Fill in product details
4. Click "List Product"
5. ✅ Product should appear in "Browse" section
6. ✅ Refresh page - product still there
7. ✅ Open in another browser/device - product visible

### Test Deleting a Product
1. Go to Dashboard/My Products
2. Click delete on a product
3. ✅ Product disappears from all views
4. ✅ Refresh page - still deleted

### Test Persistence Across Devices
1. Create a product on Device A
2. Go to Device B
3. Open the same app
4. ✅ Product from Device A visible on Device B

---

## Troubleshooting

### Products not showing after creation
**Issue**: Created product doesn't appear
**Solution**:
1. Check browser console for errors (F12)
2. Make sure backend is running (`python run.py`)
3. Make sure Firebase service account key exists
4. Check network tab for failed API calls

### API connection errors
**Issue**: "Error connecting to API"
**Solution**:
1. Verify backend is running on port 5000
2. Check that API_BASE in `api-integration.js` is correct
3. Make sure user is logged in (Firebase auth token needed)

### No products loading from Firebase
**Issue**: Products array stays empty
**Solution**:
1. Check Firebase Firestore console for products collection
2. Verify products have `is_active: true` field
3. Check Firebase authentication is working
4. Look at browser console for API errors

### Seller information not showing
**Issue**: "Seller: Seller" instead of actual name
**Solution**:
- Products only store `seller_id`, not seller name
- To show seller name, need to either:
  a. Add seller name to product when creating, or
  b. Fetch seller profile separately via seller_id

---

## Email Verification Requirement
✅ Products can only be listed after email is verified
- User must verify email from Firebase email link
- "Email Not Verified" alert shows if product creation attempted without verification

---

## Data Migration (If needed)
To migrate old localStorage products to Firebase:

1. Modify `listProduct()` temporarily to accept old product format:
```javascript
const newProduct = {
  // Add title -> name mapping
  name: title,
  // Add all other fields...
};
```

2. Run import script to transfer data:
```javascript
// In browser console while on app
products.forEach(p => createProduct(p));
```

---

## Performance Notes
- Firebase rules allow 1 read per document retrieval
- Consider pagination for large product catalogs
- Products load asynchronously after page loads
- UI updates automatically when Firebase data arrives

---

## Next Steps (Optional Enhancements)
1. Add seller info lookup (fetch seller name from seller_id)
2. Add real-time updates using Firebase listeners
3. Add image upload to Firebase Storage
4. Add search/advanced filtering
5. Add product recommendations based on category
6. Implement caching to reduce Firebase reads

---

## Summary of Changes Made

### Backend
- ✅ No changes needed - already fully integrated with Firebase

### Frontend (api-integration.js)
- ✅ Added `createProduct()` function
- ✅ Added `deleteProductFromFirebase()` function

### Frontend (index.html)
- ✅ Removed `localStorage.removeItem('products')` 
- ✅ Added `loadProductsFromFirebase()` function
- ✅ Made `listProduct()` async and calls API
- ✅ Updated `deleteProduct()` to use API
- ✅ Updated all product rendering to handle Firebase format
- ✅ Updated `showProductDetail()` for Firebase fields
- ✅ Updated `buyProduct()` and `buyProductFromDetail()`
- ✅ Updated `renderProducts()` and `renderHomeProducts()`

---

## Questions?
Check your backend logs and browser console for detailed error messages.

