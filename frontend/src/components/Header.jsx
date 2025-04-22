import { useState } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Hamburger from '../assets/icons/hamburger.svg';
import Brand from '../assets/icons/logo.png';
import Back from '../assets/icons/backButton.png';
import './Header.css';

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
}

const Header = () => {
  const [showNavbar, setShowNavbar] = useState(false);
  const { logout, auth } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const isAuthPage = location.pathname === '/login' || 
                     location.pathname === '/signup' || 
                     location.pathname === '/microsoft-callback' ||
                     location.pathname === '/';
                     
  if (isAuthPage) {
    return null;
  }

  const handleLogout = () => {
    // Clear app data from localStorage
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("userData");
  
    // Optionally clear all localStorage
    // localStorage.clear();
  
    // Tell the backend to end the session and clear the sessionid cookie
    fetch("http://localhost:8000/logout/", {
      method: "POST",
      credentials: "include", // Include sessionid
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    }).then(() => {
      logout();        // clear context state
      navigate("/login");
    }).catch((err) => {
      console.error("Logout failed", err);
      logout();
      navigate("/login");
    });
  };
  
  const handleGoBack = () => {
    navigate(-1);
  };

  return (
    <nav className="navbar">
      <div className="back-button" onClick={handleGoBack}>
        <img src={Back} alt="Back Button" />
      </div>

      <NavLink to="/home" className="logo">
        <img src={Brand} alt="Brand Logo" />
      </NavLink>

      <div 
        className="menu-container"
        onMouseEnter={() => setShowNavbar(true)}
        onMouseLeave={() => setShowNavbar(false)}
      >
        <div className="menu-icon">
          <img src={Hamburger} alt="Hamburger Icon" />
        </div>

        <div className={`nav-elements ${showNavbar ? 'active' : ''}`}>
          <ul>
            <li>
              <NavLink to="/forms">View All Forms</NavLink>
            </li>
            <li>
              <NavLink to="/changeAddressForm">Change Address</NavLink>
            </li>
            <li>
              <NavLink to="/diplomaRequestForm">Request Diploma</NavLink>
            </li>
            {Number(auth?.role) === 1 && (
              <li>
                <NavLink to="/admin/requests">Admin</NavLink>
              </li>
            )}
            {Number(auth?.role) === 1 && (
              <li>
                <NavLink to="/employeeManagement">Employee Management</NavLink>
              </li>
            )}
            <li>
              <NavLink to="/login" className="logout-btn" onClick={handleLogout}>
                Logout
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;