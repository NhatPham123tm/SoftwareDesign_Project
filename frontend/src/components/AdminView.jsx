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
  const [showDelegateModal, setShowDelegateModal] = useState(false);
  const [selectedDelegatee, setSelectedDelegatee] = useState("");
  const [userDelegations, setUserDelegations] = useState([]);
  const [selectedForm, setSelectedForm] = useState(null);
  const [rejectionReason, setRejectionReason] = useState("");
  const [signatureData, setSignatureData] = useState(null); 
  const [signatureSaved, setSignatureSaved] = useState(false);
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [historyForm, setHistoryForm] = useState(null);
  const [activeTab, setActiveTab] = useState("status");

  const formTypeNames = {
    DiplomaRequestForm: "Diploma Request",
    ChangeAddressForm: "Change of Address",
    PayrollRequestForm: "Payroll Request",
    ReimbursementForm: "Reimbursement Request",
  }
  
  function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
  }

  const fetchUserDelegations = async() => {
    try {
      const response = await fetch("http://localhost:8000/api/user_delegations", {
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
        method: "GET",
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        setUserDelegations(data);
      } else {
        setMessage("Failed to fetch user delegations.");
      }
    } catch (error) {
      setMessage("Error fetching forms: " + error.message);
    }
  };

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
        console.log(nonDraftForms);
      } else {
        setMessage("Failed to fetch forms.");
      }
    } catch (error) {
      console.error("Error fetching forms:", error);
      setMessage("Something went wrong. Please try again.");
    }
  };
  
  useEffect(() => {
    fetchForms();
    fetchUserDelegations();
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
        fetchForms();
        fetchUserDelegations();
      } else {
        setMessage("Failed to update form.");
      }
    } catch (error) {
      console.error("Error approving/rejecting form:", error);
      setMessage("Something went wrong. Please try again.");
    }
  };

  const handleDelegate = async () => {
    if (!selectedDelegatee) {
      setMessage("Please select a delegatee.");
      return;
    }

    const body = {
      request: selectedForm.id,
      delegatee: selectedDelegatee,  
    };

    try {
      const response = await fetch("http://localhost:8000/api/delegate", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        credentials: "include",
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(`Delegation created successfully: ${data.delegator} delegated to ${data.delegatee_role}`);
        setShowDelegateModal(false);
        setSelectedForm(null);
        setSelectedDelegatee("");
        fetchForms();
        fetchUserDelegations();
      } else {
        const data = await response.json();
        setMessage(`Error: ${data.detail}`);
      }
    } catch (error) {
      setMessage("Error delegating task: " + error.message);
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
              <th>Submitted By</th>
              <th>Status</th>
              <th>Assigned To</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredForms.map((form) => (
              <tr key={form.id}>
                <td>{formTypeNames[form.form_type] || form.form_type}</td>
                <td>{form.data.name}</td>
                <td>{form.status}</td>
                <td>{form.assigned_to.name}</td>
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
                  <button
                    className="delegate-btn"
                    onClick={() => {
                      setSelectedForm(form);
                      setShowDelegateModal(true);
                      setSignatureData(null); 
                      setSignatureSaved(false); 
                    }}
                  >
                    Assign
                  </button>
                  <button
                    className="history-btn"
                    onClick={() => {
                      setHistoryForm(form);
                      setShowHistoryModal(true);
                    }}
                  >
                    View History
                  </button>
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
                onClick={() => {
                  setShowRejectModal(false);
                  setRejectionReason("");
                  setSelectedForm(null);
                }}
              >
                Cancel
              </button>

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
              
            </div>
          </div>
        </div>
      )}
      {showDelegateModal && selectedForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Assignees</h3>

            <select
              value={selectedDelegatee}
              onChange={(e) => setSelectedDelegatee(e.target.value)}
            >
              <option defaultValue="">Choose an Assignee</option>
              {userDelegations.map((delegatee, i) => (
                <option key={i} value={delegatee.id}>{delegatee.name} {delegatee.role_name}</option>
              ))}
            </select>

            <div className="modal-buttons">
              <button
                className="reject-btn"
                onClick={() => {
                  setShowDelegateModal(false);
                  setSelectedForm(null);
                  setSignatureData(null); 
                  setSignatureSaved(false); 
                }}
              >
                Cancel
              </button>

              <button
                className="delegate-btn"
                onClick={handleDelegate}
              >
                Assign
              </button>
            </div>
          </div>
        </div>
      )}
       {showHistoryModal && historyForm && (
          <div className="modal-overlay">
            <div className="modal-content history-modal">
              <h3>History for {historyForm.data?.name}</h3>
              <div className="history-tabs">
                <button
                  className={activeTab === "status" ? "active" : ""}
                  onClick={() => setActiveTab("status")}
                >
                  Status History
                </button>
                <button
                  className={activeTab === "delegation" ? "active" : ""}
                  onClick={() => setActiveTab("delegation")}
                >
                  Delegation History
                </button>
              </div>
              {activeTab === "status" && (
                <div className="history-content">
                  <h4>Status History</h4>
                  {historyForm.status_history?.length > 0 ? (
                    <div className="history-list">
                      <ul>
                        {historyForm.status_history.map((entry, index) => (
                          <li key={index}>
                            <strong>Status:</strong> {entry.status} <br />
                            <strong>Changed By:</strong> User {entry.changed_by} <br />
                            <strong>Time:</strong> {new Date(entry.timestamp).toLocaleString()}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : (
                    <p>No status history found.</p>
                  )}
                </div>
              )}
              {activeTab === "delegation" && (
                <div className="history-content">
                  <h4>Delegation History</h4>
                  {historyForm.delegate_history?.length > 0 ? (
                    <div className="history-list">
                      <ul>
                        {historyForm.delegate_history.map((entry, index) => (
                          <li key={index}>
                            <strong>Delegated To:</strong> User {entry.delegated_to} <br />
                            <strong>Delegator:</strong> User {entry.delegator} <br />
                            <strong>Time:</strong> {new Date(entry.timestamp).toLocaleString()}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : (
                    <p>No delegation history found.</p>
                  )}
                </div>
              )}
              <div className="modal-buttons">
                <button
                  className="reject-btn"
                  onClick={() => {
                    setShowHistoryModal(false);
                    setHistoryForm(null);
                  }}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
          )}
    </div>
  );
};

export default AdminView;
