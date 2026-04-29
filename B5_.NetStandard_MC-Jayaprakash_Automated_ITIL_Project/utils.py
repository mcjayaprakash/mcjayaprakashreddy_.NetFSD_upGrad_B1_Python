

import os
import json
import csv
import re
import functools
import time
from datetime import datetime
from functools import wraps

# Paths for data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TICKETS_FILE = os.path.join(DATA_DIR, 'tickets.json')
LOGS_FILE = os.path.join(DATA_DIR, 'logs.txt')
BACKUP_FILE = os.path.join(DATA_DIR, 'backup.csv')


def ensure_data_directory_exists():
    """Ensure data directory exists"""
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        return True
    except Exception as e:
        log_event("ERROR", f"Failed to create data directory: {str(e)}")
        return False


def log_event(level, message):
    """
    Log events to logs.txt file
    Levels: INFO, WARNING, ERROR, SUCCESS
    
    Args:
        level (str): Log level (INFO, WARNING, ERROR, SUCCESS)
        message (str): Message to log
    """
    try:
        ensure_data_directory_exists()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        with open(LOGS_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message)
        
        # Also print to console for visibility
        print(log_message.strip())
    except Exception as e:
        print(f"Error logging event: {str(e)}")


def load_tickets_from_json():
    """
    Load all tickets from tickets.json file
    
    Returns:
        dict: Dictionary containing all tickets, or empty dict if file doesn't exist
    """
    try:
        if not os.path.exists(TICKETS_FILE):
            log_event("INFO", f"Tickets file not found at {TICKETS_FILE}. Starting with empty tickets.")
            return {}
        
        with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        log_event("INFO", f"Successfully loaded {len(tickets)} tickets from file.")
        return tickets
    except FileNotFoundError:
        log_event("WARNING", f"Tickets file not found: {TICKETS_FILE}")
        return {}
    except json.JSONDecodeError:
        log_event("ERROR", f"Invalid JSON in tickets file: {TICKETS_FILE}")
        return {}
    except Exception as e:
        log_event("ERROR", f"Error loading tickets: {str(e)}")
        return {}


