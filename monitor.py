"""
System Monitoring Module for Smart IT Service Desk
Monitors CPU, RAM, and Disk usage with automatic ticket generation for breaches
"""

import psutil
from datetime import datetime
from utils import log_event, print_error_message, print_success_message, print_warning_message


class Monitor:
    """
    System monitoring class
    Demonstrates: Encapsulation, Static methods, Class methods
    """
    
    # System health thresholds
    CPU_THRESHOLD = 90      # Percentage
    RAM_THRESHOLD = 95      # Percentage
    DISK_THRESHOLD = 10     # Free space percentage
    
    # Track alerts to avoid duplicate tickets
    _last_alert_time = {}
    _alert_cooldown = 3600  # 1 hour cooldown between same type alerts
    
    def __init__(self):
        """Initialize monitor"""
        self.cpu_usage = 0
        self.ram_usage = 0
        self.disk_usage = 0
        self.disk_free = 0
        log_event("INFO", "System Monitor initialized")
    
    def get_cpu_usage(self):
        """
        Get current CPU usage percentage
        
        Returns:
            float: CPU usage percentage (0-100)
        """
        try:
            cpu = psutil.cpu_percent(interval=1)
            self.cpu_usage = cpu
            return cpu
        except Exception as e:
            log_event("ERROR", f"Error getting CPU usage: {str(e)}")
            return 0
    
    def get_ram_usage(self):
        """
        Get current RAM usage percentage
        
        Returns:
            float: RAM usage percentage (0-100)
        """
        try:
            ram = psutil.virtual_memory().percent
            self.ram_usage = ram
            return ram
        except Exception as e:
            log_event("ERROR", f"Error getting RAM usage: {str(e)}")
            return 0
    
    def get_disk_usage(self):
        """
        Get current disk usage information
        
        Returns:
            tuple: (disk_usage_percent, free_percent, total, used, free)
        """
        try:
            disk = psutil.disk_usage('/')
            self.disk_usage = disk.percent
            free_percent = 100 - disk.percent
            self.disk_free = free_percent
            
            return {
                'usage_percent': disk.percent,
                'free_percent': free_percent,
                'total': disk.total,
                'used': disk.used,
                'free': disk.free
            }
        except Exception as e:
            log_event("ERROR", f"Error getting disk usage: {str(e)}")
            return {
                'usage_percent': 0,
                'free_percent': 100,
                'total': 0,
                'used': 0,
                'free': 0
            }
    
    def get_system_health_summary(self):
        """
        Get complete system health summary
        
        Returns:
            dict: System health information
        """
        try:
            cpu = self.get_cpu_usage()
            ram = self.get_ram_usage()
            disk = self.get_disk_usage()
            
            return {
                'cpu_usage': cpu,
                'ram_usage': ram,
                'disk_usage': disk['usage_percent'],
                'disk_free': disk['free_percent'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'health_status': self._determine_health_status(cpu, ram, disk['free_percent'])
            }
        except Exception as e:
            log_event("ERROR", f"Error getting system health summary: {str(e)}")
            return {}
    
    def _determine_health_status(self, cpu, ram, disk_free):
        """
        Determine overall system health status
        
        Args:
            cpu (float): CPU usage percentage
            ram (float): RAM usage percentage
            disk_free (float): Free disk percentage
        
        Returns:
            str: Health status (Healthy, Warning, Critical)
        """
        critical_count = 0
        
        if cpu > self.CPU_THRESHOLD:
            critical_count += 1
        if ram > self.RAM_THRESHOLD:
            critical_count += 1
        if disk_free < self.DISK_THRESHOLD:
            critical_count += 1
        
        if critical_count >= 2:
            return "Critical"
        elif critical_count == 1:
            return "Warning"
        else:
            return "Healthy"
    
    def check_system_health(self):
        """
        Check system health and identify issues
        
        Returns:
            list: List of issues detected
        """
        issues = []
        
        try:
            cpu = self.get_cpu_usage()
            ram = self.get_ram_usage()
            disk = self.get_disk_usage()
            
            if cpu > self.CPU_THRESHOLD:
                issues.append({
                    'type': 'High CPU usage on server',
                    'value': f"{cpu}%",
                    'threshold': f"{self.CPU_THRESHOLD}%"
                })
                log_event("WARNING", f"High CPU usage detected: {cpu}%")
            
            if ram > self.RAM_THRESHOLD:
                issues.append({
                    'type': 'RAM usage critical',
                    'value': f"{ram}%",
                    'threshold': f"{self.RAM_THRESHOLD}%"
                })
                log_event("WARNING", f"High RAM usage detected: {ram}%")
            
            if disk['free_percent'] < self.DISK_THRESHOLD:
                issues.append({
                    'type': 'Disk space full',
                    'value': f"{disk['free_percent']}% free",
                    'threshold': f"< {self.DISK_THRESHOLD}% free"
                })
                log_event("WARNING", f"Low disk space detected: {disk['free_percent']}% free")
            
            return issues
        
        except Exception as e:
            log_event("ERROR", f"Error checking system health: {str(e)}")
            return []
    
    def display_system_health(self):
        """
        Display formatted system health information
        """
        try:
            health = self.get_system_health_summary()
            
            if not health:
                print_error_message("Unable to retrieve system health")
                return
            
            print("\n" + "="*60)
            print("SYSTEM HEALTH STATUS".center(60))
            print("="*60)
            
            # CPU Usage
            cpu = health['cpu_usage']
            cpu_status = "🔴 CRITICAL" if cpu > self.CPU_THRESHOLD else "🟡 WARNING" if cpu > 80 else "🟢 OK"
            print(f"CPU Usage:        {cpu:>6.2f}%    [{cpu_status}]")
            
            # RAM Usage
            ram = health['ram_usage']
            ram_status = "🔴 CRITICAL" if ram > self.RAM_THRESHOLD else "🟡 WARNING" if ram > 80 else "🟢 OK"
            print(f"RAM Usage:        {ram:>6.2f}%    [{ram_status}]")
            
            # Disk Usage
            disk_free = health['disk_free']
            disk_status = "🔴 CRITICAL" if disk_free < self.DISK_THRESHOLD else "🟡 WARNING" if disk_free < 20 else "🟢 OK"
            print(f"Disk Free:        {disk_free:>6.2f}%    [{disk_status}]")
            
            # Overall Status
            overall_status = health['health_status']
            overall_emoji = "🔴" if overall_status == "Critical" else "🟡" if overall_status == "Warning" else "🟢"
            print(f"\nOverall Status:   {overall_emoji} {overall_status}")
            print(f"Timestamp:        {health['timestamp']}")
            
            print("="*60)
        
        except Exception as e:
            log_event("ERROR", f"Error displaying system health: {str(e)}")
            print_error_message("Error displaying system health")
    
    @staticmethod
    def get_process_list(top_n=5):
        """
        Get top N processes by CPU usage
        
        Args:
            top_n (int): Number of top processes to return
        
        Returns:
            list: List of process information
        """
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    if pinfo['cpu_percent'] is not None:
                        processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and get top N
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:top_n]
        
        except Exception as e:
            log_event("ERROR", f"Error getting process list: {str(e)}")
            return []
    
    @staticmethod
    def display_top_processes(top_n=5):
        """
        Display top N processes by CPU usage
        
        Args:
            top_n (int): Number of top processes to display
        """
        try:
            processes = Monitor.get_process_list(top_n)
            
            if not processes:
                print_error_message("Unable to retrieve process list")
                return
            
            print("\n" + "="*80)
            print("TOP PROCESSES BY CPU USAGE".center(80))
            print("="*80)
            print(f"{'PID':<10} {'Process Name':<30} {'CPU %':<15} {'Memory %':<15}")
            print("-"*80)
            
            for proc in processes:
                print(f"{proc['pid']:<10} {proc['name'][:29]:<30} "
                      f"{proc['cpu_percent']:<15.2f} {proc['memory_percent']:<15.2f}")
            
            print("="*80)
        
        except Exception as e:
            log_event("ERROR", f"Error displaying processes: {str(e)}")
            print_error_message("Error displaying process information")
    
    @classmethod
    def set_cpu_threshold(cls, threshold):
        """Set CPU threshold"""
        cls.CPU_THRESHOLD = threshold
        log_event("INFO", f"CPU threshold set to {threshold}%")
    
    @classmethod
    def set_ram_threshold(cls, threshold):
        """Set RAM threshold"""
        cls.RAM_THRESHOLD = threshold
        log_event("INFO", f"RAM threshold set to {threshold}%")
    
    @classmethod
    def set_disk_threshold(cls, threshold):
        """Set disk threshold"""
        cls.DISK_THRESHOLD = threshold
        log_event("INFO", f"Disk threshold set to {threshold}%")
    
    def __str__(self):
        """String representation"""
        return f"Monitor(CPU:{self.cpu_usage:.1f}%, RAM:{self.ram_usage:.1f}%, Disk:{self.disk_usage:.1f}%)"


