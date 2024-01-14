import PendingApprovalItem from "./PendingApprovalItem";

const PendingApprovalsTable = ({approvals}) => {
  return (
    <>
      {approvals.map((approval) => (
        <PendingApprovalItem approval={approval}/>
      ))}
    </>
  )
}

export default PendingApprovalsTable