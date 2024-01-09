import ParticipantsList from "./ParticipantsList";
import React, {useState} from "react";
import formatDate from "../utils/format";
import AddParticipantModal from "./AddParticipantModal";

const buttonsContainerStyle = {
  display: 'flex',
  justifyContent: 'flex-end',
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

function ApplicationRow({
                          application,
                          competitionName,
                          expanded,
                          participantsData,
                          onToggleExpand,
                          onDeleteApplication,
                          onDeleteParticipantInTable,
                          onAddParticipant
                        }) {
  const [showAddParticipantModal, setShowAddParticipantModal] = useState(false);

  const handleShowAddParticipantModal = () => {
    setShowAddParticipantModal(true);
  };

  const handleCloseAddParticipantModal = () => {
    setShowAddParticipantModal(false);
  };

  return (
    <>
      <tr>
        <td>{competitionName}</td>
        <td>{formatDate(application.created_at)}</td>
        <td style={buttonsContainerStyle}>
          <button style={buttonStyle} onClick={() => onToggleExpand(application.id)}>
            {expanded ? 'Ukryj' : 'Wyświetl'}
          </button>
          <button style={buttonStyle} onClick={handleShowAddParticipantModal}>
            Dodaj
          </button>
          <button style={buttonStyle} onClick={() => onDeleteApplication(application.id)}>
            Usuń aplikację
          </button>
        </td>
      </tr>
      {expanded && (
        <tr>
          <td colSpan="3">
            <ParticipantsList
              participants={participantsData[application.id] || []}
              onDeleteParticipant={onDeleteParticipantInTable}
            />
          </td>
        </tr>
      )}
      <AddParticipantModal
        applicationId={application.id}
        show={showAddParticipantModal}
        handleClose={handleCloseAddParticipantModal}
        onAddParticipant={onAddParticipant}
      />
    </>
  );
}

export default ApplicationRow;