"""
Professional Insurance Premium Calculator - Flask Application
Minimal infrastructure with sophisticated actuarial business logic
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from product_manager import ProfessionalProductManager
from regulatory_engine import ProfessionalRegulatoryEngine
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'professional-actuarial-demo-2024'

# Initialize professional components
product_manager = ProfessionalProductManager()
regulatory_engine = ProfessionalRegulatoryEngine()


@app.route('/')
def index():
    """Main quote interface"""
    return render_template('index.html')


@app.route('/api/quote', methods=['POST'])
def generate_quote():
    """Generate professional insurance quote"""
    try:
        data = request.get_json()
        
        # Extract applicant data
        applicant_data = {
            'name': data.get('name', ''),
            'age': int(data.get('age', 30)),
            'gender': data.get('gender', 'male'),
            'date_of_birth': data.get('date_of_birth', ''),
            'medical_history': {
                'conditions': data.get('medical_conditions', []),
                'height': float(data.get('height', 70)),
                'weight': float(data.get('weight', 170))
            },
            'lifestyle': {
                'smoking_status': data.get('smoking_status', 'non_smoker'),
                'alcohol_use': data.get('alcohol_use', 'moderate_use'),
                'hazardous_activities': data.get('hazardous_activities', [])
            },
            'occupation': {
                'title': data.get('occupation_title', ''),
                'class': int(data.get('occupation_class', 2))
            },
            'financial_info': {
                'annual_income': float(data.get('annual_income', 100000)),
                'net_worth': float(data.get('net_worth', 200000)),
                'total_debt': float(data.get('total_debt', 50000))
            },
            'beneficiary': data.get('beneficiary', '')
        }
        
        # Extract product details
        product_type = data.get('product_type', 'term_life')
        coverage_amount = int(data.get('coverage_amount', 500000))
        policy_term = int(data.get('policy_term', 20))
        
        # Generate quote based on product type
        if product_type in ['term_life', 'whole_life']:
            quote = product_manager.generate_life_insurance_quote(
                applicant_data,
                coverage_amount,
                policy_term,
                product_type
            )
        elif product_type == 'disability_income':
            monthly_benefit = int(data.get('monthly_benefit', 3000))
            benefit_period = data.get('benefit_period', 'to_age_65')
            waiting_period = int(data.get('waiting_period', 90))
            
            quote = product_manager.generate_disability_insurance_quote(
                applicant_data,
                monthly_benefit,
                benefit_period,
                waiting_period
            )
        elif product_type == 'critical_illness':
            quote = product_manager.generate_critical_illness_quote(
                applicant_data,
                coverage_amount
            )
        else:
            return jsonify({'error': 'Invalid product type'}), 400
        
        # Format response
        response = {
            'success': True,
            'quote': {
                'product_name': quote.product_name,
                'monthly_premium': round(quote.premium_quote.gross_premium, 2),
                'annual_premium': round(quote.premium_quote.gross_premium * 12, 2),
                'coverage_amount': coverage_amount,
                'risk_multiplier': round(quote.risk_assessment.overall_risk_multiplier, 2),
                'underwriting_decision': quote.risk_assessment.underwriting_decision.value,
                'approved_coverage': quote.risk_assessment.maximum_coverage,
                'breakdown': quote.premium_quote.breakdown,
                'policy_details': quote.policy_details,
                'explanation': quote.premium_quote.explanation,
                'underwriter_notes': quote.underwriter_notes,
                'quote_valid_until': quote.quote_valid_until
            },
            'risk_assessment': {
                'overall_risk_multiplier': quote.risk_assessment.overall_risk_multiplier,
                'medical_risk_multiplier': quote.risk_assessment.medical_risk_multiplier,
                'lifestyle_risk_multiplier': quote.risk_assessment.lifestyle_risk_multiplier,
                'occupation_risk_multiplier': quote.risk_assessment.occupation_risk_multiplier,
                'financial_risk_score': quote.risk_assessment.financial_risk_score,
                'risk_factors': quote.risk_assessment.risk_factors_identified,
                'decision': quote.risk_assessment.underwriting_decision.value
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error generating quote: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error generating quote: {str(e)}'
        }), 500


@app.route('/api/multi-quote', methods=['POST'])
def generate_multi_quote():
    """Generate quotes for multiple products"""
    try:
        data = request.get_json()
        
        # Extract applicant data (same as single quote)
        applicant_data = {
            'name': data.get('name', ''),
            'age': int(data.get('age', 30)),
            'gender': data.get('gender', 'male'),
            'medical_history': {
                'conditions': data.get('medical_conditions', []),
                'height': float(data.get('height', 70)),
                'weight': float(data.get('weight', 170))
            },
            'lifestyle': {
                'smoking_status': data.get('smoking_status', 'non_smoker'),
                'alcohol_use': data.get('alcohol_use', 'moderate_use'),
                'hazardous_activities': data.get('hazardous_activities', [])
            },
            'occupation': {
                'title': data.get('occupation_title', ''),
                'class': int(data.get('occupation_class', 2))
            },
            'financial_info': {
                'annual_income': float(data.get('annual_income', 100000)),
                'net_worth': float(data.get('net_worth', 200000)),
                'total_debt': float(data.get('total_debt', 50000))
            }
        }
        
        # Extract requested products
        requested_products = data.get('products', [])
        
        # Generate multi-product quotes
        quotes = product_manager.generate_multi_product_quote(applicant_data, requested_products)
        
        # Format response
        formatted_quotes = []
        for quote in quotes:
            formatted_quote = {
                'product_type': quote.product_type,
                'product_name': quote.product_name,
                'monthly_premium': round(quote.premium_quote.gross_premium, 2),
                'annual_premium': round(quote.premium_quote.gross_premium * 12, 2),
                'risk_multiplier': round(quote.risk_assessment.overall_risk_multiplier, 2),
                'underwriting_decision': quote.risk_assessment.underwriting_decision.value,
                'approved_coverage': quote.risk_assessment.maximum_coverage,
                'explanation': quote.premium_quote.explanation
            }
            formatted_quotes.append(formatted_quote)
        
        return jsonify({
            'success': True,
            'quotes': formatted_quotes
        })
        
    except Exception as e:
        print(f"Error generating multi-quote: {e}")
        return jsonify({
            'success': False,
            'error': f'Error generating quotes: {str(e)}'
        }), 500


@app.route('/api/reserves', methods=['POST'])
def calculate_reserves():
    """Calculate regulatory reserves for policy portfolio"""
    try:
        data = request.get_json()
        policy_portfolio = data.get('policies', [])
        
        # Calculate reserves
        reserve_calculation = regulatory_engine.calculate_comprehensive_reserves(policy_portfolio)
        
        response = {
            'success': True,
            'reserves': {
                'policy_reserves': round(reserve_calculation.policy_reserves, 2),
                'unearned_premium_reserves': round(reserve_calculation.unearned_premium_reserves, 2),
                'claims_reserves': round(reserve_calculation.claims_reserves, 2),
                'total_reserves': round(reserve_calculation.total_reserves, 2),
                'solvency_margin': round(reserve_calculation.solvency_margin, 2),
                'risk_based_capital': round(reserve_calculation.risk_based_capital, 2),
                'regulatory_requirements_met': reserve_calculation.regulatory_requirements_met,
                'compliance_notes': reserve_calculation.compliance_notes
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error calculating reserves: {e}")
        return jsonify({
            'success': False,
            'error': f'Error calculating reserves: {str(e)}'
        }), 500


@app.route('/api/product-info')
def get_product_info():
    """Get available product information"""
    try:
        with open('data/product_definitions.json', 'r') as f:
            products = json.load(f)['products']
        
        # Format product information for frontend
        formatted_products = {}
        for product_type, product_data in products.items():
            formatted_products[product_type] = {
                'name': product_data['name'],
                'description': product_data['description'],
                'min_coverage': product_data.get('min_coverage', 0),
                'max_coverage': product_data.get('max_coverage', 10000000),
                'min_age': product_data['min_age'],
                'max_age': product_data['max_age']
            }
        
        return jsonify({
            'success': True,
            'products': formatted_products
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error loading product info: {str(e)}'
        }), 500


@app.route('/api/health')
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Professional Insurance Premium Calculator'
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Professional Insurance Premium Calculator...")
    print("Access the application at: http://localhost:5000")
    print("API Documentation:")
    print("  POST /api/quote - Generate single product quote")
    print("  POST /api/multi-quote - Generate multiple product quotes")
    print("  POST /api/reserves - Calculate regulatory reserves")
    print("  GET /api/product-info - Get product information")
    print("  GET /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5001)