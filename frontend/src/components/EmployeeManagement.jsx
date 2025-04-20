import React, { useState, useEffect } from "react";
import Modal from './Modal';
import './AdminView.css';

const EmployeeManagement = () => {
    const [employee, setEmployee] = useState(null);
    const [employees, setEmployees] = useState([]);
    const [filteredEmployees, setFilteredEmployees] = useState([]);
    const [selectedStatus, setSelectedStatus] = useState("all");
    const [selectedRole, setSelectedRole] = useState("all");
    const [selectedDepartment, setSelectedDepartment] = useState("");
    const [modal, setModal] = useState(false);
    const [form, setForm] = useState({
        name: "",
        email: "",
        status: "",
        role_name: "",
        role_department: "",
      });

    const Roles = {
        admin: "Admin",
        manager: "Manager",
        employee: "Employee",
    };

    const Departments = {
        all: "All",
        finance: "Finance",
        registrar: "Registrar",
    };

    function getCSRFToken() {
        const match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? match[1] : null;
    }

    const toggleModal = async (employee) => {
        setEmployee(employee);
        setForm({
            name: employee.name,
            email: employee.email,
            status: employee.status,
            role_name: employee.role.role_name,
            role_department: employee.role.department,
        });
        setModal(!modal);
    };

    const handleInputChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (id) => {
        fetch(`http://localhost:8000/api/ura/${id}/`, {
            method: "PATCH",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify(form),
        })
        .then(() => {
            fetchEmployees();
            setModal(false);
        })
        .catch((error) => console.error("Error updating employee:", error));
    };

    const fetchEmployees = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/ura", {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
            },
        });

        if (response.ok) {
            const data = await response.json();
            const Employees = data.filter(user => user.role.role_name !== "basicuser");
            setEmployees(Employees);
            setFilteredEmployees(Employees);
        }             
        else {
            console.error("Failed to fetch employees:");
        }}
        catch (error) {
            console.error("Error fetching Employees:", error);
        }
    };
    
    useEffect(() => {
        fetchEmployees();
    }, [])

    useEffect(() => {
        console.log(employees)
        console.log(filteredEmployees)
        const filtered = employees.filter((employees) => {
            const matchesStatus = selectedStatus ? selectedStatus === "all" || employees.status === selectedStatus : true;
            const matchesRole = selectedRole ? selectedRole === "all" || employees.role.role_name === selectedRole : true;
            const matchesDepartment = selectedDepartment ? employees.role.department === selectedDepartment : true;
            return matchesStatus && matchesRole && matchesDepartment;
        });
        setFilteredEmployees(filtered);
    }, [selectedStatus, selectedRole, selectedDepartment]);
    
    const handleDelete = (id) => {
        try {
            fetch(`http://localhost:8000/api/ura/${id}/`, {
                method: "DELETE",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
            }
        })
        fetchEmployees();
        } catch (error){
            console.error("Error deleting employee:", error)
        }
    };

    return (
        <div className="admin-view-container">
             <Modal modal={modal} setModal={setModal}>
                { employee !== null &&
                <div>
                    <h2>Edit Employee</h2>
                    <input name="name" placeholder="Name" value={form.name} onChange={handleInputChange} />
                    <input name="email" placeholder="Email" value={form.email} onChange={handleInputChange} />
                    <select name="status" value={form.status} onChange={handleInputChange}>
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                        <option value="banned">Banned</option>
                    </select>
                    <select name="role_name" value={form.role_name} onChange={handleInputChange}>
                        <option value="basicuser">Basic User</option>
                        <option value="admin">Admin</option>
                        <option value="manager">Manager</option>
                        <option value="employee">Employee</option>
                    </select>
                    <select name="role_department" value={form.role_department} onChange={handleInputChange}>
                        <option value="all">All</option>
                        <option value="finance">Finance</option>
                        <option value="registrar">Registrar</option>
                    </select>
                    <button className="approve-btn" onClick={() => handleSubmit(employee.id)}>
                        Update User
                    </button>
                </div>}
            </Modal>
            <h2 className="admin-view-header">All Employees</h2>
            <div className="dropdown">
                <label htmlFor="status">Filter by Status: </label>
                <select
                    id="status"
                    value={selectedStatus}
                    onChange={(e) => setSelectedStatus(e.target.value)}
                    >
                    <option value="all">All Status</option>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="banned">Banned</option>
                </select>
            </div>

            <div className="dropdown">
                <label htmlFor="role">Filter by Role: </label>
                <select
                    id="role"
                    value={selectedRole}
                    onChange={(e) => setSelectedRole(e.target.value)}
                >
                <option value="">All Roles</option>
                {Object.keys(Roles).map((type) => (
                    <option key={type} value={type}>
                        {Roles[type]}
                    </option>
                ))}
                </select>
            </div>

            <div className="dropdown">
                <label htmlFor="form-type">Filter by Department: </label>
                <select
                    id="department"
                    value={selectedDepartment}
                    onChange={(e) => setSelectedDepartment(e.target.value)}
                >
                <option value="">All Departments</option>
                {Object.keys(Departments).map((type) => (
                    <option key={type} value={type}>
                        {Departments[type]}
                    </option>
                ))}
                </select>
            </div>
            {filteredEmployees.length === 0 ? (
                <p className="no-forms-message">No matching forms found.</p>
            ) : (
                <table className="forms-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Status</th>
                            <th>Role</th>
                            <th>Department</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredEmployees.map((employee) => (
                            <tr key={employee.id}>
                                <td>{employee.name}</td>
                                <td>{employee.email}</td>
                                <td>{employee.status}</td>
                                <td>{employee.role.role_name}</td>
                                <td>{employee.role.department}</td>
                                <td>
                                    <div>
                                        <button onClick={() => toggleModal(employee)}>Edit</button>
                                    </div>
                                    <button onClick={() => handleDelete(employee.id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                        
                    </tbody>
                   
                </table>
            )}
        </div>
    );
};

export default EmployeeManagement;