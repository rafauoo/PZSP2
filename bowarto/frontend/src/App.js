import React, {Component} from "react";
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarExample from "./Nav";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login"
import ParticipantsTable from "./pages/Paricipants";
import Konkursy from "./pages/Konkursy";
import RegisterParticipantTable from "./pages/RegisterParicipant"
import CreateCompetition from "./pages/CreateCompetition";
import UserPanel from "./pages/UserPanel/UserPanel";
import UserProfile from "./pages/UserProfile";
import AdminPanel from "./pages/AdminPanel/AdminPanel";
import PendingApprovals from "./pages/PendingApprovals";


class App extends Component {
  render() {
    return (
      <div>
        <NavbarExample/>
        <main role="main" className="container">
          <Router>
            <Routes>
              <Route exact path="/" element={<Konkursy/>}></Route>
              <Route exact path="/create_competition"
                     element={<CreateCompetition/>}></Route>
              <Route exact path="/register" element={<Register/>}></Route>
              <Route exact path="/login" element={<Login/>}></Route>
              <Route exact path="/user_panel" element={<UserPanel/>}></Route>
              <Route exact path="/admin_panel" element={<AdminPanel/>}></Route>
              <Route exact path="/register_participant"
                     element={<RegisterParticipantTable/>}></Route>
              <Route exact path="/profile" element={<UserProfile/>}></Route>
              <Route exact path="/pending_approvals"
                     element={<PendingApprovals/>}/>
            </Routes>
          </Router>
        </main>
      </div>
    );
  }
}

export default App;
