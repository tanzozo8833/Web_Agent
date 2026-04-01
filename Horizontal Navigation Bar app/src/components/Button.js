import React from "react";
import "./Button.css";

const Button = ({ label, variant = "primary", onClick }) => {
  const buttonClass = `btn btn--${variant}`;

  return (
    <button className={buttonClass} onClick={onClick}>
      {label}
    </button>
  );
};

export default Button;
