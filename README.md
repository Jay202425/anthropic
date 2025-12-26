# Financial Risk & Gain Analysis Model using Anthropic Claude

A sophisticated financial analysis tool that uses Claude AI to assess risk levels and identify gain opportunities based on personal financial inputs like loans, savings, income, and expenses.

## Features

- **Multi-turn Conversations**: Uses multi-turn dialogue with Claude for deeper financial insights
- **Risk Assessment**: Calculates risk scores and identifies key risk factors
- **Gain Identification**: Identifies opportunities for financial growth
- **Personalized Recommendations**: Provides actionable financial advice
- **Interactive CLI**: Easy-to-use command-line interface for entering financial data
- **Batch Analysis**: Analyze multiple financial profiles programmatically

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd c:\Users\Administrator\Anthropic
   ```

2. **Install dependencies** (already done in virtual environment):
   ```bash
   pip install anthropic python-dotenv
   ```

3. **Set up your API key**:
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key to the `.env` file:
     ```
     ANTHROPIC_API_KEY=sk-ant-...
     ```

## Usage

### Interactive Mode (Manual Input)

Run the interactive analyzer to enter your financial information:

```bash
python financial_analyzer.py
```

You'll be prompted to enter:
- Annual Income
- Total Savings
- Total Loans/Debt
- Monthly Expenses
- Current Investment Amount

### Batch Analysis (Sample Profiles)

Run the sample analysis with predefined profiles:

```bash
python sample_analysis.py
```

This analyzes 5 different financial profiles:
- Young Professional
- Mid-Career Developer
- Small Business Owner
- Conservative Saver
- High Debt Profile

## How It Works

### The FinancialAnalyzer Class

```python
analyzer = FinancialAnalyzer()
analysis = analyzer.analyze_financial_situation(financial_data)
```

The analyzer performs a multi-turn conversation with Claude:

1. **Initial Analysis**: Analyzes the raw financial data and provides initial insights
2. **Detailed Metrics**: Generates risk scores, identifies risk factors and gain opportunities
3. **Recommendations**: Provides 5 specific, actionable financial recommendations

### Key Metrics Generated

- **Debt-to-Savings Ratio**: Shows financial stability
- **Risk Score**: 0-100 scale (0=no risk, 100=maximum risk)
- **Risk Level**: Low, Medium, High, or Critical
- **Risk Factors**: Top factors contributing to financial risk
- **Gain Opportunities**: Specific opportunities to improve finances
- **Actionable Recommendations**: Concrete steps to reduce risk and increase gains

## Example Output

```
=============================================================
FINANCIAL ANALYSIS RESULTS
=============================================================

📊 INITIAL ANALYSIS:
Based on your financial profile, here's my comprehensive analysis...

📈 DETAILED METRICS:
Risk Score: 45/100
Risk Level: Medium
Top Risk Factors:
1. Debt-to-income ratio of 64%
2. Limited emergency fund...

💡 RECOMMENDATIONS:
1. Build emergency fund to 6 months of expenses
2. Create aggressive loan repayment plan...
```

## Project Structure

```
c:\Users\Administrator\Anthropic\
├── financial_analyzer.py      # Main analyzer class and CLI
├── sample_analysis.py          # Sample profile analysis
├── .env.example                # Configuration template
└── README.md                   # This file
```

## API Model

The system uses Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`), which provides:
- Advanced reasoning for financial analysis
- Multi-turn conversation capability
- Accurate financial metrics calculation
- Contextual recommendations

## Financial Inputs

The model accepts and analyzes:

| Input | Description | Type |
|-------|-------------|------|
| Annual Income | Total yearly earnings | Float |
| Total Savings | Cash savings and liquid assets | Float |
| Total Loans | All outstanding debt (car, student, mortgage, credit cards) | Float |
| Monthly Expenses | Average monthly spending | Float |
| Investment Amount | Current investment portfolio value | Float |

## Risk Categories

- **Low Risk** (0-25): Strong financial position, minimal debt, good savings
- **Medium Risk** (26-50): Manageable debt, moderate savings, some concerns
- **High Risk** (51-75): High debt levels, low savings, significant concerns
- **Critical Risk** (76-100): Severe financial distress, immediate action needed

## Gain Opportunities

The analyzer identifies opportunities such as:
- Debt consolidation
- Investment diversification
- Emergency fund building
- Income optimization
- Expense reduction strategies

## Error Handling

The system includes error handling for:
- Invalid API keys
- Network errors
- Invalid user input
- Missing environment variables

## Requirements

- Python 3.8+
- Anthropic API account with available credits
- Virtual environment (recommended)

## Notes

- All financial data is processed in real-time through the Anthropic API
- Conversations are multi-turn for deeper analysis
- Each analysis may consume multiple API calls
- Keep your API key secure and never commit it to version control

## Future Enhancements

- Database storage of analysis history
- Comparative analysis across multiple profiles
- Goal-based recommendations
- Integration with financial APIs
- Export analysis to PDF/CSV
- Mobile app interface
- Machine learning for pattern recognition

## Support

For issues with the Anthropic API, visit: https://console.anthropic.com

For general financial advice disclaimers: This tool provides AI-generated insights based on the data provided. Always consult with a qualified financial advisor before making major financial decisions.
