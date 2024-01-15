// ParticipantsList.js
import React from 'react';
import Table from 'react-bootstrap/Table';
import ParticipantItem from './ParticipantItem';

function ParticipantsList({
                            participants,
                            onDeleteParticipant,
                            onEditParticipant,
                            onAddAttachment,
                            onDownloadFile,
                            onRemoveFile
                          }) {
  return (
    <Table bordered striped hover responsive className="participants-list mt-3">
      <thead>
      <tr>
        <th>Imię i nazwisko</th>
        <th>E-mail</th>
        <th>Załącznik</th>
      </tr>
      </thead>
      <tbody>
      {participants.map((participant) => (
        <ParticipantItem
          participant={participant}
          onDelete={onDeleteParticipant}
          onEditParticipant={onEditParticipant}
          onAddAttachment={onAddAttachment}
          onDownloadFile={onDownloadFile}
          onRemoveFile={onRemoveFile}
        />
      ))}
      </tbody>
    </Table>
  );
}

export default ParticipantsList;
