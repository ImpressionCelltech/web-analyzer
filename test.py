import requests
from report_formatter import ReportFormatter

def test_api():
    try:
        urls_to_test = {
            "urls": [
                "icelltech.ca"
            ]
        }

        print("Testing API...")
        print(f"Sending request to analyze URLs: {urls_to_test['urls']}")
        
        response = requests.post(
            "http://localhost:8000/api/analyze",
            json=urls_to_test
        )
        
        if response.status_code == 200:
            print("\nAnalysis completed successfully!")
            result_data = response.json()
            
            # Generate and save HTML report
            formatter = ReportFormatter(result_data['data'])
            report_path = formatter.save_report()
            
            print(f"\nReport generated successfully!")
            print(f"Report saved to: {report_path}")
            print("\nKey findings:")
            print(f"- Sites analyzed: {result_data['data']['successful_analyses']} / {result_data['data']['total_sites']}")
            print(f"- Analysis time: {result_data['data']['analysis_time']}")
            print("\nAverage scores:")
            for metric, score in result_data['data']['average_scores'].items():
                print(f"- {metric.replace('_', ' ').title()}: {score:.1f}/10")
            
        else:
            print(f"\nError: Status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_api()