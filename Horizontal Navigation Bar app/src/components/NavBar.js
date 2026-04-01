import React from "react";
import "./NavBar.css";

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="navbar__logo">
        <span className="navbar__brand">MyApp</span>
      </div>
      <ul className="navbar__menu">
        <li className="navbar__item">
          <a href="#home" className="navbar__link navbar__link--active">Home</a>
        </li>
        <li className="navbar__item">
          <a href="#about" className="navbar__link">About</a>
        </li>
        <li className="navbar__item">
          <a href="#services" className="navbar__link">Services</a>
        </li>
        <li className="navbar__item">
          <a href="#contact" className="navbar__link">Contact</a>
        </li>
      </ul>
      <div className="navbar__actions">
        <button className="navbar__btn">Login</button>
        <button className="navbar__btn navbar__btn--primary">Sign Up</button>
      </div>
    </nav>
  );
};

export default NavBar;
