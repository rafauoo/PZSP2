import React from "react";
import PendingApprovalItem from "./PendingApprovalItem";

const PendingApprovalsTable = ({ approvals }) => {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
      <thead>
        <tr>
          <th>Użytkownik</th>
          <th>Szkoła</th>
        </tr>
      </thead>
      <tbody>
        {approvals.map((approval) => (
          <PendingApprovalItem key={approval.id} approval={approval} />
        ))}
      </tbody>
    </table>
  );
};

export default PendingApprovalsTable