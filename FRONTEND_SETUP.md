# 🎨 React Frontend - Setup & Build Guide

## Quick Start

```bash
# Create React app
npx create-react-app skincare-nepal-frontend
cd skincare-nepal-frontend

# Install dependencies
npm install axios tailwindcss react-router-dom zustand react-query

# Configure Tailwind
npx tailwindcss init -p

# Start development server
npm start
```

Visit: http://localhost:3000

---

## Project Structure

```
skincare-nepal-frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Profile.jsx
│   │   │   └── SkinAnalysis.jsx
│   │   ├── Consultations/
│   │   │   ├── BookConsultation.jsx
│   │   │   ├── ConsultationList.jsx
│   │   │   └── ChatWindow.jsx
│   │   ├── Products/
│   │   │   ├── ProductList.jsx
│   │   │   ├── ProductDetail.jsx
│   │   │   └── Cart.jsx
│   │   └── Common/
│   │       ├── Navbar.jsx
│   │       ├── Footer.jsx
│   │       └── Loading.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── consultations.js
│   │   ├── products.js
│   │   └── payments.js
│   ├── store/
│   │   ├── authStore.js
│   │   ├── userStore.js
│   │   └── cartStore.js
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── About.jsx
│   │   ├── Contact.jsx
│   │   └── NotFound.jsx
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── public/
├── package.json
└── tailwind.config.js
```

---

## Core Files to Create

### 1. API Service (`src/services/api.js`)

```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 2. Authentication Service (`src/services/auth.js`)

```javascript
import api from './api';

export const authService = {
  register: (userData) => api.post('/api/users/register', userData),
  login: (email, password) => api.post('/api/auth/login', { email, password }),
  getProfile: () => api.get('/api/users/me'),
  logout: () => localStorage.removeItem('access_token'),
};
```

### 3. Auth Store (`src/store/authStore.js`)

```javascript
import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  isLoggedIn: !!localStorage.getItem('access_token'),

  setUser: (user) => set({ user }),
  setToken: (token) => {
    localStorage.setItem('access_token', token);
    set({ token, isLoggedIn: true });
  },
  logout: () => {
    localStorage.removeItem('access_token');
    set({ user: null, token: null, isLoggedIn: false });
  },
}));
```

### 4. Login Component (`src/components/Auth/Login.jsx`)

```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { authService } from '../../services/auth';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const setToken = useAuthStore((state) => state.setToken);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authService.login(email, password);
      setToken(response.data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold mb-6">Login</h2>
        
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="mt-4 text-center">
          Don't have an account? <a href="/register" className="text-blue-600">Register</a>
        </p>
      </div>
    </div>
  );
}
```

### 5. Protected Route (`src/components/Auth/ProtectedRoute.jsx`)

```javascript
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export default function ProtectedRoute({ children }) {
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);

  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }

  return children;
}
```

### 6. App Routes (`src/App.jsx`)

```javascript
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
```

---

## Environment Variables

Create `.env`:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000
```

For production:
```
REACT_APP_API_URL=https://your-api.railway.app
```

---

## Key Features to Build

### 1. User Authentication
- ✅ Login/Register pages
- ✅ Protected routes
- ✅ JWT token management
- ✅ Profile management

### 2. Skin Analysis
- ✅ Photo upload
- ✅ Analysis display
- ✅ Recommendations
- ✅ History tracking

### 3. Consultations
- ✅ Book consultation
- ✅ List consultations
- ✅ Chat interface
- ✅ Payment integration

### 4. Products
- ✅ Product listing
- ✅ Product detail
- ✅ Shopping cart
- ✅ Checkout

---

## Deployment to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

---

## Styling with Tailwind

```bash
# tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
      },
    },
  },
  plugins: [],
}
```

---

## Testing

```bash
npm install @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

---

## Performance Tips

1. **Code Splitting**
   ```javascript
   import { lazy, Suspense } from 'react';
   const Dashboard = lazy(() => import('./Dashboard'));
   
   <Suspense fallback={<Loading />}>
     <Dashboard />
   </Suspense>
   ```

2. **Caching**
   - Use React Query for API caching
   - Implement service worker for offline support

3. **Images**
   - Optimize with tools like TinyPNG
   - Use WebP format
   - Lazy load images

---

## Ready to Build? 🚀

Next steps:
1. Create React app: `npx create-react-app skincare-nepal-frontend`
2. Install dependencies: `npm install axios tailwindcss react-router-dom zustand`
3. Create component structure
4. Build login/register flow
5. Connect to backend API
6. Deploy to Vercel

Start coding! 💻
