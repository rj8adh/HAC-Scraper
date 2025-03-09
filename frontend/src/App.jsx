import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [baseURL, setBaseURL] = useState("");
  const [data, setData] = useState(null);

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/login", {
        username,
        password,
        baseURL,
      });
      alert(response.data.message);
    } catch (error) {
      alert("Login failed: " + error.response?.data?.detail);
    }
  };

  const fetchData = async (endpoint) => {
    try {
      const response = await axios.get(`http://localhost:8000/${endpoint}`, {
        params: { username },
      });
      setData(response.data);
    } catch (error) {
      alert(`Error fetching ${endpoint}: ` + error.response?.data?.detail);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Grade Management System</h2>
      <div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="text"
          placeholder="Base URL"
          value={baseURL}
          onChange={(e) => setBaseURL(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
      </div>
      <div>
        <button onClick={() => fetchData("grades")}>Get Grades</button>
        <button onClick={() => fetchData("transcript")}>Get Transcript</button>
        <button onClick={() => fetchData("assignments")}>Get Assignments</button>
        <button onClick={() => fetchData("official_gpa")}>Get Official GPA</button>
      </div>
      {data && (
        <div>
          <h3>Response Data:</h3>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default App;