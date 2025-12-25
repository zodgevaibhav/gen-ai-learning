import React from 'react';
import UserProfile from '../components/UserProfile';

const ProfilePage: React.FC<{ token: string }> = ({ token }) => {
  return (
    <div>
      <h1>Your Profile</h1>
      <UserProfile token={token} />
    </div>
  );
};

export default ProfilePage;
```

### Notes
- Ensure to handle token storage (e.g., in local storage) and retrieval for the profile page.
- You may want to implement routing using `react-router-dom` to navigate between pages.
- Consider adding error handling, loading states, and form validation for a production-ready application.
- Security measures such as HTTPS, input sanitization, and proper error handling should be implemented in the API and UI.