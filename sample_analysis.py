"""
Example usage of the Financial Analyzer with sample data.
This script demonstrates how to use the analyzer with predefined financial profiles.
"""

from financial_analyzer import FinancialAnalyzer
import json


def analyze_sample_profiles():
    """Analyze multiple sample financial profiles."""
    
    analyzer = FinancialAnalyzer()
    
    # Define sample financial profiles
    sample_profiles = {
        "Young Professional": {
            "annual_income": 65000,
            "total_savings": 15000,
            "total_loans": 35000,  # Student loans
            "monthly_expenses": 2500,
            "investment_amount": 5000,
        },
        "Mid-Career Developer": {
            "annual_income": 120000,
            "total_savings": 85000,
            "total_loans": 0,
            "monthly_expenses": 4000,
            "investment_amount": 25000,
        },
        "Small Business Owner": {
            "annual_income": 200000,
            "total_savings": 50000,
            "total_loans": 150000,  # Business loan
            "monthly_expenses": 6000,
            "investment_amount": 10000,
        },
        "Conservative Saver": {
            "annual_income": 45000,
            "total_savings": 120000,
            "total_loans": 0,
            "monthly_expenses": 1800,
            "investment_amount": 2000,
        },
        "High Debt Profile": {
            "annual_income": 55000,
            "total_savings": 3000,
            "total_loans": 95000,  # Car, credit cards, etc.
            "monthly_expenses": 3500,
            "investment_amount": 0,
        }
    }
    
    results = {}
    
    for profile_name, financial_data in sample_profiles.items():
        print(f"\n{'='*70}")
        print(f"Analyzing: {profile_name}")
        print(f"{'='*70}")
        print(f"Profile Data: {json.dumps(financial_data, indent=2)}")
        print("\nAnalyzing...")
        
        # Get quick risk assessment
        risk_assessment = analyzer.get_risk_assessment(financial_data)
        results[profile_name] = {
            "profile": financial_data,
            "risk_assessment": risk_assessment
        }
        
        print(f"\nRisk Assessment:\n{risk_assessment}")
    
    return results


if __name__ == "__main__":
    print("Financial Profile Analysis Examples")
    print("====================================\n")
    
    try:
        results = analyze_sample_profiles()
        
        print("\n" + "="*70)
        print("SUMMARY OF ALL ANALYSES")
        print("="*70)
        
        for profile_name, result in results.items():
            print(f"\n{profile_name}:")
            print(result["risk_assessment"][:100] + "...")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your ANTHROPIC_API_KEY environment variable!")
