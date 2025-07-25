"""
Professional Underwriting Engine
Implements comprehensive risk assessment with medical, lifestyle, occupation, and financial underwriting
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class UnderwritingDecision(Enum):
    APPROVED_STANDARD = "approved_standard"
    APPROVED_SUBSTANDARD = "approved_substandard"
    APPROVED_PREFERRED = "approved_preferred"
    DECLINED = "declined"
    POSTPONED = "postponed"


@dataclass
class RiskAssessment:
    """Comprehensive risk assessment result"""
    overall_risk_multiplier: float
    medical_risk_multiplier: float
    lifestyle_risk_multiplier: float
    occupation_risk_multiplier: float
    financial_risk_score: float
    underwriting_decision: UnderwritingDecision
    maximum_coverage: int
    risk_factors_identified: List[str]
    underwriting_notes: str


class ProfessionalUnderwritingEngine:
    """Professional underwriting engine with comprehensive risk assessment"""
    
    def __init__(self):
        self.underwriting_rules = self._load_json_data('data/underwriting_rules.json')
        self.product_definitions = self._load_json_data('data/product_definitions.json')
        self.morbidity_tables = self._load_json_data('data/morbidity_tables.json')
    
    def _load_json_data(self, filepath: str) -> Dict:
        """Load underwriting data from JSON files"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Using empty data.")
            return {}
    
    def perform_comprehensive_risk_assessment(self,
                                            applicant_data: Dict,
                                            product_type: str,
                                            coverage_amount: int) -> RiskAssessment:
        """
        Perform comprehensive underwriting risk assessment
        
        Args:
            applicant_data: Complete applicant information
            product_type: Type of insurance product
            coverage_amount: Requested coverage amount
        
        Returns:
            RiskAssessment: Comprehensive risk assessment result
        """
        
        # Initialize risk factors
        risk_factors_identified = []
        
        # Medical underwriting
        medical_risk, medical_factors = self._assess_medical_risk(applicant_data.get('medical_history', {}))
        risk_factors_identified.extend(medical_factors)
        
        # Lifestyle risk assessment
        lifestyle_risk, lifestyle_factors = self._assess_lifestyle_risk(applicant_data.get('lifestyle', {}))
        risk_factors_identified.extend(lifestyle_factors)
        
        # Occupation risk assessment  
        occupation_risk, occupation_factors = self._assess_occupation_risk(
            applicant_data.get('occupation', {}),
            applicant_data.get('age', 30)
        )
        risk_factors_identified.extend(occupation_factors)
        
        # Financial underwriting
        financial_risk, financial_factors = self._assess_financial_capacity(
            applicant_data.get('financial_info', {}),
            coverage_amount,
            product_type
        )
        risk_factors_identified.extend(financial_factors)
        
        # Calculate overall risk multiplier
        overall_risk = self._combine_risk_factors(medical_risk, lifestyle_risk, occupation_risk)
        
        # Determine underwriting decision
        decision, max_coverage = self._make_underwriting_decision(
            overall_risk, 
            financial_risk,
            coverage_amount,
            risk_factors_identified
        )
        
        # Generate underwriting notes
        notes = self._generate_underwriting_notes(
            risk_factors_identified,
            overall_risk,
            decision,
            applicant_data
        )
        
        return RiskAssessment(
            overall_risk_multiplier=overall_risk,
            medical_risk_multiplier=medical_risk,
            lifestyle_risk_multiplier=lifestyle_risk,
            occupation_risk_multiplier=occupation_risk,
            financial_risk_score=financial_risk,
            underwriting_decision=decision,
            maximum_coverage=max_coverage,
            risk_factors_identified=risk_factors_identified,
            underwriting_notes=notes
        )
    
    def _assess_medical_risk(self, medical_history: Dict) -> Tuple[float, List[str]]:
        """Assess medical risk factors and calculate multiplier"""
        medical_multiplier = 1.0
        risk_factors = []
        
        medical_conditions = medical_history.get('conditions', [])
        
        for condition in medical_conditions:
            condition_found = False
            
            # Check each medical category
            for category_name, category_data in self.underwriting_rules['medical_conditions'].items():
                if condition in category_data:
                    condition_info = category_data[condition]
                    medical_multiplier *= condition_info['multiplier']
                    risk_factors.append(f"Medical: {condition} (Risk: {condition_info['multiplier']}x)")
                    condition_found = True
                    break
            
            if not condition_found:
                # Unknown condition - apply conservative multiplier
                medical_multiplier *= 1.5
                risk_factors.append(f"Medical: {condition} (Unknown condition - conservative rating)")
        
        # BMI assessment
        if 'height' in medical_history and 'weight' in medical_history:
            bmi = self._calculate_bmi(medical_history['weight'], medical_history['height'])
            bmi_multiplier, bmi_factor = self._assess_bmi_risk(bmi)
            medical_multiplier *= bmi_multiplier
            if bmi_factor:
                risk_factors.append(bmi_factor)
        
        # Age-based risk adjustment for medical conditions
        age = medical_history.get('age', 30)
        if len(medical_conditions) > 0 and age > 60:
            age_adjustment = 1.1  # 10% increase for older applicants with medical conditions
            medical_multiplier *= age_adjustment
            risk_factors.append(f"Age adjustment for medical conditions: {age_adjustment}x")
        
        return medical_multiplier, risk_factors
    
    def _assess_lifestyle_risk(self, lifestyle_info: Dict) -> Tuple[float, List[str]]:
        """Assess lifestyle risk factors"""
        lifestyle_multiplier = 1.0
        risk_factors = []
        
        # Smoking assessment
        smoking_status = lifestyle_info.get('smoking_status', 'non_smoker')
        if smoking_status != 'non_smoker':
            smoking_rules = self.underwriting_rules['lifestyle_factors']['smoking']
            if smoking_status in smoking_rules:
                smoking_mult = smoking_rules[smoking_status]['multiplier']
                lifestyle_multiplier *= smoking_mult
                risk_factors.append(f"Smoking: {smoking_status} ({smoking_mult}x multiplier)")
        
        # Alcohol use assessment
        alcohol_use = lifestyle_info.get('alcohol_use', 'moderate_use')
        alcohol_rules = self.underwriting_rules['lifestyle_factors']['alcohol']
        if alcohol_use in alcohol_rules:
            alcohol_mult = alcohol_rules[alcohol_use]['multiplier']
            lifestyle_multiplier *= alcohol_mult
            if alcohol_mult > 1.0:
                risk_factors.append(f"Alcohol use: {alcohol_use} ({alcohol_mult}x multiplier)")
        
        # Hazardous activities
        hazardous_activities = lifestyle_info.get('hazardous_activities', [])
        hazardous_rules = self.underwriting_rules['lifestyle_factors']['hazardous_activities']
        
        for activity in hazardous_activities:
            if activity in hazardous_rules:
                activity_mult = hazardous_rules[activity]['multiplier']
                lifestyle_multiplier *= activity_mult
                risk_factors.append(f"Hazardous activity: {activity} ({activity_mult}x multiplier)")
        
        return lifestyle_multiplier, risk_factors
    
    def _assess_occupation_risk(self, occupation_info: Dict, age: int) -> Tuple[float, List[str]]:
        """Assess occupation-based risk factors"""
        occupation_multiplier = 1.0
        risk_factors = []
        
        occupation_class = occupation_info.get('class', 2)  # Default to standard class
        occupation_title = occupation_info.get('title', 'Unknown')
        
        # Get occupation multiplier
        occupation_rules = self.underwriting_rules['occupation_factors']
        class_key = f"class_{occupation_class}_professional" if occupation_class == 1 else \
                   f"class_{occupation_class}_standard" if occupation_class == 2 else \
                   f"class_{occupation_class}_skilled" if occupation_class == 3 else \
                   f"class_{occupation_class}_manual" if occupation_class == 4 else \
                   "class_5_hazardous"
        
        if class_key in occupation_rules:
            occupation_multiplier = occupation_rules[class_key]['multiplier']
            if occupation_multiplier != 1.0:
                risk_factors.append(f"Occupation: {occupation_title} - Class {occupation_class} ({occupation_multiplier}x)")
        
        # Additional risk for hazardous occupations and older workers
        if occupation_class >= 4 and age > 50:
            age_occupation_adjustment = 1.2
            occupation_multiplier *= age_occupation_adjustment
            risk_factors.append(f"Age + hazardous occupation adjustment: {age_occupation_adjustment}x")
        
        return occupation_multiplier, risk_factors
    
    def _assess_financial_capacity(self, financial_info: Dict, coverage_amount: int, product_type: str) -> Tuple[float, List[str]]:
        """Assess financial underwriting and capacity"""
        financial_risk_score = 1.0
        risk_factors = []
        
        annual_income = financial_info.get('annual_income', 0)
        net_worth = financial_info.get('net_worth', 0)
        
        # Income-based coverage limits
        financial_rules = self.underwriting_rules['financial_underwriting']
        
        if product_type in ['term_life', 'whole_life']:
            max_income_multiple = financial_rules['income_multiples']['life_insurance']['max_coverage_multiple']
            max_coverage_by_income = annual_income * max_income_multiple
            
            if coverage_amount > max_coverage_by_income:
                financial_risk_score = 2.0  # High risk score
                risk_factors.append(f"Coverage exceeds {max_income_multiple}x annual income limit")
        
        elif product_type == 'disability_income':
            max_benefit_pct = financial_rules['income_multiples']['disability_insurance']['max_benefit_percentage']
            monthly_income = annual_income / 12
            max_monthly_benefit = monthly_income * max_benefit_pct
            monthly_coverage = coverage_amount  # Assuming coverage_amount is monthly benefit
            
            if monthly_coverage > max_monthly_benefit:
                financial_risk_score = 2.0
                risk_factors.append(f"Monthly benefit exceeds {max_benefit_pct*100}% of monthly income")
        
        # Net worth requirements for high coverage amounts
        if coverage_amount >= 1000000:
            net_worth_rules = financial_rules['net_worth_requirements']
            
            if coverage_amount >= 5000000:
                min_net_worth = net_worth_rules['coverage_5m_plus']['min_net_worth']
                if net_worth < min_net_worth:
                    financial_risk_score = 3.0
                    risk_factors.append(f"Net worth below ${min_net_worth:,} requirement for ${coverage_amount:,} coverage")
            
            elif coverage_amount >= 1000000:
                min_net_worth = net_worth_rules['coverage_1m_plus']['min_net_worth']
                if net_worth < min_net_worth:
                    financial_risk_score = 2.0
                    risk_factors.append(f"Net worth below ${min_net_worth:,} requirement for ${coverage_amount:,} coverage")
        
        # Debt-to-income assessment
        total_debt = financial_info.get('total_debt', 0)
        if annual_income > 0:
            debt_to_income = total_debt / annual_income
            if debt_to_income > 0.4:  # More than 40% DTI
                financial_risk_score *= 1.3
                risk_factors.append(f"High debt-to-income ratio: {debt_to_income:.1%}")
        
        return financial_risk_score, risk_factors
    
    def _combine_risk_factors(self, medical_risk: float, lifestyle_risk: float, occupation_risk: float) -> float:
        """Combine individual risk factors into overall multiplier"""
        # Use multiplicative approach with some diminishing returns for very high risks
        combined_risk = medical_risk * lifestyle_risk * occupation_risk
        
        # Cap extreme risk multipliers at 10x for practical purposes
        return min(combined_risk, 10.0)
    
    def _make_underwriting_decision(self, 
                                  overall_risk: float, 
                                  financial_risk: float,
                                  coverage_amount: int,
                                  risk_factors: List[str]) -> Tuple[UnderwritingDecision, int]:
        """Make final underwriting decision based on risk assessment"""
        
        # Financial capacity issues - immediate decline
        if financial_risk >= 3.0:
            return UnderwritingDecision.DECLINED, 0
        
        # Risk-based decision making
        if overall_risk <= 0.95:
            # Preferred risk - better than standard
            return UnderwritingDecision.APPROVED_PREFERRED, coverage_amount
        
        elif overall_risk <= 2.0:
            # Standard or mildly substandard risk
            if overall_risk <= 1.2:
                return UnderwritingDecision.APPROVED_STANDARD, coverage_amount
            else:
                # Substandard but acceptable
                max_coverage = min(coverage_amount, 2000000)  # Cap at $2M for substandard
                return UnderwritingDecision.APPROVED_SUBSTANDARD, max_coverage
        
        elif overall_risk <= 4.0:
            # High risk - significant coverage reduction
            max_coverage = min(coverage_amount, 500000)  # Cap at $500K for high risk
            return UnderwritingDecision.APPROVED_SUBSTANDARD, max_coverage
        
        else:
            # Extreme risk - decline
            return UnderwritingDecision.DECLINED, 0
    
    def _calculate_bmi(self, weight_lbs: float, height_inches: float) -> float:
        """Calculate BMI from weight and height"""
        if height_inches <= 0:
            return 25  # Default BMI if invalid height
        
        return (weight_lbs * 703) / (height_inches ** 2)
    
    def _assess_bmi_risk(self, bmi: float) -> Tuple[float, Optional[str]]:
        """Assess risk based on BMI"""
        if bmi < 18.5:
            return 1.2, f"Underweight BMI: {bmi:.1f} (1.2x multiplier)"
        elif 18.5 <= bmi < 25:
            return 1.0, None  # Normal weight
        elif 25 <= bmi < 30:
            return 1.1, f"Overweight BMI: {bmi:.1f} (1.1x multiplier)"
        elif 30 <= bmi < 35:
            return 1.3, f"Obese Class I BMI: {bmi:.1f} (1.3x multiplier)"
        elif 35 <= bmi < 40:
            return 2.0, f"Obese Class II BMI: {bmi:.1f} (2.0x multiplier)"
        else:
            return 3.0, f"Obese Class III BMI: {bmi:.1f} (3.0x multiplier)"
    
    def _generate_underwriting_notes(self, 
                                   risk_factors: List[str],
                                   overall_risk: float,
                                   decision: UnderwritingDecision,
                                   applicant_data: Dict) -> str:
        """Generate professional underwriting notes"""
        
        notes = f"""UNDERWRITING ASSESSMENT SUMMARY
        
Decision: {decision.value.replace('_', ' ').title()}
Overall Risk Multiplier: {overall_risk:.2f}x

RISK FACTORS IDENTIFIED:
"""
        
        if risk_factors:
            for i, factor in enumerate(risk_factors, 1):
                notes += f"{i}. {factor}\n"
        else:
            notes += "No significant risk factors identified.\n"
        
        notes += f"""
UNDERWRITING RATIONALE:
Risk multiplier of {overall_risk:.2f}x calculated using professional actuarial standards.
Assessment includes medical history, lifestyle factors, occupation classification, and financial capacity analysis.

RECOMMENDATIONS:
"""
        
        if decision == UnderwritingDecision.APPROVED_PREFERRED:
            notes += "Preferred risk classification - excellent health and lifestyle profile."
        elif decision == UnderwritingDecision.APPROVED_STANDARD:
            notes += "Standard risk classification - acceptable risk profile within normal parameters."
        elif decision == UnderwritingDecision.APPROVED_SUBSTANDARD:
            notes += "Substandard risk classification - elevated risk requiring premium adjustment and/or coverage limitations."
        elif decision == UnderwritingDecision.DECLINED:
            notes += "Application declined due to excessive risk factors or financial capacity limitations."
        else:
            notes += "Application postponed pending additional information or medical examination."
        
        return notes