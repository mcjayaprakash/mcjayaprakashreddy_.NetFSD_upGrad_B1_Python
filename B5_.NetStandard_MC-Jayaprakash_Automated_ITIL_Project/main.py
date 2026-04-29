"""
Main Application Module for Smart IT Service Desk & System Monitoring Automation
Main entry point with menu system and application orchestration
"""

import sys
import os
from datetime import datetime
from utils import (
    display_banner, display_menu, validate_input, log_event, 
    pause_execution, print_success_message, print_error_message,
    print_warning_message, print_info_message, ensure_data_directory_exists,
    backup_tickets_to_csv, clear_screen, display_ticket_details
)
from tickets import TicketManager, Ticket, ProblemRecord
from monitor import Monitor, SystemHealthAlert
from reports import ReportGenerator
from scheduler import SLAScheduler, EscalationManager


class ITServiceDeskApplication:
    """
    Main application class for IT Service Desk
    Demonstrates: Composition, Error handling, Application orchestration
    """
    
    def __init__(self):
        """Initialize the application"""
        try:
            ensure_data_directory_exists()
            self.ticket_manager = TicketManager()
            self.monitor = Monitor()
            self.health_alert = SystemHealthAlert(self.ticket_manager)
            self.report_generator = ReportGenerator(self.ticket_manager.tickets)
            self.sla_scheduler = SLAScheduler(self.ticket_manager, check_interval=60)
            self.escalation_manager = EscalationManager(self.ticket_manager)
            log_event("INFO", "IT Service Desk Application started")
        except Exception as e:
            log_event("ERROR", f"Error initializing application: {str(e)}")
            print_error_message("Error initializing application. Exiting...")
            sys.exit(1)
    
    def display_main_menu(self):
        """Display main menu"""
        options = [
            "Ticket Management",
            "System Monitoring",
            "SLA Management",
            "Reports & Analytics",
            "Exit Application"
        ]
        display_menu("SMART IT SERVICE DESK MAIN MENU", options)
    
    def ticket_management_menu(self):
        """Ticket management submenu"""
        while True:
            try:
                options = [
                    "Create New Ticket",
                    "View All Tickets",
                    "Search Ticket by ID",
                    "Update Ticket Status",
                    "Close Ticket",
                    "Delete Ticket",
                    "View Ticket Details",
                    "Back to Main Menu"
                ]
                display_menu("TICKET MANAGEMENT", options)
                
                choice = validate_input("Enter your choice (1-8): ")
                
                if choice == '1':
                    self.create_ticket_flow()
                elif choice == '2':
                    self.view_all_tickets_flow()
                elif choice == '3':
                    self.search_ticket_flow()
                elif choice == '4':
                    self.update_ticket_status_flow()
                elif choice == '5':
                    self.close_ticket_flow()
                elif choice == '6':
                    self.delete_ticket_flow()
                elif choice == '7':
                    self.view_ticket_details_flow()
                elif choice == '8':
                    break
                else:
                    print_error_message("Invalid choice. Please try again.")
            
            except Exception as e:
                log_event("ERROR", f"Error in ticket management menu: {str(e)}")
                print_error_message(f"An error occurred: {str(e)}")
            
            pause_execution()
    
    def create_ticket_flow(self):
        """Flow for creating a ticket"""
        try:
            print("\n" + "="*60)
            print("CREATE NEW TICKET".center(60))
            print("="*60)
            
            # Get employee information
            employee_name = validate_input("Enter Employee Name: ")
            if not employee_name:
                print_error_message("Employee name cannot be empty!")
                return
            
            department = validate_input("Enter Department: ")
            if not department:
                print_error_message("Department cannot be empty!")
                return
            
            # Display issue categories
            categories = [
                'Server Down',
                'Internet Down',
                'Laptop Slow',
                'Password Reset',
                'Printer not working',
                'Outlook not opening',
                'Disk space full',
                'High CPU usage on server',
                'Application crash'
            ]
            
            print("\nAvailable Issue Categories:")
            for i, cat in enumerate(categories, 1):
                print(f"  {i}. {cat}")
            
            category_choice = validate_input("Select category (1-9): ")
            try:
                cat_idx = int(category_choice) - 1
                if 0 <= cat_idx < len(categories):
                    category = categories[cat_idx]
                else:
                    print_error_message("Invalid category selection!")
                    return
            except ValueError:
                print_error_message("Invalid input!")
                return
            
            # Get issue description
            issue_description = validate_input("Enter Issue Description: ")
            if not issue_description or issue_description.strip() == "":
                print_error_message("Issue description cannot be empty!")
                log_event("ERROR", "Attempted to create ticket with empty description")
                return
            
            # Create ticket
            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                department=department,
                issue_description=issue_description,
                category=category
            )
            
            if ticket:
                print("\n" + "-"*60)
                display_ticket_details(ticket.to_dict())
        
        except Exception as e:
            log_event("ERROR", f"Error creating ticket: {str(e)}")
            print_error_message(f"Error creating ticket: {str(e)}")
    
    def view_all_tickets_flow(self):
        """Flow for viewing all tickets"""
        try:
            self.ticket_manager.view_all_tickets()
        except Exception as e:
            log_event("ERROR", f"Error viewing tickets: {str(e)}")
            print_error_message(f"Error viewing tickets: {str(e)}")
    
    def search_ticket_flow(self):
        """Flow for searching tickets"""
        try:
            ticket_id = validate_input("Enter Ticket ID to search: ")
            if not ticket_id:
                print_error_message("Ticket ID cannot be empty!")
                return
            
            ticket = self.ticket_manager.get_ticket_by_id(ticket_id)
            if ticket:
                print("\n" + "-"*60)
                display_ticket_details(ticket)
        
        except Exception as e:
            log_event("ERROR", f"Error searching ticket: {str(e)}")
            print_error_message(f"Error searching ticket: {str(e)}")
    
    def update_ticket_status_flow(self):
        """Flow for updating ticket status"""
        try:
            ticket_id = validate_input("Enter Ticket ID: ")
            if not ticket_id:
                print_error_message("Ticket ID cannot be empty!")
                return
            
            ticket = self.ticket_manager.get_ticket_by_id(ticket_id)
            if not ticket:
                return
            
            print("\nAvailable Statuses:")
            statuses = ['Open', 'In Progress', 'Closed']
            for i, status in enumerate(statuses, 1):
                print(f"  {i}. {status}")
            
            status_choice = validate_input("Select new status (1-3): ")
            try:
                status_idx = int(status_choice) - 1
                if 0 <= status_idx < len(statuses):
                    new_status = statuses[status_idx]
                    self.ticket_manager.update_ticket_status(ticket_id, new_status)
                else:
                    print_error_message("Invalid status selection!")
            except ValueError:
                print_error_message("Invalid input!")
        
        except Exception as e:
            log_event("ERROR", f"Error updating ticket: {str(e)}")
            print_error_message(f"Error updating ticket: {str(e)}")
    
    def close_ticket_flow(self):
        """Flow for closing a ticket"""
        try:
            ticket_id = validate_input("Enter Ticket ID to close: ")
            if not ticket_id:
                print_error_message("Ticket ID cannot be empty!")
                return
            
            self.ticket_manager.close_ticket(ticket_id)
        
        except Exception as e:
            log_event("ERROR", f"Error closing ticket: {str(e)}")
            print_error_message(f"Error closing ticket: {str(e)}")
    
    def delete_ticket_flow(self):
        """Flow for deleting a ticket"""
        try:
            ticket_id = validate_input("Enter Ticket ID to delete: ")
            if not ticket_id:
                print_error_message("Ticket ID cannot be empty!")
                return
            
            confirmation = validate_input(f"Are you sure you want to delete ticket {ticket_id}? (yes/no): ")
            if confirmation.lower() == 'yes':
                self.ticket_manager.delete_ticket(ticket_id)
            else:
                print_info_message("Deletion cancelled.")
        
        except Exception as e:
            log_event("ERROR", f"Error deleting ticket: {str(e)}")
            print_error_message(f"Error deleting ticket: {str(e)}")
    
    def view_ticket_details_flow(self):
        """Flow for viewing detailed ticket information"""
        try:
            ticket_id = validate_input("Enter Ticket ID: ")
            if not ticket_id:
                print_error_message("Ticket ID cannot be empty!")
                return
            
            ticket = self.ticket_manager.get_ticket_by_id(ticket_id)
            if ticket:
                print("\n" + "="*60)
                print("DETAILED TICKET INFORMATION".center(60))
                print("="*60)
                display_ticket_details(ticket)
        
        except Exception as e:
            log_event("ERROR", f"Error viewing ticket details: {str(e)}")
            print_error_message(f"Error viewing ticket details: {str(e)}")
    
    def system_monitoring_menu(self):
        """System monitoring submenu"""
        while True:
            try:
                options = [
                    "View System Health Status",
                    "View Monitoring Thresholds",
                    "Configure Thresholds",
                    "Back to Main Menu"
                ]
                display_menu("SYSTEM MONITORING", options)
                
                choice = validate_input("Enter your choice (1-4): ")
                
                if choice == '1':
                    self.monitor.display_system_health()
                elif choice == '2':
                    self.view_thresholds()
                elif choice == '3':
                    self.configure_thresholds()
                elif choice == '4':
                    break
                else:
                    print_error_message("Invalid choice. Please try again.")
            
            except Exception as e:
                log_event("ERROR", f"Error in monitoring menu: {str(e)}")
                print_error_message(f"An error occurred: {str(e)}")
            
            pause_execution()
    
    def check_system_issues(self):
        """Check and display system issues"""
        try:
            issues = self.monitor.check_system_health()
            
            if not issues:
                print_success_message("System is healthy. No issues detected.")
                return
            
            print("\n" + "="*60)
            print("SYSTEM HEALTH ISSUES".center(60))
            print("="*60)
            
            for i, issue in enumerate(issues, 1):
                print(f"\nIssue {i}:")
                print(f"  Type: {issue['type']}")
                print(f"  Current Value: {issue['value']}")
                print(f"  Threshold: {issue['threshold']}")
        
        except Exception as e:
            log_event("ERROR", f"Error checking system issues: {str(e)}")
            print_error_message(f"Error checking system issues: {str(e)}")
    
    def create_alert_tickets(self):
        """Create alert tickets for system issues"""
        try:
            created_tickets = self.health_alert.check_and_create_alert_tickets()
            
            if created_tickets:
                print_success_message(f"Created {len(created_tickets)} alert ticket(s)!")
                for ticket_id in created_tickets:
                    print(f"  - {ticket_id}")
            else:
                print_info_message("No system issues detected. No tickets created.")
        
        except Exception as e:
            log_event("ERROR", f"Error creating alert tickets: {str(e)}")
            print_error_message(f"Error creating alert tickets: {str(e)}")
    
    def view_thresholds(self):
        """View current monitoring thresholds"""
        print("\n" + "="*60)
        print("MONITORING THRESHOLDS".center(60))
        print("="*60)
        print(f"CPU Usage Alert:          > {Monitor.CPU_THRESHOLD}%")
        print(f"RAM Usage Alert:          > {Monitor.RAM_THRESHOLD}%")
        print(f"Disk Space Alert:         < {Monitor.DISK_THRESHOLD}% free")
        print("="*60)
    
    def configure_thresholds(self):
        """Configure monitoring thresholds"""
        try:
            print("\n" + "="*60)
            print("CONFIGURE MONITORING THRESHOLDS".center(60))
            print("="*60)
            
            cpu = validate_input(f"Enter CPU threshold (current: {Monitor.CPU_THRESHOLD}%): ")
            if cpu and cpu.isdigit():
                Monitor.set_cpu_threshold(int(cpu))
                print_success_message("CPU threshold updated!")
            
            ram = validate_input(f"Enter RAM threshold (current: {Monitor.RAM_THRESHOLD}%): ")
            if ram and ram.isdigit():
                Monitor.set_ram_threshold(int(ram))
                print_success_message("RAM threshold updated!")
            
            disk = validate_input(f"Enter Disk threshold (current: {Monitor.DISK_THRESHOLD}%): ")
            if disk and disk.isdigit():
                Monitor.set_disk_threshold(int(disk))
                print_success_message("Disk threshold updated!")
        
        except Exception as e:
            log_event("ERROR", f"Error configuring thresholds: {str(e)}")
            print_error_message(f"Error configuring thresholds: {str(e)}")
    
    def sla_management_menu(self):
        """SLA Management submenu with real-time monitoring"""
        while True:
            try:
                # Show monitoring status
                status = self.sla_scheduler.get_monitoring_status()
                monitoring_indicator = "🟢 ACTIVE" if status['active'] else "🔴 INACTIVE"
                
                options = [
                    "View SLA Status for All Tickets",
                    "View Escalation Alerts",
                    "View SLA Timings",
                    "Escalate Ticket Manually",
                    "Back to Main Menu"
                ]
                display_menu("SLA MANAGEMENT", options)
                
                choice = validate_input("Enter your choice (1-5): ")
                
                if choice == '1':
                    self.view_sla_status()
                elif choice == '2':
                    self.view_escalation_alerts()
                elif choice == '3':
                    self.view_sla_timings()
                elif choice == '4':
                    self.escalate_ticket_manually()
                elif choice == '5':
                    break
                else:
                    print_error_message("Invalid choice. Please try again.")
            
            except Exception as e:
                log_event("ERROR", f"Error in SLA management menu: {str(e)}")
                print_error_message(f"An error occurred: {str(e)}")
            
            pause_execution()
    
    def view_monitoring_status(self):
        """Display real-time monitoring status and statistics"""
        try:
            status = self.sla_scheduler.get_monitoring_status()
            print("\n" + "="*60)
            print("REAL-TIME SLA MONITORING STATUS".center(60))
            print("="*60)
            print(f"Monitoring Active: {'Yes ✓' if status['active'] else 'No ✗'}")
            print(f"Check Interval: {status['check_interval']} seconds")
            print(f"SLA Breach Alerts Sent: {status['breached_alerts_sent']}")
            print(f"Escalations Triggered: {status['escalations_triggered']}")
            print("="*60)
        except Exception as e:
            log_event("ERROR", f"Error viewing monitoring status: {str(e)}")
            print_error_message(f"Error: {str(e)}")
    
    def escalate_ticket_manually(self):
        """Manually escalate a ticket"""
        try:
            print("\n" + "="*60)
            print("MANUAL TICKET ESCALATION".center(60))
            print("="*60)
            
            ticket_id = validate_input("Enter Ticket ID to escalate: ")
            
            if ticket_id not in self.ticket_manager.tickets:
                print_error_message(f"Ticket {ticket_id} not found!")
                return
            
            reason = input("Enter escalation reason (optional): ")
            
            if self.escalation_manager.escalate_ticket(ticket_id, reason):
                print_success_message(f"Ticket {ticket_id} has been escalated!")
                escalation_level = self.escalation_manager.get_escalation_level(ticket_id)
                print(f"Current Escalation Level: {escalation_level}")
            else:
                print_error_message("Failed to escalate ticket!")
                
        except Exception as e:
            log_event("ERROR", f"Error escalating ticket: {str(e)}")
            print_error_message(f"Error: {str(e)}")
    
    def view_sla_status(self):
        """View SLA status for all tickets"""
        try:
            sla_status = self.ticket_manager.check_sla_status()
            
            print("\n" + "="*60)
            print("SLA STATUS REPORT".center(60))
            print("="*60)
            
            breached = sla_status.get('sla_breached', [])
            escalations = sla_status.get('escalation_alerts', [])
            
            print(f"\nSLA Breached Tickets ({len(breached)}):")
            if breached:
                for ticket_id in breached:
                    print(f"  ⚠️  {ticket_id}")
            else:
                print("  ✅ None")
            
            print(f"\nEscalation Alerts ({len(escalations)}):")
            if escalations:
                for ticket_id in escalations:
                    print(f"  ⚠️  {ticket_id}")
            else:
                print("  ✅ None")
            
            print("\n" + "="*60)
        
        except Exception as e:
            log_event("ERROR", f"Error viewing SLA status: {str(e)}")
            print_error_message(f"Error viewing SLA status: {str(e)}")
    
    def view_sla_compliance(self):
        """View SLA compliance metrics"""
        try:
            metrics = ReportGenerator.get_sla_compliance_metrics(self.ticket_manager.tickets)
            
            print("\n" + "="*60)
            print("SLA COMPLIANCE METRICS".center(60))
            print("="*60)
            print(f"Total Closed Tickets{'':<20} {metrics.get('total_closed_tickets', 0)}")
            print(f"SLA Compliant{'':<28} {metrics.get('sla_compliant_tickets', 0)}")
            print(f"SLA Breached{'':<29} {metrics.get('sla_breached_tickets', 0)}")
            print(f"Compliance Rate{'':<25} {metrics.get('compliance_rate', '0%')}")
            print("="*60)
        
        except Exception as e:
            log_event("ERROR", f"Error viewing SLA compliance: {str(e)}")
            print_error_message(f"Error viewing SLA compliance: {str(e)}")
    
    def view_escalation_alerts(self):
        """View escalation alerts"""
        try:
            sla_status = self.ticket_manager.check_sla_status()
            escalations = sla_status.get('escalation_alerts', [])
            
            print("\n" + "="*60)
            print("ESCALATION ALERTS".center(60))
            print("="*60)
            
            if not escalations:
                print_success_message("No escalation alerts at this time.")
                return
            
            print(f"\nTotal Escalation Alerts: {len(escalations)}\n")
            
            for ticket_id in escalations:
                ticket = self.ticket_manager.get_ticket_by_id(ticket_id)
                if ticket:
                    print(f"🔴 {ticket_id}")
                    print(f"   Category: {ticket['category']}")
                    print(f"   Priority: {ticket['priority']}")
                    print(f"   Status: {ticket['status']}")
                    print(f"   Created: {ticket['created_date']}\n")
        
        except Exception as e:
            log_event("ERROR", f"Error viewing escalation alerts: {str(e)}")
            print_error_message(f"Error viewing escalation alerts: {str(e)}")
    
    def view_sla_timings(self):
        """View SLA timings"""
        print("\n" + "="*60)
        print("SLA TIMINGS".center(60))
        print("="*60)
        print(f"Priority P1 (Server Down){'':<21} 1 Hour")
        print(f"Priority P2 (Internet Down){'':<19} 4 Hours")
        print(f"Priority P3 (Laptop/Printer){'':<18} 8 Hours")
        print(f"Priority P4 (Password Reset){'':<18} 24 Hours")
        print("\nEscalation Timings:")
        print(f"Priority P1{'':<45} 30 Minutes")
        print(f"Priority P2{'':<45} 2 Hours")
        print("="*60)
    
    def reports_analytics_menu(self):
        """Reports and analytics submenu"""
        while True:
            try:
                options = [
                    "View Daily Summary Report",
                    "View Monthly Trend Report",
                    "Save Daily Report to File",
                    "Save Monthly Report to File",
                    "Backup Tickets to CSV",
                    "Back to Main Menu"
                ]
                display_menu("REPORTS & ANALYTICS", options)
                
                choice = validate_input("Enter your choice (1-6): ")
                
                if choice == '1':
                    self.report_generator.display_daily_summary()
                elif choice == '2':
                    self.report_generator.display_monthly_trend()
                elif choice == '3':
                    self.report_generator.save_daily_report_to_file()
                elif choice == '4':
                    self.report_generator.save_monthly_report_to_file()
                elif choice == '5':
                    self.backup_tickets()
                elif choice == '6':
                    break
                else:
                    print_error_message("Invalid choice. Please try again.")
            
            except Exception as e:
                log_event("ERROR", f"Error in reports menu: {str(e)}")
                print_error_message(f"An error occurred: {str(e)}")
            
            pause_execution()
    
    def view_ticket_statistics(self):
        """View ticket statistics"""
        try:
            stats = self.ticket_manager.get_statistics()
            
            print("\n" + "="*70)
            print("TICKET STATISTICS OVERVIEW".center(70))
            print("="*70)
            
            print(f"\n{'OVERALL STATISTICS':.<40} {'':<20}")
            print(f"  Total Tickets{'':<26} {stats.get('total', 0)}")
            print(f"  Open Tickets{'':<27} {stats.get('open', 0)}")
            print(f"  In Progress{'':<28} {stats.get('in_progress', 0)}")
            print(f"  Closed Tickets{'':<26} {stats.get('closed', 0)}")
            print(f"  SLA Breached{'':<27} {stats.get('sla_breached', 0)}")
            
            print(f"\n{'PRIORITY BREAKDOWN':.<40} {'':<20}")
            priorities = stats.get('by_priority', {})
            for priority in ['P1', 'P2', 'P3', 'P4']:
                count = priorities.get(priority, 0)
                print(f"  {priority}{'':<35} {count}")
            
            print(f"\n{'TOP 5 DEPARTMENTS':.<40} {'':<20}")
            depts = sorted(stats.get('by_department', {}).items(), key=lambda x: x[1], reverse=True)[:5]
            for dept, count in depts:
                print(f"  {dept[:30]:<30} {count}")
            
            print(f"\n{'TOP 5 CATEGORIES':.<40} {'':<20}")
            cats = sorted(stats.get('by_category', {}).items(), key=lambda x: x[1], reverse=True)[:5]
            for cat, count in cats:
                print(f"  {cat[:30]:<30} {count}")
            
            print("\n" + "="*70)
        
        except Exception as e:
            log_event("ERROR", f"Error viewing statistics: {str(e)}")
            print_error_message(f"Error viewing statistics: {str(e)}")
    
    def backup_tickets(self):
        """Backup tickets to CSV"""
        try:
            if backup_tickets_to_csv(self.ticket_manager.tickets):
                print_success_message("Tickets backed up successfully!")
            else:
                print_error_message("Failed to backup tickets!")
        except Exception as e:
            log_event("ERROR", f"Error backing up tickets: {str(e)}")
            print_error_message(f"Error backing up tickets: {str(e)}")
    
    def system_configuration_menu(self):
        """System configuration submenu"""
        while True:
            try:
                options = [
                    "View Total Tickets Created",
                    "View Application Logs",
                    "Clear Old Logs",
                    "Back to Main Menu"
                ]
                display_menu("SYSTEM CONFIGURATION", options)
                
                choice = validate_input("Enter your choice (1-4): ")
                
                if choice == '1':
                    self.view_total_tickets()
                elif choice == '2':
                    self.view_logs()
                elif choice == '3':
                    self.clear_logs()
                elif choice == '4':
                    break
                else:
                    print_error_message("Invalid choice. Please try again.")
            
            except Exception as e:
                log_event("ERROR", f"Error in configuration menu: {str(e)}")
                print_error_message(f"An error occurred: {str(e)}")
            
            pause_execution()
    
    def view_total_tickets(self):
        """View total tickets created"""
        total = Ticket.get_total_tickets()
        print(f"\n✅ Total Tickets Created in This Session: {total}")
    
    def view_logs(self):
        """View application logs"""
        try:
            from utils import LOGS_FILE
            
            if not os.path.exists(LOGS_FILE):
                print_error_message("No logs found!")
                return
            
            with open(LOGS_FILE, 'r', encoding='utf-8') as f:
                logs = f.readlines()
            
            print("\n" + "="*80)
            print("APPLICATION LOGS (Last 20 entries)".center(80))
            print("="*80)
            
            for line in logs[-20:]:
                print(line.rstrip())
            
            print("="*80)
        
        except Exception as e:
            log_event("ERROR", f"Error viewing logs: {str(e)}")
            print_error_message(f"Error viewing logs: {str(e)}")
    
    def clear_logs(self):
        """Clear old logs"""
        try:
            from utils import LOGS_FILE
            
            confirmation = validate_input("Are you sure you want to clear all logs? (yes/no): ")
            if confirmation.lower() == 'yes':
                with open(LOGS_FILE, 'w', encoding='utf-8') as f:
                    f.write("")
                print_success_message("Logs cleared successfully!")
                log_event("WARNING", "Application logs cleared by user")
            else:
                print_info_message("Operation cancelled.")
        
        except Exception as e:
            log_event("ERROR", f"Error clearing logs: {str(e)}")
            print_error_message(f"Error clearing logs: {str(e)}")
    
    def help_and_about(self):
        """Display help and about information"""
        help_text = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    SMART IT SERVICE DESK HELP & ABOUT                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📋 FEATURES:

