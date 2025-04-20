import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import './Form.css';
import Signature from './Signature'; 

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
}

const ReimbursementForm = () => {
    const location = useLocation();
    const [message, setMessage] = useState("");
    const userDataRaw = localStorage.getItem("userData");
    const userData = userDataRaw ? JSON.parse(userDataRaw) : {};
    const fullName = userData.name || "";

    const [formData, setFormData] = useState({
        employeeName: "",
        employeeId: "",
        reimbursementItems: "",
        purpose: "",
        mealInfo: "",
        costCenter1: "",
        amount1: "",
        costCenter2: "",
        amount2: "",
        totalReimbursement: "",
        date: new Date().toLocaleDateString(),
        form_type: "ReimbursementForm",
        draftId: null,
        signature: "", 
    });

  useEffect(() => {
    setFormData(prevData => ({
      ...prevData,
      name: fullName,
    }));

    if (location.state?.formData?.data) {
      setFormData({
        ...location.state.formData.data,
        draftId: location.state.formData.id || null,
      });
    }
  }, [location.state, fullName]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSignatureChange = (signatureData) => {
    setFormData((prevState) => ({
      ...prevState,
      signature: signatureData,
    }));
  };
  
  const navigate = useNavigate();
  const handleSubmit = async (e, status = 'submitted') => {
    e.preventDefault();

    const requestData = {};
    for (let key in formData) {
      if (key !== 'draftId') {
        requestData[key] = formData[key];
      }
    }
    requestData.status = status;

    const draftId = formData.draftId || null;
    const url = `http://localhost:8000/api/forms/${draftId ? `${draftId}/` : ''}`;
    
    try {
      const response = await fetch(url, {
        method: draftId ? "PUT" : "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(requestData),
      });

      const data = await response.json();

      if (response.ok) {
        if (status === 'submitted') {
          navigate('/forms');
          setMessage("Form submitted successfully!");
        } else {
          setMessage("Form saved as draft.");
        }

        if (status === 'Draft' && !draftId && data.request && data.request.id) {
          setFormData((prevState) => ({
            ...prevState,
            draftId: data.request.id,
          }));
        }
      } else {
        setMessage(data.error || "Submission failed.");
        console.error("API error:", data);
      }
    } catch (error) {
      console.error("Submission error:", error);
      setMessage("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={(e) => handleSubmit(e, 'submitted')}>
        <h2>Reimbursement Form</h2>
  
        <label>
          Employee Name:
          <input
            type="text"
            name="employeeName"
            value={formData.employeeName}
            onChange={handleChange}
            required
          />
        </label>
  
        <label>
          Employee ID:
          <input
            type="text"
            name="employeeId"
            value={formData.employeeId}
            onChange={handleChange}
            required
          />
        </label>
  
        <label>
          Reimbursement Items:
          <input
            type="text"
            name="reimbursementItems"
            value={formData.reimbursementItems}
            onChange={handleChange}
            required
          />
        </label>
  
        <label>
          Purpose:
          <input
            type="text"
            name="purpose"
            value={formData.purpose}
            onChange={handleChange}
            required
          />
        </label>
  
        <label>
          Meal Info (if applicable):
          <input
            type="text"
            name="mealInfo"
            value={formData.mealInfo}
            onChange={handleChange}
          />
        </label>
  
        <label>
          Cost Center 1:
          <input
            type="text"
            name="costCenter1"
            value={formData.costCenter1}
            onChange={handleChange}
          />
        </label>
  
        <label>
          Amount 1:
          <input
            type="number"
            name="amount1"
            value={formData.amount1}
            onChange={handleChange}
          />
        </label>
  
        <label>
          Cost Center 2:
          <input
            type="text"
            name="costCenter2"
            value={formData.costCenter2}
            onChange={handleChange}
          />
        </label>
  
        <label>
          Amount 2:
          <input
            type="number"
            name="amount2"
            value={formData.amount2}
            onChange={handleChange}
          />
        </label>
  
        <label>
          Total Reimbursement:
          <input
            type="number"
            name="totalReimbursement"
            value={formData.totalReimbursement}
            onChange={handleChange}
            required
          />
        </label>
  
        <label>
          Date:
          <input
            type="text"
            name="date"
            value={formData.date}
            onChange={handleChange}
            readOnly
          />
        </label>
  
        <div className="signature-container">
          <label>Signature:</label>
          <div className="signature-box">
            <Signature initialSignature={formData.signature} onSave={handleSignatureChange} />
          </div>
        </div>
  
        <div className="form-buttons">
          <button type="button" onClick={(e) => handleSubmit(e, 'Draft')}>Save as Draft</button>
          <button type="submit">Submit</button>
        </div>
      </form>
  
      {message && <p className="form-message">{message}</p>}
    </div>
  );
};

export default ReimbursementForm;
