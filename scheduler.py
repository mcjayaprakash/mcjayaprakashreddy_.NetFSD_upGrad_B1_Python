"""
SLAScheduler and EscalationManager for IT Service Desk
Handles SLA tracking, monitoring, and ticket escalation
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class SLAScheduler:
    """
    SLA Scheduler for monitoring ticket SLAs and triggering alerts
    """
    
    # SLA response times in hours by priority
    SLA_TIMES = {
        'P1': 1,   # Critical - 1 hour
        'P2': 4,   # High - 4 hours
        'P3': 8,   # Medium - 8 hours
        'P4': 24   # Low - 24 hours
    }
    
    def __init__(self, ticket_manager, check_interval: int = 60):
        """
        Initialize SLA Scheduler
        
        Args:
            ticket_manager: TicketManager instance
            check_interval: Interval in seconds to check SLAs
        """
        self.ticket_manager = ticket_manager
        self.check_interval = check_interval
        self.monitoring_active = False
        self.monitor_thread = None
        self.breached_alerts_sent = 0
        self.escalations_triggered = 0
    
    def start_monitoring(self):
        """Start SLA monitoring in background thread"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop SLA monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                self._check_sla_breaches()
                time.sleep(self.check_interval)
            except Exception:
                pass  # Continue monitoring even if error occurs
    
    def _check_sla_breaches(self):
        """Check for SLA breaches and trigger alerts"""
        tickets = self.ticket_manager.tickets
        current_time = datetime.now()
        
        for ticket in tickets:
            if ticket.get('status') == 'Closed':
                continue
            
            priority = ticket.get('priority', 'P4')
            sla_hours = self.SLA_TIMES.get(priority, 24)
            created = ticket.get('created_at', '')
            
            if created:
                try:
                    created_time = datetime.fromisoformat(created)
                    elapsed = (current_time - created_time).total_seconds() / 3600
                    
                    if elapsed > sla_hours:
                        self.breached_alerts_sent += 1
                except Exception:
                    pass
    
    def get_sla_status(self, ticket_id: str) -> Dict:
        """
        Get SLA status for a specific ticket
        
        Args:
            ticket_id: Ticket ID to check
            
        Returns:
            Dictionary with SLA status information
        """
        ticket = self.ticket_manager.get_ticket_by_id(ticket_id)
        if not ticket:
            return {'error': 'Ticket not found'}
        
        priority = ticket.get('priority', 'P4')
        sla_hours = self.SLA_TIMES.get(priority, 24)
        status = ticket.get('status', 'Open')
        created = ticket.get('created_at', '')
        
        result = {
            'ticket_id': ticket_id,
            'priority': priority,
            'sla_hours': sla_hours,
            'status': status,
            'created_at': created
        }
        
        if created and status != 'Closed':
            try:
                created_time = datetime.fromisoformat(created)
                elapsed = (datetime.now() - created_time).total_seconds() / 3600
                remaining = sla_hours - elapsed
                
                result['elapsed_hours'] = round(elapsed, 2)
                result['remaining_hours'] = round(remaining, 2)
                result['breached'] = remaining < 0
                result['breach_amount'] = round(abs(remaining), 2) if remaining < 0 else 0
            except Exception:
                pass
        
        return result
    
    def get_monitoring_status(self) -> Dict:
        """Get current monitoring status"""
        return {
            'active': self.monitoring_active,
            'check_interval': self.check_interval,
            'breached_alerts_sent': self.breached_alerts_sent,
            'escalations_triggered': self.escalations_triggered
        }
    
    def get_sla_timings(self) -> Dict:
        """Get SLA timing information for all priorities"""
        return self.SLA_TIMES.copy()


class EscalationManager:
    """
    Manages ticket escalation based on SLA breaches
    """
    
    def __init__(self, ticket_manager):
        """
        Initialize Escalation Manager
        
        Args:
            ticket_manager: TicketManager instance
        """
        self.ticket_manager = ticket_manager
        self.escalation_history = []
    
    def check_escalations(self) -> List[Dict]:
        """
        Check for tickets that need escalation
        
        Returns:
            List of tickets that have breached SLA
        """
        escalated = []
        tickets = self.ticket_manager.tickets
        current_time = datetime.now()
        
        for ticket in tickets:
            if ticket.get('status') == 'Closed':
                continue
            
            priority = ticket.get('priority', 'P4')
            sla_hours = SLAScheduler.SLA_TIMES.get(priority, 24)
            created = ticket.get('created_at', '')
            
            if created:
                try:
                    created_time = datetime.fromisoformat(created)
                    elapsed = (current_time - created_time).total_seconds() / 3600
                    
                    if elapsed > sla_hours:
                        escalated.append({
                            'ticket_id': ticket.get('ticket_id'),
                            'priority': priority,
                            'elapsed_hours': round(elapsed, 2),
                            'sla_hours': sla_hours,
                            'breach': round(elapsed - sla_hours, 2)
                        })
                except Exception:
                    pass
        
        return escalated
    
    def escalate_ticket(self, ticket_id: str, reason: str = "") -> bool:
        """
        Manually escalate a ticket
        
        Args:
            ticket_id: Ticket ID to escalate
            reason: Reason for escalation
            
        Returns:
            True if successful, False otherwise
        """
        ticket = self.ticket_manager.get_ticket_by_id(ticket_id)
        if not ticket:
            return False
        
        self.escalation_history.append({
            'ticket_id': ticket_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        
        return True
    
    def get_escalation_history(self) -> List[Dict]:
        """Get escalation history"""
        return self.escalation_history.copy()