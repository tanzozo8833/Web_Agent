import React from "react";
import Button from "./Button";
import Dropdown from "./Dropdown";
import "./Home.css";

const Home = () => {
  const dropdownOptions = [
    { value: "option1", label: "Option 1" },
    { value: "option2", label: "Option 2" },
    { value: "option3", label: "Option 3" },
  ];

  return (
    <div className="home">
      <header className="home__header">
        <h1 className="home__title">Welcome to MyApp</h1>
        <p className="home__subtitle">
          A modern web application with horizontal navigation
        </p>
      </header>

      <main className="home__content">
        <section className="home__section">
          <h2 className="home__section-title">Components Demo</h2>
          <p className="home__text">
            This page demonstrates the key components available in this application:
          </p>
          
          <div className="home__demo">
            <div className="home__demo-item">
              <h3 className="home__demo-title">Buttons</h3>
              <div className="home__buttons">
                <Button label="Primary" variant="primary" />
                <Button label="Secondary" variant="secondary" />
                <Button label="Success" variant="success" />
                <Button label="Danger" variant="danger" />
              </div>
            </div>

            <div className="home__demo-item">
              <h3 className="home__demo-title">Dropdown</h3>
              <Dropdown 
                options={dropdownOptions} 
                placeholder="Select an option" 
                onSelect={(value) => console.log("Selected:", value)}
              />
            </div>
          </div>
        </section>

        <section className="home__section">
          <h2 className="home__section-title">Features</h2>
          <ul className="home__features">
            <li className="home__feature-item">
              <span className="home__feature-icon">✓</span>
              Responsive horizontal navigation bar
            </li>
            <li className="home__feature-item">
              <span className="home__feature-icon">✓</span>
              Customizable button components with multiple variants
            </li>
            <li className="home__feature-item">
              <span className="home__feature-icon">✓</span>
              Interactive dropdown menus
            </li>
            <li className="home__feature-item">
              <span className="home__feature-icon">✓</span>
              Clean and modern design
            </li>
          </ul>
        </section>
      </main>

      <footer className="home__footer">
        <p className="home__footer-text">© 2026 MyApp. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;
