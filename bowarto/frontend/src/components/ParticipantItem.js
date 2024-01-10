// ParticipantItem.js
import React, {useState} from 'react';
import EditParticipantModal from './EditParticipantModal';
import AttachmentModal from './AttachmentModal';
import Button from 'react-bootstrap/Button';

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
                         }) {
  const [attachment, setAttachment] = useState(null);
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

  const handleAttachmentUpload = () => {
    console.log('File upload logic goes here:', newAttachment);
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
        <td></td>
        <td style={buttonContainerStyle}>
          {attachment && (
            <div>
              Current Attachment: {attachment.name}
            </div>
          )}
        </td>
        <td style={buttonContainerStyle}>
          <button style={buttonStyle} onClick={handleShowAttachmentForm}>
            Załącz pracę
          </button>
          <button style={buttonStyle} onClick={handleShowEditModal}>
            Edytuj
          </button>
          <button style={buttonStyle} onClick={() => handleDelete(participant.id)}>
            Usuń
          </button>
        </td>
      </tr>

      <AttachmentModal
        show={showAttachmentForm}
        handleClose={() => setShowAttachmentForm(false)}
        handleAttachmentUpload={(newAttachment) => {
          console.log('File upload logic goes here:', newAttachment);
          setAttachment(newAttachment);
        }}
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
