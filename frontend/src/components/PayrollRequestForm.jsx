import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import './Form.css';
import Signature from './Signature'; 

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
}

const PayrollRequestForm = () => {
    const location = useLocation();
    const [message, setMessage] = useState("");
    const userDataRaw = localStorage.getItem("userData");
    const userData = userDataRaw ? JSON.parse(userDataRaw) : {};
    const fullName = userData.name || "";

    const [formData, setFormData] = useState({
        employeeName: "",
        employeeId: "",
        educationLevel: "", //Undergraduate, Graduate, PostDoc, Other
        requestedAction: "", //New Hire, Rehire/Transfer, Payroll Change
        startDate1: "",
        endDate1: "",
        salary1: "", //num
        fte1: "", //num
        speedType1: "",
        budgetPercentage1: "", //num
        positionTitle1: "",
        benefitsType1: "", //Eligible, Not Eligible, Insurance
        startDate2: "",
        endDate2: "",
        salary2: "", //num
        fte2: "", //num
        speedType2: "",
        budgetPercentage2: "", //num
        positionTitle2: "",
        benefitsType2: "", //Eligible, Not Eligible, Insurance
        //If Payroll Change
        jobTitle: "",
        positionNumber: "",
        terminationDate: "",
        terminationReason: "",
        budgetChangeEffectiveDate: "",
        fromSpeedType: "",
        toSpeedType: "",
        fteChangeEffectiveDate: "",
        fromFte: "", //num
        toFte: "", //num
        payRateChangeEffectiveDate: "",
        currentRate: "", //num
        newPayRate: "", //num
        payRateChangeReason: "",
        reallocationDates: "",
        reallocationFromPosition: "",
        reallocationToPosition: "",
        otherSpecification: "",
        date: new Date().toLocaleDateString(),
        form_type: "PayrollRequestForm",
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
        <h2>Payroll Request Form</h2>
  
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
          Education Level:
          <select
            name="educationLevel"
            value={formData.educationLevel}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select education level</option>
            <option value="Undergraduate">Undergraduate</option>
            <option value="Graduate">Graduate</option>
            <option value="PostDoc">PostDoc</option>
            <option value="Other">Other</option>
          </select>
        </label>
  
        <label>
          Requested Action:
          <select
            name="requestedAction"
            value={formData.requestedAction}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select an action</option>
            <option value="New Hire">New Hire</option>
            <option value="Rehire/Transfer">Rehire/Transfer</option>
            <option value="Payroll Change">Payroll Change</option>
          </select>
        </label>
  
        {/* First Assignment Details */}
        <h3>First Assignment</h3>
  
        <label>Start Date:
          <input type="date" name="startDate1" value={formData.startDate1} onChange={handleChange} />
        </label>
  
        <label>End Date:
          <input type="date" name="endDate1" value={formData.endDate1} onChange={handleChange} />
        </label>
  
        <label>Salary:
          <input type="number" name="salary1" value={formData.salary1} onChange={handleChange} />
        </label>
  
        <label>FTE:
          <input type="number" name="fte1" value={formData.fte1} onChange={handleChange} />
        </label>
  
        <label>SpeedType:
          <input type="text" name="speedType1" value={formData.speedType1} onChange={handleChange} />
        </label>
  
        <label>Budget %:
          <input type="number" name="budgetPercentage1" value={formData.budgetPercentage1} onChange={handleChange} />
        </label>
  
        <label>Position Title:
          <input type="text" name="positionTitle1" value={formData.positionTitle1} onChange={handleChange} />
        </label>
  
        <label>Benefits Type:
          <select name="benefitsType1" value={formData.benefitsType1} onChange={handleChange}>
            <option value="">Select</option>
            <option value="Eligible">Eligible</option>
            <option value="Not Eligible">Not Eligible</option>
            <option value="Insurance">Insurance</option>
          </select>
        </label>
  
        {/* Second Assignment Details */}
        <h3>Second Assignment (optional)</h3>
  
        <label>Start Date:
          <input type="date" name="startDate2" value={formData.startDate2} onChange={handleChange} />
        </label>
  
        <label>End Date:
          <input type="date" name="endDate2" value={formData.endDate2} onChange={handleChange} />
        </label>
  
        <label>Salary:
          <input type="number" name="salary2" value={formData.salary2} onChange={handleChange} />
        </label>
  
        <label>FTE:
          <input type="number" name="fte2" value={formData.fte2} onChange={handleChange} />
        </label>
  
        <label>SpeedType:
          <input type="text" name="speedType2" value={formData.speedType2} onChange={handleChange} />
        </label>
  
        <label>Budget %:
          <input type="number" name="budgetPercentage2" value={formData.budgetPercentage2} onChange={handleChange} />
        </label>
  
        <label>Position Title:
          <input type="text" name="positionTitle2" value={formData.positionTitle2} onChange={handleChange} />
        </label>
  
        <label>Benefits Type:
          <select name="benefitsType2" value={formData.benefitsType2} onChange={handleChange}>
            <option value="">Select</option>
            <option value="Eligible">Eligible</option>
            <option value="Not Eligible">Not Eligible</option>
            <option value="Insurance">Insurance</option>
          </select>
        </label>
  
        {/* Payroll Change Details */}
        {formData.requestedAction === "Payroll Change" && (
          <>
            <h3>Payroll Change Details</h3>
  
            <label>Job Title:
              <input type="text" name="jobTitle" value={formData.jobTitle} onChange={handleChange} />
            </label>
  
            <label>Position Number:
              <input type="text" name="positionNumber" value={formData.positionNumber} onChange={handleChange} />
            </label>
  
            <label>Termination Date:
              <input type="date" name="terminationDate" value={formData.terminationDate} onChange={handleChange} />
            </label>
  
            <label>Termination Reason:
              <input type="text" name="terminationReason" value={formData.terminationReason} onChange={handleChange} />
            </label>
  
            <label>Budget Change Effective Date:
              <input type="date" name="budgetChangeEffectiveDate" value={formData.budgetChangeEffectiveDate} onChange={handleChange} />
            </label>
  
            <label>From SpeedType:
              <input type="text" name="fromSpeedType" value={formData.fromSpeedType} onChange={handleChange} />
            </label>
  
            <label>To SpeedType:
              <input type="text" name="toSpeedType" value={formData.toSpeedType} onChange={handleChange} />
            </label>
  
            <label>FTE Change Effective Date:
              <input type="date" name="fteChangeEffectiveDate" value={formData.fteChangeEffectiveDate} onChange={handleChange} />
            </label>
  
            <label>From FTE:
              <input type="number" name="fromFte" value={formData.fromFte} onChange={handleChange} />
            </label>
  
            <label>To FTE:
              <input type="number" name="toFte" value={formData.toFte} onChange={handleChange} />
            </label>
  
            <label>Pay Rate Change Effective Date:
              <input type="date" name="payRateChangeEffectiveDate" value={formData.payRateChangeEffectiveDate} onChange={handleChange} />
            </label>
  
            <label>Current Rate:
              <input type="number" name="currentRate" value={formData.currentRate} onChange={handleChange} />
            </label>
  
            <label>New Pay Rate:
              <input type="number" name="newPayRate" value={formData.newPayRate} onChange={handleChange} />
            </label>
  
            <label>Pay Rate Change Reason:
              <input type="text" name="payRateChangeReason" value={formData.payRateChangeReason} onChange={handleChange} />
            </label>

            <label>Reallocation Dates:
                <input type="text" name="reallocationDates" value={formData.reallocationDates} onChange={handleChange} />
            </label>
    
            <label>Reallocation From Position:
                <input type="text" name="reallocationFromPosition" value={formData.reallocationFromPosition} onChange={handleChange} />
            </label>
    
            <label>Reallocation To Position:
                <input type="text" name="reallocationToPosition" value={formData.reallocationToPosition} onChange={handleChange} />
            </label>
    
            <label>Other Specification:
                <input type="text" name="otherSpecification" value={formData.otherSpecification} onChange={handleChange} />
            </label>
          </>
        )}
  
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

export default PayrollRequestForm;
