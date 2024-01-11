import ParticipantsList from "./ParticipantsList";
import React, {useState} from "react";
import formatDate from "../utils/format";
import AddParticipantModal from "./AddParticipantModal";
import {deleteParticipantAndCheckApplication, submitForm} from "../requests/user_panel";

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
                          expanded,
                          onToggleExpand,
                          onDeleteApplication,
                          onDeleteParticipant,
                          onAddParticipant,
                          onEditParticipant,
                          onAddAttachment,
                          onDownloadFile,
                          onRemoveFile
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
        <td>{application.competition.title}</td>
        <td>{formatDate(application.created_at)}</td>
        <td style={buttonsContainerStyle}>
          <button style={buttonStyle} onClick={() => onToggleExpand(application.id)}>
            {expanded ? 'Ukryj' : 'Wyświetl'}
          </button>
          <button style={buttonStyle} onClick={() => handleShowAddParticipantModal(application.competition.id)}>
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
              participants={application.participants || []}
              onDeleteParticipant={onDeleteParticipant}
              onEditParticipant={onEditParticipant}
              onAddAttachment={onAddAttachment}
              onDownloadFile={onDownloadFile}
              onRemoveFile={onRemoveFile}
            />
          </td>
        </tr>
      )}
      <AddParticipantModal
        competitionId={application.competition.id}
        show={showAddParticipantModal}
        handleClose={handleCloseAddParticipantModal}
        onAddParticipant={onAddParticipant}
      />

    </>
  );
}

export default ApplicationRow;
