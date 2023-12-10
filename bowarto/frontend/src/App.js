import React, { Component } from "react";
import "./App.css";

import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarExample from "./Nav";


class App extends Component {
  state = {
    fields: {}
  };

  onChange = updatedValue => {
    this.setState({
      fields: {
        ...this.state.fields,
        ...updatedValue
      }
    });
  };

  render() {
    return (
      <div className="App">
        <NavbarExample></NavbarExample>
      </div>
    );
  }
}

export default App;
