import React from "react";
import "./Setting.css";

const Setting = () => {
  return (
    <div className="setting-page">
      <h1>Setting Page</h1>
      <div className="setting-section">
        <h2>General Settings</h2>
        <label>
          Enable Notifications:
          <input type="checkbox" defaultChecked />
        </label>
        <label>
          Dark Mode:
          <input type="checkbox" />
        </label>
      </div>
      <div className="setting-section">
        <h2>Account Settings</h2>
        <p>Email: user@example.com</p>
        <button className="setting-button">Change Password</button>
        <button className="setting-button">Delete Account</button>
      </div>
    </div>
  );
};

export default Setting;
