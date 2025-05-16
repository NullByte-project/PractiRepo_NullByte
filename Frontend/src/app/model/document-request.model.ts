export interface DocumentRequest {
  _id: string;
  practice_id: string;
  practice_title: string;
  requester_name: string;
  requester_email: string;
  request_date: Date;
  status: 'pending' | 'approved' | 'rejected';
  response_date?: Date;
  admin_notes?: string;
  response_by_id?: string;
}

export enum DocumentRequestStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected'
}