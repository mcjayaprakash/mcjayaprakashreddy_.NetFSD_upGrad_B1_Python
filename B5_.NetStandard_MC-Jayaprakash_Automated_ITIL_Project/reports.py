"""
Reports Module for Smart IT Service Desk
Generates daily and monthly reports with statistics and trends
"""

from datetime import datetime, timedelta
from utils import log_event, print_error_message, print_success_message
import json
import os


class ReportGenerator:
    """
    Generates various reports from ticket data
    Demonstrates: Encapsulation, Static methods
    """
    
    def __init__(self, tickets):
        """
        Initialize report generator
        
        Args:
            tickets (dict): Dictionary of all tickets
        """
        self.tickets = tickets
        self.report_dir = os.path.join(os.path.dirname(__file__), 'data', 'reports')
        self._ensure_report_dir()
    
    def _ensure_report_dir(self):
        """Ensure reports directory exists"""
        try:
            if not os.path.exists(self.report_dir):
                os.makedirs(self.report_dir)
        except Exception as e:
            log_event("ERROR", f"Error creating reports directory: {str(e)}")
    
    def generate_daily_summary_report(self):
        """
        Generate daily summary report
        
        Returns:
            dict: Daily summary report with all metrics
        """
        try:
            report = {
                'report_type': 'Daily Summary',
                'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'date': datetime.now().strftime("%Y-%m-%d"),
                'metrics': {}
            }
            
            # Calculate metrics
            total_tickets = len(self.tickets)
            open_tickets = sum(1 for t in self.tickets.values() if t['status'] == 'Open')
            in_progress = sum(1 for t in self.tickets.values() if t['status'] == 'In Progress')
            closed_tickets = sum(1 for t in self.tickets.values() if t['status'] == 'Closed')
            
            high_priority = sum(1 for t in self.tickets.values() if t['priority'] in ['P1', 'P2'])
            sla_breached = sum(1 for t in self.tickets.values() if t.get('sla_breached', False))
            
            # Count by priority
            priority_breakdown = {
                'P1': sum(1 for t in self.tickets.values() if t['priority'] == 'P1'),
                'P2': sum(1 for t in self.tickets.values() if t['priority'] == 'P2'),
                'P3': sum(1 for t in self.tickets.values() if t['priority'] == 'P3'),
                'P4': sum(1 for t in self.tickets.values() if t['priority'] == 'P4')
            }
            
            # Count by department
            department_breakdown = {}
            for ticket in self.tickets.values():
                dept = ticket.get('department', 'Unknown')
                department_breakdown[dept] = department_breakdown.get(dept, 0) + 1
            
            # Count by category
            category_breakdown = {}
            for ticket in self.tickets.values():
                cat = ticket.get('category', 'Unknown')
                category_breakdown[cat] = category_breakdown.get(cat, 0) + 1
            
            report['metrics'] = {
                'total_tickets': total_tickets,
                'open_tickets': open_tickets,
                'in_progress_tickets': in_progress,
                'closed_tickets': closed_tickets,
                'high_priority_tickets': high_priority,
                'sla_breached_tickets': sla_breached,
                'priority_breakdown': priority_breakdown,
                'department_breakdown': department_breakdown,
                'category_breakdown': category_breakdown,
                'resolution_rate': f"{(closed_tickets / total_tickets * 100):.2f}%" if total_tickets > 0 else "0%"
            }
            
            log_event("SUCCESS", "Daily summary report generated")
            return report
        
        except Exception as e:
            log_event("ERROR", f"Error generating daily report: {str(e)}")
            return {}
    
    def generate_monthly_trend_report(self):
        """
        Generate monthly trend report
        
        Returns:
            dict: Monthly trend report with trends and analysis
        """
        try:
            report = {
                'report_type': 'Monthly Trend',
                'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'month': datetime.now().strftime("%B %Y"),
                'trends': {}
            }
            
            # Get tickets from last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_tickets = {}
            
            for ticket_id, ticket in self.tickets.items():
                try:
                    created = datetime.strptime(ticket['created_date'], "%Y-%m-%d %H:%M:%S")
                    if created >= thirty_days_ago:
                        recent_tickets[ticket_id] = ticket
                except:
                    pass
            
            # Most common issue (category)
            category_count = {}
            for ticket in recent_tickets.values():
                cat = ticket.get('category', 'Unknown')
                category_count[cat] = category_count.get(cat, 0) + 1
            
            most_common_issue = max(category_count.items(), key=lambda x: x[1]) if category_count else ('N/A', 0)
            
            # Average resolution time
            closed_tickets = [t for t in recent_tickets.values() if t['status'] == 'Closed' and t.get('closed_date')]
            avg_resolution_hours = 0
            
            if closed_tickets:
                total_resolution_hours = 0
                for ticket in closed_tickets:
                    try:
                        created = datetime.strptime(ticket['created_date'], "%Y-%m-%d %H:%M:%S")
                        closed = datetime.strptime(ticket['closed_date'], "%Y-%m-%d %H:%M:%S")
                        hours = (closed - created).total_seconds() / 3600
                        total_resolution_hours += hours
                    except:
                        pass
                
                avg_resolution_hours = total_resolution_hours / len(closed_tickets) if closed_tickets else 0
            
            # Department with most incidents
            dept_count = {}
            for ticket in recent_tickets.values():
                dept = ticket.get('department', 'Unknown')
                dept_count[dept] = dept_count.get(dept, 0) + 1
            
            dept_with_most = max(dept_count.items(), key=lambda x: x[1]) if dept_count else ('N/A', 0)
            
            # Trend analysis - ticket volume by week
            weekly_count = {}
            for ticket in recent_tickets.values():
                try:
                    created = datetime.strptime(ticket['created_date'], "%Y-%m-%d %H:%M:%S")
                    week_num = created.isocalendar()[1]
                    year = created.year
                    week_key = f"{year}-W{week_num:02d}"
                    weekly_count[week_key] = weekly_count.get(week_key, 0) + 1
                except:
                    pass
            
            # Priority trend
            priority_trend = {}
            for ticket in recent_tickets.values():
                priority = ticket.get('priority', 'Unknown')
                priority_trend[priority] = priority_trend.get(priority, 0) + 1
            
            report['trends'] = {
                'total_tickets_30days': len(recent_tickets),
                'most_common_issue': {
                    'category': most_common_issue[0],
                    'count': most_common_issue[1]
                },
                'average_resolution_hours': round(avg_resolution_hours, 2),
                'department_with_most_incidents': {
                    'department': dept_with_most[0],
                    'incident_count': dept_with_most[1]
                },
                'weekly_ticket_volume': weekly_count,
                'priority_distribution': priority_trend,
                'category_distribution': category_count,
                'department_distribution': dept_count
            }
            
            log_event("SUCCESS", "Monthly trend report generated")
            return report
        
        except Exception as e:
            log_event("ERROR", f"Error generating monthly report: {str(e)}")
            return {}
    
    def display_daily_summary(self):
        """Display formatted daily summary report"""
        try:
            report = self.generate_daily_summary_report()
            
            if not report:
                print_error_message("Unable to generate daily report")
                return
            
            metrics = report.get('metrics', {})
            
            print("\n" + "="*70)
            print("DAILY SUMMARY REPORT".center(70))
            print(f"Date: {report.get('date')}".center(70))
            print("="*70)
            
            print(f"\n{'TICKET SUMMARY':.<40} {'':<20}")
            print(f"  Total Tickets{'':<24} {metrics.get('total_tickets', 0)}")
            print(f"  Open Tickets{'':<25} {metrics.get('open_tickets', 0)}")
            print(f"  In Progress{'':<26} {metrics.get('in_progress_tickets', 0)}")
            print(f"  Closed Tickets{'':<24} {metrics.get('closed_tickets', 0)}")
            print(f"  Resolution Rate{'':<23} {metrics.get('resolution_rate', '0%')}")
            
            print(f"\n{'PRIORITY BREAKDOWN':.<40} {'':<20}")
            priority_breakdown = metrics.get('priority_breakdown', {})
            for priority in ['P1', 'P2', 'P3', 'P4']:
                count = priority_breakdown.get(priority, 0)
                print(f"  {priority}{'':<32} {count}")
            
            print(f"\n{'CRITICAL METRICS':.<40} {'':<20}")
            print(f"  High Priority Tickets (P1+P2){'':<8} {metrics.get('high_priority_tickets', 0)}")
            print(f"  SLA Breached Tickets{'':<18} {metrics.get('sla_breached_tickets', 0)}")
            
            print(f"\n{'TOP DEPARTMENTS':.<40} {'':<20}")
            dept_breakdown = metrics.get('department_breakdown', {})
            for dept, count in sorted(dept_breakdown.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {dept[:30]:<30} {count}")
            
            print(f"\n{'TOP CATEGORIES':.<40} {'':<20}")
            cat_breakdown = metrics.get('category_breakdown', {})
            for cat, count in sorted(cat_breakdown.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {cat[:30]:<30} {count}")
            
            print("\n" + "="*70)
        
        except Exception as e:
            log_event("ERROR", f"Error displaying daily summary: {str(e)}")
            print_error_message("Error displaying daily summary")
    
    def display_monthly_trend(self):
        """Display formatted monthly trend report"""
        try:
            report = self.generate_monthly_trend_report()
            
            if not report:
                print_error_message("Unable to generate monthly report")
                return
            
            trends = report.get('trends', {})
            
            print("\n" + "="*70)
            print("MONTHLY TREND REPORT".center(70))
            print(f"Month: {report.get('month')}".center(70))
            print("="*70)
            
            print(f"\n{'OVERVIEW':.<40} {'':<20}")
            print(f"  Total Tickets (Last 30 days){'':<10} {trends.get('total_tickets_30days', 0)}")
            
            most_common = trends.get('most_common_issue', {})
            print(f"\n{'MOST COMMON ISSUE':.<40} {'':<20}")
            print(f"  Category{'':<31} {most_common.get('category', 'N/A')}")
            print(f"  Occurrences{'':<28} {most_common.get('count', 0)}")
            
            print(f"\n{'RESOLUTION METRICS':.<40} {'':<20}")
            avg_hours = trends.get('average_resolution_hours', 0)
            print(f"  Avg Resolution Time (Hours){'':<11} {avg_hours:.2f}")
            
            dept_most = trends.get('department_with_most_incidents', {})
            print(f"\n{'DEPARTMENT WITH MOST INCIDENTS':.<40} {'':<20}")
            print(f"  Department{'':<28} {dept_most.get('department', 'N/A')}")
            print(f"  Incident Count{'':<24} {dept_most.get('incident_count', 0)}")
            
            print(f"\n{'PRIORITY DISTRIBUTION':.<40} {'':<20}")
            priority_dist = trends.get('priority_distribution', {})
            for priority in ['P1', 'P2', 'P3', 'P4']:
                count = priority_dist.get(priority, 0)
                print(f"  {priority}{'':<32} {count}")
            
            print(f"\n{'WEEKLY TICKET VOLUME':.<40} {'':<20}")
            weekly = trends.get('weekly_ticket_volume', {})
            for week, count in sorted(weekly.items())[-4:]:  # Show last 4 weeks
                print(f"  {week:<30} {count}")
            
            print("\n" + "="*70)
        
        except Exception as e:
            log_event("ERROR", f"Error displaying monthly trend: {str(e)}")
            print_error_message("Error displaying monthly trend")
    
    def save_daily_report_to_file(self):
        """Save daily report to file"""
        try:
            report = self.generate_daily_summary_report()
            filename = os.path.join(self.report_dir, f"daily_report_{datetime.now().strftime('%Y%m%d')}.json")
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4)
            
            log_event("SUCCESS", f"Daily report saved to {filename}")
            print_success_message(f"Daily report saved to {filename}")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error saving daily report: {str(e)}")
            print_error_message("Error saving daily report")
            return False
    
    def save_monthly_report_to_file(self):
        """Save monthly report to file"""
        try:
            report = self.generate_monthly_trend_report()
            month_str = datetime.now().strftime('%Y%m')
            filename = os.path.join(self.report_dir, f"monthly_report_{month_str}.json")
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4)
            
            log_event("SUCCESS", f"Monthly report saved to {filename}")
            print_success_message(f"Monthly report saved to {filename}")
            return True
        
        except Exception as e:
            log_event("ERROR", f"Error saving monthly report: {str(e)}")
            print_error_message("Error saving monthly report")
            return False
    
    @staticmethod
    def export_tickets_to_json(tickets, filename="export.json"):
        """Export tickets to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tickets, f, indent=4)
            log_event("SUCCESS", f"Tickets exported to {filename}")
            return True
        except Exception as e:
            log_event("ERROR", f"Error exporting tickets: {str(e)}")
            return False
    
    @staticmethod
    def get_sla_compliance_metrics(tickets):
        """
        Calculate SLA compliance metrics
        
        Args:
            tickets (dict): All tickets
        
        Returns:
            dict: SLA compliance metrics
        """
        try:
            total_closed = sum(1 for t in tickets.values() if t['status'] == 'Closed')
            sla_compliant = sum(1 for t in tickets.values() 
                              if t['status'] == 'Closed' and not t.get('sla_breached', False))
            
            compliance_rate = (sla_compliant / total_closed * 100) if total_closed > 0 else 0
            
            return {
                'total_closed_tickets': total_closed,
                'sla_compliant_tickets': sla_compliant,
                'sla_breached_tickets': total_closed - sla_compliant,
                'compliance_rate': f"{compliance_rate:.2f}%"
            }
        
        except Exception as e:
            log_event("ERROR", f"Error calculating SLA metrics: {str(e)}")
            return {}
