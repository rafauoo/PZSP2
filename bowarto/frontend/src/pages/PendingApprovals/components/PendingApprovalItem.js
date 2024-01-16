import React, { useState } from 'react';
import Table from "react-bootstrap/Table";
import { approvePendingApproval, rejectPendingApproval } from '../../../api/requests/pendingApproval';
import { buttonStyle, buttonStyleAttach, buttonStyleDelete, innerTable } from '../../../styles/styles';

const PendingApprovalItem = ({approval}) => {
  const [showDetails, setShowDetails] = useState(false);

  const toggleDetails = () => {
    setShowDetails(!showDetails);
  };

  const onAccept = async () => {
    await approvePendingApproval(approval.id)
    .then(_ => {
      window.alert("Wniosek został zaakceptowany.");
      window.location.reload();
    })
    .catch(_ => {
      window.alert("Nie udało się zaakceptować wniosku.");
    })
  };

  const onDeny = async () => {
    await rejectPendingApproval(approval.id)
    .then(_ => {
      window.alert("Wniosek został odrzucony.");
      window.location.reload();
    })
    .catch(_ => {
      window.alert("Nie udało się odrzucić wniosku.");
    })
  };

  return (
    <tr valign="top">
      <td>
        <p>{approval.user.email}</p>
        {showDetails && (
          <Table style={innerTable}>
          <tbody>
            <tr>
              <td>Imię</td>
              <td>{approval.user.first_name}</td>
            </tr>
            <tr>
              <td>Nazwisko</td>
              <td>{approval.user.last_name}</td>
            </tr>
            <tr>
              <td>typ</td>
              <td>{approval.user.user_type}</td>
            </tr>
          </tbody>
        </Table>
        )}
      </td>
      <td>
        <p>{approval.school.name}, {approval.school.postcode} {approval.school.city}</p>
        {showDetails && (
          <Table style={innerTable}>
            <tbody>
              <tr>
                <td>telefon</td>
                <td>{approval.school.phone_number}</td>
              </tr>
              <tr>
                <td>fax</td>
                <td>{approval.school.fax_number}</td>
              </tr>
              <tr>
                <td>email</td>
                <td>{approval.school.email}</td>
              </tr>
              <tr>
                <td>strona</td>
                <td>{approval.school.website}</td>
              </tr>
              <tr>
                <td>numer budynku</td>
                <td>{approval.school.building_number}</td>
              </tr>
              <tr>
                <td>numer mieszkania</td>
                <td>{approval.school.apartment_number}</td>
              </tr>
            </tbody>
          </Table>
        )}
      </td>
      <td>
        <button onClick={toggleDetails} style={buttonStyle}>
          {showDetails ? 'Zwiń' : 'Rozwiń'}
        </button>
      </td>
      <td>
        <button onClick={onAccept} style={buttonStyleAttach}>
          Zaakceptuj
        </button>
      </td>
      <td>
        <button onClick={onDeny} style={buttonStyleDelete}>
          Odrzuć
        </button>
      </td>
    </tr>
  );
  
}

export default PendingApprovalItem;
