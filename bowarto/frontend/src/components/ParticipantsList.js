// ParticipantsList.js
import React from 'react';
import Table from 'react-bootstrap/Table';
import ParticipantItem from './ParticipantItem';

function ParticipantsList({
                            participants,
                            onDeleteParticipant,
                            onEditParticipant
                          }) {
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
          onDelete={onDeleteParticipant}
          onEditParticipant={onEditParticipant}
        />
      ))}
      </tbody>
    </Table>
  );
}

export default ParticipantsList;
