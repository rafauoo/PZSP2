import React from "react";
import ParticipantItem from "../../../components/ParticipantItem";
import Table from "react-bootstrap/Table";

const participantsTable = ({participants}) => {
  return (
    <Table>
      <thead>
      <tr>
        <th>Imię i nazwisko</th>
        <th>E-mail</th>
        <th>Załącznik</th>
        <th></th>
      </tr>
      </thead>
      {participants.map((participant) => (
        <ParticipantItem
          participant={participant}/>
      ))}
    </Table>
  )
}

export default participantsTable;