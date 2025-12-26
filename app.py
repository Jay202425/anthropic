"""
Flask Web Server for Financial Analyzer
Provides a web interface for users to input financial data and get AI-powered analysis.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from financial_analyzer import FinancialAnalyzer
import os
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Check if API key exists
if not os.getenv('ANTHROPIC_API_KEY'):
    print("WARNING: ANTHROPIC_API_KEY not set in .env file")

# Initialize analyzer
try:
    analyzer = FinancialAnalyzer()
except Exception as e:
    print(f"Warning: Could not initialize analyzer: {e}")
    analyzer = None


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze financial data and return AI-powered insights.
    Expects JSON with financial data.
    """
    try:
        # Validate API key
        if not os.getenv('ANTHROPIC_API_KEY'):
            return jsonify({
                'error': 'API key not configured',
                'message': 'Please set ANTHROPIC_API_KEY in .env file'
            }), 500
        
        # Get financial data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = [
            'annual_income',
            'total_savings',
            'total_loans',
            'monthly_expenses',
            'investment_amount'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Convert string values to float
        try:
            financial_data = {
                'annual_income': float(data['annual_income']),
                'total_savings': float(data['total_savings']),
                'total_loans': float(data['total_loans']),
                'monthly_expenses': float(data['monthly_expenses']),
                'investment_amount': float(data['investment_amount'])
            }
        except ValueError as e:
            return jsonify({'error': f'Invalid number format: {str(e)}'}), 400
        
        # Validate non-negative values
        for key, value in financial_data.items():
            if value < 0:
                return jsonify({'error': f'{key} must be non-negative'}), 400
        
        # Perform analysis
        print(f"Analyzing financial data: {financial_data}")
        
        # Initialize analyzer if not done
        if analyzer is None:
            return jsonify({
                'error': 'Analyzer initialization failed',
                'message': 'Check API key and try again'
            }), 500
        
        analysis = analyzer.analyze_financial_situation(financial_data)
        
        # Calculate additional metrics
        monthly_income = financial_data['annual_income'] / 12
        monthly_surplus = monthly_income - financial_data['monthly_expenses']
        debt_to_savings = (
            financial_data['total_loans'] / financial_data['total_savings']
            if financial_data['total_savings'] > 0
            else float('inf')
        )
        
        return jsonify({
            'success': True,
            'analysis': {
                'initial_analysis': analysis['initial_analysis'],
                'detailed_metrics': analysis['detailed_metrics'],
                'recommendations': analysis['recommendations']
            },
            'metrics': {
                'monthly_income': round(monthly_income, 2),
                'monthly_surplus': round(monthly_surplus, 2),
                'debt_to_savings_ratio': round(debt_to_savings, 2) if debt_to_savings != float('inf') else 'Infinity',
                'savings_rate': round((monthly_surplus / monthly_income * 100) if monthly_income > 0 else 0, 2)
            },
            'input_data': financial_data
        }), 200
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@app.route('/api/quick-assessment', methods=['POST'])
def quick_assessment():
    """Get a quick risk assessment without full analysis."""
    try:
        if not os.getenv('ANTHROPIC_API_KEY'):
            return jsonify({
                'error': 'API key not configured',
                'message': 'Please set ANTHROPIC_API_KEY in .env file'
            }), 500
        
        data = request.get_json()
        
        # Convert to float
        try:
            financial_data = {
                'annual_income': float(data['annual_income']),
                'total_savings': float(data['total_savings']),
                'total_loans': float(data['total_loans']),
                'monthly_expenses': float(data['monthly_expenses']),
                'investment_amount': float(data['investment_amount'])
            }
        except (ValueError, KeyError) as e:
            return jsonify({'error': f'Invalid input: {str(e)}'}), 400
        
        if analyzer is None:
            return jsonify({'error': 'Analyzer not initialized'}), 500
        
        assessment = analyzer.get_risk_assessment(financial_data)
        
        return jsonify({
            'success': True,
            'assessment': assessment
        }), 200
        
    except Exception as e:
        print(f"Error in quick assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if the API is running and configured."""
    api_key_set = bool(os.getenv('ANTHROPIC_API_KEY'))
    
    return jsonify({
        'status': 'healthy' if api_key_set else 'warning',
        'api_key_configured': api_key_set,
        'message': 'Ready' if api_key_set else 'API key not configured'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Financial Analyzer Web Server...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='localhost', port=5000)
