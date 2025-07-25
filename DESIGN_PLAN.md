# Professional Insurance Premium Calculator - Demo System

## 1. Design Approach (设计思路)

### System Overview
Professional-grade insurance premium calculation with comprehensive business logic, delivered through minimal infrastructure. The system demonstrates actuarial expertise while maintaining simplicity in deployment.

**Core Philosophy**: Maximum business sophistication, minimal technical complexity.

### Key Features
- **Comprehensive Rate Structures**: Multi-dimensional rate tables (age, gender, coverage, risk class)
- **Professional Actuarial Logic**: Proper mortality tables, morbidity adjustments, policy reserves
- **Risk Assessment Engine**: Medical underwriting rules, lifestyle factors, occupation classes
- **Product Portfolio**: Multiple insurance types with distinct calculation methodologies
- **Regulatory Compliance**: Standard actuarial practices and reserve calculations

### Minimal Infrastructure Architecture
```
┌─────────────────┐    ┌─────────────────────────────────┐    ┌─────────────────┐
│  Simple Web UI  │───▶│     Professional Calculator     │───▶│  Detailed Quote │
│                 │    │                                 │    │                 │
│ - Product Form  │    │ ├─ Mortality Tables            │    │ - Premium       │
│ - Risk Inputs   │    │ ├─ Morbidity Adjustments       │    │ - Reserves      │
│ - Submit        │    │ ├─ Underwriting Engine         │    │ - Risk Analysis │
│                 │    │ ├─ Reserve Calculations        │    │ - Breakdown     │
│                 │    │ └─ Regulatory Compliance       │    │ - Explanations  │
└─────────────────┘    └─────────────────────────────────┘    └─────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ Actuarial Data  │
                               │ ├─ CSO Tables   │
                               │ ├─ Morbidity    │
                               │ ├─ Lapse Rates  │
                               │ └─ Expense Loads│
                               └─────────────────┘
```

## 2. Minimal Technology Stack

### Infrastructure (Keep Simple)
- **Backend**: Single Python Flask file (~300 lines)
- **Data**: JSON files with actuarial tables
- **Frontend**: Single HTML page with vanilla JavaScript
- **Deployment**: Can run locally with `python app.py`
- **Internationalization**: Bilingual support (English/Chinese) with client-side language switching

### Business Logic (Keep Sophisticated)
- **Professional actuarial calculations**
- **Industry-standard methodologies**
- **Comprehensive risk assessment**
- **Multiple product types**
- **Bilingual interface supporting Chinese market requirements**

### Language Support Features
- **Dynamic Language Switching**: Toggle between English and Chinese without page reload
- **Localized Interface**: All form labels, buttons, and navigation in both languages
- **Professional Insurance Terms**: Accurate translation of actuarial and insurance terminology
- **Cultural Adaptation**: UI adjustments for Chinese reading patterns and preferences
- **Persistent Language Choice**: User language preference saved in browser localStorage

## 3. Professional Calculation Accuracy (确保计算正确性)

### Actuarial Standards Compliance

#### Industry-Standard Methodologies
- **CSO Mortality Tables**: Use standard Commissioner's Standard Ordinary tables
- **Morbidity Tables**: Industry-standard disability and critical illness rates
- **Reserve Calculations**: Proper policy reserve computation per regulatory standards
- **Risk Classification**: Professional underwriting guidelines and risk factors

#### Professional Validation Framework
- **Actuarial Review**: All formulas follow established actuarial principles
- **Benchmark Testing**: Compare results with industry standard calculations
- **Edge Case Analysis**: Professional handling of high-risk and unusual cases
- **Regulatory Alignment**: Ensure compliance with insurance regulations

#### Calculation Verification Methods
```
Professional Testing Approach
├── Actuarial Formula Verification
│   ├── Mortality calculations vs CSO tables
│   ├── Present value calculations
│   ├── Reserve adequacy testing
│   └── Risk adjustment factors
├── Business Logic Testing
│   ├── Product-specific calculation rules
│   ├── Underwriting decision trees
│   ├── Multi-factor risk assessment
│   └── Policy benefit calculations
└── Industry Benchmarking
    ├── Compare with manual calculations
    ├── Cross-check with actuarial software
    ├── Validate against published rates
    └── Expert actuarial review
```

## 4. Professional Calculator Components

### 4.1 Actuarial Calculation Engine
```python
class ProfessionalPremiumCalculator:
    def __init__(self, actuarial_tables):
        self.mortality_tables = actuarial_tables['mortality']
        self.morbidity_tables = actuarial_tables['morbidity']
        self.expense_factors = actuarial_tables['expenses']
        self.lapse_rates = actuarial_tables['lapse']
    
    def calculate_life_premium(self, age, gender, coverage, risk_class, policy_term):
        """Professional life insurance premium calculation"""
        # Mortality cost calculation using CSO tables
        mortality_cost = self._calculate_mortality_cost(age, gender, policy_term)
        
        # Present value of benefits
        benefit_pv = self._present_value_benefits(coverage, mortality_cost)
        
        # Present value of premiums
        premium_pv = self._present_value_premiums(policy_term, self.lapse_rates[risk_class])
        
        # Expense loading and profit margin
        expense_load = self._calculate_expense_load(coverage)
        profit_margin = self._calculate_profit_margin(risk_class)
        
        # Final premium calculation
        net_premium = benefit_pv / premium_pv
        gross_premium = net_premium * (1 + expense_load + profit_margin)
        
        return self._generate_professional_quote(gross_premium, net_premium, 
                                               mortality_cost, expense_load)
    
    def calculate_disability_premium(self, age, gender, occupation, benefit_amount):
        """Professional disability insurance calculation"""
        # Morbidity rates by occupation class
        morbidity_rate = self.morbidity_tables[occupation][age][gender]
        
        # Disability benefit present value
        benefit_pv = self._calculate_disability_pv(benefit_amount, morbidity_rate, age)
        
        # Apply occupation multipliers and waiting period adjustments
        adjusted_premium = self._apply_occupation_factors(benefit_pv, occupation)
        
        return self._generate_disability_quote(adjusted_premium, morbidity_rate, occupation)
```

