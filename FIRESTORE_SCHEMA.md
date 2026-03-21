# Firebase Firestore Data Model - Complete Reference

## Overview
The application uses Firebase Firestore as the database. This document outlines the complete data structure and how it integrates with the frontend.

---

## Collections Structure

```
Firestore Database
├── products/          ← Product listings
├── users/             ← User profiles
├── sellers/           ← Seller information
├── carts/             ← Shopping carts
├── wishlists/         ← Wishlist items
├── orders/            ← Purchase orders
└── reviews/           ← Product reviews
```

---

## 1. Products Collection

### Firestore Path
```
/products/{productId}
```

### Document Structure

```javascript
{
  // Primary Fields
  "id": "product_xyz123",                    // Unique product ID
  "seller_id": "user_abc456",                // Firebase Auth user ID of seller
  "name": "Samsung Galaxy S21",              // Product name
  "description": "Used Samsung phone in excellent condition",
  "category": "electronics",                 // Category for filtering
  
  // Pricing
  "price": 35000,                            // Current selling price
  "original_price": 50000,                   // Original/MRP
  "discount_percentage": 30,                 // Calculated discount
  
  // Inventory
  "stock": 1,                                // Available quantity
  
  // Media
  "image_url": "https://...",                // Primary image URL
  "images": [                                // Array of image URLs
    "https://...",
    "https://...",
    "https://..."
  ],
  
  // Details
  "condition": "like-new",                   // new | like-new | used
  "tags": ["electronics", "phone", "used"],  // Search tags
  
  // Shipping & Returns
  "delivery_days": 3,                        // Expected delivery time
  "return_period_days": 7,                   // Return window
  
  // Metrics
  "views": 1205,                             // Number of product views
  "wishlist_count": 45,                      // Added to wishlist by
  "cart_count": 23,                          // Added to cart by
  "rating": 4.5,                             // Average rating (0-5)
  "review_count": 12,                        // Total reviews
  
  // Status
  "is_active": true,                         // Soft delete flag
  
  // Timestamps
  "created_at": 1704067200000,               // Unix timestamp (milliseconds)
  "updated_at": 1704067200000                // Unix timestamp (milliseconds)
}
```

### Field Details

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | ✅ | Unique product identifier |
| seller_id | string | ✅ | Firebase user ID of the seller |
| name | string | ✅ | Product title/name |
| description | string | ✅ | Product description |
| category | string | ✅ | Product category for filtering |
| price | float | ✅ | Current selling price |
| original_price | float | ✅ | Original/MRP (for discount calc) |
| discount_percentage | float | ⚠️ | Auto-calculated discount % |
| stock | integer | ✅ | Available quantity |
| image_url | string | ⚠️ | Primary product image |
| images | array | ⚠️ | Array of product images |
| condition | string | ✅ | E.g., "new", "like-new", "used" |
| tags | array | ⚠️ | Search tags |
| delivery_days | integer | ✅ | Days for delivery |
| return_period_days | integer | ✅ | Days for returns |
| views | integer | 🔧 | Auto-updated view count |
| wishlist_count | integer | 🔧 | Auto-updated wishlist count |
| cart_count | integer | 🔧 | Auto-updated cart count |
| rating | float | 🔧 | Average rating from reviews |
| review_count | integer | 🔧 | Total number of reviews |
| is_active | boolean | 🔧 | Soft delete (false = deleted) |
| created_at | number | 🔧 | Auto-set creation timestamp |
| updated_at | number | 🔧 | Auto-updated timestamp |

✅ = Required by user input  
⚠️ = Optional  
🔧 = System-managed

---

## 2. Frontend to Firebase Field Mapping

### When Creating Product

**Frontend Form** → **Firestore Document**

```javascript
// Frontend collects:
{
  title: "Samsung Galaxy S21",       // Maps to: name
  description: "...",                 // Maps to: description
  category: "electronics",            // Maps to: category
  price: 35000,                       // Maps to: price
  originalPrice: 50000,               // Maps to: original_price
  image: "https://...",               // Maps to: image_url
  images: [...],                      // Maps to: images
  stock: 1,                           // Maps to: stock
  condition: "like-new",              // Maps to: condition
  tags: [...],                        // Maps to: tags
  discount_percentage: 30,            // Maps to: discount_percentage
  delivery_days: 3,                   // Maps to: delivery_days
  return_period_days: 7               // Maps to: return_period_days
}

// API call transforms to:
POST /api/products/create
{
  name: "Samsung Galaxy S21",
  description: "...",
  category: "electronics",
  price: 35000,
  original_price: 50000,
  image_url: "https://...",
  images: [...],
  stock: 1,
  condition: "like-new",
  tags: [...],
  discount_percentage: 30,
  delivery_days: 3,
  return_period_days: 7
}
```

### When Rendering Products

**Firestore Document** → **Frontend Display**

```javascript
// Firestore returns:
{
  id: "prod_123",
  name: "Samsung Galaxy S21",
  image_url: "https://...",
  images: [...],
  seller_id: "user_abc",
  ...
}

// Frontend handles both old and new formats:
const title = product.title || product.name;
const image = product.image || product.image_url;
const seller = product.seller || "Unknown";

// Displays with fallbacks for missing fields
```

---

## 3. Example: Complete Flow

### User Creates a Product

**Step 1: Frontend Collects Data**
```javascript
{
  title: "iPhone 12",
  category: "electronics",
  price: 30000,
  originalPrice: 45000,
  description: "Excellent condition",
  images: ["url1", "url2"],
  condition: "like-new"
}
```

