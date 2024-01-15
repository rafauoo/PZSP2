import {apiRequest} from "./base";
import {pendingApprovalsUrl} from "../urls";

export const getPendingApprovalList = async () => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(pendingApprovalsUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching pending approvals:', error.message);
    throw error;
  }
};

export const createPendingApproval = async (pendingApprovalData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(pendingApprovalsUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(pendingApprovalData),
    });
  } catch (error) {
    console.error('Error creating pending approval:', error.message);
    throw error;
  }
};

export const getPendingApprovalByID = async (pendingApprovalID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${pendingApprovalsUrl}${pendingApprovalID}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,

      },
    });
  } catch (error) {
    console.error('Error fetching pending approval by ID:', error.message);
    throw error;
  }
};

export const approvePendingApproval = async (pendingApprovalID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${pendingApprovalsUrl}${pendingApprovalID}/approve/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error approving pending approval:', error.message);
    throw error;
  }
};

export const rejectPendingApproval = async (pendingApprovalID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${pendingApprovalsUrl}${pendingApprovalID}/reject/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error rejecting pending approval:', error.message);
    throw error;
  }
};