### 4.2 Professional Data Structures
```json
{
  "mortality_tables": {
    "CSO_2017": {
      "male": {"20": 0.00058, "30": 0.00076, "40": 0.00147},
      "female": {"20": 0.00039, "30": 0.00053, "40": 0.00095}
    }
  },
  "morbidity_tables": {
    "disability": {
      "professional": {"30": 0.002, "40": 0.004, "50": 0.008},
      "manual_labor": {"30": 0.006, "40": 0.012, "50": 0.024}
    }
  },
  "underwriting_rules": {
    "life_insurance": {
      "medical_conditions": {
        "diabetes": {"multiplier": 1.5, "max_coverage": 500000},
        "hypertension": {"multiplier": 1.2, "max_coverage": 1000000}
      },
      "lifestyle_factors": {
        "smoking": {"multiplier": 2.0},
        "hazardous_sports": {"multiplier": 1.3}
      }
    }
  },
  "reserve_factors": {
    "policy_reserves": {"term_life": 0.02, "whole_life": 0.15},
    "regulatory_margin": 0.05
  }
}
```

### 4.3 Risk Assessment Engine
```python
class UnderwritingEngine:
    def assess_risk(self, applicant_data):
        """Comprehensive risk assessment"""
        base_risk = self._calculate_base_risk(applicant_data.age, applicant_data.gender)
        
        # Medical underwriting
        medical_risk = self._assess_medical_history(applicant_data.medical_conditions)
        
        # Lifestyle factors
        lifestyle_risk = self._assess_lifestyle(applicant_data.smoking, 
                                              applicant_data.alcohol_use,
                                              applicant_data.hazardous_activities)
        
        # Occupation risk
        occupation_risk = self._assess_occupation(applicant_data.occupation,
                                                applicant_data.income)
        
        # Financial underwriting
        financial_risk = self._assess_financial_capacity(applicant_data.net_worth,
                                                       applicant_data.coverage_amount)
        
        return self._combine_risk_factors(base_risk, medical_risk, 
                                        lifestyle_risk, occupation_risk, financial_risk)
```

## 5. Implementation Plan - Professional Focus

### Week 1: Actuarial Foundation
- **Day 1**: Extract and structure data from insurance_premium_table.pdf into professional actuarial tables
- **Day 2**: Implement core mortality/morbidity calculation functions with proper present value mathematics
- **Day 3**: Build comprehensive risk assessment and underwriting logic
- **Day 4**: Implement multiple product types (life, disability, critical illness) with distinct methodologies
- **Day 5**: Add reserve calculations, expense loading, and regulatory compliance features

### Simple File Structure (Minimal Infrastructure)
```
premiumcalculator/
├── app.py                    # Flask backend (single file)
├── actuarial_calculator.py   # Professional calculation engine
├── underwriting_engine.py    # Risk assessment logic
├── data/
│   ├── mortality_tables.json # CSO and other standard tables
│   ├── morbidity_tables.json # Disability and CI rates
│   ├── underwriting_rules.json # Medical and lifestyle factors
│   └── product_definitions.json # Product specifications
├── templates/
│   └── index.html           # Professional quote interface
└── static/
    ├── style.css           # Clean, professional styling
    └── calculator.js       # Client-side validation and AJAX
```

## 6. Professional Quality Assurance

### Actuarial Validation Approach
- **Formula Verification**: Every calculation follows established actuarial principles
- **Industry Benchmarking**: Compare outputs with published industry rates
- **Edge Case Testing**: Proper handling of high-risk scenarios and unusual cases
- **Regulatory Compliance**: Ensure all calculations meet insurance regulatory standards

### Professional Testing Standards
```python
# Example professional test cases
def test_mortality_calculation():
    """Test mortality cost calculation against CSO tables"""
    calculator = ProfessionalPremiumCalculator(actuarial_tables)
    
    # Test standard case: 35-year-old non-smoking male
    result = calculator.calculate_mortality_cost(35, 'male', 20)
    expected = calculate_manual_cso_cost(35, 'male', 20)  # Manual calculation
    assert abs(result - expected) < 0.01
    
    # Test edge case: 65-year-old with medical conditions
    result = calculator.calculate_with_medical_history(65, 'female', ['diabetes'])
    assert result.risk_multiplier == 1.5  # Per underwriting guidelines

def test_present_value_accuracy():
    """Verify present value calculations use correct discount rates"""
    # Test with industry-standard 3.5% discount rate
    pv = calculator._present_value_benefits(100000, mortality_rates)
    manual_pv = calculate_manual_present_value(100000, 0.035, mortality_rates)
    assert abs(pv - manual_pv) < 1.0  # Within $1 accuracy
```

### Business Logic Validation
- **Medical Underwriting**: Proper application of medical condition multipliers
- **Occupation Classification**: Accurate risk assessment by occupation class
- **Financial Underwriting**: Appropriate coverage limits based on income/net worth
- **Product-Specific Rules**: Each insurance type follows its own calculation methodology

This approach ensures the system demonstrates true actuarial professionalism while maintaining minimal technical infrastructure requirements.