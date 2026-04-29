"""
ITIL (IT Infrastructure Library) Implementation Module
Implements Industry best practices for IT Service Management
Demonstrates: OOP, Advanced Python, Design Patterns
"""

from datetime import datetime, timedelta
from utils import log_event, print_success_message, print_error_message
from custom_exceptions import (
    DataValidationError, InvalidTicketError, UnauthorizedActionError
)
import json
import os


class IncidentManagement:
    """
    ITIL Incident Management Process
    Handles unplanned interruptions and restoration of service
    
    Demonstrates:
    - Encapsulation
    - Business logic implementation
    - State management
    """
    
    # Severity levels
    SEVERITY_LEVELS = {
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Critical': 4
    }
    
    # Incident priorities mapped to ITIL severity
    PRIORITY_TO_SEVERITY = {
        'P1': 'Critical',
        'P2': 'High',
        'P3': 'Medium',
        'P4': 'Low'
    }
    
    def __init__(self):
        """Initialize incident management"""
        self.incidents = {}
        self.incident_counter = 0
        log_event("INFO", "Incident Management initialized")
    
    def create_incident(self, ticket_id, employee_name, issue_description, 
                       priority='P4', impact_level='Low'):
        """
        Create a new incident from ticket
        
        Args:
            ticket_id (str): Associated ticket ID
            employee_name (str): Employee name
            issue_description (str): Description of incident
            priority (str): Priority level (P1-P4)
            impact_level (str): Impact level (Low, Medium, High, Critical)
        
        Returns:
            dict: Created incident record
        """
        try:
            if not ticket_id or not employee_name:
                raise DataValidationError('ticket_id/employee_name', 'non-empty', 'empty value')
            
            self.incident_counter += 1
            incident_id = f"INC{self.incident_counter:05d}"
            
            incident = {
                'incident_id': incident_id,
                'ticket_id': ticket_id,
                'employee_name': employee_name,
                'issue_description': issue_description,
                'priority': priority,
                'severity': self.PRIORITY_TO_SEVERITY.get(priority, 'Low'),
                'impact_level': impact_level,
                'status': 'Registered',  # Registered -> Investigated -> Diagnosed -> Resolved
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'resolution_notes': [],
                'workaround_provided': False
            }
            
            self.incidents[incident_id] = incident
            log_event("INFO", f"Incident {incident_id} created for ticket {ticket_id}")
            return incident
        
        except Exception as e:
            log_event("ERROR", f"Error creating incident: {str(e)}")
            raise
    
    def update_incident_status(self, incident_id, new_status, resolution_note=''):
        """
        Update incident status following ITIL workflow
        
        Args:
            incident_id (str): Incident ID
            new_status (str): New status
            resolution_note (str): Optional resolution note
        
        Returns:
            bool: True if updated successfully
        """
        try:
            if incident_id not in self.incidents:
                raise KeyError(f"Incident {incident_id} not found")
            
            incident = self.incidents[incident_id]
            old_status = incident['status']
            
            # Valid status transitions
            valid_transitions = {
                'Registered': ['Investigated', 'Resolved'],
                'Investigated': ['Diagnosed', 'Resolved'],
                'Diagnosed': ['Resolved', 'Workaround Provided'],
                'Workaround Provided': ['Resolved'],
                'Resolved': []
            }
            
            if new_status not in valid_transitions.get(old_status, []):
                raise UnauthorizedActionError(
                    f"transition from {old_status} to {new_status}",
                    "Invalid state transition in incident workflow"
                )
            
            incident['status'] = new_status
            if resolution_note:
                incident['resolution_notes'].append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'note': resolution_note
                })
            
            log_event("INFO", f"Incident {incident_id} status updated: {old_status} -> {new_status}")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error updating incident status: {str(e)}")
            raise


