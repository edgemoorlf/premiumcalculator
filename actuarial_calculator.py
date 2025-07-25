"""
Professional Actuarial Calculator
Implements industry-standard insurance premium calculations with proper actuarial methodology
"""

import json
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class QuoteResult:
    """Professional insurance quote result"""
    gross_premium: float
    net_premium: float
    expense_load: float
    profit_margin: float
    commission: float
    reserves: float
    risk_multiplier: float
    breakdown: Dict
    explanation: str


class ActuarialCalculator:
    """Professional actuarial calculation engine with industry-standard methodologies"""
    
    def __init__(self):
        self.mortality_tables = self._load_json_data('data/mortality_tables.json')
        self.morbidity_tables = self._load_json_data('data/morbidity_tables.json')
        self.underwriting_rules = self._load_json_data('data/underwriting_rules.json')
        self.product_definitions = self._load_json_data('data/product_definitions.json')
    
    def _load_json_data(self, filepath: str) -> Dict:
        """Load actuarial data from JSON files"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Using empty data.")
            return {}
    
    def calculate_life_insurance_premium(self, 
                                       age: int, 
                                       gender: str, 
                                       coverage_amount: int,
                                       policy_term: int,
                                       product_type: str = 'term_life',
                                       risk_factors: Dict = None) -> QuoteResult:
        """
        Professional life insurance premium calculation using actuarial principles
        
        Args:
            age: Applicant age
            gender: 'male' or 'female'
            coverage_amount: Death benefit amount
            policy_term: Policy term in years
            product_type: 'term_life' or 'whole_life'
            risk_factors: Dictionary of medical/lifestyle risk factors
        """
        if risk_factors is None:
            risk_factors = {}
        
        # Get product specifications
        product = self.product_definitions['products'][product_type]
        
        # Validate inputs
        self._validate_life_insurance_inputs(age, coverage_amount, policy_term, product)
        
        # Calculate mortality cost using CSO tables
        mortality_cost = self._calculate_mortality_cost(age, gender, policy_term)
        
        # Calculate present value of benefits
        benefit_pv = self._calculate_benefit_present_value(coverage_amount, mortality_cost, age, gender, policy_term)
        
        # Calculate present value of premiums
        premium_pv = self._calculate_premium_present_value(policy_term, age, gender)
        
        # Net premium calculation
        net_premium = benefit_pv / premium_pv if premium_pv > 0 else 0
        
        # Apply risk multipliers
        risk_multiplier = self._calculate_risk_multiplier(risk_factors)
        adjusted_net_premium = net_premium * risk_multiplier
        
        # Add expense loads and profit margin
        expense_load = product['expense_load']
        profit_margin = product['profit_margin'] 
        commission = product['commission']
        
        # Gross premium calculation
        gross_premium = adjusted_net_premium * (1 + expense_load + profit_margin + commission)
        
        # Calculate reserves
        reserves = self._calculate_policy_reserves(coverage_amount, product_type)
        
        # Generate breakdown
        breakdown = {
            'base_mortality_cost': mortality_cost,
            'net_premium': net_premium,
            'risk_adjustment': risk_multiplier,
            'adjusted_net_premium': adjusted_net_premium,
            'expense_loading': gross_premium * expense_load / (1 + expense_load + profit_margin + commission),
            'profit_margin': gross_premium * profit_margin / (1 + expense_load + profit_margin + commission),
            'commission': gross_premium * commission / (1 + expense_load + profit_margin + commission),
            'policy_reserves': reserves,
            'annual_premium': gross_premium * 12 if product_type == 'term_life' else gross_premium
        }
        
        explanation = self._generate_life_explanation(age, gender, coverage_amount, policy_term, risk_multiplier, product_type)
        
        return QuoteResult(
            gross_premium=gross_premium,
            net_premium=net_premium,
            expense_load=expense_load,
            profit_margin=profit_margin,
            commission=commission,
            reserves=reserves,
            risk_multiplier=risk_multiplier,
            breakdown=breakdown,
            explanation=explanation
        )
    
    def calculate_disability_premium(self,
                                   age: int,
                                   gender: str,
                                   occupation_class: int,
                                   monthly_benefit: int,
                                   benefit_period: str = 'to_age_65',
                                   waiting_period: int = 90) -> QuoteResult:
        """
        Professional disability insurance premium calculation
        """
        product = self.product_definitions['products']['disability_income']
        
        self._validate_disability_inputs(age, monthly_benefit, occupation_class, product)
        
        # Get morbidity rates for occupation class
        occ_data = self.morbidity_tables['disability_tables']['occupation_classes'][str(occupation_class)]
        
        # Find closest age in morbidity table
        closest_age = self._find_closest_age(age, occ_data['rates'])
        morbidity_rate = occ_data['rates'][str(closest_age)][gender]
        
        # Calculate disability benefit present value
        benefit_pv = self._calculate_disability_present_value(monthly_benefit, morbidity_rate, age, benefit_period)
        
        # Calculate premium present value
        premium_pv = self._calculate_premium_present_value(65 - age, age, gender)  # To age 65
        
        # Net premium
        net_premium = benefit_pv / premium_pv if premium_pv > 0 else 0
        
        # Apply waiting period adjustments
        waiting_adjustment = self._get_waiting_period_adjustment(waiting_period)
        adjusted_net_premium = net_premium * waiting_adjustment['benefit_percentage']
        
        # Add loadings
        expense_load = product['expense_load']
        profit_margin = product['profit_margin']
        commission = product['commission']
        
        gross_premium = adjusted_net_premium * (1 + expense_load + profit_margin + commission)
        
        # Calculate reserves
        reserves = self._calculate_policy_reserves(monthly_benefit * 12, 'disability_income')
        
        breakdown = {
            'base_morbidity_rate': morbidity_rate,
            'net_premium': net_premium,
            'waiting_period_adjustment': waiting_adjustment['benefit_percentage'],
            'adjusted_net_premium': adjusted_net_premium,
            'monthly_premium': gross_premium,
            'annual_premium': gross_premium * 12,
            'occupation_class': occupation_class,
            'occupation_description': occ_data['name']
        }
        
        explanation = self._generate_disability_explanation(age, gender, occupation_class, monthly_benefit, benefit_period)
        
        return QuoteResult(
            gross_premium=gross_premium,
            net_premium=net_premium,
            expense_load=expense_load,
            profit_margin=profit_margin,
            commission=commission,
            reserves=reserves,
            risk_multiplier=1.0,
            breakdown=breakdown,
            explanation=explanation
        )
    
    def _calculate_mortality_cost(self, age: int, gender: str, term: int) -> float:
        """Calculate mortality cost using CSO tables"""
        cso_table = self.mortality_tables['CSO_2017'][gender]
        discount_rate = self.mortality_tables['discount_rates']['standard']
        
        total_cost = 0.0
        for year in range(term):
            current_age = min(age + year, 80)  # Cap at table maximum
            mortality_rate = cso_table.get(str(current_age), cso_table['80'])
            
            # Present value of mortality cost for this year
            pv_factor = 1 / ((1 + discount_rate) ** year)
            total_cost += mortality_rate * pv_factor
        
        return total_cost
    
    def _calculate_benefit_present_value(self, coverage: int, mortality_cost: float, age: int, gender: str, term: int) -> float:
        """Calculate present value of death benefits"""
        return coverage * mortality_cost
    
    def _calculate_premium_present_value(self, term: int, age: int, gender: str) -> float:
        """Calculate present value of premium payments"""
        discount_rate = self.mortality_tables['discount_rates']['standard']
        cso_table = self.mortality_tables['CSO_2017'][gender]
        
        pv_premiums = 0.0
        survival_prob = 1.0
        
        for year in range(term):
            current_age = min(age + year, 80)
            mortality_rate = cso_table.get(str(current_age), cso_table['80'])
            
            # Probability of surviving to pay premium
            pv_factor = survival_prob / ((1 + discount_rate) ** year)
            pv_premiums += pv_factor
            
            # Update survival probability for next year
            survival_prob *= (1 - mortality_rate)
        
        return pv_premiums
    
    def _calculate_disability_present_value(self, monthly_benefit: int, morbidity_rate: float, age: int, benefit_period: str) -> float:
        """Calculate present value of disability benefits"""
        discount_rate = self.mortality_tables['discount_rates']['standard']
        
        if benefit_period == 'to_age_65':
            years = max(65 - age, 0)
        else:
            years = int(benefit_period.split('_')[0])
        
        annual_benefit = monthly_benefit * 12
        pv_benefits = 0.0
        
        for year in range(years):
            pv_factor = 1 / ((1 + discount_rate) ** year)
            pv_benefits += annual_benefit * morbidity_rate * pv_factor
        
        return pv_benefits
    
    def _calculate_risk_multiplier(self, risk_factors: Dict) -> float:
        """Calculate composite risk multiplier from medical and lifestyle factors"""
        multiplier = 1.0
        
        # Medical conditions
        if 'medical_conditions' in risk_factors:
            for condition in risk_factors['medical_conditions']:
                if condition in self.underwriting_rules['medical_conditions']:
                    for category in self.underwriting_rules['medical_conditions'].values():
                        if condition in category:
                            multiplier *= category[condition]['multiplier']
                            break
        
        # Lifestyle factors
        if 'smoking_status' in risk_factors:
            smoking = self.underwriting_rules['lifestyle_factors']['smoking']
            if risk_factors['smoking_status'] in smoking:
                multiplier *= smoking[risk_factors['smoking_status']]['multiplier']
        
        if 'hazardous_activities' in risk_factors:
            hazardous = self.underwriting_rules['lifestyle_factors']['hazardous_activities']
            for activity in risk_factors['hazardous_activities']:
                if activity in hazardous:
                    multiplier *= hazardous[activity]['multiplier']
        
        return multiplier
    
    def _calculate_policy_reserves(self, coverage_amount: int, product_type: str) -> float:
        """Calculate required policy reserves per regulatory standards"""
        reserve_factors = self.product_definitions['regulatory_requirements']['reserve_factors']
        reserve_factor = reserve_factors.get(product_type, 0.05)
        
        return coverage_amount * reserve_factor
    
    def _get_waiting_period_adjustment(self, waiting_days: int) -> Dict:
        """Get waiting period adjustment factors"""
        waiting_periods = self.morbidity_tables['waiting_periods']['disability']
        
        if waiting_days <= 30:
            return waiting_periods['30_days']
        elif waiting_days <= 90:
            return waiting_periods['90_days'] 
        elif waiting_days <= 180:
            return waiting_periods['180_days']
        else:
            return waiting_periods['365_days']
    
    def _find_closest_age(self, age: int, age_data: Dict) -> int:
        """Find closest age in actuarial table"""
        ages = [int(a) for a in age_data.keys()]
        return min(ages, key=lambda x: abs(x - age))
    
    def _validate_life_insurance_inputs(self, age: int, coverage: int, term: int, product: Dict):
        """Validate life insurance inputs against product limits"""
        if age < product['min_age'] or age > product['max_age']:
            raise ValueError(f"Age {age} outside valid range {product['min_age']}-{product['max_age']}")
        
        if coverage < product['min_coverage'] or coverage > product['max_coverage']:
            raise ValueError(f"Coverage ${coverage:,} outside valid range ${product['min_coverage']:,}-${product['max_coverage']:,}")
        
        if 'terms' in product and term not in product['terms']:
            raise ValueError(f"Term {term} not available. Valid terms: {product['terms']}")
    
    def _validate_disability_inputs(self, age: int, benefit: int, occ_class: int, product: Dict):
        """Validate disability insurance inputs"""
        if age < product['min_age'] or age > product['max_age']:
            raise ValueError(f"Age {age} outside valid range {product['min_age']}-{product['max_age']}")
        
        if benefit < product['min_monthly_benefit'] or benefit > product['max_monthly_benefit']:
            raise ValueError(f"Monthly benefit ${benefit:,} outside valid range ${product['min_monthly_benefit']:,}-${product['max_monthly_benefit']:,}")
        
        if str(occ_class) not in self.morbidity_tables['disability_tables']['occupation_classes']:
            raise ValueError(f"Invalid occupation class {occ_class}")
    
    def _generate_life_explanation(self, age: int, gender: str, coverage: int, term: int, risk_mult: float, product_type: str) -> str:
        """Generate professional explanation of life insurance calculation"""
        return f"""Life Insurance Premium Calculation:

Applicant: {age}-year-old {gender}
Coverage: ${coverage:,} {product_type.replace('_', ' ').title()}
Term: {term} years
Risk Multiplier: {risk_mult:.2f}x

This premium is calculated using industry-standard CSO 2017 mortality tables with proper actuarial present value methodology. The calculation includes mortality costs, expense loadings, profit margins, and regulatory reserve requirements."""
    
    def _generate_disability_explanation(self, age: int, gender: str, occ_class: int, benefit: int, period: str) -> str:
        """Generate professional explanation of disability insurance calculation"""
        occ_name = self.morbidity_tables['disability_tables']['occupation_classes'][str(occ_class)]['name']
        
        return f"""Disability Income Insurance Calculation:

Applicant: {age}-year-old {gender}
Occupation: Class {occ_class} - {occ_name}  
Monthly Benefit: ${benefit:,}
Benefit Period: {period.replace('_', ' ').title()}

Premium calculated using professional morbidity tables specific to occupation class, with proper present value methodology and regulatory compliance standards."""