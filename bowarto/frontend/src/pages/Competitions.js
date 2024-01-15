import React, {useState, useEffect} from "react";
import Table from "react-bootstrap/Table";
import AddParticipantModal from "../components/AddParticipantModal";
import {submitForm} from "../requests/user_panel";
import {getCompetitionList} from "../api/requests/competition";
import {
  handleAddParticipantLogic,
  handleDownloadFileLogic
} from "./UserPanel/UserPanelHelpers";
import MessageModal from "../components/MessageModal";
import Button from "react-bootstrap/Button";

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

const formatDate = (dateString) => {
  const options = {day: "numeric", month: "numeric", year: "numeric"};
  return new Date(dateString).toLocaleDateString("pl-PL", options);
};

const CompetitionsTable = ({
                             competitions,
                             title,
                             handleDownloadFile,
                             handleShowAddParticipantModal,
                           }) => {
  const [expanded, setExpanded] = useState(false)
  return (
    <Table striped bordered={false} hover>
      <thead>
      <tr>
        <th>
          <h1>{title}</h1>
        </th>
        <th style={centeredCellStyle}>Data rozpoczęcia konkursu</th>
        <th style={centeredCellStyle}>Data zakończenia konkursu</th>
        <th style={centeredCellStyle}>
          <button style={buttonStyle}
                  onClick={() => setExpanded(!expanded)}>{expanded ? "Ukryj" : "Pokaż"}</button>
        </th>
      </tr>
      </thead>
      {expanded ? (
        <tbody>
        {competitions.map((competition, index) => (
          <tr key={competition.id}>
            <td>
              <h4>{competition.title}</h4>
              <p>{competition.description}</p>
            </td>
            <td
              style={centeredCellStyle}>{formatDate(competition.start_at)}</td>
            <td style={centeredCellStyle}>{formatDate(competition.end_at)}</td>
            <td style={centeredCellStyle}>
              {competition.regulation && (
                <Button
                  style={buttonStyle}
                  onClick={() => handleDownloadFile(competition.regulation.id)}
                >
                  Regulamin
                </Button>
              )}
              {competition.poster && (
                <Button
                  style={buttonStyle}
                  onClick={() => handleDownloadFile(competition.poster.id)}
                >
                  Plakat
                </Button>
              )}
              {title === "Aktualne konkursy" && sessionStorage.getItem('role') === 'user' ? (
                <Button
                  style={buttonStyle}
                  onClick={() => handleShowAddParticipantModal(competition.id)}
                >
                  Dodaj
                </Button>
              ) : null}
            </td>
          </tr>
        ))}
        </tbody>) : null}
    </Table>
  );
}
const Competitions = () => {
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [messageText, setMessageText] = useState('');

  const [comingCompetitions, setComingCompetitions] = useState([]);
  const [ongoingCompetitions, setOngoingCompetitions] = useState([]);
  const [otherCompetitions, setOtherCompetitions] = useState([]);
  const [showAddParticipantModal, setShowAddParticipantModal] = useState(false);
  const [selectedCompetitionId, setSelectedCompetitionId] = useState(null);

  const handleCloseAddParticipantModal = () => {
    setSelectedCompetitionId(null);
    setShowAddParticipantModal(false);
  };

  const fetchData = async () => {
    try {
      const competitions = await getCompetitionList();
      const now = new Date();

      const comingCompetitions = competitions
        .filter((competition) => new Date(competition.start_at) > now)
        .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));

      const ongoingCompetitions = competitions
        .filter(
          (competition) =>
            new Date(competition.end_at) > now &&
            new Date(competition.start_at) <= now
        )
        .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));

      const otherCompetitions = competitions
        .filter((competition) => new Date(competition.end_at) <= now)
        .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));

      setComingCompetitions(comingCompetitions);
      setOngoingCompetitions(ongoingCompetitions);
      setOtherCompetitions(otherCompetitions);

      console.log("Data fetched successfully!");
    } catch (error) {
      console.log("Error fetching data:", error);
    }
  };

  const handleDownloadFile = async (attachmentId) => {
    const {showMessageModal, messageText} = await handleDownloadFileLogic(
      attachmentId
    );

    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  const handleAddParticipant = async (competitionId, newParticipant) => {
    const {
      _, showMessageModal, messageText
    } = await handleAddParticipantLogic(competitionId, newParticipant);

    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };
  const handleShowAddParticipantModal = (competitionId) => {
    setSelectedCompetitionId(competitionId);
    setShowAddParticipantModal(true);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>

      <CompetitionsTable
        title="Aktualne konkursy"
        competitions={ongoingCompetitions}
        handleDownloadFile={handleDownloadFile}
        handleShowAddParticipantModal={handleShowAddParticipantModal}
      />

      <CompetitionsTable
        title="Nadchodzące konkursy"
        competitions={comingCompetitions}
        handleDownloadFile={handleDownloadFile}
        onActionButtonClick={(competitionId) =>
          handleShowAddParticipantModal(competitionId)
        }
      />


      <CompetitionsTable title="Starsze konkursy"
                         handleDownloadFile={handleDownloadFile}
                         competitions={otherCompetitions}/>

      <AddParticipantModal
        competitionId={selectedCompetitionId}
        show={showAddParticipantModal}
        handleClose={handleCloseAddParticipantModal}
        onAddParticipant={handleAddParticipant}
      />
      <MessageModal
        show={showMessageModal}
        onClose={() => {
          setShowMessageModal(false);
          setMessageText('');
        }}
        message={messageText}
      />
    </div>
  );
};

export default Competitions;