class SystemHealthAlert:
    """
    Manages system health alerts and automatic ticket generation
    """
    
    def __init__(self, ticket_manager=None):
        """
        Initialize alert manager
        
        Args:
            ticket_manager: TicketManager instance for creating tickets
        """
        self.monitor = Monitor()
        self.ticket_manager = ticket_manager
        self.active_alerts = {}
    
    def check_and_create_alert_tickets(self):
        """
        Check system health and create tickets for issues
        
        Returns:
            list: List of created ticket IDs
        """
        try:
            issues = self.monitor.check_system_health()
            created_tickets = []
            
            for issue in issues:
                ticket = self._create_alert_ticket(issue)
                if ticket:
                    created_tickets.append(ticket.ticket_id)
            
            return created_tickets
        
        except Exception as e:
            log_event("ERROR", f"Error checking and creating alert tickets: {str(e)}")
            return []
    
    def _create_alert_ticket(self, issue):
        """
        Create a high-priority ticket for a system issue
        
        Args:
            issue (dict): Issue information
        
        Returns:
            Ticket: Created ticket or None if failed
        """
        try:
            if not self.ticket_manager:
                log_event("ERROR", "Ticket manager not available for alert creation")
                return None
            
            # Create high-priority alert ticket
            issue_type = issue['type']
            ticket = self.ticket_manager.create_ticket(
                employee_name="System Administrator",
                department="IT Infrastructure",
                issue_description=f"{issue_type}\nValue: {issue['value']}\nThreshold: {issue['threshold']}",
                category=issue_type
            )
            
            if ticket:
                log_event("WARNING", f"Alert ticket created for: {issue_type}")
                print_warning_message(f"High-priority alert: {issue_type}")
            
            return ticket
        
        except Exception as e:
            log_event("ERROR", f"Error creating alert ticket: {str(e)}")
            return None
    
    def get_alert_summary(self):
        """
        Get summary of active alerts
        
        Returns:
            dict: Alert summary
        """
        health = self.monitor.get_system_health_summary()
        issues = self.monitor.check_system_health()
        
        return {
            'system_health': health,
            'issues': issues,
            'issue_count': len(issues),
            'status': health.get('health_status', 'Unknown')
        }
