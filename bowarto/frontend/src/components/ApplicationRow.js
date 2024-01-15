import ParticipantsList from "./ParticipantsList";
import React, { useState } from "react";
import formatDate from "../utils/format";
import AddParticipantModal from "./AddParticipantModal";
import {
  deleteParticipantAndCheckApplication,
  submitForm
} from "../requests/user_panel";
import { buttonContainerStyle, buttonContainerStyleParticipants, buttonStyleBasic, buttonStyleDelete, buttonStyleEdit, buttonStyledShow, buttonStyledShow1, iconButtonStyle } from "../styles/styles";


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
        <td>
          <h2>{application.competition.title}</h2>
        </td>
        <td style={buttonContainerStyleParticipants}>
          <button style={buttonStyledShow1}
            onClick={() => onToggleExpand(application.id)}>
            <img src={require('../images/view-white.png')} alt="Widok" style={iconButtonStyle} />
            {expanded ? 'Ukryj' : 'Wyświetl'}
          </button>
          <button style={buttonStyleEdit}
            onClick={() => handleShowAddParticipantModal(application.competition.id)}>
            <img src={require('../images/add.png')} alt="Dodaj" style={iconButtonStyle} />
            Dodaj
          </button>
          <button style={buttonStyleDelete}
            onClick={() => onDeleteApplication(application.id)}>
            <img src={require('../images/delete.png')} alt="Usuń" style={iconButtonStyle} />
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