class ServiceRequestManagement:
    """
    ITIL Service Request Management Process
    Handles standard requests for service fulfillment (password resets, software installs, etc.)
    
    Demonstrates:
    - Process workflow implementation
    - Approval tracking
    - Status management
    """
    
    # Service request types
    REQUEST_TYPES = {
        'Password Reset': 1,
        'Software Installation': 2,
        'Hardware Request': 3,
        'Access Request': 4,
        'VPN Setup': 5,
        'Printer Configuration': 6
    }
    
    # Approval workflow levels
    APPROVAL_LEVELS = ['Requested', 'Manager Approval', 'IT Approval', 'Fulfilled', 'Closed']
    
    def __init__(self):
        """Initialize service request management"""
        self.service_requests = {}
        self.request_counter = 0
        log_event("INFO", "Service Request Management initialized")
    
    def create_service_request(self, employee_name, department, request_type, description):
        """
        Create new service request
        
        Args:
            employee_name (str): Employee name
            department (str): Department
            request_type (str): Type of service request
            description (str): Detailed description
        
        Returns:
            dict: Created service request
        """
        try:
            if request_type not in self.REQUEST_TYPES:
                raise DataValidationError('request_type', 'valid request type', request_type)
            
            self.request_counter += 1
            request_id = f"SR{self.request_counter:05d}"
            
            service_request = {
                'request_id': request_id,
                'employee_name': employee_name,
                'department': department,
                'request_type': request_type,
                'description': description,
                'status': 'Requested',
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'approvals': {
                    'manager_approval': None,
                    'it_approval': None
                },
                'fulfillment_date': None,
                'completion_date': None
            }
            
            self.service_requests[request_id] = service_request
            log_event("INFO", f"Service Request {request_id} created")
            return service_request
        
        except Exception as e:
            log_event("ERROR", f"Error creating service request: {str(e)}")
            raise
    
    def approve_request(self, request_id, approval_type, approver_name, approved=True, comments=''):
        """
        Approve or reject service request
        
        Args:
            request_id (str): Service request ID
            approval_type (str): 'manager' or 'it'
            approver_name (str): Name of approver
            approved (bool): Approval decision
            comments (str): Optional comments
        
        Returns:
            bool: True if approval processed
        """
        try:
            if request_id not in self.service_requests:
                raise KeyError(f"Service Request {request_id} not found")
            
            request = self.service_requests[request_id]
            approval_key = f"{approval_type}_approval"
            
            request['approvals'][approval_key] = {
                'approved': approved,
                'approver': approver_name,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'comments': comments
            }
            
            # Update status if both approvals are complete
            if request['approvals']['manager_approval'] and request['approvals']['it_approval']:
                if all(a['approved'] for a in request['approvals'].values()):
                    request['status'] = 'Fulfilled'
                    request['fulfillment_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_event("INFO", f"Service Request {request_id} {approval_type} approval: {approved}")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error approving service request: {str(e)}")
            raise


class ProblemManagement:
    """
    ITIL Problem Management Process
    Identifies and manages problems (root causes of incidents)
    Creates problem records when issue occurs 5+ times
    
    Demonstrates:
    - Data aggregation
    - Pattern detection
    - Permanent solution tracking
    """
    
    PROBLEM_THRESHOLD = 5  # Create problem record after 5 occurrences
    
    def __init__(self):
        """Initialize problem management"""
        self.problems = {}
        self.problem_counter = 0
        self.issue_occurrences = {}  # Track repeated issues
        log_event("INFO", "Problem Management initialized")
    
    def track_issue_occurrence(self, category):
        """
        Track issue occurrences to detect repeated problems
        
        Args:
            category (str): Issue category
        
        Returns:
            dict: Problem record if threshold reached, None otherwise
        """
        try:
            if category not in self.issue_occurrences:
                self.issue_occurrences[category] = []
            
            self.issue_occurrences[category].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            occurrence_count = len(self.issue_occurrences[category])
            
            # Create problem record if threshold reached
            if occurrence_count == self.PROBLEM_THRESHOLD:
                problem = self.create_problem_record(category, occurrence_count)
                log_event("WARNING", f"Problem record created for '{category}' after {occurrence_count} occurrences")
                return problem
            
            if occurrence_count % self.PROBLEM_THRESHOLD == 0:
                log_event("WARNING", f"Issue '{category}' has occurred {occurrence_count} times")
            
            return None
        
        except Exception as e:
            log_event("ERROR", f"Error tracking issue occurrence: {str(e)}")
            raise
    
    def create_problem_record(self, issue_category, occurrence_count):
        """
        Create permanent problem record for recurring issue
        
        Args:
            issue_category (str): Category of the issue
            occurrence_count (int): Number of occurrences
        
        Returns:
            dict: Problem record
        """
        try:
            self.problem_counter += 1
            problem_id = f"PRB{self.problem_counter:05d}"
            
            problem_record = {
                'problem_id': problem_id,
                'issue_category': issue_category,
                'first_occurrence': datetime.now().strftime("%Y-%m-%d"),
                'occurrence_count': occurrence_count,
                'status': 'Open',  # Open -> Analysis -> Solution Identified -> Implemented -> Closed
                'severity': self._calculate_severity(occurrence_count),
                'root_cause': None,
                'permanent_solution': None,
                'workarounds': [],
                'related_tickets': [],
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'resolved_date': None
            }
            
            self.problems[problem_id] = problem_record
            log_event("SUCCESS", f"Problem record {problem_id} created for '{issue_category}'")
            return problem_record
        
        except Exception as e:
            log_event("ERROR", f"Error creating problem record: {str(e)}")
            raise
    
    def _calculate_severity(self, occurrence_count):
        """
        Calculate problem severity based on occurrence count
        
        Args:
            occurrence_count (int): Number of times issue occurred
        
        Returns:
            str: Severity level
        """
        if occurrence_count >= 20:
            return 'Critical'
        elif occurrence_count >= 15:
            return 'High'
        elif occurrence_count >= 10:
            return 'Medium'
        else:
            return 'Low'
    
    def add_root_cause_analysis(self, problem_id, root_cause, analysis_notes):
        """
        Add root cause analysis to problem record
        
        Args:
            problem_id (str): Problem ID
            root_cause (str): Root cause description
            analysis_notes (str): Detailed analysis notes
        
        Returns:
            bool: True if added successfully
        """
        try:
            if problem_id not in self.problems:
                raise KeyError(f"Problem {problem_id} not found")
            
            problem = self.problems[problem_id]
            problem['root_cause'] = root_cause
            problem['analysis_notes'] = analysis_notes
            problem['status'] = 'Analysis'
            
            log_event("INFO", f"Root cause analysis added to {problem_id}")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error adding root cause analysis: {str(e)}")
            raise
    
    def add_permanent_solution(self, problem_id, solution_description, implementation_steps):
        """
        Add permanent solution to problem record
        
        Args:
            problem_id (str): Problem ID
            solution_description (str): Solution description
            implementation_steps (list): Steps to implement solution
        
        Returns:
            bool: True if added successfully
        """
        try:
            if problem_id not in self.problems:
                raise KeyError(f"Problem {problem_id} not found")
            
            problem = self.problems[problem_id]
            problem['permanent_solution'] = {
                'description': solution_description,
                'implementation_steps': implementation_steps,
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            problem['status'] = 'Solution Identified'
            
            log_event("INFO", f"Permanent solution added to {problem_id}")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error adding permanent solution: {str(e)}")
            raise


class ChangeManagement:
    """
    ITIL Change Management Process
    Tracks and manages changes to IT infrastructure and systems
    
    Demonstrates:
    - Change request workflow
    - Impact assessment
    - Implementation tracking
    """
    
    CHANGE_TYPES = ['Standard', 'Normal', 'Emergency']
    CHANGE_STATUSES = ['Requested', 'Planned', 'Approved', 'Implemented', 'Verified', 'Closed', 'Backed Out']
    
    def __init__(self):
        """Initialize change management"""
        self.changes = {}
        self.change_counter = 0
        log_event("INFO", "Change Management initialized")
    
    def create_change_request(self, requested_by, description, change_type='Normal', 
                            affected_systems=None, implementation_plan=None):
        """
        Create change request
        
        Args:
            requested_by (str): Name of requester
            description (str): Description of change
            change_type (str): Type of change (Standard, Normal, Emergency)
            affected_systems (list): Systems affected by change
            implementation_plan (dict): Plan for implementation
        
        Returns:
            dict: Change request record
        """
        try:
            if change_type not in self.CHANGE_TYPES:
                raise DataValidationError('change_type', 'valid change type', change_type)
            
            self.change_counter += 1
            change_id = f"CHG{self.change_counter:05d}"
            
            change_request = {
                'change_id': change_id,
                'requested_by': requested_by,
                'description': description,
                'change_type': change_type,
                'affected_systems': affected_systems or [],
                'implementation_plan': implementation_plan,
                'status': 'Requested',
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'approvals': [],
                'implementation_date': None,
                'verification_results': None,
                'rollback_plan': None
            }
            
            self.changes[change_id] = change_request
            log_event("INFO", f"Change Request {change_id} created by {requested_by}")
            return change_request
        
        except Exception as e:
            log_event("ERROR", f"Error creating change request: {str(e)}")
            raise


# File paths for ITIL data persistence
ITIL_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'itil')


def ensure_itil_data_directory():
    """Ensure ITIL data directory exists"""
    try:
        if not os.path.exists(ITIL_DATA_DIR):
            os.makedirs(ITIL_DATA_DIR)
        return True
    except Exception as e:
        log_event("ERROR", f"Error creating ITIL data directory: {str(e)}")
        return False


def save_problem_records(problem_management):
    """Save problem records to JSON file"""
    try:
        ensure_itil_data_directory()
        filepath = os.path.join(ITIL_DATA_DIR, 'problems.json')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(problem_management.problems, f, indent=4)
        
        log_event("SUCCESS", f"Saved {len(problem_management.problems)} problem records")
        return True
    
    except Exception as e:
        log_event("ERROR", f"Error saving problem records: {str(e)}")
        return False


def load_problem_records():
    """Load problem records from JSON file"""
    try:
        filepath = os.path.join(ITIL_DATA_DIR, 'problems.json')
        
        if not os.path.exists(filepath):
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        
        log_event("INFO", f"Loaded {len(problems)} problem records")
        return problems
    
    except Exception as e:
        log_event("ERROR", f"Error loading problem records: {str(e)}")
        return {}
