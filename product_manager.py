"""
Professional Insurance Product Manager
Handles multiple insurance product types with distinct calculation methodologies
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from actuarial_calculator import ActuarialCalculator, QuoteResult
from underwriting_engine import ProfessionalUnderwritingEngine, RiskAssessment


@dataclass
class ProductQuote:
    """Complete insurance product quote with underwriting"""
    product_type: str
    product_name: str
    premium_quote: QuoteResult
    risk_assessment: RiskAssessment
    policy_details: Dict
    quote_valid_until: str
    underwriter_notes: str


class ProfessionalProductManager:
    """Manages multiple insurance products with professional methodologies"""
    
    def __init__(self):
        self.calculator = ActuarialCalculator()
        self.underwriter = ProfessionalUnderwritingEngine()
        self.product_definitions = self._load_json_data('data/product_definitions.json')
    
    def _load_json_data(self, filepath: str) -> Dict:
        """Load product data from JSON files"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Using empty data.")
            return {}
    
    def generate_life_insurance_quote(self,
                                    applicant_data: Dict,
                                    coverage_amount: int,
                                    policy_term: int,
                                    product_type: str = 'term_life') -> ProductQuote:
        """
        Generate comprehensive life insurance quote with underwriting
        
        Args:
            applicant_data: Complete applicant information including demographics, health, lifestyle
            coverage_amount: Requested death benefit
            policy_term: Policy term in years
            product_type: 'term_life' or 'whole_life'
        """
        
        # Perform comprehensive underwriting
        risk_assessment = self.underwriter.perform_comprehensive_risk_assessment(
            applicant_data, product_type, coverage_amount
        )
        
        # Adjust coverage based on underwriting decision
        approved_coverage = min(coverage_amount, risk_assessment.maximum_coverage)
        
        if approved_coverage == 0:
            # Application declined
            return self._create_declined_quote(product_type, risk_assessment)
        
        # Extract basic demographics for actuarial calculation
        age = applicant_data.get('age', 30)
        gender = applicant_data.get('gender', 'male')
        
        # Create risk factors dictionary for premium calculation
        risk_factors = {
            'medical_conditions': applicant_data.get('medical_history', {}).get('conditions', []),
            'smoking_status': applicant_data.get('lifestyle', {}).get('smoking_status', 'non_smoker'),
            'hazardous_activities': applicant_data.get('lifestyle', {}).get('hazardous_activities', [])
        }
        
        # Calculate premium using actuarial methods
        premium_quote = self.calculator.calculate_life_insurance_premium(
            age=age,
            gender=gender,
            coverage_amount=approved_coverage,
            policy_term=policy_term,
            product_type=product_type,
            risk_factors=risk_factors
        )
        
        # Adjust premium based on underwriting risk multiplier
        premium_quote.gross_premium *= risk_assessment.overall_risk_multiplier
        premium_quote.risk_multiplier = risk_assessment.overall_risk_multiplier
        
        # Create policy details
        policy_details = self._create_life_policy_details(
            applicant_data, approved_coverage, policy_term, product_type
        )
        
        return ProductQuote(
            product_type=product_type,
            product_name=self.product_definitions['products'][product_type]['name'],
            premium_quote=premium_quote,
            risk_assessment=risk_assessment,
            policy_details=policy_details,
            quote_valid_until=self._calculate_quote_expiry(),
            underwriter_notes=risk_assessment.underwriting_notes
        )
    
    def generate_disability_insurance_quote(self,
                                          applicant_data: Dict,
                                          monthly_benefit: int,
                                          benefit_period: str = 'to_age_65',
                                          waiting_period: int = 90) -> ProductQuote:
        """Generate comprehensive disability insurance quote"""
        
        product_type = 'disability_income'
        
        # Perform underwriting assessment
        risk_assessment = self.underwriter.perform_comprehensive_risk_assessment(
            applicant_data, product_type, monthly_benefit * 12  # Convert to annual for underwriting
        )
        
        approved_monthly_benefit = min(monthly_benefit, risk_assessment.maximum_coverage // 12)
        
        if approved_monthly_benefit == 0:
            return self._create_declined_quote(product_type, risk_assessment)
        
        # Extract applicant information
        age = applicant_data.get('age', 30)
        gender = applicant_data.get('gender', 'male')
        occupation_class = applicant_data.get('occupation', {}).get('class', 2)
        
        # Calculate disability premium
        premium_quote = self.calculator.calculate_disability_premium(
            age=age,
            gender=gender,
            occupation_class=occupation_class,
            monthly_benefit=approved_monthly_benefit,
            benefit_period=benefit_period,
            waiting_period=waiting_period
        )
        
        # Apply underwriting risk adjustment
        premium_quote.gross_premium *= risk_assessment.overall_risk_multiplier
        premium_quote.risk_multiplier = risk_assessment.overall_risk_multiplier
        
        # Create policy details
        policy_details = self._create_disability_policy_details(
            applicant_data, approved_monthly_benefit, benefit_period, waiting_period
        )
        
        return ProductQuote(
            product_type=product_type,
            product_name=self.product_definitions['products'][product_type]['name'],
            premium_quote=premium_quote,
            risk_assessment=risk_assessment,
            policy_details=policy_details,
            quote_valid_until=self._calculate_quote_expiry(),
            underwriter_notes=risk_assessment.underwriting_notes
        )
    
    def generate_critical_illness_quote(self,
                                      applicant_data: Dict,
                                      coverage_amount: int) -> ProductQuote:
        """Generate critical illness insurance quote"""
        
        product_type = 'critical_illness'
        
        # Perform underwriting
        risk_assessment = self.underwriter.perform_comprehensive_risk_assessment(
            applicant_data, product_type, coverage_amount
        )
        
        approved_coverage = min(coverage_amount, risk_assessment.maximum_coverage)
        
        if approved_coverage == 0:
            return self._create_declined_quote(product_type, risk_assessment)
        
        # Calculate critical illness premium using specialized methodology
        premium_quote = self._calculate_critical_illness_premium(
            applicant_data, approved_coverage, risk_assessment
        )
        
        policy_details = self._create_critical_illness_policy_details(
            applicant_data, approved_coverage
        )
        
        return ProductQuote(
            product_type=product_type,
            product_name=self.product_definitions['products'][product_type]['name'],
            premium_quote=premium_quote,
            risk_assessment=risk_assessment,
            policy_details=policy_details,
            quote_valid_until=self._calculate_quote_expiry(),
            underwriter_notes=risk_assessment.underwriting_notes
        )
    
    def generate_multi_product_quote(self,
                                   applicant_data: Dict,
                                   requested_products: List[Dict]) -> List[ProductQuote]:
        """Generate quotes for multiple products simultaneously"""
        
        quotes = []
        
        for product_request in requested_products:
            product_type = product_request['type']
            
            try:
                if product_type in ['term_life', 'whole_life']:
                    quote = self.generate_life_insurance_quote(
                        applicant_data,
                        product_request['coverage_amount'],
                        product_request.get('policy_term', 20),
                        product_type
                    )
                elif product_type == 'disability_income':
                    quote = self.generate_disability_insurance_quote(
                        applicant_data,
                        product_request['monthly_benefit'],
                        product_request.get('benefit_period', 'to_age_65'),
                        product_request.get('waiting_period', 90)
                    )
                elif product_type == 'critical_illness':
                    quote = self.generate_critical_illness_quote(
                        applicant_data,
                        product_request['coverage_amount']
                    )
                else:
                    continue  # Skip unknown product types
                
                quotes.append(quote)
                
            except Exception as e:
                print(f"Error generating quote for {product_type}: {e}")
                continue
        
        return quotes
    
    def _calculate_critical_illness_premium(self,
                                          applicant_data: Dict,
                                          coverage_amount: int,
                                          risk_assessment: RiskAssessment) -> QuoteResult:
        """Calculate critical illness premium using morbidity tables"""
        
        age = applicant_data.get('age', 30)
        gender = applicant_data.get('gender', 'male')
        
        # Load critical illness morbidity data
        ci_tables = self.calculator.morbidity_tables.get('critical_illness_tables', {})
        product = self.product_definitions['products']['critical_illness']
        
        # Calculate combined morbidity rate for all covered conditions
        total_morbidity_rate = 0.0
        closest_age = self.calculator._find_closest_age(age, ci_tables['conditions']['cancer'])
        
        for condition in product['covered_conditions']:
            if condition in ci_tables['conditions']:
                condition_rate = ci_tables['conditions'][condition][str(closest_age)][gender]
                total_morbidity_rate += condition_rate
        
        # Calculate present value of benefits
        discount_rate = self.calculator.mortality_tables['discount_rates']['standard']
        benefit_pv = 0.0
        
        # Critical illness typically pays out once, so calculate probability over policy term
        for year in range(20):  # 20-year term typical for CI
            pv_factor = 1 / ((1 + discount_rate) ** year)
            benefit_pv += coverage_amount * total_morbidity_rate * pv_factor
        
        # Calculate premium present value (similar to term life)
        premium_pv = self.calculator._calculate_premium_present_value(20, age, gender)
        
        # Net premium
        net_premium = benefit_pv / premium_pv if premium_pv > 0 else 0
        
        # Add expense loads
        expense_load = product['expense_load']
        profit_margin = product['profit_margin']
        commission = product['commission']
        
        gross_premium = net_premium * (1 + expense_load + profit_margin + commission)
        
        # Apply underwriting risk multiplier
        gross_premium *= risk_assessment.overall_risk_multiplier
        
        # Calculate reserves
        reserves = coverage_amount * self.product_definitions['regulatory_requirements']['reserve_factors']['critical_illness']
        
        breakdown = {
            'base_morbidity_rate': total_morbidity_rate,
            'net_premium': net_premium,
            'gross_premium': gross_premium,
            'annual_premium': gross_premium * 12,
            'covered_conditions': product['covered_conditions'],
            'reserves': reserves
        }
        
        explanation = f"""Critical Illness Insurance Calculation:

Applicant: {age}-year-old {gender}
Coverage: ${coverage_amount:,} lump sum benefit
Covered Conditions: {', '.join(product['covered_conditions'])}
Combined Morbidity Rate: {total_morbidity_rate:.4f}
Risk Multiplier: {risk_assessment.overall_risk_multiplier:.2f}x

Premium calculated using professional morbidity tables for critical illness conditions with proper actuarial present value methodology."""
        
        return QuoteResult(
            gross_premium=gross_premium,
            net_premium=net_premium,
            expense_load=expense_load,
            profit_margin=profit_margin,
            commission=commission,
            reserves=reserves,
            risk_multiplier=risk_assessment.overall_risk_multiplier,
            breakdown=breakdown,
            explanation=explanation
        )
    
    def _create_life_policy_details(self,
                                  applicant_data: Dict,
                                  coverage_amount: int,
                                  policy_term: int,
                                  product_type: str) -> Dict:
        """Create detailed policy information for life insurance"""
        
        product = self.product_definitions['products'][product_type]
        
        return {
            'policy_type': product['name'],
            'insured_name': applicant_data.get('name', 'Applicant'),
            'date_of_birth': applicant_data.get('date_of_birth', ''),
            'gender': applicant_data.get('gender', '').title(),
            'death_benefit': coverage_amount,
            'policy_term': f"{policy_term} years",
            'premium_payment_period': f"{policy_term} years" if product_type == 'term_life' else 'Life',
            'beneficiary': applicant_data.get('beneficiary', 'To be designated'),
            'policy_features': self._get_life_policy_features(product_type),
            'exclusions': self._get_standard_exclusions('life'),
            'conversion_options': self._get_conversion_options(product_type),
            'renewal_provisions': self._get_renewal_provisions(product_type)
        }
    
    def _create_disability_policy_details(self,
                                        applicant_data: Dict,
                                        monthly_benefit: int,
                                        benefit_period: str,
                                        waiting_period: int) -> Dict:
        """Create detailed policy information for disability insurance"""
        
        return {
            'policy_type': 'Disability Income Insurance',
            'insured_name': applicant_data.get('name', 'Applicant'),
            'occupation': applicant_data.get('occupation', {}).get('title', 'Unknown'),
            'monthly_benefit': monthly_benefit,
            'benefit_period': benefit_period.replace('_', ' ').title(),
            'waiting_period': f"{waiting_period} days",
            'definition_of_disability': 'Own occupation for first 24 months, then any occupation',
            'cost_of_living_adjustment': 'Available with 3% annual increase',
            'exclusions': self._get_standard_exclusions('disability'),
            'renewability': 'Guaranteed renewable to age 65',
            'partial_benefits': 'Proportionate benefits for partial disability'
        }
    
    def _create_critical_illness_policy_details(self,
                                              applicant_data: Dict,
                                              coverage_amount: int) -> Dict:
        """Create detailed policy information for critical illness insurance"""
        
        product = self.product_definitions['products']['critical_illness']
        
        return {
            'policy_type': 'Critical Illness Insurance',
            'insured_name': applicant_data.get('name', 'Applicant'),
            'lump_sum_benefit': coverage_amount,
            'covered_conditions': product['covered_conditions'],
            'survival_period': '30 days from diagnosis',
            'policy_term': '20 years',
            'renewability': 'Guaranteed renewable',
            'exclusions': self._get_standard_exclusions('critical_illness'),
            'benefit_payment': 'Lump sum upon first diagnosis of covered condition',
            'return_of_premium': 'Available at end of term if no claims'
        }
    
    def _create_declined_quote(self, product_type: str, risk_assessment: RiskAssessment) -> ProductQuote:
        """Create quote for declined application"""
        
        # Create a minimal quote result for declined application
        declined_quote = QuoteResult(
            gross_premium=0.0,
            net_premium=0.0,
            expense_load=0.0,
            profit_margin=0.0,
            commission=0.0,
            reserves=0.0,
            risk_multiplier=risk_assessment.overall_risk_multiplier,
            breakdown={'status': 'declined'},
            explanation="Application declined due to excessive risk factors."
        )
        
        return ProductQuote(
            product_type=product_type,
            product_name=f"Declined - {self.product_definitions['products'][product_type]['name']}",
            premium_quote=declined_quote,
            risk_assessment=risk_assessment,
            policy_details={'status': 'Application Declined'},
            quote_valid_until='N/A',
            underwriter_notes=risk_assessment.underwriting_notes
        )
    
    def _get_life_policy_features(self, product_type: str) -> List[str]:
        """Get standard policy features for life insurance"""
        common_features = [
            'Accelerated death benefit for terminal illness',
            'Waiver of premium for disability',
            '31-day grace period for premium payments'
        ]
        
        if product_type == 'whole_life':
            common_features.extend([
                'Cash value accumulation',
                'Policy loan availability',
                'Dividend participation (if applicable)'
            ])
        elif product_type == 'term_life':
            common_features.append('Convertible to permanent insurance')
        
        return common_features
    
    def _get_standard_exclusions(self, product_type: str) -> List[str]:
        """Get standard policy exclusions"""
        exclusions = {
            'life': [
                'Suicide within first 2 years',
                'Death due to war or military service',
                'Death while committing a felony'
            ],
            'disability': [
                'Pre-existing conditions (first 12 months)',
                'Intentionally self-inflicted injuries',
                'Disabilities due to war or military service',
                'Normal pregnancy and childbirth'
            ],
            'critical_illness': [
                'Pre-existing conditions',
                'Self-inflicted conditions',
                'Conditions due to alcohol or drug abuse',
                'Conditions diagnosed within first 90 days'
            ]
        }
        
        return exclusions.get(product_type, [])
    
    def _get_conversion_options(self, product_type: str) -> str:
        """Get conversion options for term life insurance"""
        if product_type == 'term_life':
            return 'Convertible to whole life or universal life without medical exam within first 10 years'
        return 'Not applicable'
    
    def _get_renewal_provisions(self, product_type: str) -> str:
        """Get renewal provisions"""
        if product_type == 'term_life':
            return 'Guaranteed renewable to age 95 with level premiums during initial term'
        elif product_type == 'whole_life':
            return 'Permanent coverage with guaranteed premiums'
        return 'As specified in policy contract'
    
    def _calculate_quote_expiry(self) -> str:
        """Calculate quote expiration date (typically 30 days)"""
        from datetime import datetime, timedelta
        expiry = datetime.now() + timedelta(days=30)
        return expiry.strftime('%Y-%m-%d')


# Example usage and testing
if __name__ == "__main__":
    # Example applicant data
    sample_applicant = {
        'name': 'John Smith',
        'age': 35,
        'gender': 'male',
        'date_of_birth': '1988-05-15',
        'medical_history': {
            'conditions': ['hypertension_controlled'],
            'height': 70,  # inches
            'weight': 180  # pounds
        },
        'lifestyle': {
            'smoking_status': 'non_smoker',
            'alcohol_use': 'moderate_use',
            'hazardous_activities': []
        },
        'occupation': {
            'title': 'Software Engineer',
            'class': 1
        },
        'financial_info': {
            'annual_income': 120000,
            'net_worth': 300000,
            'total_debt': 40000
        },
        'beneficiary': 'Jane Smith (Spouse)'
    }
    
    # Test the product manager
    product_manager = ProfessionalProductManager()
    
    # Generate term life quote
    life_quote = product_manager.generate_life_insurance_quote(
        sample_applicant,
        coverage_amount=500000,
        policy_term=20,
        product_type='term_life'
    )
    
    print(f"Term Life Quote: ${life_quote.premium_quote.gross_premium:.2f}/month")
    print(f"Risk Assessment: {life_quote.risk_assessment.underwriting_decision.value}")
    print(f"Risk Multiplier: {life_quote.risk_assessment.overall_risk_multiplier:.2f}x")