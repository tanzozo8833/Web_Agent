import React from "react";
import "./Sidebar.css";
import { FaHome, FaInbox, FaUser, FaCalendar, FaSearch, FaChartBar, FaFile, FaCog } from "react-icons/fa";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h2 className="logo">Designer</h2>

      <ul>
        <li className="active"><FaHome /> Dashboard</li>
        <li><FaInbox /> Inbox</li>
        <li><FaUser /> Accounts</li>
        <li><FaCalendar /> Schedule</li>
        <li><FaSearch /> Search</li>
        <li><FaChartBar /> Analytics</li>
        <li><FaFile /> Files</li>
        <li><FaCog /> Setting</li>
      </ul>
    </div>
  );
};

export default Sidebar;