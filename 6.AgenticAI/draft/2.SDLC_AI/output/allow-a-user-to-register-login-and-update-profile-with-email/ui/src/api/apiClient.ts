import axios from 'axios';

const API_URL = 'https://api.example.com'; // Replace with your API URL

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const loginUser = async (email: string, password: string) => {
  const response = await apiClient.post('/login', { email, password });
  return response.data;
};

export const getUserProfile = async (token: string) => {
  const response = await apiClient.get('/profile', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};
```

### 2. Login Form Component
```typescript
