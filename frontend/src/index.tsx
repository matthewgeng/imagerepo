import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import axios from "axios";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

// setting axios baseurl depending on environment variable
if (process.env.REACT_APP_PROD === "true") {
  if (window.location.hostname === process.env.REACT_APP_HOST_NAME) {
    axios.defaults.baseURL = `https://${process.env.REACT_APP_HOST_NAME}:${process.env.REACT_APP_PROXY}`;
  } else {
    axios.defaults.baseURL = `https://${process.env.REACT_APP_HOST_IP}:${process.env.REACT_APP_PROXY}`;
  }
} else if (process.env.REACT_APP_PROXY != null) {
  axios.defaults.baseURL = `https://localhost:${process.env.REACT_APP_PROXY}`;
} else {
  axios.defaults.baseURL = `http://localhost:8000`;
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
