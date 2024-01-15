import axios from 'axios';
import { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';

function ParticipantsTable() {
  const [participants, setParticipants] = useState([]);

  useEffect(() => {
    axios.get(`http://20.108.53.69/api/participants`)
      .then(res => {
        const participantsData = res.data;
        setParticipants(participantsData);
        console.log(participantsData)
      })
  }, []);

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Imię</th>
          <th>Nazwisko</th>
          <th>E-mail</th>
        </tr>
      </thead>
      <tbody>
        {
          participants.map(participant =>
            <tr key={participant.id}>
              <td hidden >{participant.id}</td>
              <td >{participant.first_name}</td>
              <td >{participant.last_name}</td>
              <td >{participant.email}</td>
              <td>
                <a href='#'>Pokaż konkursy</a>
              </td>
            </tr>
          )
        }
      </tbody>
    </Table>
  );
}

export default ParticipantsTable;
