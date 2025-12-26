"""
Streamlit Web Interface for Financial Analyzer
AI-Powered Risk Assessment & Gain Analysis
"""

import streamlit as st
from financial_analyzer import FinancialAnalyzer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Financial Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .analysis-box {
        background: #f8f9ff;
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    h1 {
        color: #667eea;
        text-align: center;
        padding: 20px 0;
    }
    h2 {
        color: #764ba2;
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
    api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY')
    if api_key:
        try:
            st.session_state.analyzer = FinancialAnalyzer()
        except Exception as e:
            st.error(f"Error initializing analyzer: {str(e)}")
    else:
        st.warning("API key not configured")

if 'results' not in st.session_state:
    st.session_state.results = None

# Header
st.markdown("# 💰 Financial Analyzer")
st.markdown("### AI-Powered Risk Assessment & Gain Analysis")

# Check API Key
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    st.warning("⚠️ **API Key Not Configured**")
    st.info("Please set your ANTHROPIC_API_KEY in the Streamlit secrets or .env file")
else:
    st.success("✅ API Key Configured")

st.divider()

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Enter Your Financial Data")
    
    with st.form("financial_form"):
        annual_income = st.number_input(
            "Annual Income ($)",
            min_value=0.0,
            max_value=10000000.0,
            step=1000.0,
            value=85000.0,
            help="Your total yearly earnings"
        )
        
        total_savings = st.number_input(
            "Total Savings ($)",
            min_value=0.0,
            max_value=100000000.0,
            step=1000.0,
            value=25000.0,
            help="Cash and liquid assets"
        )
        
        total_loans = st.number_input(
            "Total Loans / Debt ($)",
            min_value=0.0,
            max_value=100000000.0,
            step=1000.0,
            value=40000.0,
            help="All outstanding debt (car, student, mortgage, credit cards)"
        )
        
        monthly_expenses = st.number_input(
            "Monthly Expenses ($)",
            min_value=0.0,
            max_value=1000000.0,
            step=100.0,
            value=3200.0,
            help="Average monthly spending"
        )
        
        investment_amount = st.number_input(
            "Investment Amount ($)",
            min_value=0.0,
            max_value=100000000.0,
            step=1000.0,
            value=8000.0,
            help="Current investment portfolio value"
        )
        
        submitted = st.form_submit_button(
            "📈 Analyze",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not api_key:
                st.error("Please configure your API key first")
            else:
                financial_data = {
                    'annual_income': annual_income,
                    'total_savings': total_savings,
                    'total_loans': total_loans,
                    'monthly_expenses': monthly_expenses,
                    'investment_amount': investment_amount
                }
                
                try:
                    with st.spinner("🔄 Analyzing your financial situation..."):
                        analysis = st.session_state.analyzer.analyze_financial_situation(financial_data)
                        st.session_state.results = {
                            'analysis': analysis,
                            'input_data': financial_data
                        }
                    st.success("✅ Analysis Complete!")
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

with col2:
    st.subheader("📋 Analysis Results")
    
    if st.session_state.results:
        results = st.session_state.results
        analysis = results['analysis']
        data = results['input_data']
        
        # Calculate metrics
        monthly_income = data['annual_income'] / 12
        monthly_surplus = monthly_income - data['monthly_expenses']
        debt_to_savings = (
            data['total_loans'] / data['total_savings']
            if data['total_savings'] > 0
            else float('inf')
        )
        savings_rate = (monthly_surplus / monthly_income * 100) if monthly_income > 0 else 0
        
        # Display metrics in columns
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric(
                "Monthly Income",
                f"${monthly_income:,.0f}",
                delta=None
            )
            st.metric(
                "Debt-to-Savings Ratio",
                f"{debt_to_savings:.2f}" if debt_to_savings != float('inf') else "∞",
                delta=None
            )
        
        with metric_col2:
            st.metric(
                "Monthly Surplus",
                f"${monthly_surplus:,.0f}",
                delta=None
            )
            st.metric(
                "Savings Rate",
                f"{savings_rate:.1f}%",
                delta=None
            )
        
        st.divider()
        
        # Display analysis sections
        with st.expander("📊 Initial Analysis", expanded=True):
            st.markdown(analysis['initial_analysis'])
        
        with st.expander("📈 Detailed Metrics", expanded=True):
            st.markdown(analysis['detailed_metrics'])
        
        with st.expander("💡 Recommendations", expanded=True):
            st.markdown(analysis['recommendations'])
        
        st.divider()
        
        # Download report
        report_text = f"""
# Financial Analysis Report

## Your Financial Data
- Annual Income: ${data['annual_income']:,.2f}
- Total Savings: ${data['total_savings']:,.2f}
- Total Loans: ${data['total_loans']:,.2f}
- Monthly Expenses: ${data['monthly_expenses']:,.2f}
- Investment Amount: ${data['investment_amount']:,.2f}

## Key Metrics
- Monthly Income: ${monthly_income:,.2f}
- Monthly Surplus: ${monthly_surplus:,.2f}
- Debt-to-Savings Ratio: {debt_to_savings:.2f if debt_to_savings != float('inf') else '∞'}
- Savings Rate: {savings_rate:.1f}%

## Initial Analysis
{analysis['initial_analysis']}

## Detailed Metrics
{analysis['detailed_metrics']}

## Recommendations
{analysis['recommendations']}
"""
        
        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name="financial_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    else:
        st.info("👈 Fill in your financial information and click 'Analyze' to get started")

# Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📚 About This App")
st.sidebar.markdown("""
This Financial Analyzer uses **Anthropic's Claude AI** to provide:

- **Risk Assessment**: Get a 0-100 risk score
- **Financial Metrics**: Understand your debt-to-savings ratio
- **Gain Opportunities**: Identify ways to improve your finances
- **Personalized Recommendations**: Get 5 specific action items

### Input Fields
1. **Annual Income** - Your yearly earnings
2. **Total Savings** - Cash & liquid assets
3. **Total Loans** - All debt
4. **Monthly Expenses** - Average spending
5. **Investment Amount** - Portfolio value

### Risk Levels
- 🟢 **Low (0-25)**: Strong position, minimal debt
- 🟡 **Medium (26-50)**: Manageable, some concerns
- 🟠 **High (51-75)**: Significant concerns
- 🔴 **Critical (76-100)**: Immediate action needed
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🔗 Links")
st.sidebar.markdown("""
- [GitHub Repository](https://github.com/Jay202425/anthropic)
- [Anthropic API Docs](https://docs.anthropic.com)
- [Streamlit Documentation](https://docs.streamlit.io)
""")

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Financial Analyzer | Built with Anthropic Claude & Streamlit")
