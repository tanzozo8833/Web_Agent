import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";
import { FaHome, FaInbox, FaUser, FaCalendar, FaSearch, FaChartBar, FaFile, FaCog } from "react-icons/fa";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h2 className="logo">Designer</h2>

      <ul>
        <li>
          <NavLink to="/" className={({ isActive }) => (isActive ? "active" : "")}>
            <FaHome /> Dashboard
          </NavLink>
        </li>
        <li><FaInbox /> Inbox</li>
        <li><FaUser /> Accounts</li>
        <li><FaCalendar /> Schedule</li>
        <li><FaSearch /> Search</li>
        <li><FaChartBar /> Analytics</li>
        <li><FaFile /> Files</li>
        <li>
          <NavLink to="/setting" className={({ isActive }) => (isActive ? "active" : "")}>
            <FaCog /> Setting
          </NavLink>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;