// ParticipantItem.js
import React, {useState} from 'react';
import EditParticipantModal from './EditParticipantModal';
import AttachmentModal from './AttachmentModal';
import Button from 'react-bootstrap/Button';
import AttachmentDisplay from "./AttachmentDisplay";

const tableRowStyle = {
  borderBottom: '1px solid #ddd',
  padding: '8px',
};

const buttonContainerStyle = {
  display: 'flex',
  justifyContent: 'flex-end',
  gap: '10px',
};

const buttonStyle = {
  backgroundColor: 'rgb(131, 203, 83)',
  borderRadius: '5px',
  color: 'black',
  padding: '5px 10px',
  border: 'none',
  cursor: 'pointer',
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
            <button style={buttonStyle} onClick={handleShowAttachmentForm}>
              Załącz pracę
            </button>
            <button style={buttonStyle} onClick={handleShowEditModal}>
              Edytuj
            </button>
            <button style={buttonStyle}
                    onClick={() => handleDelete(participant.id)}>
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