1. TICKET MANAGEMENT
   • Create, view, search, update, and delete support tickets
   • Automatic priority assignment based on issue type
   • Ticket classification (Incident, Service Request, Problem Record)
   • Real-time ticket status tracking

2. SLA MANAGEMENT
   • Automatic SLA tracking for all ticket priorities (P1-P4)
   • Escalation alerts for critical tickets
   • SLA breach detection and reporting
   • Compliance metrics

3. SYSTEM MONITORING
   • Real-time CPU, RAM, and Disk usage monitoring
   • Automatic high-priority ticket generation for system issues
   • Top process visualization
   • Configurable monitoring thresholds

4. ITIL COMPLIANCE
   • Incident Management for unplanned interruptions
   • Service Request Management for fulfillment requests
   • Problem Management with root cause analysis
   • Automatic problem record creation (5+ occurrences)

5. REPORTING & ANALYTICS
   • Daily Summary Reports with key metrics
   • Monthly Trend Reports with historical analysis
   • Department and category-wise breakdowns
   • SLA compliance metrics

6. DATA PERSISTENCE
   • All tickets stored in tickets.json
   • Automatic backups to backup.csv
   • Comprehensive application logging
   • Persistent session recovery

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PRIORITY LEVELS:

Priority | Issue Type              | SLA Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   P1    | Server Down             | 1 Hour
   P2    | Internet Down           | 4 Hours
   P3    | Laptop Slow, Printer    | 8 Hours
   P4    | Password Reset          | 24 Hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SYSTEM MONITORING THRESHOLDS:

