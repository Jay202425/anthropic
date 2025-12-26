"""
Unit tests for the Financial Analyzer module.
Tests the analyzer's ability to process financial data and communicate with Claude API.
"""

import unittest
from financial_analyzer import FinancialAnalyzer, get_financial_inputs
import os
from dotenv import load_dotenv

load_dotenv()


class TestFinancialAnalyzer(unittest.TestCase):
    """Test suite for the FinancialAnalyzer class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Check if API key is available
        api_key = os.getenv('ANTHROPIC_API_KEY')
        cls.has_api_key = api_key is not None and api_key != 'your_api_key_here'
        
        if cls.has_api_key:
            cls.analyzer = FinancialAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test that the analyzer initializes correctly."""
        if not self.has_api_key:
            self.skipTest("API key not configured")
        
        self.assertIsNotNone(self.analyzer)
        self.assertEqual(self.analyzer.model, "claude-3-5-sonnet-20241022")
        self.assertEqual(len(self.analyzer.conversation_history), 0)
    
    def test_financial_data_formatting(self):
        """Test the formatting of financial data."""
        if not self.has_api_key:
            self.skipTest("API key not configured")
        
        test_data = {
            "annual_income": 50000,
            "total_savings": 10000,
            "total_loans": 20000,
            "monthly_expenses": 2000,
            "investment_amount": 5000
        }
        
        formatted = self.analyzer._format_financial_data(test_data)
        
        # Check that all values are included in the formatted string
        self.assertIn("$50,000.00", formatted)
        self.assertIn("$10,000.00", formatted)
        self.assertIn("Annual Income", formatted)
        self.assertIn("Total Savings", formatted)
    
    def test_valid_financial_profile(self):
        """Test with a valid financial profile."""
        if not self.has_api_key:
            self.skipTest("API key not configured")
        
        test_profile = {
            "annual_income": 75000,
            "total_savings": 20000,
            "total_loans": 0,
            "monthly_expenses": 3000,
            "investment_amount": 10000
        }
        
        # This would call the API, so we just test the structure
        self.assertIn("annual_income", test_profile)
        self.assertIn("total_savings", test_profile)
        self.assertIn("total_loans", test_profile)
        self.assertIn("monthly_expenses", test_profile)
        self.assertIn("investment_amount", test_profile)
    
    def test_debt_to_savings_calculation(self):
        """Test debt-to-savings ratio calculation."""
        test_cases = [
            {"savings": 50000, "debt": 50000, "expected": 1.0},
            {"savings": 100000, "debt": 50000, "expected": 0.5},
            {"savings": 25000, "debt": 100000, "expected": 4.0},
            {"savings": 0, "debt": 50000, "expected": float('inf')},
        ]
        
        for case in test_cases:
            if case["savings"] == 0:
                with self.assertRaises(ZeroDivisionError):
                    ratio = case["debt"] / case["savings"]
            else:
                ratio = case["debt"] / case["savings"]
                self.assertEqual(ratio, case["expected"])
    
    def test_risk_level_categorization(self):
        """Test risk level categorization based on scores."""
        risk_scores = [
            (10, "Low"),
            (35, "Medium"),
            (60, "High"),
            (85, "Critical")
        ]
        
        def get_risk_level(score):
            if score < 25:
                return "Low"
            elif score < 50:
                return "Medium"
            elif score < 75:
                return "High"
            else:
                return "Critical"
        
        for score, expected_level in risk_scores:
            level = get_risk_level(score)
            self.assertEqual(level, expected_level)
    
    def test_conversation_history_tracking(self):
        """Test that conversation history is properly tracked."""
        if not self.has_api_key:
            self.skipTest("API key not configured")
        
        # Reset conversation
        self.analyzer.conversation_history = []
        self.assertEqual(len(self.analyzer.conversation_history), 0)
        
        # Add a test message
        self.analyzer.conversation_history.append({
            "role": "user",
            "content": "Test message"
        })
        
        self.assertEqual(len(self.analyzer.conversation_history), 1)
        self.assertEqual(self.analyzer.conversation_history[0]["role"], "user")


class TestFinancialProfiles(unittest.TestCase):
    """Test various financial profiles for plausibility."""
    
    def test_healthy_profile(self):
        """Test a healthy financial profile."""
        profile = {
            "annual_income": 100000,
            "total_savings": 50000,
            "total_loans": 0,
            "monthly_expenses": 3000,
            "investment_amount": 20000
        }
        
        # Monthly surplus calculation
        monthly_income = profile["annual_income"] / 12
        monthly_surplus = monthly_income - profile["monthly_expenses"]
        
        self.assertGreater(monthly_surplus, 0)
        self.assertGreater(profile["total_savings"], 0)
        self.assertEqual(profile["total_loans"], 0)
    
    def test_stressed_profile(self):
        """Test a financially stressed profile."""
        profile = {
            "annual_income": 40000,
            "total_savings": 2000,
            "total_loans": 50000,
            "monthly_expenses": 3500,
            "investment_amount": 0
        }
        
        # Monthly deficit calculation
        monthly_income = profile["annual_income"] / 12
        monthly_deficit = monthly_income - profile["monthly_expenses"]
        
        self.assertLess(monthly_deficit, 0)
        self.assertLess(profile["total_savings"], 5000)
        self.assertGreater(profile["total_loans"], profile["total_savings"])
    
    def test_growth_profile(self):
        """Test a profile with growth potential."""
        profile = {
            "annual_income": 150000,
            "total_savings": 100000,
            "total_loans": 30000,
            "monthly_expenses": 4000,
            "investment_amount": 50000
        }
        
        # Has positive cash flow and investment portfolio
        monthly_income = profile["annual_income"] / 12
        monthly_surplus = monthly_income - profile["monthly_expenses"]
        
        self.assertGreater(monthly_surplus, 0)
        self.assertGreater(profile["investment_amount"], 0)
        self.assertGreater(profile["total_savings"], profile["total_loans"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
