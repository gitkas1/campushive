// ============================================
// 🔌 API CONNECTION SETUP
// ============================================

const API_BASE = 'http://localhost:5000/api';

/**
 * Get Firebase ID token
 */
async function getFirebaseIdToken() {
  try {
    const user = firebase.auth().currentUser;
    if (!user) {
      console.warn('No user logged in');
      return null;
    }
    return await user.getIdToken();
  } catch (error) {
    console.error('Error getting ID token:', error);
    return null;
  }
}

/**
 * Make API call to backend
 */
async function apiCall(endpoint, method = 'GET', body = null) {
  const token = await getFirebaseIdToken();
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };
  
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`;
  }
  
  if (body) {
    options.body = JSON.stringify(body);
  }
  
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, options);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error);
    throw error;
  }
}

// ============================================
// 🛒 PRODUCT OPERATIONS
// ============================================

/**
 * Add to cart
 */
async function addToCart(productId, quantity = 1) {
  try {
    const token = await getFirebaseIdToken();
    
    if (!token) {
      alert('Please login to add items to cart');
      return false;
    }
    
    const result = await apiCall('/cart/add', 'POST', {
      product_id: productId,
      quantity: parseInt(quantity)
    });
    
    if (result.success) {
      alert(`✅ Added ${quantity} item(s) to cart`);
      return true;
    }
  } catch (error) {
    alert('Error adding to cart: ' + error.message);
    return false;
  }
}

/**
 * Add to wishlist
 */
async function addToWishlist(productId) {
  try {
    const token = await getFirebaseIdToken();
    
    if (!token) {
      alert('Please login to use wishlist');
      return false;
    }
    
    const result = await apiCall('/wishlist/add', 'POST', {
      product_id: productId
    });
    
    if (result.success) {
      alert('❤️ Added to wishlist');
      return true;
    }
  } catch (error) {
    alert('Error: ' + error.message);
  }
}

/**
 * Get all products
 */
async function getAllProducts() {
  try {
    const result = await apiCall('/products/all', 'GET');
    
    if (result.success) {
      console.log('✅ Products loaded:', result.products);
      return result.products;
    }
  } catch (error) {
    console.error('Error loading products:', error);
  }
}

/**
 * Create a new product (save to Firebase)
 */
async function createProduct(productData) {
  try {
    const token = await getFirebaseIdToken();
    
    if (!token) {
      alert('❌ Please login to create products');
      return null;
    }
    
    const result = await apiCall('/products/create', 'POST', {
      name: productData.title,
      description: productData.description,
      category: productData.category,
      price: productData.price,
      original_price: productData.originalPrice,
      image_url: productData.image || '',
      images: productData.images || [],
      stock: productData.stock || 1,
      condition: productData.condition || 'new',
      tags: productData.tags || [],
      discount_percentage: productData.discount_percentage || 0,
      delivery_days: productData.delivery_days || 3,
      return_period_days: productData.return_period_days || 7
    });
    
    if (result.success) {
      console.log('✅ Product created:', result.product_id);
      return result.product_id;
    } else {
      alert('❌ Error creating product: ' + result.error);
      return null;
    }
  } catch (error) {
    console.error('Error creating product:', error);
    alert('❌ Error: ' + error.message);
    return null;
  }
}

/**
 * Delete a product
 */
async function deleteProductFromFirebase(productId) {
  try {
    const token = await getFirebaseIdToken();
    
    if (!token) {
      alert('❌ Please login to delete products');
      return false;
    }
    
    const result = await apiCall(`/products/${productId}`, 'DELETE');
    
    if (result.success) {
      console.log('✅ Product deleted:', productId);
      return true;
    } else {
      alert('❌ Error deleting product: ' + result.error);
      return false;
    }
  } catch (error) {
    console.error('Error deleting product:', error);
    alert('❌ Error: ' + error.message);
    return false;
  }
}

/**
 * Filter products by category
 */
async function filterByCategory(category) {
  try {
    const result = await apiCall(`/products/all?category=${category}`, 'GET');
    
    if (result.success) {
      console.log(`✅ Filtered by ${category}:`, result.products);
      return result.products;
    }
  } catch (error) {
    console.error('Error filtering:', error);
  }
}

/**
 * Get cart
 */
async function getCart() {
  try {
    const result = await apiCall('/cart/', 'GET');
    
    if (result.success) {
      console.log('✅ Cart:', result.cart);
      return result.cart;
    }
  } catch (error) {
    console.error('Error getting cart:', error);
  }
}

/**
 * Get product details
 */
async function getProductDetails(productId) {
  try {
    const result = await apiCall(`/products/${productId}`, 'GET');
    
    if (result.success) {
      console.log('✅ Product details:', result.product);
      return result.product;
    }
  } catch (error) {
    console.error('Error loading product:', error);
  }
}

// ============================================
// ⭐ REVIEW OPERATIONS
// ============================================

/**
 * Add review
 */
async function addReview(productId, rating, comment) {
  try {
    const token = await getFirebaseIdToken();
    
    if (!token) {
      alert('Please login to leave a review');
      return false;
    }
    
    const result = await apiCall('/reviews/add', 'POST', {
      product_id: productId,
      rating: parseInt(rating),
      comment: comment
    });
    
    if (result.success) {
      alert('✅ Review submitted!');
      return true;
    }
  } catch (error) {
    alert('Error: ' + error.message);
  }
}

/**
 * Get product reviews
 */
async function getProductReviews(productId) {
  try {
    const result = await apiCall(`/reviews/${productId}`, 'GET');
    
    if (result.success) {
      console.log('✅ Reviews:', result.reviews);
      return result.reviews;
    }
  } catch (error) {
    console.error('Error loading reviews:', error);
  }
}

// ============================================
// 👤 SELLER OPERATIONS
// ============================================

/**
 * Get seller profile
 */
async function getSellerProfile(sellerId) {
  try {
    const result = await apiCall(`/sellers/${sellerId}`, 'GET');
    
    if (result.success) {
      console.log('✅ Seller:', result.seller);
      return result.seller;
    }
  } catch (error) {
    console.error('Error loading seller:', error);
  }
}

/**
 * Follow seller
 */
async function followSeller(sellerId) {
  try {
    const token = await getFirebaseIdToken();
    
    if (!token) {
      alert('Please login to follow');
      return false;
    }
    
    const result = await apiCall(`/sellers/${sellerId}/follow`, 'POST');
    
    if (result.success) {
      alert('✅ Following seller');
      return true;
    }
  } catch (error) {
    alert('Error: ' + error.message);
  }
}

// ============================================
// 🔍 SEARCH & FILTER
// ============================================

/**
 * Search products by price range
 */
async function searchByPrice(minPrice, maxPrice) {
  try {
    const result = await apiCall(`/products/all?min_price=${minPrice}&max_price=${maxPrice}`, 'GET');
    
    if (result.success) {
      console.log(`✅ Products from ₹${minPrice} to ₹${maxPrice}:`, result.products);
      return result.products;
    }
  } catch (error) {
    console.error('Error searching:', error);
  }
}

// ============================================
// ✅ API STATUS CHECK
// ============================================

/**
 * Check if backend is online
 */
async function checkBackendStatus() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    const result = await response.json();
    
    if (result.status === 'healthy') {
      console.log('✅ Backend is online and running!');
      return true;
    }
  } catch (error) {
    console.error('❌ Backend is offline:', error);
    return false;
  }
}

// ============================================
// 🎯 INITIALIZE ON PAGE LOAD
// ============================================

document.addEventListener('DOMContentLoaded', async function() {
  console.log('🚀 Website loaded!');
  
  // Check if backend is online
  const isBackendOnline = await checkBackendStatus();
  
  if (isBackendOnline) {
    console.log('✅ Ready to use marketplace features!');
    
    // Load products on page load
    getAllProducts();
  } else {
    console.warn('⚠️ Backend is offline. Make sure to run start_server.bat');
  }
  
  // Setup Firebase auth listener
  firebase.auth().onAuthStateChanged(user => {
    if (user) {
      console.log('✅ User logged in:', user.email);
    } else {
      console.log('👤 No user logged in');
    }
  });
});
