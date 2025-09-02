// Test script to verify frontend-backend connection
// Run this in the browser console to test the API connection

const testApiConnection = async () => {
  const API_URL = 'https://guestrelationsapp.onrender.com/api';
  
  try {
    console.log('🧪 Testing API connection...');
    
    // Test health endpoint
    const healthResponse = await fetch(`${API_URL}/health`);
    const healthData = await healthResponse.json();
    console.log('✅ Health check:', healthData);
    
    // Test root endpoint
    const rootResponse = await fetch('https://guestrelationsapp.onrender.com/');
    const rootData = await rootResponse.json();
    console.log('✅ Root endpoint:', rootData);
    
    console.log('🎉 API connection successful!');
    return true;
  } catch (error) {
    console.error('❌ API connection failed:', error);
    return false;
  }
};

// Run the test
testApiConnection();
