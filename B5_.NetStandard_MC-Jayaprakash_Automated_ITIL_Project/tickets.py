"""
Ticket Management Module for Smart IT Service Desk
Implements OOP concepts with Ticket, IncidentTicket, ServiceRequest, and ProblemRecord classes
"""

from datetime import datetime, timedelta
from utils import log_event, get_next_ticket_id, load_tickets_from_json, save_tickets_to_json
from utils import print_error_message, print_success_message, display_ticket_details
from utils import validate_input, display_banner
from abc import ABC, abstractmethod


class Ticket(ABC):
    """
    Abstract Base Ticket class - Base class for all ticket types
    Demonstrates: Abstraction, Encapsulation, Inheritance base
    """
    
    # Class variable to track total tickets created
    _total_tickets = 0
    
    # Priority mapping
    PRIORITY_MAP = {
        'Server Down': 'P1',
        'Internet Down': 'P2',
        'Laptop Slow': 'P3',
        'Password Reset': 'P4',
        'Printer not working': 'P3',
        'Outlook not opening': 'P3',
        'Disk space full': 'P2',
        'High CPU usage on server': 'P1',
        'Application crash': 'P2'
    }
    
    # SLA Timings in hours
    SLA_TIMINGS = {
        'P1': 1,      # 1 hour
        'P2': 4,      # 4 hours
        'P3': 8,      # 8 hours
        'P4': 24      # 24 hours
    }
    
    # Escalation timings in minutes
    ESCALATION_TIMINGS = {
        'P1': 30,     # 30 minutes
        'P2': 120,    # 2 hours
    }
    
    def __init__(self, ticket_id, employee_name, department, issue_description, 
                 category, priority='P4', status='Open'):
        """
        Constructor for Ticket class
        
        Args:
            ticket_id (str): Auto-generated ticket ID
            employee_name (str): Name of employee raising ticket
            department (str): Department of employee
            issue_description (str): Description of the issue
            category (str): Category of issue
            priority (str): Priority level (P1-P4)
            status (str): Ticket status (Open/In Progress/Closed)
        """
        # Private attributes (encapsulation)
        self._ticket_id = ticket_id
        self._employee_name = employee_name
        self._department = department
        self._issue_description = issue_description
        self._category = category
        self._priority = priority
        self._status = status
        self._created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._updated_date = self._created_date
        self._closed_date = None
        self._assigned_to = self._assign_default_staff()
        self._sla_breached = False
        
        Ticket._total_tickets += 1
    
    def _assign_default_staff(self):
        """
        Assign ticket to default support staff based on priority
        Demonstrates: Encapsulation and business logic
        
        Returns:
            str: Name of assigned support staff member
        """
        # Assign based on priority level for better distribution
        priority_to_staff = {
            'P1': 'Senior Support (Priority)',
            'P2': 'Support Team Lead',
            'P3': 'Support Specialist',
            'P4': 'Junior Support Technician'
        }
        return priority_to_staff.get(self._priority, 'Support Team Lead')
    
    @property
    def ticket_id(self):
        """Get ticket ID (read-only property)"""
        return self._ticket_id
    
    @property
    def employee_name(self):
        """Get employee name"""
        return self._employee_name
    
    @property
    def department(self):
        """Get department"""
        return self._department
    
    @property
    def issue_description(self):
        """Get issue description"""
        return self._issue_description
    
    @property
    def category(self):
        """Get category"""
        return self._category
    
    @property
    def priority(self):
        """Get priority"""
        return self._priority
    
    @property
    def status(self):
        """Get status"""
        return self._status
    
    @status.setter
    def status(self, value):
        """Set status with validation"""
        valid_statuses = ['Open', 'In Progress', 'Closed']
        if value in valid_statuses:
            self._status = value
            self._updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if value == 'Closed':
                self._closed_date = self._updated_date
        else:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
    
    @property
    def created_date(self):
        """Get creation date"""
        return self._created_date
    
    @property
    def updated_date(self):
        """Get last updated date"""
        return self._updated_date
    
    @property
    def closed_date(self):
        """Get closed date"""
        return self._closed_date
    
    @property
    def sla_breached(self):
        """Get SLA breach status"""
        return self._sla_breached
    
    @sla_breached.setter
    def sla_breached(self, value):
        """Set SLA breach status"""
        self._sla_breached = value
    
    @property
    def assigned_to(self):
        """Get assigned to"""
        return self._assigned_to
    
    @assigned_to.setter
    def assigned_to(self, value):
        """Set assigned to"""
        self._assigned_to = value
    
    @abstractmethod
    def get_ticket_type(self):
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @staticmethod
    def get_priority_for_category(category):
        """
        Static method to determine priority from category
        Demonstrates: Static method usage
        
        Args:
            category (str): Issue category
        
        Returns:
            str: Priority level (P1-P4)
        """
        return Ticket.PRIORITY_MAP.get(category, 'P4')
    
    @staticmethod
    def get_sla_hours(priority):
        """
        Static method to get SLA hours for priority
        
        Args:
            priority (str): Priority level
        
        Returns:
            int: SLA hours
        """
        return Ticket.SLA_TIMINGS.get(priority, 24)
    
    @classmethod
    def get_total_tickets(cls):
        """
        Class method to get total tickets created
        Demonstrates: Class method usage
        
        Returns:
            int: Total tickets created
        """
        return cls._total_tickets
    
    def check_sla_breach(self):
        """
        Check if ticket has breached SLA
        
        Returns:
            bool: True if SLA breached, False otherwise
        """
        if self._status == 'Closed':
            return False
        
        try:
            created = datetime.strptime(self._created_date, "%Y-%m-%d %H:%M:%S")
            current = datetime.now()
            elapsed_hours = (current - created).total_seconds() / 3600
            
            sla_hours = self.get_sla_hours(self._priority)
            
            if elapsed_hours > sla_hours:
                self._sla_breached = True
                log_event("WARNING", f"SLA breached for ticket {self._ticket_id}")
                return True
            return False
        except Exception as e:
            log_event("ERROR", f"Error checking SLA: {str(e)}")
            return False
    
    def check_escalation_needed(self):
        """
        Check if ticket needs escalation
        
        Returns:
            bool: True if escalation needed, False otherwise
        """
        if self._status == 'Closed':
            return False
        
        try:
            created = datetime.strptime(self._created_date, "%Y-%m-%d %H:%M:%S")
            current = datetime.now()
            elapsed_minutes = (current - created).total_seconds() / 60
            
            escalation_minutes = self.ESCALATION_TIMINGS.get(self._priority)
            
            if escalation_minutes and elapsed_minutes > escalation_minutes:
                log_event("WARNING", f"Escalation alert for ticket {self._ticket_id} (Priority: {self._priority})")
                return True
            return False
        except Exception as e:
            log_event("ERROR", f"Error checking escalation: {str(e)}")
            return False
    
    def to_dict(self):
        """
        Convert ticket to dictionary
        
        Returns:
            dict: Ticket as dictionary
        """
        return {
            'ticket_id': self._ticket_id,
            'employee_name': self._employee_name,
            'department': self._department,
            'issue_description': self._issue_description,
            'category': self._category,
            'priority': self._priority,
            'status': self._status,
            'created_date': self._created_date,
            'updated_date': self._updated_date,
            'closed_date': self._closed_date,
            'assigned_to': self._assigned_to,
            'sla_breached': self._sla_breached,
            'ticket_type': self.get_ticket_type()
        }
    
    def __str__(self):
        """String representation of ticket"""
        return f"Ticket {self._ticket_id}: {self._category} - {self._status} (Priority: {self._priority})"
    
    def __repr__(self):
        """Official string representation"""
        return f"Ticket(id={self._ticket_id}, status={self._status}, priority={self._priority})"


