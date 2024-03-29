import React, {useState, useEffect} from "react";
import Table from "react-bootstrap/Table";
import AddParticipantModal from "../components/AddParticipantModal";
import {submitForm} from "../requests/user_panel";
import {
  deleteCompetitionByID,
  getCompetitionList
} from "../api/requests/competition";
import {
  handleAddParticipantLogic,
  handleDownloadFileLogic
} from "./UserPanel/UserPanelHelpers";
import MessageModal from "../components/MessageModal";
import Button from "react-bootstrap/Button";
import EditCompetitionModal from "./AdminPanel/components/EditCompetitionModal";
import {
  buttonStyle,
  buttonStyle1,
  buttonStyle2,
  buttonStyleEdit,
  buttonStyled,
  buttonStyledShow,
  centeredCellStyle,
  headerShowStyle,
  iconButtonStyle,
  iconButtonStyleAdd,
  titled,
  buttonStyleDelete
} from "../styles/styles";
import refreshAccessToken from "../requests/refresh";
import {apiRequest} from "../api/requests/base";
import {competitionsUrl} from "../api/urls";

const formatDate = (dateString) => {
  const options = {day: "numeric", month: "numeric", year: "numeric"};
  return new Date(dateString).toLocaleDateString("pl-PL", options);
};

const CompetitionDataRow = ({
                              competition,
                              title,
                              handleDownloadFile,
                              handleShowAddParticipantModal
                            }) => {
  const handleModalClose = async () => {
    try {
      await refreshAccessToken();
      const accessToken = sessionStorage.getItem('access');
      await fetch(`${competitionsUrl}${competition.id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
      });
      window.location.reload();
    } catch (error) {
      console.error('Error editing competition:', error.message);
      window.location.reload();
      throw error;
    }

  };

  return (
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
            style={buttonStyle2}
            onClick={() => handleDownloadFile(competition.regulation.id)}
          >
            <img src={require('../images/download.png')} alt="Pobierz regulamin"
                 style={iconButtonStyle}/>
            Regulamin
          </Button>
        )}
      </td>
      <td style={centeredCellStyle}>
        {competition.poster && (
          <Button
            style={buttonStyle2}
            onClick={() => handleDownloadFile(competition.poster.id)}
          >
            <img src={require('../images/download.png')} alt="Pobierz plakat"
                 style={iconButtonStyle}/>
            Plakat
          </Button>
        )}
      </td>
      <td style={centeredCellStyle}>
        {title === "Aktualne konkursy" && sessionStorage.getItem('role') === 'user' ? (
          <Button
            style={buttonStyle1}
            onClick={() => handleShowAddParticipantModal(competition.id)}
          >
            <img src={require('../images/add.png')} alt="Dodaj"
                 style={iconButtonStyleAdd}/>
          </Button>
        ) : null}
        {sessionStorage.getItem('role') === 'admin' ? (
          <td style={centeredCellStyle}>
            <button
              style={buttonStyleDelete}
              onClick={handleModalClose}
            >
              Usuń
            </button>
          </td>
        ) : null}
      </td>
    </tr>
  )
}

const CompetitionsTable = ({
                             competitions,
                             title,
                             handleDownloadFile,
                             handleShowAddParticipantModal,
                           }) => {
  const [expanded, setExpanded] = useState(false)
  console.log(sessionStorage.getItem('role'))
  return (
    <Table striped bordered={false} hover>
      <thead>
      <tr>
        <th>
          <h1 style={titled}>{title}</h1>
        </th>
        <th
          style={centeredCellStyle}>{expanded ? "Data rozpoczęcia konkursu" : ""}</th>
        <th
          style={centeredCellStyle}>{expanded ? "Data zakończenia konkursu" : ""}</th>
        <th colSpan="3" style={headerShowStyle}>
          <button style={buttonStyledShow}
                  onClick={() => setExpanded(!expanded)}>{expanded ? "Ukryj" : "Pokaż"}</button>
        </th>
      </tr>
      </thead>
      {expanded ? (
        <tbody>
        {competitions.map((competition, index) => (
          <CompetitionDataRow title={title} competition={competition}
                              handleShowAddParticipantModal={handleShowAddParticipantModal}
                              handleDownloadFile={handleDownloadFile}/>
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
      <br></br>
      <CompetitionsTable
        title="Aktualne konkursy"
        competitions={ongoingCompetitions}
        handleDownloadFile={handleDownloadFile}
        handleShowAddParticipantModal={handleShowAddParticipantModal}
      />
      <br></br>
      <CompetitionsTable
        title="Nadchodzące konkursy"
        competitions={comingCompetitions}
        handleDownloadFile={handleDownloadFile}
        onActionButtonClick={(competitionId) =>
          handleShowAddParticipantModal(competitionId)
        }
      />

      <br></br>
      <CompetitionsTable title="Zakończone konkursy"
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