def save_tickets_to_json(tickets):
    """
    Save tickets to tickets.json file
    
    Args:
        tickets (dict): Dictionary of tickets to save
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_data_directory_exists()
        with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tickets, f, indent=4, ensure_ascii=False)
        log_event("SUCCESS", f"Saved {len(tickets)} tickets to file.")
        return True
    except Exception as e:
        log_event("ERROR", f"Error saving tickets: {str(e)}")
        return False


def backup_tickets_to_csv(tickets):
    """
    Create automatic backup of tickets to backup.csv file
    
    Args:
        tickets (dict): Dictionary of tickets to backup
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_data_directory_exists()
        
        if not tickets:
            log_event("WARNING", "No tickets to backup")
            return False
        
        # Collect all unique fieldnames from all tickets
        all_fieldnames = set()
        for ticket in tickets.values():
            all_fieldnames.update(ticket.keys())
        
        # Define standard fieldnames in consistent order
        standard_fields = [
            'ticket_id', 'employee_name', 'department', 'issue_description',
            'category', 'priority', 'status', 'created_date', 'updated_date',
            'closed_date', 'assigned_to', 'sla_breached', 'ticket_type',
            'request_type', 'fulfillment_date', 'approval_status'
        ]
        
        # Use standard fields first, then add any extra fields
        fieldnames = standard_fields + sorted(all_fieldnames - set(standard_fields))
        
        with open(BACKUP_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(tickets.values())
        
        log_event("SUCCESS", f"Backed up {len(tickets)} tickets to CSV file.")
        return True
    except Exception as e:
        log_event("ERROR", f"Error creating backup: {str(e)}")
        return False


def get_next_ticket_id(tickets):
    """
    Generate next auto-incremented ticket ID
    
    Args:
        tickets (dict): Dictionary of existing tickets
    
    Returns:
        str: Next ticket ID (e.g., TKT001, TKT002, etc.)
    """
    try:
        if not tickets:
            return "TKT001"
        
        # Extract numeric IDs from existing ticket IDs
        numeric_ids = []
        for ticket_id in tickets.keys():
            try:
                # Remove 'TKT' prefix and convert to int
                num = int(ticket_id.replace('TKT', ''))
                numeric_ids.append(num)
            except ValueError:
                continue
        
        if numeric_ids:
            next_id = max(numeric_ids) + 1
        else:
            next_id = 1
        
        return f"TKT{next_id:03d}"
    except Exception as e:
        log_event("ERROR", f"Error generating ticket ID: {str(e)}")
        return "TKT001"


def display_menu(title, options):
    """
    Display a formatted menu
    
    Args:
        title (str): Menu title
        options (list): List of menu options
    """
    print("\n" + "="*60)
    print(f"{title.center(60)}")
    print("="*60)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("="*60)


def display_banner():
    """Display application banner"""
    banner = """
    --- Smart IT Service Desk & System Monitoring Automation for TechNova Solutions ---
    """
    print(banner)


def validate_input(prompt, input_type=str, required=True):
    """
    Validate user input
    
    Args:
        prompt (str): Prompt message
        input_type (type): Expected input type (str, int)
        required (bool): Whether input is required
    
    Returns:
        any: Validated input value
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if required and not user_input:
                print("⚠️  This field is required. Please enter a value.")
                continue
            
            if input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            else:
                return user_input
        
        except ValueError:
            print(f"⚠️  Invalid input. Please enter a valid {input_type.__name__}.")
        except Exception as e:
            log_event("ERROR", f"Input validation error: {str(e)}")
            print("⚠️  An error occurred. Please try again.")


def format_datetime(dt):
    """
    Format datetime object to string
    
    Args:
        dt (str): DateTime string or datetime object
    
    Returns:
        str: Formatted datetime string
    """
    try:
        if isinstance(dt, str):
            return dt
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        log_event("ERROR", f"Error formatting datetime: {str(e)}")
        return str(dt)


def display_ticket_details(ticket):
    """
    Display ticket details in a formatted way
    
    Args:
        ticket (dict): Ticket dictionary containing details
    """
    print("\n" + "-"*60)
    for key, value in ticket.items():
        print(f"{key:.<20} {value}")
    print("-"*60)


def pause_execution(message="Press Enter to continue..."):
    """Pause execution and wait for user input"""
    input(f"\n{message}")


def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_success_message(message):
    """Print success message with formatting"""
    print(f"\n✅ {message}")


def print_error_message(message):
    """Print error message with formatting"""
    print(f"\n❌ {message}")


def print_warning_message(message):
    """Print warning message with formatting"""
    print(f"\n⚠️  {message}")


def print_info_message(message):
    """Print info message with formatting"""
    print(f"\nℹ️  {message}")


# ============================================================================
# ADVANCED PYTHON FEATURES - DECORATORS, GENERATORS, REGEX, ETC.
# ============================================================================

def timing_decorator(func):
    """
    Decorator to measure function execution time
    Demonstrates: Decorators, Higher-order functions
    
    Args:
        func: Function to measure
    
    Returns:
        Wrapper function with timing capability
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        if execution_time > 0.1:  # Only log if > 100ms
            log_event("INFO", f"Function '{func.__name__}' executed in {execution_time:.3f} seconds")
        
        return result
    return wrapper


def logging_decorator(func):
    """
    Decorator to log function calls
    Demonstrates: Decorators, Metaprogramming
    
    Args:
        func: Function to log
    
    Returns:
        Wrapper function with logging capability
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ', '.join(str(arg) for arg in args[1:])  # Skip self
        log_event("INFO", f"Calling {func.__name__}({args_str})")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            log_event("ERROR", f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper


def cache_decorator(func):
    """
    Decorator for caching function results
    Demonstrates: Decorators, Memoization, Functional programming
    
    Args:
        func: Function to cache
    
    Returns:
        Wrapper function with caching capability
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = str(args) + str(kwargs)
        if cache_key not in cache:
            cache[cache_key] = func(*args, **kwargs)
        return cache[cache_key]
    
    wrapper.cache = cache
    return wrapper


def validate_regex_decorator(pattern):
    """
    Decorator factory for regex validation
    Demonstrates: Decorator factories, Functional programming
    
    Args:
        pattern (str): Regex pattern to validate against
    
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = args[1] if len(args) > 1 else None
            if value and not re.match(pattern, str(value)):
                raise ValueError(f"Value '{value}' does not match pattern '{pattern}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# GENERATORS - DEMONSTRATES LAZY EVALUATION
# ============================================================================

def ticket_generator(tickets, status=None, priority=None):
    """
    Generator function to yield tickets with optional filtering
    Demonstrates: Generators, Lazy evaluation, Yield
    
    Args:
        tickets (dict): Dictionary of tickets
        status (str): Optional status filter
        priority (str): Optional priority filter
    
    Yields:
        tuple: (ticket_id, ticket) for matching tickets
    """
    for ticket_id, ticket in tickets.items():
        if status and ticket.get('status') != status:
            continue
        if priority and ticket.get('priority') != priority:
            continue
        yield ticket_id, ticket


def log_generator(filepath):
    """
    Generator to read log file line by line
    Demonstrates: File handling with generators, Memory efficiency
    
    Args:
        filepath (str): Path to log file
    
    Yields:
        str: Log line
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        log_event("WARNING", f"Log file not found: {filepath}")
        return


def batch_generator(iterable, batch_size):
    """
    Generator to yield items in batches
    Demonstrates: Generator patterns, Data chunking
    
    Args:
        iterable: Iterable to batch
        batch_size (int): Size of each batch
    
    Yields:
        list: Batch of items
    """
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


# ============================================================================
# ITERATORS - CUSTOM ITERATION BEHAVIOR
# ============================================================================

class TicketIterator:
    """
    Custom iterator for tickets
    Demonstrates: Iterator protocol, __iter__ and __next__
    """
    
    def __init__(self, tickets):
        """Initialize ticket iterator"""
        self.tickets = list(tickets.items())
        self.index = 0
    
    def __iter__(self):
        """Return iterator object"""
        return self
    
    def __next__(self):
        """Get next ticket"""
        if self.index >= len(self.tickets):
            raise StopIteration
        ticket_id, ticket = self.tickets[self.index]
        self.index += 1
        return ticket_id, ticket


class PaginatedTicketIterator:
    """
    Paginated iterator for tickets
    Demonstrates: Custom iteration with pagination
    """
    
    def __init__(self, tickets, page_size=10):
        """Initialize paginated iterator"""
        self.tickets = list(tickets.items())
        self.page_size = page_size
        self.current_page = 0
    
    def __iter__(self):
        """Return iterator object"""
        self.current_page = 0
        return self
    
    def __next__(self):
        """Get next page of tickets"""
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        
        if start_idx >= len(self.tickets):
            raise StopIteration
        
        page = self.tickets[start_idx:end_idx]
        self.current_page += 1
        return page
    
    def total_pages(self):
        """Get total number of pages"""
        return (len(self.tickets) + self.page_size - 1) // self.page_size


# ============================================================================
# REGEX VALIDATION FUNCTIONS
# ============================================================================

def validate_ticket_id(ticket_id):
    """
    Validate ticket ID format using regex
    Format: TKT followed by 3 digits
    
    Args:
        ticket_id (str): Ticket ID to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^TKT\d{3}$'
    return bool(re.match(pattern, ticket_id))


def validate_email(email):
    """
    Validate email format using regex
    
    Args:
        email (str): Email to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_priority(priority):
    """
    Validate priority format using regex
    Format: P followed by 1-4
    
    Args:
        priority (str): Priority to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^P[1-4]$'
    return bool(re.match(pattern, priority))


def validate_phone_number(phone):
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[\d\-\+\(\)\s]{10,}$'
    return bool(re.match(pattern, phone))


def extract_ticket_ids(text):
    """
    Extract all ticket IDs from text using regex
    
    Args:
        text (str): Text to search
    
    Returns:
        list: List of ticket IDs found
    """
    pattern = r'TKT\d{3}'
    return re.findall(pattern, text)


# ============================================================================
# MAP, FILTER, REDUCE OPERATIONS
# ============================================================================

def get_ticket_categories(tickets):
    """
    Get unique categories from tickets using functional programming
    Demonstrates: Map, lambda functions
    
    Args:
        tickets (dict): Dictionary of tickets
    
    Returns:
        set: Unique categories
    """
    categories = set(map(lambda ticket: ticket.get('category', 'Unknown'), tickets.values()))
    return categories


def get_high_priority_tickets(tickets):
    """
    Filter tickets with high priority (P1, P2)
    Demonstrates: Filter, lambda functions
    
    Args:
        tickets (dict): Dictionary of tickets
    
    Returns:
        list: List of high priority tickets
    """
    high_priority = list(filter(
        lambda ticket_item: ticket_item[1].get('priority') in ['P1', 'P2'],
        tickets.items()
    ))
    return high_priority


def calculate_ticket_statistics(tickets):
    """
    Calculate ticket statistics using reduce pattern
    Demonstrates: Functional programming patterns
    
    Args:
        tickets (dict): Dictionary of tickets
    
    Returns:
        dict: Statistics
    """
    from functools import reduce
    
    stats = reduce(lambda acc, ticket: {
        'total': acc['total'] + 1,
        'open': acc['open'] + (1 if ticket[1].get('status') == 'Open' else 0),
        'closed': acc['closed'] + (1 if ticket[1].get('status') == 'Closed' else 0),
        'high_priority': acc['high_priority'] + (1 if ticket[1].get('priority') in ['P1', 'P2'] else 0),
    }, tickets.items(), {
        'total': 0,
        'open': 0,
        'closed': 0,
        'high_priority': 0
    })
    
    return stats


# ============================================================================
# CONTEXT MANAGERS FOR FILE OPERATIONS
# ============================================================================

class ManagedFileOperation:
    """
    Context manager for safe file operations
    Demonstrates: Context managers, __enter__ and __exit__
    """
    
    def __init__(self, filepath, mode='r', encoding='utf-8'):
        """Initialize file context manager"""
        self.filepath = filepath
        self.mode = mode
        self.encoding = encoding
        self.file = None
    
    def __enter__(self):
        """Enter context - open file"""
        try:
            self.file = open(self.filepath, self.mode, encoding=self.encoding)
            return self.file
        except IOError as e:
            log_event("ERROR", f"Failed to open file {self.filepath}: {str(e)}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - close file"""
        if self.file:
            self.file.close()
        if exc_type:
            log_event("ERROR", f"Exception occurred: {exc_val}")
        return False


def safe_read_json(filepath):
    """
    Safely read JSON file using context manager
    
    Args:
        filepath (str): Path to JSON file
    
    Returns:
        dict: Loaded JSON data or empty dict if error
    """
    try:
        with ManagedFileOperation(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        log_event("ERROR", f"Error reading JSON file: {str(e)}")
        return {}


def safe_write_json(filepath, data):
    """
    Safely write JSON file using context manager
    
    Args:
        filepath (str): Path to JSON file
        data (dict): Data to write
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with ManagedFileOperation(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        log_event("ERROR", f"Error writing JSON file: {str(e)}")
        return False
