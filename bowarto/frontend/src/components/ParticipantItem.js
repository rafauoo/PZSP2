// ParticipantItem.js
import React, {useState} from 'react';
import EditParticipantModal from './EditParticipantModal';
import AttachmentModal from './AttachmentModal';
import AttachmentDisplay from "./AttachmentDisplay";
import {buttonStyleDelete, buttonStyleEdit, buttonStyleAttach, iconButtonStyle} from "../styles/styles.js";

const tableRowStyle = {
  borderBottom: '1px solid #ddd',
  padding: '8px',
};

const buttonContainerStyle = {
  display: 'flex',
  justifyContent: 'flex-end',
  gap: '10px',
};

function ParticipantItem({
                           participant,
                           onDelete,
                           onEditParticipant,
                           onAddAttachment,
                           onDownloadFile,
                           onRemoveFile
                         }) {
  const [showAttachmentForm, setShowAttachmentForm] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [newAttachment, setNewAttachment] = useState(null);

  const handleDelete = async (participantId) => {
    onDelete(participantId);
  };

  const handleShowEditModal = () => {
    setShowEditModal(true);
  };

  const handleAttachmentChange = (e) => {
    const file = e.target.files[0];
    setNewAttachment(file);
  };

  const handleAddAttachment = () => {
    setNewAttachment(null);
    setShowAttachmentForm(false);
  };

  const handleShowAttachmentForm = () => {
    setShowAttachmentForm(true);
  };

  return (
    <>
      <tr className="participant-item" style={tableRowStyle}>
        <td>{participant.first_name} {participant.last_name}</td>
        <td>{participant.email}</td>
        <td style={buttonContainerStyle}>
          {participant.attachment && (
            <AttachmentDisplay attachment={participant.attachment.id}
                               participant={participant.id}
                               onDownload={onDownloadFile}
                               onRemove={onRemoveFile}/>
          )}
        </td>
        <td>
          <div style={buttonContainerStyle}>
            {!participant.attachment ? (
              <button style={buttonStyleAttach} onClick={handleShowAttachmentForm}>
                <img src={require('../images/attach.png')} alt="Załącz" style={iconButtonStyle} />
                Załącz pracę
              </button>
            ) : null}
            <button style={buttonStyleEdit} onClick={handleShowEditModal}>
              <img src={require('../images/edit.png')} alt="Edytuj" style={iconButtonStyle} />
              Edytuj
            </button>
            <button style={buttonStyleDelete}
                    onClick={() => handleDelete(participant.id)}>
              <img src={require('../images/delete.png')} alt="Usuń" style={iconButtonStyle}/>
              Usuń
            </button>
          </div>
        </td>
      </tr>

      <AttachmentModal
        show={showAttachmentForm}
        handleClose={() => setShowAttachmentForm(false)}
        onAddAttachment={onAddAttachment}
        participantId={participant.id}
      />

      <EditParticipantModal
        show={showEditModal}
        handleClose={() => setShowEditModal(false)}
        onEditParticipant={onEditParticipant}
        editedParticipant={participant}
      />
    </>
  );
}

export default ParticipantItem;