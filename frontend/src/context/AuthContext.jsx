// AuthContext.js

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem("userData");

    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setAuth(parsedUser);
    }

    setLoading(false);
  }, []);

  const login = useCallback((user) => {
    // user = { userId, name, email, role, status }
    const userData = {
      id: user.userId,
      name: user.name,
      email: user.email,
      role: user.role,
      status: user.status,
    };

    localStorage.setItem("userData", JSON.stringify(userData));
    setAuth(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("userData");
    document.cookie = ""
    setAuth(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        auth,
        login,
        logout,
        loading,
        isAuthenticated: !!auth,
        userId: auth?.id || null,
        name: auth?.name || null,
        email: auth?.email || null,
        role: auth?.role || null,
        status: auth?.status || null,
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};
