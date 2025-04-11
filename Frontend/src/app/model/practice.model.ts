export interface Practice {
  _id: string;
  title: string;
  year: number;
  practice_type: string;
  file_url?: string;
  institution?: string;
  author?: string;
  municipality?: string;
}