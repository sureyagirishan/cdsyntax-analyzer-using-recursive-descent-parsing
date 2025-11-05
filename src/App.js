import React, { useState } from "react";
import { isParsed } from "./Parser";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");

  const handleChange = (e) => {
    const value = e.target.value;
    setInput(value);
    if (value === "") {
      setResult("");
    } else {
      setResult(isParsed(value) ? "String is PARSED ✅" : "Not Parsed ❌");
    }
  };

  return (
    <div className="container">
      <h1>Recursive Descent Parser</h1>
      <input
        type="text"
        placeholder="Type your string"
        value={input}
        onChange={handleChange}
        className="textbox"
      />
      <div className="result">{result}</div>
    </div>
  );
}

export default App;
