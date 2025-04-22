import React, { useState, useEffect } from "react";
import Signature from "./Signature"; 
import './AdminView.css';

const AdminView = () => {
  const [forms, setForms] = useState([]);
  const [filteredForms, setFilteredForms] = useState([]);
  const [message, setMessage] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("submitted");
  const [selectedFormType, setSelectedFormType] = useState("");
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [showApproveModal, setShowApproveModal] = useState(false);
  const [selectedForm, setSelectedForm] = useState(null);
  const [rejectionReason, setRejectionReason] = useState("");
  const [signatureData, setSignatureData] = useState(null); 
  const [signatureSaved, setSignatureSaved] = useState(false); 

  const formTypeNames = {
    DiplomaRequestForm: "Diploma Request",
    ChangeAddressForm: "Change of Address",
  };
  
  function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
  }
  
  useEffect(() => {
    const fetchForms = async () => {

      try {
        const response = await fetch("http://localhost:8000/api/admin/requests/", {
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        });

        if (response.ok) {
          const data = await response.json();
          const nonDraftForms = data.filter(form => form.status !== "Draft");
          setForms(nonDraftForms);
          setFilteredForms(nonDraftForms);
        } else {
          setMessage("Failed to fetch forms.");
        }
      } catch (error) {
        console.error("Error fetching forms:", error);
        setMessage("Something went wrong. Please try again.");
      }
    };

    fetchForms();
  }, []); 

  useEffect(() => {
    const filtered = forms.filter((form) => {
      const matchesStatus = selectedStatus === "all" || form.status === selectedStatus;
      const matchesFormType = selectedFormType ? form.form_type === selectedFormType : true;
      return matchesStatus && matchesFormType;
    });
    setFilteredForms(filtered);
  }, [selectedStatus, selectedFormType, forms]);

  const handleApproval = async (id, status, reason = "") => {

    const body = { status };
    if (status === "rejected") {
      body.reason_for_return = reason;
    }
    
    if (signatureData) {
      body.admin_signature = signatureData;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/admin/requests/${id}/${status}/`, {
        method: "PUT",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        setMessage(`Form ${status} successfully!`);
        setForms((prevForms) =>
          prevForms.map((form) =>
            form.id === id
              ? { ...form, status, reason_for_return: body.reason_for_return || "" }
              : form
          )
        );
        setSignatureData(null);

        
        setShowApproveModal(false);
      } else {
        setMessage("Failed to update form.");
      }
    } catch (error) {
      console.error("Error approving/rejecting form:", error);
      setMessage("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="admin-view-container">
      <h2 className="admin-view-header">Submitted Forms</h2>
      {message && <p className="form-message">{message}</p>}

      <div className="dropdown">
        <label htmlFor="form-type">Filter by Form Type: </label>
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

      <div className="dropdown">
        <label htmlFor="status">Filter by Status: </label>
        <select
          id="status"
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
        >
          <option value="all">All</option>
          <option value="submitted">Submitted</option>
          <option value="rejected">Rejected</option>
          <option value="approved">Approved</option>
        </select>
      </div>

      {filteredForms.length === 0 ? (
        <p className="no-forms-message">No matching forms found.</p>
      ) : (
        <table className="forms-table">
          <thead>
            <tr>
              <th>Form Type</th>
              <th>Name</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredForms.map((form) => (
              <tr key={form.id}>
                <td>{formTypeNames[form.form_type] || form.form_type}</td>
                <td>{form.data.name}</td>
                <td>{form.status}</td>
                <td>
                  <button
                    className="approve-btn"
                    onClick={() => {
                      setSelectedForm(form);
                      setShowApproveModal(true);
                      setSignatureData(null); 
                      setSignatureSaved(false); 
                    }}
                  >
                    Approve
                  </button>
                  <button
                    className="reject-btn"
                    onClick={() => {
                      setSelectedForm(form);
                      setShowRejectModal(true);
                    }}
                  >
                    Reject
                  </button>
                  {form.pdf && (
                    <div className="pdf-link">
                      <a
                        href={`http://localhost:8000/${form.pdf}`}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        View PDF
                      </a>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {showApproveModal && selectedForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Approve Form</h3>
            <p>Please sign to approve <strong>{selectedForm?.data?.name}'s</strong> form:</p>
            <Signature label="Admin Signature" onSave={(signature) => {
              setSignatureData(signature);
              setSignatureSaved(true);  
            }} />

            <div className="modal-buttons">
              <button
                className="approve-btn"
                onClick={() => {
                  if (signatureSaved) {
                    handleApproval(selectedForm.id, "approved");
                  } else {
                    setMessage("Please provide a signature before submitting.");
                  }
                }}
              >
                Submit Approval
              </button>
              <button
                className="reject-btn"
                onClick={() => {
                  setShowApproveModal(false);
                  setSelectedForm(null);
                  setSignatureData(null);
                  setSignatureSaved(false);
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {showRejectModal && selectedForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Reject Form</h3>
            <p>Please provide a reason for rejecting <strong>{selectedForm?.data?.name}'s</strong> form:</p>
            <textarea
              value={rejectionReason}
              onChange={(e) => setRejectionReason(e.target.value)}
              placeholder="Enter rejection reason..."
            />
            <div className="modal-buttons">
              <button
                className="reject-btn"
                onClick={async () => {
                  if (!rejectionReason.trim()) {
                    setMessage("Rejection reason is required.");
                    return;
                  }

                  await handleApproval(selectedForm.id, "rejected", rejectionReason);
                  setShowRejectModal(false);
                  setRejectionReason("");
                  setSelectedForm(null);
                }}
              >
                Submit Rejection
              </button>
              <button
                className="reject-btn"
                onClick={() => {
                  setShowRejectModal(false);
                  setRejectionReason("");
                  setSelectedForm(null);
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminView;
