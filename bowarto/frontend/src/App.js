import React, { Component } from "react";
import "./App.css";

import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarExample from "./Nav";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Konkursy from "./pages/Konkursy";
import Home from "./pages/Home";
import Register from "./pages/Register";


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
              <Route exact path="/register" element={<Register />}></Route>
            </Routes>
          </Router>
        </main>
      </div>
    );
  }
}

export default App;