class IncidentTicket(Ticket):
    """
    Incident Ticket class - For incident management
    Demonstrates: Inheritance, Method overriding
    """
    
    def __init__(self, ticket_id, employee_name, department, issue_description, 
                 category, priority='P3', status='Open', severity='Medium'):
        """
        Constructor for IncidentTicket
        
        Args:
            severity (str): Severity level (Low, Medium, High, Critical)
        """
        super().__init__(ticket_id, employee_name, department, issue_description, 
                        category, priority, status)
        self._severity = severity
        self._resolution_notes = ""
        self._incident_category = "Unplanned Interruption"
    
    def get_ticket_type(self):
        """Override abstract method"""
        return "Incident"
    
    def add_resolution_notes(self, notes):
        """Add resolution notes to incident"""
        self._resolution_notes = notes
        log_event("INFO", f"Resolution notes added to incident {self._ticket_id}")
    
    def get_severity(self):
        """Get severity level"""
        return self._severity
    
    def to_dict(self):
        """Override to_dict method"""
        data = super().to_dict()
        data['severity'] = self._severity
        data['resolution_notes'] = self._resolution_notes
        data['incident_category'] = self._incident_category
        return data


class ServiceRequest(Ticket):
    """
    Service Request class - For service request management
    Demonstrates: Inheritance, Method overriding
    """
    
    def __init__(self, ticket_id, employee_name, department, issue_description, 
                 category, priority='P4', status='Open', request_type='Standard'):
        """
        Constructor for ServiceRequest
        
        Args:
            request_type (str): Type of request (Standard, Urgent, Expedited)
        """
        super().__init__(ticket_id, employee_name, department, issue_description, 
                        category, priority, status)
        self._request_type = request_type
        self._fulfillment_date = None
        self._approval_status = "Pending"
    
    def get_ticket_type(self):
        """Override abstract method"""
        return "Service Request"
    
    def approve_request(self):
        """Approve the service request"""
        self._approval_status = "Approved"
        log_event("INFO", f"Service request {self._ticket_id} approved")
    
    def fulfill_request(self):
        """Mark request as fulfilled"""
        self._fulfillment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Closed"
        log_event("SUCCESS", f"Service request {self._ticket_id} fulfilled")
    
    def get_approval_status(self):
        """Get approval status"""
        return self._approval_status
    
    def to_dict(self):
        """Override to_dict method"""
        data = super().to_dict()
        data['request_type'] = self._request_type
        data['fulfillment_date'] = self._fulfillment_date
        data['approval_status'] = self._approval_status
        return data


