import React, { useState } from 'react';
import { approvePendingApproval, rejectPendingApproval } from '../../../api/requests/pendingApproval';

const PendingApprovalItem = ({approval}) => {
  const [showDetails, setShowDetails] = useState(false);

  const toggleDetails = () => {
    setShowDetails(!showDetails);
  };

  const onAccept = async () => {
    await approvePendingApproval(approval.id)
    .then(_ => {
      window.alert("Wniosek został zaakceptowany.");
    })
    .catch(_ => {
      window.alert("Nie udało się zaakceptować wniosku.");
    })
  };

  const onDeny = async () => {
    await rejectPendingApproval(approval.id)
    .then(_ => {
      window.alert("Wniosek został odrzucony.");
    })
    .catch(_ => {
      window.alert("Nie udało się odrzucić wniosku.");
    })
  };

  return (
    <tr valign="top">
      <td>
        <p>{approval.user.first_name} {approval.user.last_name}</p>
        {showDetails && (
          <table cellSpacing="8">
          <tbody>
            <tr>
              <td>email</td>
              <td>{approval.user.email}</td>
            </tr>
            <tr>
              <td>typ</td>
              <td>{approval.user.user_type}</td>
            </tr>
          </tbody>
        </table>
        )}
      </td>
      <td>
        <p>{approval.school.name}, {approval.school.postcode} {approval.school.city}</p>
        {showDetails && (
          <table cellSpacing="8">
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
          </table>
        )}
      </td>
      <td>
        <button onClick={toggleDetails}>
          {showDetails ? 'Zwiń' : 'Rozwiń'}
        </button>
      </td>
      <td>
        <button onClick={onAccept}>
          Zaakceptuj
        </button>
      </td>
      <td>
        <button onClick={onDeny}>
          Odrzuć
        </button>
      </td>
    </tr>
  );
  
}

export default PendingApprovalItem;
