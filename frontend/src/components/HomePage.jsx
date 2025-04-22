import React from 'react';
import './HomePage.css';
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
}

const HomePage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAuthData = async () => {
      const localUserData = localStorage.getItem("userData");
      const accessToken = localStorage.getItem("access_token");
  
      if (localUserData && accessToken) {
        const user = JSON.parse(localUserData);
        login(user);
        return;
      }
  
      // If local auth fails, try session login
      axios.get("http://localhost:8000/api/microsoft-login/", {
        withCredentials: true,
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      })
      .then((res) => {
        if (res.status === 200) {
          const { user } = res.data;
          login({
            userId: user.id,
            name: user.name,
            email: user.email,
            role: user.role,
            status: user.status,
          });
        } else {
          console.warn("Unexpected response status. Redirecting.");
          navigate("/login");
        }
      })
      .catch((err) => {
        console.warn("No session cookie found or error occurred. Redirecting to login.", err);
        navigate("/login");
      });
    };
  
    fetchAuthData();
  }, []);
  
  return (
    <div className="home-container">
      <div className="box-container">
        <div className="box">
          <h2>Welcome to Uranium City</h2>
          <p>Under Maintenance</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
