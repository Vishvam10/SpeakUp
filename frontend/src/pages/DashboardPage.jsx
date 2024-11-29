import React from "react";
import { Link } from "react-router-dom";

function DashboardPage() {
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
        <h3>Dashboard</h3>
        <ul>
          <li>
            <Link to="/settings">Settings</Link>
          </li>
          {/* Add more links as needed */}
        </ul>
      </div>
      <div style={{ flex: 1, padding: "20px" }}>
        {/* This area will be filled with your content later */}
        <h2>Welcome to your Dashboard!</h2>
      </div>
    </div>
  );
}

export default DashboardPage;
