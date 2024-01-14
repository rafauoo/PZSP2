const PendingApprovalItem = ({approval}) => {
  return (
    <tr>
      <td><p>{approval.user.first_name} {approval.user.last_name}</p></td>
      <td><p>{approval.school.name}</p></td>
      <td></td>
    </tr>
  )
}

export default PendingApprovalItem;
