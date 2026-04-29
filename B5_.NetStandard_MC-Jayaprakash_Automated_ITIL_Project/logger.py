"""
Logger module for IT Service Desk application.
Provides logging functionality for ticket operations and system events.
"""

import logging
import os
from datetime import datetime


def setup_logger(name: str = "it_service_desk", log_file: str = "data/logs.txt") -> logging.Logger:
    """
    Set up and configure a logger for the application.
    
    Args:
        name: Logger name
        log_file: Path to the log file
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_ticket_event(logger: logging.Logger, event_type: str, ticket_id: str, details: str = ""):
    """
    Log a ticket-related event.
    
    Args:
        logger: Logger instance
        event_type: Type of event (created, updated, resolved, closed)
        ticket_id: ID of the ticket
        details: Additional details about the event
    """
    message = f"Ticket {ticket_id} - {event_type}"
    if details:
        message += f": {details}"
    logger.info(message)


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log an error with context.
    
    Args:
        logger: Logger instance
        error: The exception that occurred
        context: Context information about where the error occurred
    """
    message = f"Error"
    if context:
        message += f" in {context}"
    message += f": {str(error)}"
    logger.error(message)


# Default logger instance
default_logger = setup_logger()