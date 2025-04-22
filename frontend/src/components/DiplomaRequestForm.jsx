import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import './Form.css';
import Signature from './Signature'; 

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
}

const DiplomaRequestForm = () => {
  const location = useLocation();
  const [message, setMessage] = useState("");
  const userDataRaw = localStorage.getItem("userData");
  const userData = userDataRaw ? JSON.parse(userDataRaw) : {};
  const fullName = userData.name || "";
  const studentID = userData.id || "";


  const [formData, setFormData] = useState({
    StudentIdNumber: "",
    name: "",
    email: "",
    birthDate: "",
    phoneNumber: "",
    degree: "",
    major: "",
    honors: "",
    college: "",
    GradDateSemester: "spring",
    GradDateYear: "",
    address: "",
    date: new Date().toLocaleDateString(),
    form_type: "DiplomaRequestForm",
    draftId: null,
    signature: "", 
  });

  useEffect(() => {
    setFormData(prevData => ({
      ...prevData,
      name: fullName,
      StudentIdNumber: studentID
    }));

    if (location.state?.formData?.data) {
      setFormData({
        ...location.state.formData.data,
        draftId: location.state.formData.id || null,
      });
    }
  }, [location.state, fullName, studentID]);

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
        <h2>Diploma Request Form</h2>

        <label>
          Student ID:
          <input
            type="text"
            name="StudentIdNumber"
            value={formData.StudentIdNumber || ""}
            onChange={handleChange}
            required
            minLength={7}
            maxLength={7}
            pattern="[0-9]+" 
            title="Please enter 7-digit number only"
          />
        </label>

        <label>
          Name:
          <input
            type="text"
            name="name"
            value={formData.name || ""}
            onChange={handleChange}
            required
            maxLength={50}
          />
        </label>

        <label>
          Email:
          <input
            type="email"
            name="email"
            value={formData.email || ""}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Date of Birth:
          <input
            type="date"
            name="birthDate"
            value={formData.birthDate || ""}
            onChange={handleChange}
            required
            max={new Date().toISOString().split("T")[0]}
            title="Please enter a date before today"
          />
        </label>

        <label>
          Phone:
          <input
            type="tel"
            name="phoneNumber"
            value={formData.phoneNumber || ""}
            onChange={handleChange}
            required
            minLength={10}
            maxLength={10}
            pattern="[0-9]+" 
            title="Please enter numbers only"
          />
        </label>

        <label>
          Degree:
          <select
            type="text"
            name="degree"
            value={formData.degree || ""}
            onChange={handleChange}
            required
            maxLength={50}>
            <option value="" disabled>Select a Degree</option>
            <option value="Asso">Associate</option>
            <option value="Bach">Bachelor's</option>
            <option value="Mast">Master's</option>
            <option value="Doct">Doctoral</option>
          </select>
        </label>

        <label>
          Major:
          <input
            type="text"
            name="major"
            value={formData.major || ""}
            onChange={handleChange}
            required
            maxLength={50}
          />
        </label>

        <label>
          Honors (Optional):
          <input
            type="text"
            name="honors"
            value={formData.honors || ""}
            onChange={handleChange}
            maxLength={50}
          />
        </label>

        <label>
          College:
          <input
            type="text"
            name="college"
            value={formData.college || ""}
            onChange={handleChange}
            required
            maxLength={50}
          />
        </label>

        <label>
          Graduation Semester:
          <select
            name="GradDateSemester"
            value={formData.GradDateSemester || "spring"}
            onChange={handleChange}
            required>
            <option value="" disabled>Select a Semester</option>
            <option value="spring">Spring</option>
            <option value="summer">Summer</option>
            <option value="fall">Fall</option>
          </select>
        </label>

        <label>
          Graduation Year:
          <input
            type="text"
            name="GradDateYear"
            value={formData.GradDateYear}
            onChange={handleChange}
            required
            minLength={4}
            maxLength={4}
            pattern="[0-9]{4}"
            title="Please enter 4-digit year"
          />
        </label>

        <label>
          Address:
          <input
            type="text"
            name="address"
            value={formData.address || ""}
            onChange={handleChange}
            required
            maxLength={50}
          />
        </label>

        <label>
          Date:
          <input
            type="text"
            name="date"
            value={formData.date || new Date().toLocaleDateString()}
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
          <button
            type="button"
            onClick={(e) => handleSubmit(e, 'Draft')}
          >
            Save as Draft
          </button>
        </div>
      </form>

      {message && <p className="form-message">{message}</p>}
    </div>
  );
};

export default DiplomaRequestForm;