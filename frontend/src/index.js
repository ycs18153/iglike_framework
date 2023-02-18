import "./index.css"

import App from "./App"
import React from "react"
import ReactDOM from "react-dom"
import reportWebVitals from "./reportWebVitals"

import { LiffProvider } from 'react-liff';
// import { BrowserRouter } from "react-router-dom";
// import { Route, Routes } from "react-router-dom";

// Importing the Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';

const liffId = "1657883296-DR8N1ejq";

ReactDOM.render(
    <React.StrictMode>
        <LiffProvider liffId={liffId}>
            <App />
        </LiffProvider>
    </React.StrictMode>,
    document.getElementById("root")
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