class ProblemRecord(Ticket):
    """
    Problem Record class - For problem management (when same issue occurs 5+ times)
    Demonstrates: Inheritance, Method overriding
    """
    
    def __init__(self, ticket_id, employee_name, department, issue_description, 
                 category, priority='P2', status='Open', occurrence_count=5):
        """
        Constructor for ProblemRecord
        
        Args:
            occurrence_count (int): Number of times the issue has occurred
        """
        super().__init__(ticket_id, employee_name, department, issue_description, 
                        category, priority, status)
        self._occurrence_count = occurrence_count
        self._root_cause = ""
        self._permanent_solution = ""
        self._related_incidents = []
        self._problem_status = "Identified"
    
    def get_ticket_type(self):
        """Override abstract method"""
        return "Problem Record"
    
    def add_root_cause(self, cause):
        """Add root cause analysis"""
        self._root_cause = cause
        log_event("INFO", f"Root cause added to problem {self._ticket_id}")
    
    def add_permanent_solution(self, solution):
        """Add permanent solution"""
        self._permanent_solution = solution
        self._problem_status = "Solved"
        log_event("SUCCESS", f"Permanent solution added to problem {self._ticket_id}")
    
    def add_related_incident(self, incident_id):
        """Add related incident ticket"""
        if incident_id not in self._related_incidents:
            self._related_incidents.append(incident_id)
    
    def get_occurrence_count(self):
        """Get number of occurrences"""
        return self._occurrence_count
    
    def to_dict(self):
        """Override to_dict method"""
        data = super().to_dict()
        data['occurrence_count'] = self._occurrence_count
        data['root_cause'] = self._root_cause
        data['permanent_solution'] = self._permanent_solution
        data['related_incidents'] = self._related_incidents
        data['problem_status'] = self._problem_status
        return data