Metric        | Alert Threshold
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CPU Usage     | > 90%
RAM Usage     | > 95%
Disk Space    | < 10% free

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 DATA STORAGE:

• Tickets: data/tickets.json
• Backups: data/backup.csv
• Logs: data/logs.txt
• Reports: data/reports/ (auto-generated)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 ABOUT:

Application: Smart IT Service Desk & System Monitoring Automation
Company: TechNova Solutions
Version: 1.0.0
Purpose: Automated IT support ticket management and system health monitoring
Technology: Python with OOP principles and ITIL best practices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ For support or feedback, contact the IT Department.

"""
        print(help_text)
        pause_execution()
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                clear_screen()
                display_banner()
                self.display_main_menu()
                
                choice = validate_input("Enter your choice (1-5): ")
                
                if choice == '1':
                    self.ticket_management_menu()
                elif choice == '2':
                    self.system_monitoring_menu()
                elif choice == '3':
                    self.sla_management_menu()
                elif choice == '4':
                    self.reports_analytics_menu()
                elif choice == '5':
                    self.exit_application()
                else:
                    print_error_message("Invalid choice. Please try again.")
                    pause_execution()
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted by user.")
            self.exit_application()
        except Exception as e:
            log_event("ERROR", f"Unexpected error in main application: {str(e)}")
            print_error_message(f"An unexpected error occurred: {str(e)}")
            sys.exit(1)
    
    def exit_application(self):
        """Exit the application gracefully"""
        try:
            print("\n" + "="*60)
            print("EXITING APPLICATION".center(60))
            print("="*60)
            
            # Final backup
            backup_tickets_to_csv(self.ticket_manager.tickets)
            
            log_event("INFO", "Application shut down normally")
            print_success_message("Thank you for using Smart IT Service Desk!")
            print("All data has been saved. Goodbye!")
            
            sys.exit(0)
        
        except Exception as e:
            log_event("ERROR", f"Error during shutdown: {str(e)}")
            print_error_message(f"Error during shutdown: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point"""
    try:
        app = ITServiceDeskApplication()
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
