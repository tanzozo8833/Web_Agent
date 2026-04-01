import React, { useState, useRef, useEffect } from "react";
import "./Dropdown.css";

const Dropdown = ({ options, placeholder, onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(null);
  const dropdownRef = useRef(null);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleSelect = (option) => {
    setSelected(option);
    setIsOpen(false);
    if (onSelect) {
      onSelect(option.value);
    }
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="dropdown" ref={dropdownRef}>
      <button 
        className={`dropdown__trigger ${isOpen ? "dropdown__trigger--open" : ""}`}
        onClick={handleToggle}
      >
        <span className="dropdown__selected">
          {selected ? selected.label : placeholder}
        </span>
        <span className="dropdown__arrow">▼</span>
      </button>
      
      {isOpen && (
        <ul className="dropdown__menu">
          {options.map((option) => (
            <li 
              key={option.value}
              className={`dropdown__item ${selected?.value === option.value ? "dropdown__item--selected" : ""}`}
              onClick={() => handleSelect(option)}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Dropdown;
