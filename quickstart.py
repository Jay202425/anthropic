#!/usr/bin/env python
"""
Quick Start Guide for Financial Analyzer

This script demonstrates how to get started with the Financial Analyzer.
"""

from financial_analyzer import FinancialAnalyzer
import os


def quick_demo():
    """Run a quick demo of the analyzer."""
    
    print("="*70)
    print("FINANCIAL ANALYZER - QUICK START DEMO")
    print("="*70)
    
    # Check API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("Please set your API key in the .env file")
        print("Copy .env.example to .env and add your API key\n")
        return
    
    # Initialize analyzer
    print("\n1. Initializing Financial Analyzer...")
    analyzer = FinancialAnalyzer()
    print("   ✓ Analyzer ready\n")
    
    # Define a sample profile
    print("2. Using sample financial profile:")
    sample_profile = {
        "annual_income": 85000,
        "total_savings": 25000,
        "total_loans": 40000,
        "monthly_expenses": 3200,
        "investment_amount": 8000,
    }
    
    print("   Annual Income: $85,000")
    print("   Total Savings: $25,000")
    print("   Total Loans: $40,000")
    print("   Monthly Expenses: $3,200")
    print("   Investment Amount: $8,000")
    
    # Get quick risk assessment
    print("\n3. Getting quick risk assessment...")
    try:
        risk_assessment = analyzer.get_risk_assessment(sample_profile)
        print("\n   Risk Assessment:")
        print("   " + "-"*66)
        for line in risk_assessment.split('\n'):
            if line.strip():
                print(f"   {line}")
    except Exception as e:
        print(f"   Error during analysis: {e}")
        print("   Make sure your ANTHROPIC_API_KEY is valid")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. Interactive Analysis (Manual Input):")
    print("   Run: python financial_analyzer.py")
    print("\n2. Sample Profile Analysis:")
    print("   Run: python sample_analysis.py")
    print("\n3. Run Unit Tests:")
    print("   Run: python test_analyzer.py")
    print("\n" + "="*70)


if __name__ == "__main__":
    quick_demo()
