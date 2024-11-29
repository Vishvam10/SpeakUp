import React, { useState } from "react";

function SettingsPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const userId = localStorage.getItem("user_id");

  const handleUserUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/user/${userId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, oldPassword, newPassword }),
        }
      );
      if (response.ok) {
        alert("User details updated successfully");
      } else {
        alert("Error updating details");
      }
    } catch (error) {
      alert("An error occurred");
    }
  };

  return (
    <div style={{ display: "flex" }}>
      <div
        style={{
          width: "200px",
          height: "100vh",
          borderRight: "1px solid #ddd",
          padding: "20px",
        }}
      >
        <h3>Settings</h3>
        <ul>
          <li>
            <a href="/dashboard">Dashboard</a>
          </li>
          {/* Add more links as needed */}
        </ul>
      </div>
      <div style={{ flex: 1, padding: "20px" }}>
        <h2>Update your details</h2>
        <form onSubmit={handleUserUpdate}>
          <div>
            <label>Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Old Password</label>
            <input
              type="password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <label>New Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Update Details</button>
        </form>
        <div>
          <h3>Other Form</h3>
          {/* Empty form for now */}
          <form>{/* Placeholder for future form fields */}</form>
        </div>
      </div>
    </div>
  );
}

export default SettingsPage;
