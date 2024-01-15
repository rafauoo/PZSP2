import React from "react";
import Table from "react-bootstrap/Table";
import PendingApprovalItem from "./PendingApprovalItem";

const PendingApprovalsTable = ({ approvals }) => {
  return (
    <Table striped bordered={false} hover>
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
    </Table>
  );
};

export default PendingApprovalsTable