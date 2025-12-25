import React, { useState } from 'react';
import LoginForm from '../components/LoginForm';
import { useHistory } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const [token, setToken] = useState<string | null>(null);
  const history = useHistory();

  const handleLogin = (token: string) => {
    setToken(token);
    history.push('/profile'); // Redirect to profile page after login
  };

  return (
    <div>
      <h1>Login</h1>
      <LoginForm onLogin={handleLogin} />
    </div>
  );
};

export default LoginPage;
```

### 5. Profile Page
```typescript
