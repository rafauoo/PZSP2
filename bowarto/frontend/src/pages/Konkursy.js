import React, { Component } from "react";
import Table from 'react-bootstrap/Table';
import axios from 'axios';

class Konkursy extends Component {
  constructor(props) {
    super(props);
    this.state = {
      ongoingCompetitions: [],
      otherCompetitions: []
    };
  }

  componentDidMount() {
    axios.get("http://20.108.53.69/api/competitions")
      .then((response) => {
        const competitions = response.data;
        const now = new Date();

        const ongoingCompetitions = competitions.filter(
          competition => new Date(competition.end_at) > now
        );

        const otherCompetitions = competitions.filter(
          competition => new Date(competition.end_at) <= now
        );

        this.setState({
          ongoingCompetitions,
          otherCompetitions
        });
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });
  }

  render() {
    const { ongoingCompetitions, otherCompetitions } = this.state;

    const formatDate = (dateString) => {
      const options = { day: 'numeric', month: 'numeric', year: 'numeric' };
      return new Date(dateString).toLocaleDateString('pl-PL', options);
    };

    const buttonStyle = {
      backgroundColor: 'rgb(131, 203, 83)',
      borderRadius: '5px',
      color: 'black',
      padding: '5px 10px',
      border: 'none',
      cursor: 'pointer',
      margin: '5px'
    };

    const centeredCellStyle = {
      textAlign: 'center',
      verticalAlign: 'middle'
    };

    return (
      <div>
        <Table striped bordered={false} hover>
          <thead>
            <tr>
              <th><h1>Aktualne konkursy</h1></th>
              <th style={centeredCellStyle}>Data zakończenia konkursu</th>
              <th style={centeredCellStyle}></th>
            </tr>
          </thead>
          <tbody>
            {ongoingCompetitions.map((competition, index) => (
              <tr key={index}>
                <td>
                  <h4>{competition.title}</h4>
                  <p>{competition.description}</p>
                </td>
                <td style={centeredCellStyle}>{formatDate(competition.end_at)}</td>
                <td style={centeredCellStyle}>
                  <button style={buttonStyle}>Regulamin</button>
                  <button style={buttonStyle}>Weź udział</button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>

        <Table striped bordered={false} hover>
          <thead>
            <tr>
              <th><h1>Starsze konkursy</h1></th>
              <th style={centeredCellStyle}>Data zakończenia konkursu</th>
              <th style={centeredCellStyle}></th>
            </tr>
          </thead>
          <tbody>
            {otherCompetitions.map((competition, index) => (
              <tr key={index}>
                <td>
                  <h4>{competition.title}</h4>
                  <p>{competition.description}</p>
                </td>
                <td style={centeredCellStyle}>{formatDate(competition.end_at)}</td>
                <td style={centeredCellStyle}>
                  <button style={buttonStyle}>Wyniki</button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    );
  }
}

export default Konkursy;
