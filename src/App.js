import React from "react";
import Sidebar from "./components/Sidebar";
import Home from "./components/Home";

function App() {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Home />
      </div>
    </div>
  );
}

export default App;