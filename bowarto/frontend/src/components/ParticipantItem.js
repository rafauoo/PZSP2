// ParticipantItem.js
import React, {useState} from 'react';
import AttachmentModal from './AttachmentModal';


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
                           applicationID,
                           onDelete
                         }) {
  const [attachment, setAttachment] = useState(null);
  const [showAttachmentForm, setShowAttachmentForm] = useState(false);
  const [newAttachment, setNewAttachment] = useState(null);

  const handleDelete = async (participantId) => {
    onDelete(participantId);
  };

  const handleAttachmentChange = (e) => {
    // Handle file attachment change
    const file = e.target.files[0];
    setNewAttachment(file);
  };

  const handleAttachmentUpload = () => {
    // Implement file upload logic here
    console.log('File upload logic goes here:', newAttachment);
    // Reset new attachment and hide the form after upload
    setNewAttachment(null);
    setShowAttachmentForm(false);
  };

  const handleShowAttachmentForm = () => {
    // Show the attachment form
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
          <button style={buttonStyle} onClick={handleShowAttachmentForm}>Załącz pracę</button>
          <button style={buttonStyle}>Edytuj</button>
          <button style={buttonStyle} onClick={() => handleDelete(participant.id)}>Usuń</button>
        </td>
      </tr>
      <AttachmentModal
        show={showAttachmentForm}
        handleClose={() => setShowAttachmentForm(false)}
        handleAttachmentUpload={(newAttachment) => {
          // Handle attachment upload logic here
          console.log('File upload logic goes here:', newAttachment);
          // Update the state with the new attachment
          setAttachment(newAttachment);
        }}
      />
    </>
  );
}

export default ParticipantItem;
