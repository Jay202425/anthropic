"""
Financial Risk and Gain Analysis Model using Anthropic API
This module analyzes financial inputs (loans, savings) to provide risk and gain assessments.
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FinancialAnalyzer:
    """A financial analysis model that uses Claude to analyze risk and gain potential."""
    
    def __init__(self):
        """Initialize the Anthropic client."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
        
        # System prompt that guides Claude for financial analysis
        self.system_prompt = """You are an expert financial advisor with deep knowledge of risk assessment, 
investment strategies, and personal finance. Your role is to analyze a person's financial situation 
based on their inputs about loans, savings, and other financial metrics.

When analyzing financial data, you should:
1. Calculate the debt-to-savings ratio
2. Assess financial risk level (Low, Medium, High, Critical)
3. Identify potential financial gains based on their current situation
4. Provide actionable recommendations
5. Consider both short-term and long-term financial implications

Always provide structured analysis with clear metrics and explanations."""
    
    def analyze_financial_situation(self, financial_data: dict) -> dict:
        """
        Analyze a person's financial situation using multi-turn conversation.
        
        Args:
            financial_data: Dictionary containing financial inputs
            
        Returns:
            Dictionary with analysis results including risk level and gain potential
        """
        # Reset conversation for new analysis
        self.conversation_history = []
        
        # First message: Present the financial data for analysis
        initial_message = self._format_financial_data(financial_data)
        self.conversation_history.append({
            "role": "user",
            "content": initial_message
        })
        
        # Get initial analysis from Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        initial_analysis = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": initial_analysis
        })
        
        # Follow-up for specific risk metrics
        risk_question = """Based on your analysis, please provide:
1. A risk score from 0-100 (0=no risk, 100=maximum risk)
2. Top 3 risk factors
3. Top 3 opportunities for financial gain
Please format this as JSON."""
        
        self.conversation_history.append({
            "role": "user",
            "content": risk_question
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        detailed_analysis = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": detailed_analysis
        })
        
        # Follow-up for recommendations
        recommendation_question = """Please provide 5 specific, actionable recommendations 
to reduce risk and maximize gain potential. Format as a numbered list with brief explanations."""
        
        self.conversation_history.append({
            "role": "user",
            "content": recommendation_question
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        recommendations = response.content[0].text
        
        # Compile the complete analysis
        return {
            "initial_analysis": initial_analysis,
            "detailed_metrics": detailed_analysis,
            "recommendations": recommendations,
            "conversation_turns": len(self.conversation_history)
        }
    
    def _format_financial_data(self, financial_data: dict) -> str:
        """Format financial data for Claude analysis."""
        formatted = "Please analyze the following financial situation:\n\n"
        
        for key, value in financial_data.items():
            # Convert snake_case to readable format
            readable_key = key.replace('_', ' ').title()
            formatted += f"- {readable_key}: ${value:,.2f}\n"
        
        formatted += "\nProvide a comprehensive financial analysis of this situation."
        return formatted
    
    def get_risk_assessment(self, financial_data: dict) -> str:
        """Get a quick risk assessment without full analysis."""
        message = f"""Quickly assess the risk level for this financial profile:
{json.dumps(financial_data, indent=2)}

Respond with ONLY: RISK_LEVEL (Low/Medium/High/Critical), then a brief 1-2 sentence explanation."""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            system=self.system_prompt,
            messages=[{"role": "user", "content": message}]
        )
        
        return response.content[0].text


def get_financial_inputs() -> dict:
    """Get financial inputs from user interactively."""
    print("\n" + "="*60)
    print("FINANCIAL RISK & GAIN ANALYSIS TOOL")
    print("="*60)
    print("\nPlease enter your financial information:\n")
    
    financial_data = {}
    
    # Collect basic financial information
    while True:
        try:
            total_income = float(input("Annual Income ($): "))
            if total_income < 0:
                print("Income must be non-negative. Try again.")
                continue
            financial_data["annual_income"] = total_income
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            total_savings = float(input("Total Savings ($): "))
            if total_savings < 0:
                print("Savings must be non-negative. Try again.")
                continue
            financial_data["total_savings"] = total_savings
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            total_loans = float(input("Total Loans/Debt ($): "))
            if total_loans < 0:
                print("Loans must be non-negative. Try again.")
                continue
            financial_data["total_loans"] = total_loans
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            monthly_expenses = float(input("Monthly Expenses ($): "))
            if monthly_expenses < 0:
                print("Expenses must be non-negative. Try again.")
                continue
            financial_data["monthly_expenses"] = monthly_expenses
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            investment_amount = float(input("Current Investment Amount ($): "))
            if investment_amount < 0:
                print("Investment must be non-negative. Try again.")
                continue
            financial_data["investment_amount"] = investment_amount
            break
        except ValueError:
            print("Please enter a valid number.")
    
    return financial_data


def main():
    """Main entry point for the financial analyzer."""
    try:
        analyzer = FinancialAnalyzer()
        
        # Get user inputs
        financial_data = get_financial_inputs()
        
        print("\n" + "="*60)
        print("ANALYZING YOUR FINANCIAL SITUATION...")
        print("="*60 + "\n")
        
        # Perform analysis
        analysis = analyzer.analyze_financial_situation(financial_data)
        
        print("\n" + "="*60)
        print("FINANCIAL ANALYSIS RESULTS")
        print("="*60)
        
        print("\n📊 INITIAL ANALYSIS:")
        print("-" * 60)
        print(analysis["initial_analysis"])
        
        print("\n📈 DETAILED METRICS:")
        print("-" * 60)
        print(analysis["detailed_metrics"])
        
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 60)
        print(analysis["recommendations"])
        
        print("\n" + "="*60)
        print(f"Analysis completed in {analysis['conversation_turns']} conversation turns.")
        print("="*60 + "\n")
        
    except KeyError:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set your API key: export ANTHROPIC_API_KEY='your-api-key'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()
