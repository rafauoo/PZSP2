// ParticipantsList.js
import React from 'react';
import Table from 'react-bootstrap/Table';
import ParticipantItem from './ParticipantItem';

function ParticipantsList({
                            participants,
                            onDeleteParticipant
                          }) {
  const handleDeleteParticipant = async (participantId) => {
    console.log(participantId)
    onDeleteParticipant(participantId);
  }
  return (
    <Table bordered striped hover responsive className="participants-list mt-3">
      <thead>
      <tr>
        <th>Imię i nazwisko</th>
        <th>Email</th>
        <th>Załącznik</th>
        <th></th>
      </tr>
      </thead>
      <tbody>
      {participants.map((participant) => (
        <ParticipantItem
          participant={participant}
          onDelete={handleDeleteParticipant}
        />
      ))}
      </tbody>
    </Table>
  );
}

export default ParticipantsList;