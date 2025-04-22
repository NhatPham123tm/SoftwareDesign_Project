import React, { useState, useEffect } from "react";
import './HomePage.css';
import Signature from "./Signature"; 
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
  const [role, setrole] = useState("");
  const [forms, setForms] = useState([]);
  const [userDelegations, setUserDelegations] = useState([]);
  const [message, setMessage] = useState("");
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [showApproveModal, setShowApproveModal] = useState(false);
  const [showDelegateModal, setShowDelegateModal] = useState(false);
  const [selectedForm, setSelectedForm] = useState(null);
  const [selectedDelegatee, setSelectedDelegatee] = useState("");
  const [rejectionReason, setRejectionReason] = useState("");
  const [signatureData, setSignatureData] = useState(null); 
  const [signatureSaved, setSignatureSaved] = useState(false);
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [historyForm, setHistoryForm] = useState(null);
  const [activeTab, setActiveTab] = useState("status");
  const [viewMode, setViewMode] = useState("current"); 

  const formTypeNames = {
    DiplomaRequestForm: "Diploma Request",
    ChangeAddressForm: "Change of Address",
    PayrollRequestForm: "Payroll Request",
    ReimbursementForm: "Reimbursement Request",
  };

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
      const response = await fetch("http://localhost:8000/api/delegated_requests", {
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
      } else {
        setMessage("Failed to fetch forms.");
      }
    } catch (error) {
      setMessage("Error fetching forms:", error);
    }
  };

  useEffect(() => {
    const fetchAuthData = async () => {
      const localUserData = localStorage.getItem("userData");
      const accessToken = localStorage.getItem("access_token");
  
      if (localUserData && accessToken) {
        const user = JSON.parse(localUserData);
        login(user);
        setrole(user.role)
        if(user.role == 2){
          navigate("/forms");
        }
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
          setrole(user.role)
          if(user.role == 2){
            navigate("/forms");
          }
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
    fetchForms();
    fetchUserDelegations();
  }, []);

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
      } else {
        const data = await response.json();
        setMessage(`Error: ${data.detail}`);
      }
    } catch (error) {
      setMessage("Error delegating task: " + error.message);
    }
  };

  const filteredForms = forms.filter(form => {
    if (viewMode === "current") {
      return !["approved", "rejected"].includes(form.status.toLowerCase());
    } else {
      return ["approved", "rejected"].includes(form.status.toLowerCase());
    }
  });

  return (
    <div className="">
      { role === 2 ? (
        <div className="box-container">
          <div className="box">
            <h2>Welcome to Uranium City</h2>
            <p>Access Forms on the Right</p>
          </div>
        </div>
      ) : (
        <div className="admin-view-container">
          <div className="admin-header">
            <h2 className="admin-view-header">Tasks</h2>
            <div className="view-toggle">
              <button 
                className={`toggle-btn ${viewMode === "current" ? "active" : ""}`}
                onClick={() => setViewMode("current")}
              >
                Current Tasks
              </button>
              <button 
                className={`toggle-btn ${viewMode === "completed" ? "active" : ""}`}
                onClick={() => setViewMode("completed")}
              >
                Completed Tasks
              </button>
            </div>
          </div>
          
          {message && <p className="form-message">{message}</p>}

          {filteredForms.length === 0 ? (
            <p className="no-forms-message">No {viewMode} tasks found.</p>
          ) : (
            <table className="forms-table">
              <thead>
                <tr>
                  <th>Form Type</th>
                  <th>Submitted By</th>
                  <th>Status</th>
                  <th>Delegator</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredForms.map((form) => (
                  <tr key={form.id}>
                    <td>{formTypeNames[form.form_type] || form.form_type}</td>
                    <td>{form.data.name}</td>
                    <td>{form.status}</td>
                    <td>{form.delegator ? form.delegator.name : "System"}</td>
                    <td>
                      {viewMode === "current" && (
                        <>
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
                            Delegate
                          </button>
                        </>
                      )}
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
          {showDelegateModal && selectedForm && (
            <div className="modal-overlay">
              <div className="modal-content">
                <h3>Delegatees</h3>

                <select
                  value={selectedDelegatee}
                  onChange={(e) => setSelectedDelegatee(e.target.value)}
                >
                  <option defaultValue="">Choose a Delegatee</option>
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
                    Delegate
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
      )}
    </div>
  );
};

export default HomePage;