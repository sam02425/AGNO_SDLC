"""
CSV-based storage for agent sessions.
"""
import os
import csv
import json
import uuid
import datetime
from typing import Dict, List, Optional, Any

class CSVAgentStorage:
    """
    Storage for agent sessions using CSV files.
    Implements a similar interface to the SqliteAgentStorage from AGNO.
    """
    def __init__(self, table_name: str, csv_dir: str = "storage/csv"):
        """
        Initialize the CSV storage.

        Args:
            table_name: Name of the table (will be used as the CSV filename)
            csv_dir: Directory to store CSV files
        """
        self.table_name = table_name
        self.csv_dir = csv_dir
        self.csv_path = os.path.join(csv_dir, f"{table_name}.csv")

        # Create directory if it doesn't exist
        os.makedirs(csv_dir, exist_ok=True)

        # Create CSV file with headers if it doesn't exist
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['session_id', 'timestamp', 'input', 'response', 'metadata'])

    def save_session(self, session_id: Optional[str] = None,
                     input_text: str = "",
                     response: str = "",
                     metadata: Dict[str, Any] = None) -> str:
        """
        Save a session to the CSV storage.

        Args:
            session_id: Optional session ID (will be generated if not provided)
            input_text: Input text for the session
            response: Response text for the session
            metadata: Additional metadata for the session

        Returns:
            The session ID
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        timestamp = datetime.datetime.now().isoformat()
        metadata_json = json.dumps(metadata or {})

        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([session_id, timestamp, input_text, response, metadata_json])

        return session_id

    def get_sessions(self, session_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get sessions from the CSV storage.

        Args:
            session_id: Optional session ID to filter by
            limit: Maximum number of sessions to return

        Returns:
            List of sessions
        """
        sessions = []

        try:
            with open(self.csv_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if session_id is None or row['session_id'] == session_id:
                        # Parse metadata from JSON string
                        try:
                            metadata = json.loads(row['metadata'])
                        except json.JSONDecodeError:
                            metadata = {}

                        sessions.append({
                            'session_id': row['session_id'],
                            'timestamp': row['timestamp'],
                            'input': row['input'],
                            'response': row['response'],
                            'metadata': metadata
                        })

                        if len(sessions) >= limit:
                            break
        except FileNotFoundError:
            # Return empty list if file doesn't exist
            pass

        return sessions

    def get_latest_session(self) -> Optional[Dict[str, Any]]:
        """Get the latest session from the CSV storage."""
        sessions = self.get_sessions(limit=1)
        return sessions[0] if sessions else None