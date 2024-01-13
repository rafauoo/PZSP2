import React, {useState, useEffect} from "react";
import {Link} from "react-router-dom";
import Table from "react-bootstrap/Table";
import axios from "axios";
import RegulaminModal from "./RegulaminModal";
import ErrorModal from "./ErrorModal";
import AddParticipantModal from "../components/AddParticipantModal";
import {submitForm} from "../requests/user_panel";

const Konkursy = () => {
  const [comingCompetitions, setComingCompetitions] = useState([]);
  const [ongoingCompetitions, setOngoingCompetitions] = useState([]);
  const [otherCompetitions, setOtherCompetitions] = useState([]);
  const [role, setRole] = useState(undefined);
  const [showAddParticipantModal, setShowAddParticipantModal] = useState(false);
  const [selectedCompetitionId, setSelectedCompetitionId] = useState(null);

  const handleShowAddParticipantModal = (competitionId) => {
    setSelectedCompetitionId(competitionId);
    setShowAddParticipantModal(true);
  };

  const handleCloseAddParticipantModal = () => {
    setSelectedCompetitionId(null);
    setShowAddParticipantModal(false);
  };

  const handleAddParticipant = async (competitionId, newParticipant) => {
    try {
      await submitForm(competitionId, newParticipant);
      handleCloseAddParticipantModal();
    } catch (error) {
      console.error("Error adding participant:", error);
    }
  };

  useEffect(() => {
    axios
      .get("http://20.108.53.69/api/competitions/")
      .then((response) => {
        const competitions = response.data;
        const now = new Date();

        const comingCompetitions = competitions
          .filter((competition) => new Date(competition.start_at) > now)
          .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));


        const ongoingCompetitions = competitions
          .filter((competition) => {
            return new Date(competition.end_at) > now && new Date(competition.start_at) <= now
          })
          .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));


        const otherCompetitions = competitions
          .filter((competition) => new Date(competition.end_at) <= now)
          .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));
        
        setComingCompetitions(comingCompetitions);
        setOngoingCompetitions(ongoingCompetitions);
        setOtherCompetitions(otherCompetitions);
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });

    setRole(sessionStorage.getItem("role"));
  }, []);

  const formatDate = (dateString) => {
    const options = {day: "numeric", month: "numeric", year: "numeric"};
    return new Date(dateString).toLocaleDateString("pl-PL", options);
  };

  const buttonStyle = {
    backgroundColor: "rgb(131, 203, 83)",
    borderRadius: "5px",
    color: "black",
    padding: "5px 10px",
    border: "none",
    cursor: "pointer",
    margin: "5px",
  };

  const centeredCellStyle = {
    textAlign: "center",
    verticalAlign: "middle",
  };

  return (
    <div>
      <Table striped bordered={false} hover>
        <thead>
        <tr>
          <th>
            <h1>Nadchodzące konkursy</h1>
          </th>
          <th style={centeredCellStyle}>Data rozpoczęcia konkursu</th>
          <th style={centeredCellStyle}>Data zakończenia konkursu</th>
          <th style={centeredCellStyle}></th>
        </tr>
        </thead>
        <tbody>
        {comingCompetitions.map((competition, index) => (
          <tr key={competition.id}>
            <td>
              <h4>{competition.title}</h4>
              <p>{competition.description}</p>
            </td>
            <td style={centeredCellStyle}>
              {formatDate(competition.start_at)}
            </td>
            <td style={centeredCellStyle}>
              {formatDate(competition.end_at)}
            </td>
            <td style={centeredCellStyle}>
              <RegulaminModal
                title={competition.title}
                description={competition.description}
              />
              <button
                style={buttonStyle}
                onClick={() => handleShowAddParticipantModal(competition.id)}
              >
                Dodaj
              </button>
            </td>
          </tr>
        ))}
        </tbody>
      </Table>
      <Table striped bordered={false} hover>
        <thead>
        <tr>
          <th>
            <h1>Aktualne konkursy</h1>
          </th>
          <th style={centeredCellStyle}>Data rozpoczęcia konkursu</th>
          <th style={centeredCellStyle}>Data zakończenia konkursu</th>
          <th style={centeredCellStyle}></th>
        </tr>
        </thead>
        <tbody>
        {ongoingCompetitions.map((competition, index) => (
          <tr key={competition.id}>
            <td>
              <h4>{competition.title}</h4>
              <p>{competition.description}</p>
            </td>
            <td style={centeredCellStyle}>
              {formatDate(competition.start_at)}
            </td>
            <td style={centeredCellStyle}>
              {formatDate(competition.end_at)}
            </td>
            <td style={centeredCellStyle}>
              <RegulaminModal
                title={competition.title}
                description={competition.description}
              />
              <button
                style={buttonStyle}
                onClick={() => handleShowAddParticipantModal(competition.id)}
              >
                Dodaj
              </button>
            </td>
          </tr>
        ))}
        </tbody>
      </Table>

      <Table striped bordered={false} hover>
        <thead>
        <tr>
          <th>
            <h1>Starsze konkursy</h1>
          </th>
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
            <td style={centeredCellStyle}>
              {formatDate(competition.end_at)}
            </td>
            <td style={centeredCellStyle}>
              <button style={buttonStyle}>Wyniki</button>
            </td>
          </tr>
        ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Konkursy;
