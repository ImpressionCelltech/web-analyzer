# report_formatter.py
import json
from typing import Dict
from datetime import datetime
import os

class ReportFormatter:
    def __init__(self, report_data: Dict):
        self.data = report_data
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    def generate_html_report(self) -> str:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Website Analysis Report - {self.data['timestamp']}</title>
            <style>
                {self._get_styles()}
            </style>
        </head>
        <body>
            <div class="container">
                {self._generate_header()}
                {self._generate_summary()}
                {self._generate_comparative_analysis()}
                {self._generate_detailed_results()}
                {self._generate_recommendations()}
            </div>
            <script>
                {self._get_scripts()}
            </script>
        </body>
        </html>
        """
        return html

    def _generate_header(self) -> str:
        return f"""
        <div class="header">
            <h1>Enhanced Website Analysis Report</h1>
            <div class="meta-info">
                <p>Generated on: {self.data['timestamp']}</p>
                <p>Analysis time: {self.data['analysis_time']}</p>
                <p>Sites analyzed: {self.data['successful_analyses']}/{self.data['total_sites']}</p>
            </div>
        </div>
        """

    def _generate_summary(self) -> str:
        stats = self.data['aggregate_stats']
        return f"""
        <div class="section">
            <h2>Analysis Summary</h2>
            <div class="score-grid">
                {self._generate_score_cards(stats['average_scores'])}
            </div>
            <div class="stats-grid">
                {self._generate_stat_cards(stats['distributions'])}
            </div>
        </div>
        """

    def _generate_comparative_analysis(self) -> str:
        if not self.data.get('comparative_analysis'):
            return ""
            
        comp = self.data['comparative_analysis']
        return f"""
        <div class="section">
            <h2>Comparative Analysis</h2>
            <div class="chart-container">
                <canvas id="distributionChart"></canvas>
            </div>
            <div class="common-issues">
                <h3>Common Issues</h3>
                {self._generate_common_issues_table(comp['common_issues'])}
            </div>
        </div>
        """

    def _generate_detailed_results(self) -> str:
        results = ""
        for site in self.data['detailed_results']:
            if site['success']:
                results += f"""
                <div class="site-analysis">
                    <h3>{site['url']}</h3>
                    <div class="metrics-grid">
                        {self._generate_metric_cards(site['metrics'])}
                    </div>
                    {self._generate_detailed_metrics_table(site)}
                </div>
                """
        return f"""
        <div class="section">
            <h2>Detailed Analysis</h2>
            {results}
        </div>
        """

    def _generate_recommendations(self) -> str:
        recs = ""
        for site_rec in self.data['recommendations']:
            recs += f"""
            <div class="site-recommendations">
                <h3>{site_rec['url']}</h3>
                <div class="priority-improvements">
                    <h4>Priority Improvements</h4>
                    {self._format_recommendations(site_rec['priority_improvements'])}
                </div>
                <div class="security-alerts">
                    <h4>Security Alerts</h4>
                    {self._format_recommendations(site_rec['security_alerts'])}
                </div>
            </div>
            """
        return f"""
        <div class="section recommendations">
            <h2>Recommendations</h2>
            {recs}
        </div>
        """

    def _get_styles(self) -> str:
        return """
            :root {
                --primary: #2563eb;
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --background: #f8fafc;
                --card: #ffffff;
                --text: #1e293b;
                --border: #e2e8f0;
            }

            body {
                font-family: system-ui, -apple-system, sans-serif;
                line-height: 1.5;
                background: var(--background);
                color: var(--text);
                margin: 0;
                padding: 0;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }

            .section {
                background: var(--card);
                border-radius: 0.5rem;
                padding: 1.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }

            .score-grid, .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
                margin: 1rem 0;
            }

            .card {
                background: var(--card);
                border-radius: 0.5rem;
                padding: 1.5rem;
                border: 1px solid var(--border);
            }

            .score {
                font-size: 2rem;
                font-weight: bold;
                margin: 1rem 0;
            }

            .good { color: var(--success); }
            .average { color: var(--warning); }
            .poor { color: var(--danger); }

            table {
                width: 100%;
                border-collapse: collapse;
                margin: 1rem 0;
            }

            th, td {
                padding: 0.75rem;
                text-align: left;
                border-bottom: 1px solid var(--border);
            }

            .recommendations .card {
                border-left: 4px solid var(--primary);
                margin-bottom: 1rem;
            }

            .security-alerts .card {
                border-left: 4px solid var(--danger);
            }
        """

    def _get_scripts(self) -> str:
        return """
        // Add any JavaScript for interactivity and charts
        """

    def save_report(self, output_dir: str = "reports") -> str:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = f"website_analysis_{self.timestamp}.html"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate_html_report())
            
        return filepath