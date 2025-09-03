// Test the fixed endpoints
const testFixedEndpoints = async () => {
  const apiUrl = 'https://guestrelationsapp.onrender.com/api';
  
  try {
    console.log('🔍 Testing fixed endpoints...');
    
    // Login first
    const formData = new FormData();
    formData.append("username", "admin");
    formData.append("password", "123");
    
    const loginResponse = await fetch(`${apiUrl}/auth/login`, {
      method: "POST",
      body: formData,
    });
    
    if (!loginResponse.ok) {
      console.log('❌ Login failed');
      return;
    }
    
    const loginData = await loginResponse.json();
    const authToken = loginData.access_token;
    const userId = loginData.user.id;
    
    console.log('✅ Login successful');
    
    // Test the main endpoints that were failing
    const endpoints = [
      { method: 'GET', path: '/tasks/', name: 'Tasks' },
      { method: 'GET', path: `/tasks/user/${userId}`, name: 'User Tasks' },
      { method: 'POST', path: '/tasks/daily?task_date=2024-01-01', name: 'Daily Tasks' },
      { method: 'GET', path: '/cases/', name: 'Cases' },
      { method: 'GET', path: '/cases/with-followups', name: 'Cases with Followups' },
      { method: 'GET', path: '/followups/with-case-info', name: 'Followups with Case Info' },
      { method: 'GET', path: '/users/', name: 'Users' },
      { method: 'GET', path: '/auth/me', name: 'Current User' }
    ];
    
    for (const endpoint of endpoints) {
      const options = {
        method: endpoint.method,
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      };
      
      const response = await fetch(`${apiUrl}${endpoint.path}`, options);
      console.log(`${endpoint.name}: ${response.status} ${response.statusText}`);
      
      if (response.ok) {
        console.log(`  ✅ ${endpoint.name} working`);
      } else {
        const errorText = await response.text();
        console.log(`  ❌ ${endpoint.name} failed: ${errorText}`);
      }
    }
    
    console.log('\n🎉 Endpoint test completed!');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
};

// Run the test
testFixedEndpoints();
