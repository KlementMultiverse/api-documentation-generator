#!/usr/bin/env python3
"""
AI-Powered Production Log Analyzer
Analyzes log files and uses AI to find root causes automatically
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.progress import track
except ImportError:
    print("Installing required packages...")
    os.system("pip install rich requests pandas")
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

console = Console()


class LogEntry:
    """Represents a single log entry"""

    def __init__(self, timestamp: str, level: str, message: str, raw: str):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.raw = raw

    def __repr__(self):
        return f"LogEntry({self.timestamp}, {self.level}, {self.message[:50]}...)"


class LogParser:
    """Parses log files into structured entries"""

    # Common log patterns
    PATTERNS = [
        # ISO timestamp: 2024-01-15 14:23:15 ERROR message
        re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\w+):\s+(.+)'),
        # Syslog: Jan 15 14:23:15 ERROR message
        re.compile(r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\w+):\s+(.+)'),
        # Python logging: [2024-01-15 14:23:15] ERROR message
        re.compile(r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+(\w+)\s+(.+)'),
        # Generic: ERROR: message or [ERROR] message
        re.compile(r'\[?(\w+)\]?:\s+(.+)'),
    ]

    def parse_file(self, filepath: str) -> List[LogEntry]:
        """Parse a log file into structured entries"""
        entries = []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                entry = self._parse_line(line)
                if entry:
                    entries.append(entry)

        console.print(f"[green]✓[/green] Parsed {len(entries)} log entries from {filepath}")
        return entries

    def _parse_line(self, line: str) -> LogEntry:
        """Parse a single log line"""
        for pattern in self.PATTERNS:
            match = pattern.match(line)
            if match:
                groups = match.groups()

                if len(groups) == 3:
                    timestamp, level, message = groups
                elif len(groups) == 2:
                    # No timestamp
                    timestamp = "unknown"
                    level, message = groups
                else:
                    continue

                return LogEntry(timestamp, level.upper(), message, line)

        # If no pattern matches, treat whole line as message
        return LogEntry("unknown", "INFO", line, line)


class PatternDetector:
    """Detects patterns and anomalies in logs"""

    def analyze(self, entries: List[LogEntry]) -> Dict[str, Any]:
        """Analyze log entries for patterns"""

        # Count by log level
        levels = Counter([e.level for e in entries])

        # Find error patterns
        errors = [e for e in entries if e.level in ['ERROR', 'CRITICAL', 'FATAL']]
        error_messages = Counter([self._normalize_message(e.message) for e in errors])

        # Timeline analysis
        timeline = self._build_timeline(errors)

        # Find cascading failures (multiple errors in short time)
        cascades = self._find_cascades(errors)

        return {
            'total_entries': len(entries),
            'level_counts': dict(levels),
            'error_count': len(errors),
            'unique_errors': len(error_messages),
            'top_errors': error_messages.most_common(5),
            'timeline': timeline,
            'cascades': cascades
        }

    def _normalize_message(self, message: str) -> str:
        """Normalize error message to find patterns"""
        # Remove numbers, IDs, timestamps
        normalized = re.sub(r'\b\d+\b', 'N', message)
        normalized = re.sub(r'\b[0-9a-f]{8,}\b', 'ID', normalized)
        return normalized[:100]  # Limit length

    def _build_timeline(self, errors: List[LogEntry]) -> List[Dict]:
        """Build timeline of errors"""
        timeline = []
        for error in errors[:20]:  # Limit to first 20
            timeline.append({
                'time': error.timestamp,
                'message': error.message[:80]
            })
        return timeline

    def _find_cascades(self, errors: List[LogEntry]) -> List[Dict]:
        """Find cascading failures (bursts of errors)"""
        if len(errors) < 3:
            return []

        cascades = []
        current_cascade = []

        for i, error in enumerate(errors):
            if i == 0:
                current_cascade = [error]
                continue

            # Simple cascade detection: 3+ errors
            if len(current_cascade) < 10:
                current_cascade.append(error)
            else:
                if len(current_cascade) >= 3:
                    cascades.append({
                        'count': len(current_cascade),
                        'first': current_cascade[0].timestamp,
                        'last': current_cascade[-1].timestamp
                    })
                current_cascade = [error]

        return cascades[:5]  # Return top 5 cascades


class AIAnalyzer:
    """Uses AI to analyze logs and suggest fixes"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('NVIDIA_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.base_url = "https://integrate.api.nvidia.com/v1"

    def analyze(self, patterns: Dict[str, Any], sample_errors: List[LogEntry]) -> str:
        """Use AI to analyze patterns and suggest fixes"""

        if not self.api_key:
            return self._fallback_analysis(patterns, sample_errors)

        # Prepare context for AI
        context = self._prepare_context(patterns, sample_errors)

        try:
            import requests

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "nvidia/llama-3.1-nemotron-70b-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert SRE analyzing production logs. Provide concise, actionable root cause analysis and fixes."
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze these production logs and provide:
1. Root cause (one sentence)
2. Top 3 recommended fixes
3. Prevention strategy

