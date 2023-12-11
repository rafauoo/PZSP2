import React, { Component } from "react";
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarExample from "./Nav";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login"
import ParticipantsTable from "./pages/Paricipants";



class App extends Component {
  render() {
    return (
      <div>
        <NavbarExample />
        <main role="main" className="container">
          <Router>
            <Routes>
              <Route exact path="/" element={<Home />}></Route>
              <Route exact path="/register" element={<Register />}></Route>
              <Route exact path="/login" element={<Login />}></Route>
              <Route exact path="/participants" element={<ParticipantsTable />}></Route>
            </Routes>
          </Router>
        </main>
      </div>
    );
  }
}
export default App;
