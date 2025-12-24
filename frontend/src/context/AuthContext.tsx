import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

interface AuthContextType {
  isLoggedIn: boolean;
  login: (pin: string) => boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

const ADMIN_PIN = '2026';
const AUTH_KEY = 'sonos_admin_auth';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    // Check localStorage on initial load
    return localStorage.getItem(AUTH_KEY) === 'true';
  });

  useEffect(() => {
    // Persist auth state
    localStorage.setItem(AUTH_KEY, isLoggedIn ? 'true' : 'false');
  }, [isLoggedIn]);

  const login = (pin: string): boolean => {
    if (pin === ADMIN_PIN) {
      setIsLoggedIn(true);
      return true;
    }
    return false;
  };

  const logout = () => {
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
