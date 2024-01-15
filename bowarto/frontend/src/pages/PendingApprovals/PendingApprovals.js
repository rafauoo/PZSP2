import React, {useEffect, useState} from "react";
import {getPendingApprovalList} from "../../api/requests/pendingApproval";
import refreshAccessToken from "../../requests/refresh";
import {getUserByID} from "../../api/requests/user";
import MessageModal from "../../components/MessageModal";
import {getSchoolByID} from "../../api/requests/school";
import PendingApprovalsTable from "./components/PendingApprovalsTable";

const LOADING_MESSAGE = "Trwa ładowanie...";

const PendingApprovals = () => {
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [messageText, setMessageText] = useState('');

  const [loading, setLoading] = useState(true);
  const [pendingApprovals, setPendingApprovals] = useState([]);

  useEffect(() => {
    fetchData()
  }, []);

  const fetchData = async () => {
    try {
      await refreshAccessToken();
      const pendingApprovals = await getPendingApprovalList();

      for (const approval of pendingApprovals) {
        const school = await getSchoolByID(approval.school);
        const user = await getUserByID(approval.user);

        approval.school = school;
        approval.user = user;
      }

      setPendingApprovals(pendingApprovals);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching pending approvals:', error);
      setLoading(false);
    }
  };

  return (
    <>
      <div>
        {loading ? (
          <p>{LOADING_MESSAGE}</p>
        ) : (
          <>
            {pendingApprovals.length !== 0 ? (
              <PendingApprovalsTable approvals={pendingApprovals} />
            ) : (
              <>
                <p>Wszystkie zgłoszenia do szkół zostały rozstrzygnięte.</p>
              </>
            )}
          </>
        )}
        <MessageModal
          show={showMessageModal}
          onClose={() => {
            setShowMessageModal(false);
            setMessageText('');
          }}
          message={messageText}
        />
      </div>
    </>
  );
}

export default PendingApprovals;