class TicketManager:
    """
    Manages all ticket operations
    Demonstrates: Encapsulation, class composition
    """
    
    def __init__(self):
        """Initialize ticket manager and load existing tickets"""
        self.tickets = load_tickets_from_json()
        self.issue_frequency = {}  # Track issue occurrences for problem detection
        self._count_issue_frequency()
        log_event("INFO", "Ticket Manager initialized")
    
    def _count_issue_frequency(self):
        """Count frequency of each issue category"""
        self.issue_frequency = {}
        for ticket in self.tickets.values():
            category = ticket.get('category', 'Unknown')
            self.issue_frequency[category] = self.issue_frequency.get(category, 0) + 1
    
    def create_ticket(self, employee_name, department, issue_description, category):
        """
        Create a new ticket
        
        Args:
            employee_name (str): Employee name
            department (str): Department
            issue_description (str): Issue description
            category (str): Issue category
        
        Returns:
            Ticket: Created ticket object or None if failed
        """
        try:
            # Validate input
            if not issue_description or issue_description.strip() == "":
                print_error_message("Issue description cannot be empty!")
                log_event("ERROR", "Attempted to create ticket with empty description")
                return None
            
            # Get next ticket ID
            ticket_id = get_next_ticket_id(self.tickets)
            
            # Determine priority based on category
            priority = Ticket.get_priority_for_category(category)
            
            # Check if this should be a Problem Record (same issue 5+ times)
            self.issue_frequency[category] = self.issue_frequency.get(category, 0) + 1
            
            if self.issue_frequency[category] >= 5:
                ticket = ProblemRecord(ticket_id, employee_name, department, 
                                      issue_description, category, priority, 
                                      'Open', self.issue_frequency[category])
                log_event("WARNING", f"Problem Record created for category '{category}' "
                                   f"(occurred {self.issue_frequency[category]} times)")
            else:
                # Create appropriate ticket type based on priority
                if priority in ['P1', 'P2']:
                    ticket = IncidentTicket(ticket_id, employee_name, department, 
                                           issue_description, category, priority)
                else:
                    ticket = ServiceRequest(ticket_id, employee_name, department, 
                                           issue_description, category, priority)
            
            # Store ticket
            self.tickets[ticket_id] = ticket.to_dict()
            save_tickets_to_json(self.tickets)
            
            log_event("SUCCESS", f"Ticket {ticket_id} created - Category: {category}, Priority: {priority}")
            print_success_message(f"Ticket {ticket_id} created successfully!")
            print(f"Priority: {priority}, Status: Open")
            
            return ticket
        
        except Exception as e:
            log_event("ERROR", f"Error creating ticket: {str(e)}")
            print_error_message(f"Error creating ticket: {str(e)}")
            return None
    
    def get_ticket_by_id(self, ticket_id):
        """
        Retrieve ticket by ID
        
        Args:
            ticket_id (str): Ticket ID to search
        
        Returns:
            dict: Ticket data or None if not found
        """
        try:
            if ticket_id not in self.tickets:
                print_error_message(f"Ticket {ticket_id} not found!")
                log_event("WARNING", f"Ticket {ticket_id} not found")
                return None
            
            return self.tickets[ticket_id]
        
        except Exception as e:
            log_event("ERROR", f"Error retrieving ticket {ticket_id}: {str(e)}")
            print_error_message(f"Error retrieving ticket: {str(e)}")
            return None
    
    def view_all_tickets(self):
        """
        Display all tickets
        
        Returns:
            int: Number of tickets displayed
        """
        try:
            if not self.tickets:
                print_error_message("No tickets found!")
                return 0
            
            print("\n" + "="*100)
            print(f"{'ID':<10} {'Employee':<15} {'Department':<15} {'Category':<20} "
                  f"{'Priority':<10} {'Status':<15}")
            print("="*100)
            
            for ticket_id, ticket in self.tickets.items():
                print(f"{ticket_id:<10} {ticket['employee_name']:<15} "
                      f"{ticket['department']:<15} {ticket['category']:<20} "
                      f"{ticket['priority']:<10} {ticket['status']:<15}")
            
            print("="*100)
            print(f"Total Tickets: {len(self.tickets)}")
            return len(self.tickets)
        
        except Exception as e:
            log_event("ERROR", f"Error viewing tickets: {str(e)}")
            print_error_message(f"Error viewing tickets: {str(e)}")
            return 0
    
    def update_ticket_status(self, ticket_id, new_status):
        """
        Update ticket status
        
        Args:
            ticket_id (str): Ticket ID
            new_status (str): New status (Open/In Progress/Closed)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            ticket = self.get_ticket_by_id(ticket_id)
            if not ticket:
                return False
            
            valid_statuses = ['Open', 'In Progress', 'Closed']
            if new_status not in valid_statuses:
                print_error_message(f"Invalid status. Must be one of {valid_statuses}")
                return False
            
            old_status = ticket['status']
            ticket['status'] = new_status
            ticket['updated_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if new_status == 'Closed':
                ticket['closed_date'] = ticket['updated_date']
            
            self.tickets[ticket_id] = ticket
            save_tickets_to_json(self.tickets)
            
            log_event("SUCCESS", f"Ticket {ticket_id} status updated: {old_status} → {new_status}")
            print_success_message(f"Ticket status updated: {old_status} → {new_status}")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error updating ticket status: {str(e)}")
            print_error_message(f"Error updating ticket: {str(e)}")
            return False
    
    def close_ticket(self, ticket_id):
        """
        Close a ticket
        
        Args:
            ticket_id (str): Ticket ID to close
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            ticket = self.get_ticket_by_id(ticket_id)
            if not ticket:
                return False
            
            if ticket['status'] == 'Closed':
                print_error_message("Ticket is already closed!")
                return False
            
            return self.update_ticket_status(ticket_id, 'Closed')
        
        except Exception as e:
            log_event("ERROR", f"Error closing ticket: {str(e)}")
            print_error_message(f"Error closing ticket: {str(e)}")
            return False
    
    def delete_ticket(self, ticket_id):
        """
        Delete a ticket
        
        Args:
            ticket_id (str): Ticket ID to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if ticket_id not in self.tickets:
                print_error_message(f"Ticket {ticket_id} not found!")
                return False
            
            ticket = self.tickets.pop(ticket_id)
            save_tickets_to_json(self.tickets)
            
            # Recalculate issue frequency
            self._count_issue_frequency()
            
            log_event("WARNING", f"Ticket {ticket_id} deleted")
            print_success_message(f"Ticket {ticket_id} deleted successfully!")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error deleting ticket: {str(e)}")
            print_error_message(f"Error deleting ticket: {str(e)}")
            return False
    
    def search_tickets(self, search_term, search_type='id'):
        """
        Search tickets by various criteria
        
        Args:
            search_term (str): Search term
            search_type (str): Type of search (id, category, status, priority, employee)
        
        Returns:
            list: List of matching tickets
        """
        try:
            results = []
            
            for ticket_id, ticket in self.tickets.items():
                match = False
                
                if search_type == 'id':
                    match = search_term.lower() in ticket_id.lower()
                elif search_type == 'category':
                    match = search_term.lower() in ticket['category'].lower()
                elif search_type == 'status':
                    match = search_term.lower() in ticket['status'].lower()
                elif search_type == 'priority':
                    match = search_term.lower() in ticket['priority'].lower()
                elif search_type == 'employee':
                    match = search_term.lower() in ticket['employee_name'].lower()
                
                if match:
                    results.append((ticket_id, ticket))
            
            return results
        
        except Exception as e:
            log_event("ERROR", f"Error searching tickets: {str(e)}")
            print_error_message(f"Error searching tickets: {str(e)}")
            return []
    
    def check_sla_status(self):
        """
        Check SLA status for all open tickets
        
        Returns:
            dict: Summary of SLA status
        """
        try:
            sla_breached = []
            escalation_alerts = []
            
            for ticket_id, ticket in self.tickets.items():
                if ticket['status'] == 'Closed':
                    continue
                
                created = datetime.strptime(ticket['created_date'], "%Y-%m-%d %H:%M:%S")
                current = datetime.now()
                
                # Check SLA breach
                elapsed_hours = (current - created).total_seconds() / 3600
                sla_hours = Ticket.get_sla_hours(ticket['priority'])
                
                if elapsed_hours > sla_hours:
                    sla_breached.append(ticket_id)
                    ticket['sla_breached'] = True
                    self.tickets[ticket_id] = ticket
                
                # Check escalation
                elapsed_minutes = (current - created).total_seconds() / 60
                escalation_map = {'P1': 30, 'P2': 120}
                escalation_minutes = escalation_map.get(ticket['priority'])
                
                if escalation_minutes and elapsed_minutes > escalation_minutes:
                    escalation_alerts.append(ticket_id)
            
            # Save updated tickets
            if sla_breached or escalation_alerts:
                save_tickets_to_json(self.tickets)
            
            return {
                'sla_breached': sla_breached,
                'escalation_alerts': escalation_alerts
            }
        
        except Exception as e:
            log_event("ERROR", f"Error checking SLA status: {str(e)}")
            return {'sla_breached': [], 'escalation_alerts': []}
    
    def get_statistics(self):
        """
        Get ticket statistics
        
        Returns:
            dict: Statistics including total, open, closed, by priority, etc.
        """
        try:
            stats = {
                'total': len(self.tickets),
                'open': 0,
                'in_progress': 0,
                'closed': 0,
                'by_priority': {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0},
                'by_department': {},
                'by_category': {},
                'sla_breached': 0
            }
            
            for ticket in self.tickets.values():
                # Count by status
                status = ticket['status']
                if status == 'Open':
                    stats['open'] += 1
                elif status == 'In Progress':
                    stats['in_progress'] += 1
                elif status == 'Closed':
                    stats['closed'] += 1
                
                # Count by priority
                stats['by_priority'][ticket['priority']] += 1
                
                # Count by department
                dept = ticket['department']
                stats['by_department'][dept] = stats['by_department'].get(dept, 0) + 1
                
                # Count by category
                cat = ticket['category']
                stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
                
                # Count SLA breached
                if ticket.get('sla_breached', False):
                    stats['sla_breached'] += 1
            
            return stats
        
        except Exception as e:
            log_event("ERROR", f"Error getting statistics: {str(e)}")
            return {}
