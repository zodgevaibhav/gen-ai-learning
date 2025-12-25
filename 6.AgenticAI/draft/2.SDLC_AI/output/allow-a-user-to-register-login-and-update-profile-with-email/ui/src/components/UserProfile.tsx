import React, { useEffect, useState } from 'react';
import { getUserProfile } from '../api/apiClient';

const UserProfile: React.FC<{ token: string }> = ({ token }) => {
  const [profile, setProfile] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getUserProfile(token);
        setProfile(data);
      } catch (err) {
        setError('Failed to fetch profile.');
      }
    };

    fetchProfile();
  }, [token]);

  if (error) return <p>{error}</p>;
  if (!profile) return <p>Loading...</p>;

  return (
    <div>
      <h2>User Profile</h2>
      <p>Name: {profile.name}</p>
      <p>Email: {profile.email}</p>
      {/* Add more profile fields as needed */}
    </div>
  );
};

export default UserProfile;
```

### 4. Login Page
```typescript
