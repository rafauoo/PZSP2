import React, { Component } from "react";
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarExample from "./Nav";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login"
import ParticipantsTable from "./pages/Paricipants";
import Konkursy from "./pages/Konkursy";
import RegisterParticipantTable from "./pages/RegisterParicipant"
import CreateCompetition from "./pages/CreateCompetition";



class App extends Component {
  render() {
    return (
      <div>
        <NavbarExample />
        <main role="main" className="container">
          <Router>
            <Routes>
              <Route exact path="/" element={<Home />}></Route>
              <Route exact path="/konkursy" element={<Konkursy />}></Route>
              <Route exact path="/createCompetition" element={<CreateCompetition />}></Route>
              <Route exact path="/register" element={<Register />}></Route>
              <Route exact path="/login" element={<Login />}></Route>
              <Route exact path="/participants" element={<ParticipantsTable />}></Route>
              <Route exact path="/registerParticipant" element={<RegisterParticipantTable />}></Route>
            </Routes>
          </Router>
        </main>
      </div>
    );
  }
}
export default App;