Log Summary:
{context}

Format your response as:
ROOT CAUSE: <one sentence>
FIXES:
1. <fix>
2. <fix>
3. <fix>
PREVENTION: <strategy>
"""
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 500
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                console.print(f"[yellow]⚠ API call failed ({response.status_code}), using fallback analysis[/yellow]")
                return self._fallback_analysis(patterns, sample_errors)

        except Exception as e:
            console.print(f"[yellow]⚠ AI analysis failed: {e}, using fallback[/yellow]")
            return self._fallback_analysis(patterns, sample_errors)

    def _prepare_context(self, patterns: Dict, sample_errors: List[LogEntry]) -> str:
        """Prepare log context for AI"""
        context = f"""Total log entries: {patterns['total_entries']}
Errors found: {patterns['error_count']}
Unique error patterns: {patterns['unique_errors']}

Top error messages:
"""
        for msg, count in patterns['top_errors'][:3]:
            context += f"- ({count}x) {msg}\n"

        context += "\nSample error logs:\n"
        for error in sample_errors[:5]:
            context += f"[{error.timestamp}] {error.level}: {error.message[:100]}\n"

        return context

    def _fallback_analysis(self, patterns: Dict, sample_errors: List[LogEntry]) -> str:
        """Fallback analysis when AI is not available"""

        analysis = "ROOT CAUSE: "

        # Simple heuristic analysis
        if patterns['error_count'] == 0:
            analysis += "No errors detected in logs. System appears healthy.\n\n"
            analysis += "FIXES:\n1. No action required\n2. Continue monitoring\n3. Review info/warning logs for potential issues\n\n"
            analysis += "PREVENTION: Maintain current monitoring and alerting"
            return analysis

        # Check for common patterns
        top_error = patterns['top_errors'][0][0] if patterns['top_errors'] else ""

        if 'connection' in top_error.lower() or 'refused' in top_error.lower():
            analysis += "Network connectivity or service connection failure\n\n"
            analysis += "FIXES:\n"
            analysis += "1. Check network connectivity between services\n"
            analysis += "2. Verify target service is running and accepting connections\n"
            analysis += "3. Review firewall rules and security groups\n\n"
            analysis += "PREVENTION: Implement health checks, connection pooling, and retry logic with exponential backoff"

        elif 'timeout' in top_error.lower():
            analysis += "Service timeout - operations taking too long\n\n"
            analysis += "FIXES:\n"
            analysis += "1. Increase timeout values in configuration\n"
            analysis += "2. Optimize slow database queries or API calls\n"
            analysis += "3. Add caching layer for frequently accessed data\n\n"
            analysis += "PREVENTION: Set up performance monitoring and alerts for slow operations"

        elif 'memory' in top_error.lower() or 'oom' in top_error.lower():
            analysis += "Memory exhaustion - possible memory leak\n\n"
            analysis += "FIXES:\n"
            analysis += "1. Increase memory allocation for the service\n"
            analysis += "2. Review code for memory leaks\n"
            analysis += "3. Restart affected services\n\n"
            analysis += "PREVENTION: Add memory monitoring, implement proper cleanup, and consider memory profiling"

        elif 'permission' in top_error.lower() or 'denied' in top_error.lower():
            analysis += "Permission or authentication failure\n\n"
            analysis += "FIXES:\n"
            analysis += "1. Review and update service permissions\n"
            analysis += "2. Verify credentials are correct and not expired\n"
            analysis += "3. Check IAM roles and policies\n\n"
            analysis += "PREVENTION: Implement proper credential rotation and access control management"

        else:
            analysis += f"Multiple errors detected: {patterns['error_count']} total, {patterns['unique_errors']} unique patterns\n\n"
            analysis += "FIXES:\n"
            analysis += "1. Review the top error messages listed above\n"
            analysis += "2. Check service logs around the error timestamps\n"
            analysis += "3. Correlate with recent deployments or configuration changes\n\n"
            analysis += "PREVENTION: Enhance logging, add monitoring alerts, and implement gradual rollouts"

        return analysis


class ReportGenerator:
    """Generates analysis reports in various formats"""

    def generate_terminal_report(self, patterns: Dict, ai_analysis: str):
        """Generate beautiful terminal report"""

        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]🔍 Log Analysis Report[/bold cyan]",
            border_style="cyan"
        ))

        # Summary table
        table = Table(title="📊 Summary", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")

        table.add_row("Total Entries", str(patterns['total_entries']))
        table.add_row("Error Count", f"[red]{patterns['error_count']}[/red]")
        table.add_row("Unique Errors", str(patterns['unique_errors']))

        console.print(table)
        console.print()

        # Top errors
        if patterns['top_errors']:
            console.print("[bold yellow]🔥 Top Error Patterns:[/bold yellow]")
            for i, (msg, count) in enumerate(patterns['top_errors'], 1):
                console.print(f"  {i}. ({count}x) {msg[:80]}...")
            console.print()

        # Timeline
        if patterns['timeline']:
            console.print("[bold blue]📅 Error Timeline:[/bold blue]")
            for item in patterns['timeline'][:5]:
                console.print(f"  [{item['time']}] {item['message']}")
            console.print()

        # AI Analysis
        console.print(Panel(
            ai_analysis,
            title="[bold green]🤖 AI Analysis & Recommendations[/bold green]",
            border_style="green"
        ))
        console.print()

    def generate_markdown_report(self, patterns: Dict, ai_analysis: str, output_file: str):
        """Generate markdown report"""

        report = f"""# 🔍 Log Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Summary