**Step 2: API Call**
```bash
POST http://localhost:5000/api/products/create
Authorization: Bearer {firebase_token}
Body: {
  name: "iPhone 12",
  category: "electronics",
  price: 30000,
  original_price: 45000,
  description: "Excellent condition",
  images: ["url1", "url2"],
  condition: "like-new"
}
```

**Step 3: Backend Processing**
```python
# Backend validates and transforms
product_id = "prod_1704067200000"
seller_id = extracted_from_token

# Backend creates in Firestore
/products/prod_1704067200000
{
  id: "prod_1704067200000",
  seller_id: "user_abc123",
  name: "iPhone 12",
  category: "electronics",
  price: 30000,
  original_price: 45000,
  description: "Excellent condition",
  images: ["url1", "url2"],
  condition: "like-new",
  is_active: true,
  created_at: 1704067200000,
  ... [other default fields]
}
```

**Step 4: Frontend Loads Products**
```javascript
// GET /api/products/all
// Returns: { success: true, products: [...] }

products = [
  {
    id: "prod_1704067200000",
    name: "iPhone 12",
    seller_id: "user_abc123",
    ...
  }
]

// Frontend renders with mapping
title = "iPhone 12"
seller = "Unknown" (only seller_id available)
price = 30000
```

---

## 4. Querying Products

### API Endpoints and Defaults

#### Get All Products
```bash
GET /api/products/all
GET /api/products/all?category=electronics
GET /api/products/all?category=electronics&limit=20&offset=0
GET /api/products/all?min_price=10000&max_price=50000

# Returns only products where is_active = true
```

#### Get Products by Seller
```bash
GET /api/products/seller/{seller_id}
GET /api/products/seller/{seller_id}?limit=50

# Returns all products where seller_id matches
```

#### Get Product Details
```bash
GET /api/products/{product_id}

# Returns single product with all fields
```

---

## 5. Firestore Query Limits & Rules

### Query Constraints
```
- Can only filter on ONE inequality operator per query
- Multiple equality filters are supported
- Cannot filter on missing fields by default
- Results limited to 100,000 documents per query
```

### Current Query Example
```javascript
db.collection('products')
  .where('is_active', '==', true)
  .where('category', '==', 'electronics')
  .where('price', '>=', 10000)
  .where('price', '<=', 50000)
  .limit(20)
  .offset(0)
```

---

## 6. Field Usage by Frontend Features

### Product Listing (Browse)
- ✅ Uses: `id`, `name`, `price`, `images`, `category`, `description`
- ⚠️ Missing: `seller` (only has seller_id)

### Product Details
- ✅ Uses: `id`, `name`, `price`, `original_price`, `images`, `description`, `condition`, `delivery_days`, `return_period_days`
- ⚠️ Additional needed: `seller_name`, `contact`, `email`, `location`

### Dashboard - My Products
- ✅ Uses: `id`, `name`, `price`, `category`, `seller_id` (for filtering)
- ✅ Auto-update: `views`, `wishlist_count`, `rating`

### Product Metrics
- ✅ `views` - Incremented on product view
- ✅ `rating` - Calculated from reviews
- ✅ `review_count` - Count of reviews
- ✅ `wishlist_count` - Count of wishlist adds
- ✅ `cart_count` - Count of cart adds

---

## 7. Future Enhancements

### Seller Information
Store seller name/contact directly with product:
```javascript
seller_name: "John Doe",
seller_email: "john@example.com",
seller_phone: "+91-9876543210",
seller_location: "Mumbai"
```

### Product Images in Firebase Storage
Instead of external URLs:
```javascript
// Current
image_url: "https://external-cdn.com/image.jpg"

// Future
image_url: "gs://bucket/products/prod_123/main.jpg"
images: [
  "gs://bucket/products/prod_123/img1.jpg",
  "gs://bucket/products/prod_123/img2.jpg"
]
```

### Inventory Tracking
```javascript
inventory: {
  total: 10,
  reserved: 2,
  available: 8
},
SKU: "PROD-12345"
```

---

## 8. Data Validation (Backend)

### Product Creation Validation
```python
required_fields = ['name', 'description', 'category', 'price', 'original_price', 'stock', 'condition']
validate_not_empty(field) for field in required_fields
validate_float(price, original_price)
validate_integer(stock, delivery_days, return_period_days)
validate_category(category)
validate_condition(condition in ['new', 'like-new', 'used'])
validate_price_logic(original_price >= price)  # Original must be >= selling price
```

### Price Validation
- Selling price must be > 0
- Original price must be >= selling price
- Discount percentage auto-calculated: `(original - selling) / original * 100`

---

## 9. Timestamps

### Format
- Unix timestamp in **milliseconds**
- Example: `1704067200000` = January 2, 2024, 08:00:00 UTC

### Usage
```javascript
// Creating
created_at = Date.now()  // Current timestamp

// Parsing in frontend
const date = new Date(product.created_at)
console.log(date.toLocaleDateString())  // "1/2/2024"

// Comparing
if (Date.now() - product.created_at < 86400000) {
  // Less than 1 day old
}
```

---

## 10. Security Rules (Firestore)

### Recommended Rules
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Products: Anyone can read active products, only owner can write
    match /products/{document=**} {
      allow read: if resource.data.is_active == true;
      allow create, update, delete: if request.auth.uid == resource.data.seller_id;
    }
    
    // Users: Only owner can read/write
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

---

## Summary

- ✅ Products stored in `/products` collection
- ✅ Each product has seller_id (not seller name)
- ✅ Frontend handles both old and new field names
- ✅ Images stored as URLs (external or Firebase Storage)
- ✅ All products must be `is_active: true` to display
- ✅ Soft deletes mark `is_active: false` instead of removing
- ✅ Metrics auto-updated: views, ratings, counts
- ✅ Full seller/contact info needs separate implementation

