import React, { Component } from "react";
import axios from "axios";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      competitionList: []
    };
  }

  refreshList = () => {
    axios.get("http://127.0.0.1:8000/api/competitions")
      .then((response) => {
        this.setState({ competitionList: response.data });
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });
  };

  render() {
    this.refreshList();
    return (
      <div>
        <h1>Competition Items</h1>
        <ul>
          {this.state.competitionList.map((item) => (
            <li key={item.id}>
              <h2>{item.title}</h2>
              <p>Description: {item.description}</p>
              <p>Created At: {item.created_at}</p>
              <p>End At: {item.end_at}</p>
              <p>Type: {item.type}</p>
            </li>
          ))}
        </ul>
      </div>
    );
  }
}
export default App;
