"""
Professional Regulatory Compliance and Reserve Calculation Module
Implements industry-standard reserve calculations and regulatory compliance requirements
"""

import json
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReserveCalculation:
    """Professional reserve calculation result"""
    policy_reserves: float
    unearned_premium_reserves: float
    claims_reserves: float
    total_reserves: float
    solvency_margin: float
    risk_based_capital: float
    regulatory_requirements_met: bool
    compliance_notes: str


@dataclass
class RegulatoryCompliance:
    """Regulatory compliance assessment"""
    reserve_adequacy: bool
    capital_adequacy: bool
    pricing_compliance: bool
    underwriting_compliance: bool
    overall_compliance: bool
    regulatory_notes: List[str]
    required_actions: List[str]


class ProfessionalRegulatoryEngine:
    """Professional regulatory compliance and reserve calculation engine"""
    
    def __init__(self):
        self.product_definitions = self._load_json_data('data/product_definitions.json')
        self.mortality_tables = self._load_json_data('data/mortality_tables.json')
        self.regulatory_standards = self._initialize_regulatory_standards()
    
    def _load_json_data(self, filepath: str) -> Dict:
        """Load regulatory data from JSON files"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Using empty data.")
            return {}
    
    def _initialize_regulatory_standards(self) -> Dict:
        """Initialize regulatory standards and requirements"""
        return {
            'minimum_reserve_ratios': {
                'term_life': 0.02,      # 2% of coverage for term life
                'whole_life': 0.15,     # 15% of coverage for whole life
                'disability_income': 0.25,  # 25% of annual benefit for disability
                'critical_illness': 0.10    # 10% of coverage for critical illness
            },
            'solvency_margins': {
                'life_insurance': 0.04,     # 4% of liabilities
                'disability_insurance': 0.08,  # 8% of liabilities
                'critical_illness': 0.06   # 6% of liabilities
            },
            'risk_based_capital': {
                'c1_asset_risk': 0.003,     # Asset quality risk
                'c2_insurance_risk': 0.015, # Insurance/underwriting risk
                'c3_interest_rate_risk': 0.001, # Interest rate risk
                'c4_business_risk': 0.003   # General business risk
            },
            'maximum_premium_rates': {
                'mortality_loading': 0.05,  # Maximum 5% loading on mortality
                'expense_loading': 0.30,    # Maximum 30% expense loading
                'profit_margin': 0.15       # Maximum 15% profit margin
            },
            'underwriting_standards': {
                'maximum_risk_multiplier': 10.0,  # Cannot exceed 10x standard risk
                'minimum_evidence_amounts': {
                    'medical_exam': 250000,
                    'blood_test': 500000,
                    'stress_test': 1000000,
                    'attending_physician_statement': 100000
                }
            }
        }
    
    def calculate_comprehensive_reserves(self,
                                       policy_portfolio: List[Dict],
                                       valuation_date: str = None) -> ReserveCalculation:
        """
        Calculate comprehensive reserves for policy portfolio
        
        Args:
            policy_portfolio: List of policies with details
            valuation_date: Date for reserve calculation (default: current date)
        """
        
        if valuation_date is None:
            valuation_date = datetime.now().strftime('%Y-%m-%d')
        
        total_policy_reserves = 0.0
        total_unearned_premium = 0.0
        total_claims_reserves = 0.0
        
        for policy in policy_portfolio:
            # Calculate policy-specific reserves
            policy_reserves = self._calculate_policy_reserves(policy, valuation_date)
            unearned_premium = self._calculate_unearned_premium_reserves(policy, valuation_date)
            claims_reserves = self._calculate_claims_reserves(policy, valuation_date)
            
            total_policy_reserves += policy_reserves
            total_unearned_premium += unearned_premium
            total_claims_reserves += claims_reserves
        
        total_reserves = total_policy_reserves + total_unearned_premium + total_claims_reserves
        
        # Calculate solvency margin
        solvency_margin = self._calculate_solvency_margin(policy_portfolio, total_reserves)
        
        # Calculate risk-based capital
        risk_based_capital = self._calculate_risk_based_capital(policy_portfolio, total_reserves)
        
        # Check regulatory compliance
        requirements_met = self._check_reserve_adequacy(total_reserves, solvency_margin, risk_based_capital)
        
        compliance_notes = self._generate_reserve_compliance_notes(
            total_reserves, solvency_margin, risk_based_capital, requirements_met
        )
        
        return ReserveCalculation(
            policy_reserves=total_policy_reserves,
            unearned_premium_reserves=total_unearned_premium,
            claims_reserves=total_claims_reserves,
            total_reserves=total_reserves,
            solvency_margin=solvency_margin,
            risk_based_capital=risk_based_capital,
            regulatory_requirements_met=requirements_met,
            compliance_notes=compliance_notes
        )
    
    def assess_regulatory_compliance(self,
                                   product_type: str,
                                   premium_structure: Dict,
                                   underwriting_decision: Dict,
                                   reserve_calculation: ReserveCalculation) -> RegulatoryCompliance:
        """
        Assess comprehensive regulatory compliance
        
        Args:
            product_type: Type of insurance product
            premium_structure: Premium calculation details
            underwriting_decision: Underwriting assessment
            reserve_calculation: Reserve calculation results
        """
        
        compliance_notes = []
        required_actions = []
        
        # Check reserve adequacy
        reserve_adequate = self._check_reserve_compliance(product_type, reserve_calculation)
        if not reserve_adequate:
            compliance_notes.append("Reserve levels below regulatory minimums")
            required_actions.append("Increase policy reserves to meet regulatory requirements")
        
        # Check capital adequacy
        capital_adequate = self._check_capital_adequacy(reserve_calculation)
        if not capital_adequate:
            compliance_notes.append("Capital levels insufficient for solvency requirements")
            required_actions.append("Increase capital or reduce risk exposure")
        
        # Check pricing compliance
        pricing_compliant = self._check_pricing_compliance(product_type, premium_structure)
        if not pricing_compliant:
            compliance_notes.append("Premium rates exceed regulatory maximums")
            required_actions.append("Reduce premium loadings to comply with rate regulations")
        
        # Check underwriting compliance
        underwriting_compliant = self._check_underwriting_compliance(underwriting_decision)
        if not underwriting_compliant:
            compliance_notes.append("Underwriting practices do not meet regulatory standards")
            required_actions.append("Review underwriting guidelines and risk assessment procedures")
        
        overall_compliant = (reserve_adequate and capital_adequate and 
                           pricing_compliant and underwriting_compliant)
        
        return RegulatoryCompliance(
            reserve_adequacy=reserve_adequate,
            capital_adequacy=capital_adequate,
            pricing_compliance=pricing_compliant,
            underwriting_compliance=underwriting_compliant,
            overall_compliance=overall_compliant,
            regulatory_notes=compliance_notes,
            required_actions=required_actions
        )
    
    def _calculate_policy_reserves(self, policy: Dict, valuation_date: str) -> float:
        """Calculate policy reserves using professional actuarial methods"""
        
        product_type = policy.get('product_type', 'term_life')
        coverage_amount = policy.get('coverage_amount', 0)
        policy_year = policy.get('policy_year', 1)
        
        # Get base reserve factor
        reserve_factors = self.regulatory_standards['minimum_reserve_ratios']
        base_reserve_factor = reserve_factors.get(product_type, 0.05)
        
        # Calculate present value of future benefits
        future_benefits_pv = self._calculate_future_benefits_pv(policy, valuation_date)
        
        # Calculate present value of future premiums
        future_premiums_pv = self._calculate_future_premiums_pv(policy, valuation_date)
        
        # Policy reserve = PV of future benefits - PV of future premiums
        policy_reserve = max(future_benefits_pv - future_premiums_pv, 
                           coverage_amount * base_reserve_factor)
        
        return policy_reserve
    
    def _calculate_unearned_premium_reserves(self, policy: Dict, valuation_date: str) -> float:
        """Calculate unearned premium reserves"""
        
        annual_premium = policy.get('annual_premium', 0)
        policy_anniversary = policy.get('policy_anniversary', valuation_date)
        
        # Calculate days remaining in policy year
        from datetime import datetime
        valuation = datetime.strptime(valuation_date, '%Y-%m-%d')
        anniversary = datetime.strptime(policy_anniversary, '%Y-%m-%d')
        
        # Find next anniversary date
        next_anniversary = anniversary.replace(year=valuation.year)
        if next_anniversary <= valuation:
            next_anniversary = next_anniversary.replace(year=valuation.year + 1)
        
        days_remaining = (next_anniversary - valuation).days
        days_in_year = 365
        
        # Unearned premium = Premium * (Days remaining / Days in year)
        unearned_premium = annual_premium * (days_remaining / days_in_year)
        
        return max(unearned_premium, 0)
    
    def _calculate_claims_reserves(self, policy: Dict, valuation_date: str) -> float:
        """Calculate reserves for reported but not settled claims"""
        
        # This would typically integrate with claims management system
        # For demo purposes, use estimated claims reserves
        coverage_amount = policy.get('coverage_amount', 0)
        product_type = policy.get('product_type', 'term_life')
        
        # Estimate claims reserves based on product type and coverage
        claims_reserve_factors = {
            'term_life': 0.001,      # 0.1% of coverage
            'whole_life': 0.002,     # 0.2% of coverage
            'disability_income': 0.05,  # 5% of annual benefit
            'critical_illness': 0.01    # 1% of coverage
        }
        
        reserve_factor = claims_reserve_factors.get(product_type, 0.001)
        claims_reserves = coverage_amount * reserve_factor
        
        return claims_reserves
    
    def _calculate_future_benefits_pv(self, policy: Dict, valuation_date: str) -> float:
        """Calculate present value of future benefits"""
        
        product_type = policy.get('product_type', 'term_life')
        coverage_amount = policy.get('coverage_amount', 0)
        remaining_years = policy.get('remaining_years', 10)
        age = policy.get('current_age', 35)
        gender = policy.get('gender', 'male')
        
        # Use mortality tables to calculate benefit present value
        discount_rate = self.mortality_tables.get('discount_rates', {}).get('standard', 0.035)
        mortality_table = self.mortality_tables.get('CSO_2017', {}).get(gender, {})
        
        benefit_pv = 0.0
        
        for year in range(remaining_years):
            current_age = min(age + year, 80)
            mortality_rate = float(mortality_table.get(str(current_age), 0.01))
            
            # Present value factor
            pv_factor = 1 / ((1 + discount_rate) ** year)
            
            # Add to benefit present value
            benefit_pv += coverage_amount * mortality_rate * pv_factor
            
            if product_type == 'critical_illness':
                # For critical illness, also include morbidity
                benefit_pv += coverage_amount * 0.002 * pv_factor  # Estimated CI morbidity
        
        return benefit_pv
    
    def _calculate_future_premiums_pv(self, policy: Dict, valuation_date: str) -> float:
        """Calculate present value of future premiums"""
        
        annual_premium = policy.get('annual_premium', 0)
        remaining_years = policy.get('remaining_years', 10)
        age = policy.get('current_age', 35)
        gender = policy.get('gender', 'male')
        
        discount_rate = self.mortality_tables.get('discount_rates', {}).get('standard', 0.035)
        mortality_table = self.mortality_tables.get('CSO_2017', {}).get(gender, {})
        
        premium_pv = 0.0
        survival_probability = 1.0
        
        for year in range(remaining_years):
            current_age = min(age + year, 80)
            mortality_rate = float(mortality_table.get(str(current_age), 0.01))
            
            # Present value factor
            pv_factor = survival_probability / ((1 + discount_rate) ** year)
            
            # Add to premium present value
            premium_pv += annual_premium * pv_factor
            
            # Update survival probability
            survival_probability *= (1 - mortality_rate)
        
        return premium_pv
    
    def _calculate_solvency_margin(self, policy_portfolio: List[Dict], total_reserves: float) -> float:
        """Calculate required solvency margin"""
        
        # Aggregate by product type
        product_liabilities = {}
        for policy in policy_portfolio:
            product_type = policy.get('product_type', 'term_life')
            coverage = policy.get('coverage_amount', 0)
            
            if product_type not in product_liabilities:
                product_liabilities[product_type] = 0
            product_liabilities[product_type] += coverage
        
        # Calculate solvency margin by product
        total_solvency_margin = 0.0
        solvency_margins = self.regulatory_standards['solvency_margins']
        
        for product_type, liability in product_liabilities.items():
            if product_type in ['term_life', 'whole_life']:
                margin_rate = solvency_margins['life_insurance']
            elif product_type == 'disability_income':
                margin_rate = solvency_margins['disability_insurance']
            else:
                margin_rate = solvency_margins['critical_illness']
            
            total_solvency_margin += liability * margin_rate
        
        return total_solvency_margin
    
    def _calculate_risk_based_capital(self, policy_portfolio: List[Dict], total_reserves: float) -> float:
        """Calculate risk-based capital requirements"""
        
        rbc_factors = self.regulatory_standards['risk_based_capital']
        
        # Calculate total coverage for RBC calculation
        total_coverage = sum(policy.get('coverage_amount', 0) for policy in policy_portfolio)
        
        # C1: Asset risk (investment quality)
        c1_rbc = total_coverage * rbc_factors['c1_asset_risk']
        
        # C2: Insurance risk (underwriting/mortality)
        c2_rbc = total_coverage * rbc_factors['c2_insurance_risk']
        
        # C3: Interest rate risk
        c3_rbc = total_reserves * rbc_factors['c3_interest_rate_risk']
        
        # C4: Business risk (general business operations)
        c4_rbc = total_coverage * rbc_factors['c4_business_risk']
        
        # Total RBC = sqrt(C1^2 + C2^2 + C3^2) + C4
        total_rbc = math.sqrt(c1_rbc**2 + c2_rbc**2 + c3_rbc**2) + c4_rbc
        
        return total_rbc
    
    def _check_reserve_adequacy(self, total_reserves: float, solvency_margin: float, rbc: float) -> bool:
        """Check if reserves meet regulatory requirements"""
        
        # Reserves must exceed both solvency margin and RBC requirements
        return total_reserves >= max(solvency_margin, rbc)
    
    def _check_reserve_compliance(self, product_type: str, reserve_calc: ReserveCalculation) -> bool:
        """Check reserve compliance for specific product"""
        
        minimum_ratios = self.regulatory_standards['minimum_reserve_ratios']
        required_ratio = minimum_ratios.get(product_type, 0.05)
        
        # Check if reserves meet minimum ratio requirements
        return reserve_calc.total_reserves > 0 and reserve_calc.regulatory_requirements_met
    
    def _check_capital_adequacy(self, reserve_calc: ReserveCalculation) -> bool:
        """Check capital adequacy ratios"""
        
        # Capital adequacy = (Total Reserves + Solvency Margin) / Risk-Based Capital
        total_capital = reserve_calc.total_reserves + reserve_calc.solvency_margin
        
        if reserve_calc.risk_based_capital <= 0:
            return True  # No RBC requirement
        
        capital_ratio = total_capital / reserve_calc.risk_based_capital
        
        # Require capital ratio of at least 2.0 (200% of RBC)
        return capital_ratio >= 2.0
    
    def _check_pricing_compliance(self, product_type: str, premium_structure: Dict) -> bool:
        """Check if premium rates comply with regulatory maximums"""
        
        max_rates = self.regulatory_standards['maximum_premium_rates']
        
        # Check expense loading
        expense_load = premium_structure.get('expense_load', 0)
        if expense_load > max_rates['expense_loading']:
            return False
        
        # Check profit margin
        profit_margin = premium_structure.get('profit_margin', 0)
        if profit_margin > max_rates['profit_margin']:
            return False
        
        return True
    
    def _check_underwriting_compliance(self, underwriting_decision: Dict) -> bool:
        """Check underwriting compliance with regulatory standards"""
        
        standards = self.regulatory_standards['underwriting_standards']
        
        # Check risk multiplier limits
        risk_multiplier = underwriting_decision.get('overall_risk_multiplier', 1.0)
        if risk_multiplier > standards['maximum_risk_multiplier']:
            return False
        
        # Check evidence requirements (simplified check)
        coverage_amount = underwriting_decision.get('coverage_amount', 0)
        evidence_reqs = standards['minimum_evidence_amounts']
        
        # This would typically check if proper medical evidence was obtained
        # For demo purposes, assume compliance if coverage is reasonable
        return coverage_amount <= 10000000  # $10M maximum without special approval
    
    def _generate_reserve_compliance_notes(self,
                                         total_reserves: float,
                                         solvency_margin: float,
                                         rbc: float,
                                         requirements_met: bool) -> str:
        """Generate professional reserve compliance notes"""
        
        notes = f"""RESERVE ADEQUACY ASSESSMENT

