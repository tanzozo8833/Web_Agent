import React from "react";

const Home = () => {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Home Page</h1>

      <button style={{ backgroundColor: "black", color: "white", padding: "10px", marginRight: "10px" }}>
        Blue Button
      </button>

      <button style={{ backgroundColor: "black", color: "white", padding: "10px", marginRight: "10px" }}>
        Green Button
      </button>

      <button style={{ backgroundColor: "black", color: "white", padding: "10px" }}>
        Red Button
      </button>
    </div>
  );
};

export default Home;