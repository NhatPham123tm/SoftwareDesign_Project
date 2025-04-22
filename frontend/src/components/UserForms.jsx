import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import './UserForms.css';

const UserForms = () => {
  const [forms, setForms] = useState([]);
  const [message, setMessage] = useState("");
  const [selectedFormType, setSelectedFormType] = useState("");
  const [selectedStatus, setSelectedStatus] = useState(""); 
  const navigate = useNavigate();


  const formTypeNames = {
    DiplomaRequestForm: "Diploma Request",
    ChangeAddressForm: "Change of Address",
  };

  const statusOptions = ["Draft", "Pending", "Rejected", "Approved", "Cancelled"];

  const getCSRFToken = () => {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
  };

  useEffect(() => {
    const fetchUserForms = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/users/forms/", {
          headers: {
            'X-CSRFToken': getCSRFToken(),
          },
          method: "GET",
          credentials: "include",
        });

        const data = await response.json();

        if (response.ok) {
          setForms(data);
        } else {
          setMessage(data.error || "Failed to fetch forms.");
        }
      } catch (error) {
        setMessage("Error fetching forms: " + error.message);
      }
    };

    fetchUserForms();
  }, []);

  const deleteForm = async (formId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/forms/${formId}/delete/`, {
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
        method: "DELETE",
        credentials: "include", 
      });

      if (response.ok) {
        setForms((prevForms) => prevForms.filter((form) => form.id !== formId));
        setMessage("Form deleted successfully.");
      } else {
        const data = await response.json();
        setMessage(data.error || "Failed to delete form.");
      }
    } catch (error) {
      setMessage("Error deleting form: " + error.message);
    }
  };

  const editForm = (form) => {
    const formUrl = `/${form.form_type}`;

    navigate(formUrl, { state: { formData: form } });
  };

  const filteredForms = forms.filter((form) => {
    const matchesType = selectedFormType ? form.form_type === selectedFormType : true;
    const matchesStatus = selectedStatus ? form.status === selectedStatus : true;
    return matchesType && matchesStatus;
  });

  return (
    <div className="user-forms-container">
      <h2>Your Forms</h2>

      {message && <p className="message">{message}</p>}

      {/* Dropdown for Form Type */}
      <div className="dropdown">
        <label htmlFor="form-type">Select Form Type: </label>
        <select
          id="form-type"
          value={selectedFormType}
          onChange={(e) => setSelectedFormType(e.target.value)}
        >
          <option value="">All Forms</option>
          {Object.keys(formTypeNames).map((type) => (
            <option key={type} value={type}>
              {formTypeNames[type]}
            </option>
          ))}
        </select>
      </div>

      {/* Dropdown for Form Status */}
      <div className="dropdown">
        <label htmlFor="form-status">Select Status: </label>
        <select
          id="form-status"
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
        >
          <option value="">All Statuses</option>
          {statusOptions.map((status) => (
            <option key={status} value={status}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {filteredForms.length === 0 && <p>You have no forms that match the selected filters.</p>}

      {filteredForms.length > 0 && (
        <ul className="forms-list">
          {filteredForms.map((form) => (
            <li key={form.id} className="form-item">
              <div className="form-card">
                <h3 className="form-type">{formTypeNames[form.form_type]}</h3>
                <p className="form-status">Status: {form.status}</p>
                {form.status === "rejected" && form.reason_for_return && (
                  <p className="form-rejection-reason">
                    Rejection Reason: {form.reason_for_return}
                  </p>
                )}

                {form.pdf && (
                  <div className="pdf-link">
                    <a
                      href={`http://localhost:8000${form.pdf}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View PDF
                    </a>
                  </div>
                )}

                {form.status === "Draft" && (
                  <button className="edit-button" onClick={() => editForm(form)}>
                    Edit Draft
                  </button>
                )}

                <button className="delete-button" onClick={() => deleteForm(form.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default UserForms;
