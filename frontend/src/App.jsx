import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useLocation } from "react-router-dom";
import { AuthProvider } from './context/AuthContext';
import Header from './components/Header';
import HomePage from './components/HomePage';
import ChangeAddressForm from './components/ChangeAddressForm';
import DiplomaRequestForm from './components/DiplomaRequestForm';
import Login from './components/Login';
import SignUp from './components/SignUp';
import UserForms from "./components/UserForms";
import AdminView from './components/AdminView';
import EmployeeManagement from './components/EmployeeManagement';
import ProtectedRoute from './components/ProtectedRoute';
import MicrosoftCallback from './components/MicrosoftCallback';

function App() {
  const hideHeaderRoutes = ["/", "/signup"];

  return (
    <AuthProvider>
      {!hideHeaderRoutes.includes(useLocation().pathname) && <Header />}
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/changeAddressForm" element={<ChangeAddressForm />} />
          <Route path="/diplomaRequestForm" element={<DiplomaRequestForm />} />
          <Route path="/forms" element={<UserForms />} />
          <Route path="/microsoft-callback" element={<MicrosoftCallback />} />
          <Route path="/admin/requests" element={<AdminView />} />
          <Route path="/employeeManagement" element={<EmployeeManagement />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;