- **Total Entries:** {patterns['total_entries']}
- **Error Count:** {patterns['error_count']}
- **Unique Error Patterns:** {patterns['unique_errors']}

## 🔥 Top Error Patterns

"""
        for i, (msg, count) in enumerate(patterns['top_errors'], 1):
            report += f"{i}. **({count}x)** {msg}\n"

        report += f"\n## 📅 Error Timeline\n\n"
        for item in patterns['timeline'][:10]:
            report += f"- `[{item['time']}]` {item['message']}\n"

        report += f"\n## 🤖 AI Analysis\n\n{ai_analysis}\n"

        report += f"\n---\n\n*Report generated by AI-Powered Production Log Analyzer*\n"

        with open(output_file, 'w') as f:
            f.write(report)

        console.print(f"[green]✓[/green] Report saved to {output_file}")


def demo_mode():
    """Run demo with sample logs"""
    console.print(Panel.fit(
        "[bold cyan]🎮 Demo Mode - Analyzing Sample Logs[/bold cyan]",
        border_style="cyan"
    ))

    # Create sample log
    sample_log = """2024-01-15 14:23:15 ERROR: Connection refused to database at db.example.com:5432
2024-01-15 14:23:16 ERROR: Failed to fetch user data from database
2024-01-15 14:23:17 ERROR: API request to /api/users failed with status 500
2024-01-15 14:23:18 ERROR: Connection refused to database at db.example.com:5432
2024-01-15 14:23:19 ERROR: Failed to fetch user data from database
2024-01-15 14:23:20 ERROR: API request to /api/products failed with status 500
2024-01-15 14:24:00 INFO: Database connection restored
2024-01-15 14:24:01 INFO: Service recovered, processing requests
"""

    # Save to temp file
    temp_file = '/tmp/sample_app.log'
    with open(temp_file, 'w') as f:
        f.write(sample_log)

    console.print(f"[yellow]Sample log created at {temp_file}[/yellow]\n")

    # Analyze it
    analyze_logs(temp_file)


def analyze_logs(filepath: str, output: str = None):
    """Main analysis function"""

    if not os.path.exists(filepath):
        console.print(f"[red]✗ Error: File not found: {filepath}[/red]")
        return

    console.print(f"\n[cyan]Analyzing {filepath}...[/cyan]\n")

    # Parse logs
    parser = LogParser()
    entries = parser.parse_file(filepath)

    if not entries:
        console.print("[yellow]No log entries found[/yellow]")
        return

    # Detect patterns
    console.print("[cyan]Detecting patterns...[/cyan]")
    detector = PatternDetector()
    patterns = detector.analyze(entries)

    # AI analysis
    console.print("[cyan]Running AI analysis...[/cyan]")
    errors = [e for e in entries if e.level in ['ERROR', 'CRITICAL', 'FATAL']]
    analyzer = AIAnalyzer()
    ai_analysis = analyzer.analyze(patterns, errors[:10])

    # Generate report
    reporter = ReportGenerator()
    reporter.generate_terminal_report(patterns, ai_analysis)

    if output:
        reporter.generate_markdown_report(patterns, ai_analysis, output)


def main():
    parser = argparse.ArgumentParser(
        description='AI-Powered Production Log Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze myapp.log              # Analyze a log file
  %(prog)s analyze app.log -o report.md   # Generate markdown report
  %(prog)s demo                           # Run demo with sample logs
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze log file')
    analyze_parser.add_argument('file', help='Path to log file')
    analyze_parser.add_argument('-o', '--output', help='Output report file (markdown)')

    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demo with sample logs')

    args = parser.parse_args()

    if args.command == 'analyze':
        analyze_logs(args.file, args.output)
    elif args.command == 'demo':
        demo_mode()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
