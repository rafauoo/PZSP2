// ParticipantItem.js
import React, {useState} from 'react';
import EditParticipantModal from '../../../components/EditParticipantModal';
import AttachmentModal from '../../../components/AttachmentModal';
import AttachmentDisplay from "../../../components/AttachmentDisplay";
import {tableRowStyle, buttonStyleDelete, buttonStyleEdit, buttonStyleAttach, iconButtonStyle, buttonContainerStyle, buttonContainerStyle1, iconButtonStyleDelete, buttonStyle2, buttonStyle} from "../../../styles/styles.js";

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
        <td style={buttonContainerStyle1}>
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
              <button style={buttonStyle} onClick={handleShowAttachmentForm}>
                <img src={require('../../../images/attach.png')} alt="Załącz" style={iconButtonStyle} />
                Załącz pracę
              </button>
            ) : null}
            <button style={buttonStyle} onClick={handleShowEditModal}>
              <img src={require('../../../images/edit.png')} alt="Edytuj" style={iconButtonStyle} />
              Edytuj
            </button>
            <button style={buttonStyleDelete}
                    onClick={() => handleDelete(participant.id)}>
              <img src={require('../../../images/delete.png')} alt="Usuń" style={iconButtonStyleDelete}/>
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