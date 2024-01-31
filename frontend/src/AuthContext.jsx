import { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const storedAccessToken = localStorage.getItem('accessToken');
  const storedUserId = localStorage.getItem('userId');

  const [accessToken, setAccessToken] = useState(storedAccessToken || null);
  const [userId, setUserId] = useState(storedUserId || null);

  const login = (token, id) => {
    setAccessToken(token);
    setUserId(id);
    localStorage.setItem('accessToken', token);
    localStorage.setItem('userId', id);
  };

  const logout = () => {
    setAccessToken(null);
    setUserId(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userId');
  };

  return (
    <AuthContext.Provider value={{ accessToken, userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
