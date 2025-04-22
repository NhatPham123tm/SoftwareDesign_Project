import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import './Form.css';
import Signature from './Signature';

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
}

const ChangeAddressForm = () => {
  const location = useLocation();
  const [message, setMessage] = useState("");
  const userDataRaw = localStorage.getItem("userData");
  const userData = userDataRaw ? JSON.parse(userDataRaw) : {};
  const fullName = userData.name || "";

  const [formData, setFormData] = useState({
    name: "",
    birthdate: "",
    streetAddress: "",
    zipCode: "",
    city: "",
    pstreetAddress: "",
    pzipCode: "",
    pcity: "",
    mstreetAddress: "",
    mzipCode: "",
    mcity: "",
    state: "",
    pstate: "",
    mstate: "",
    date: new Date().toLocaleDateString(),
    form_type: "ChangeAddressForm",
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
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSignatureChange = (signatureData) => {
    setFormData((prev) => ({
      ...prev,
      signature: signatureData,
    }));
  };
  
  const navigate = useNavigate();
  const handleSubmit = async (e, status = 'submitted') => {
    e.preventDefault();

    const { draftId, ...dataToSend } = formData;
    dataToSend.status = status;

    const url = `http://localhost:8000/api/forms/${draftId ? `${draftId}/` : ''}`;

    try {
      const response = await fetch(url, {
        method: draftId ? "PUT" : "POST",
        credentials: "include", //  use session cookies
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
      body: JSON.stringify(dataToSend),
    });

      const data = await response.json();

      if (response.ok) {
        navigate('/forms');
        setMessage(status === 'submitted' ? "Form submitted successfully!" : "Form saved as draft.");
        if (status === 'Draft' && !draftId && data.request?.id) {
          setFormData((prev) => ({ ...prev, draftId: data.request.id }));
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

  const stateOptions = [
    { value: 'AL', label: 'Alabama' },
    { value: 'AK', label: 'Alaska' },
    { value: 'AZ', label: 'Arizona' },
    { value: 'AR', label: 'Arkansas' },
    { value: 'CA', label: 'California' },
    { value: 'CO', label: 'Colorado' },
    { value: 'CT', label: 'Connecticut' },
    { value: 'DE', label: 'Delaware' },
    { value: 'DC', label: 'District Of Columbia' },
    { value: 'FL', label: 'Florida' },
    { value: 'GA', label: 'Georgia' },
    { value: 'HI', label: 'Hawaii' },
    { value: 'ID', label: 'Idaho' },
    { value: 'IL', label: 'Illinois' },
    { value: 'IN', label: 'Indiana' },
    { value: 'IA', label: 'Iowa' },
    { value: 'KS', label: 'Kansas' },
    { value: 'KY', label: 'Kentucky' },
    { value: 'LA', label: 'Louisiana' },
    { value: 'ME', label: 'Maine' },
    { value: 'MD', label: 'Maryland' },
    { value: 'MA', label: 'Massachusetts' },
    { value: 'MI', label: 'Michigan' },
    { value: 'MN', label: 'Minnesota' },
    { value: 'MS', label: 'Mississippi' },
    { value: 'MO', label: 'Missouri' },
    { value: 'MT', label: 'Montana' },
    { value: 'NE', label: 'Nebraska' },
    { value: 'NV', label: 'Nevada' },
    { value: 'NH', label: 'New Hampshire' },
    { value: 'NJ', label: 'New Jersey' },
    { value: 'NM', label: 'New Mexico' },
    { value: 'NY', label: 'New York' },
    { value: 'NC', label: 'North Carolina' },
    { value: 'ND', label: 'North Dakota' },
    { value: 'OH', label: 'Ohio' },
    { value: 'OK', label: 'Oklahoma' },
    { value: 'OR', label: 'Oregon' },
    { value: 'PA', label: 'Pennsylvania' },
    { value: 'RI', label: 'Rhode Island' },
    { value: 'SC', label: 'South Carolina' },
    { value: 'SD', label: 'South Dakota' },
    { value: 'TN', label: 'Tennessee' },
    { value: 'TX', label: 'Texas' },
    { value: 'UT', label: 'Utah' },
    { value: 'VT', label: 'Vermont' },
    { value: 'VA', label: 'Virginia' },
    { value: 'WA', label: 'Washington' },
    { value: 'WV', label: 'West Virginia' },
    { value: 'WI', label: 'Wisconsin' },
    { value: 'WY', label: 'Wyoming' },
    
  ];

  return (
    <div className="form-container">
      <form onSubmit={(e) => handleSubmit(e, 'submitted')}>
        <h2>Change of Address Form</h2>

        <label>
          Name:
          <input type="text" name="name" value={formData.name} onChange={handleChange} required maxLength={50}/>
        </label>

        <label>
          Date of Birth:
          <input type="date" name="birthdate" value={formData.birthdate} onChange={handleChange} required max={new Date().toISOString().split("T")[0]} title="Please enter a date before today"/>
        </label>

        <label>
          Street Address:
          <input type="text" name="streetAddress" value={formData.streetAddress} onChange={handleChange} required maxLength={50}/>
        </label>

        <label>
          Zip Code:
          <input type="text" name="zipCode" value={formData.zipCode} onChange={handleChange} required minLength={5} maxLength={5} pattern="[0-9]+" title="Please enter 5-digit number only"/>
        </label>

        <label>
          City:
          <input type="text" name="city" value={formData.city} onChange={handleChange} required maxLength={50}/>
        </label>

        <label>
          State:
          <select type="text" name="state" value={formData.state} onChange={handleChange} required>
            <option value="" disabled>Select a State</option>
            {stateOptions.map((state) => (
            <option key={state.value} value={state.value}>
              {state.label}
            </option>
          ))}
          </select>
        </label>

        <label>
          Previous Street Address:
          <input type="text" name="pstreetAddress" value={formData.pstreetAddress} onChange={handleChange} required maxLength={50}/>
        </label>

        <label>
          Previous Zip Code:
          <input type="text" name="pzipCode" value={formData.pzipCode} onChange={handleChange} required minLength={5} maxLength={5} pattern="[0-9]+" title="Please enter 5-digit number only"/>
        </label>

        <label>
          Previous City:
          <input type="text" name="pcity" value={formData.pcity} onChange={handleChange} required maxLength={50}/>
        </label>

        <label>
          Previous State:
          <select type="text" name="pstate" value={formData.pstate} onChange={handleChange} required>
          <option value="" disabled>Select a State</option>
            {stateOptions.map((state) => (
            <option key={state.value} value={state.value}>
              {state.label}
            </option>
          ))}
          </select>
        </label>

        <label>
          Mailing Street Address (Optional):
          <input type="text" name="mstreetAddress" value={formData.mstreetAddress} onChange={handleChange} maxLength={50}/>
        </label>

        <label>
          Mailing Zip Code (Optional):
          <input type="text" name="mzipCode" value={formData.mzipCode} onChange={handleChange} minLength={5} maxLength={5} pattern="[0-9]+" title="Please enter 5-digit number only"/>
        </label>

        <label>
          Mailing City (Optional):
          <input type="text" name="mcity" value={formData.mcity} onChange={handleChange} maxLength={50}/>
        </label>

        <label>
          Mailing State (Optional):
          <select type="text" name="mstate" value={formData.mstate} onChange={handleChange}>
          <option value="" disabled>Select a State</option>
            {stateOptions.map((state) => (
            <option key={state.value} value={state.value}>
              {state.label}
            </option>
          ))}
          </select>
        </label>

        <label>
          Date:
          <input type="text" name="date" value={formData.date} onChange={handleChange} readOnly />
        </label>

        <div className="signature-container">
          <label>Signature:</label>
          <div className="signature-box">
            <Signature initialSignature={formData.signature} onSave={handleSignatureChange} />
          </div>
        </div>

        <div className="form-buttons">
          <button type="button" className="draft-btn" onClick={(e) => handleSubmit(e, 'Draft')}>
            Save as Draft
          </button>
        </div>
      </form>

      {message && <p className="form-message">{message}</p>}
    </div>
  );
};

export default ChangeAddressForm;