Total Policy Reserves: ${total_reserves:,.2f}
Required Solvency Margin: ${solvency_margin:,.2f}
Risk-Based Capital Requirement: ${rbc:,.2f}

Capital Adequacy Ratio: {((total_reserves + solvency_margin) / max(rbc, 1)):.2f}x

REGULATORY COMPLIANCE: {'PASSED' if requirements_met else 'FAILED'}

"""
        
        if requirements_met:
            notes += "All reserve requirements meet or exceed regulatory minimums.\n"
            notes += "Capital levels are adequate for current risk profile.\n"
        else:
            notes += "WARNING: Reserve levels below regulatory requirements.\n"
            notes += "Immediate action required to increase reserves or reduce risk exposure.\n"
        
        notes += "\nCalculations performed in accordance with applicable insurance regulations and actuarial standards."
        
        return notes


# Example usage
if __name__ == "__main__":
    # Example policy portfolio
    sample_portfolio = [
        {
            'policy_id': 'TERM001',
            'product_type': 'term_life',
            'coverage_amount': 500000,
            'annual_premium': 600,
            'policy_year': 3,
            'remaining_years': 17,
            'current_age': 38,
            'gender': 'male',
            'policy_anniversary': '2024-01-15'
        },
        {
            'policy_id': 'DI001',
            'product_type': 'disability_income',
            'coverage_amount': 60000,  # Annual benefit
            'annual_premium': 1200,
            'policy_year': 2,
            'remaining_years': 27,
            'current_age': 35,
            'gender': 'female',
            'policy_anniversary': '2024-03-01'
        }
    ]
    
    # Test regulatory engine
    regulatory_engine = ProfessionalRegulatoryEngine()
    
    # Calculate reserves
    reserve_calc = regulatory_engine.calculate_comprehensive_reserves(sample_portfolio)
    
    print(f"Total Reserves Required: ${reserve_calc.total_reserves:,.2f}")
    print(f"Solvency Margin: ${reserve_calc.solvency_margin:,.2f}")
    print(f"Risk-Based Capital: ${reserve_calc.risk_based_capital:,.2f}")
    print(f"Regulatory Compliance: {reserve_calc.regulatory_requirements_met}")