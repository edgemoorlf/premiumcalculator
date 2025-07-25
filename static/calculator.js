// Professional Insurance Premium Calculator - JavaScript with Internationalization

// Global variables for i18n
let currentLanguage = 'zh'; // Default to Chinese
let translations = {};

// Global DOM element references
let form;
let resultsSection;
let loadingIndicator;
let errorDisplay;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize DOM element references
    form = document.getElementById('quoteForm');
    resultsSection = document.getElementById('results');
    loadingIndicator = document.getElementById('loading');
    errorDisplay = document.getElementById('error');

    console.log('DOM Content Loaded - Starting initialization');

    // Initialize internationalization first
    initializeI18n().then(() => {
        console.log('i18n initialized, setting up language toggle');
        // Set up language toggle handler after i18n is ready
        setupLanguageToggle();
    }).catch(error => {
        console.error('Failed to initialize i18n:', error);
        // Still try to setup language toggle even if i18n fails
        setupLanguageToggle();
    });

    // Form submission handler
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            await generateQuote();
        });
    }

    // Initialize form
    toggleProductFields();
    
    // Add BMI calculator
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    
    if (heightInput) heightInput.addEventListener('input', updateBMI);
    if (weightInput) weightInput.addEventListener('input', updateBMI);
    
    // Add input validation
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.getAttribute('min'));
            const max = parseFloat(this.getAttribute('max'));
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });
    
    // Add form auto-save to localStorage (optional enhancement)
    const autoSaveFields = ['name', 'age', 'gender', 'occupation_title', 'annual_income'];
    
    autoSaveFields.forEach(fieldName => {
        const field = document.getElementById(fieldName);
        if (field) {
            // Load saved value
            const savedValue = localStorage.getItem(`premium_calc_${fieldName}`);
            if (savedValue) {
                field.value = savedValue;
            }
            
            // Save on change
            field.addEventListener('change', function() {
                localStorage.setItem(`premium_calc_${fieldName}`, this.value);
            });
        }
    });
});

// Setup language toggle button
function setupLanguageToggle() {
    console.log('Setting up language toggle button...');
    
    const languageToggleBtn = document.getElementById('languageToggle');
    
    if (languageToggleBtn) {
        console.log('✅ Language toggle button found:', languageToggleBtn);
        
        // Remove any existing event listeners to avoid duplicates
        languageToggleBtn.removeEventListener('click', handleLanguageToggle);
        
        // Add the click event listener
        languageToggleBtn.addEventListener('click', handleLanguageToggle);
        
        console.log('✅ Language toggle event listener attached successfully');
        
        // Test the button setup by adding visual feedback
        languageToggleBtn.style.cursor = 'pointer';
        
        // Update button text to match current language
        updateToggleButtonText();
        
    } else {
        console.error('❌ Language toggle button not found in DOM');
        console.log('Available elements with IDs:', 
            Array.from(document.querySelectorAll('[id]')).map(el => el.id));
    }
}

// Separate click handler function to avoid issues with event listener management
function handleLanguageToggle(e) {
    console.log('🔄 Language toggle button clicked!');
    e.preventDefault();
    e.stopPropagation();
    
    console.log('Current language before toggle:', currentLanguage);
    
    // Add visual feedback
    const button = e.target;
    button.style.opacity = '0.7';
    setTimeout(() => {
        button.style.opacity = '1';
    }, 150);
    
    toggleLanguage();
}

// Update toggle button text
function updateToggleButtonText() {
    const toggleButton = document.getElementById('languageToggle');
    if (toggleButton && translations[currentLanguage]) {
        const newToggleText = translations[currentLanguage].language_toggle;
        console.log('📝 Updating toggle button text to:', newToggleText);
        toggleButton.textContent = newToggleText;
    }
}

// Internationalization functions
async function initializeI18n() {
    // Load saved language preference or default to Chinese
    const savedLanguage = localStorage.getItem('preferred_language') || 'zh';
    
    try {
        // Load language data
        const response = await fetch('/static/languages.json');
        translations = await response.json();
        
        // Set initial language
        await setLanguage(savedLanguage);
    } catch (error) {
        console.error('Failed to load language data:', error);
        // Fallback to Chinese
        currentLanguage = 'zh';
    }
}

async function setLanguage(language) {
    console.log('📝 Setting language to:', language);
    currentLanguage = language;
    localStorage.setItem('preferred_language', language);
    
    // Update HTML lang attribute
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
    console.log('📝 HTML lang attribute updated to:', document.documentElement.lang);
    
    // Update all translated elements
    updateTranslations();
    
    // Update language toggle button text
    updateToggleButtonText();
}

function updateTranslations() {
    console.log('Updating translations for language:', currentLanguage);
    if (!translations[currentLanguage]) {
        console.error('No translations found for language:', currentLanguage);
        return;
    }
    
    const elements = document.querySelectorAll('[data-i18n]');
    console.log('Found elements to translate:', elements.length);
    
    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = getNestedTranslation(translations[currentLanguage], key);
        
        if (translation) {
            if (element.tagName === 'INPUT' && element.type === 'text') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        } else {
            console.warn('No translation found for key:', key);
        }
    });
    
    console.log('Translation update complete');
}

function getNestedTranslation(obj, path) {
    return path.split('.').reduce((current, key) => {
        return current && current[key] ? current[key] : null;
    }, obj);
}

function toggleLanguage() {
    const newLanguage = currentLanguage === 'en' ? 'zh' : 'en';
    console.log('🔄 Toggling language from', currentLanguage, 'to', newLanguage);
    
    // Check if we have translations for the new language
    if (!translations[newLanguage]) {
        console.error('❌ No translations available for language:', newLanguage);
        console.log('Available languages:', Object.keys(translations));
        return;
    }
    
    setLanguage(newLanguage);
}

function t(key) {
    return getNestedTranslation(translations[currentLanguage], key) || key;
}

// Toggle product-specific fields
window.toggleProductFields = function() {
    const productType = document.getElementById('product_type').value;
    
    // Hide all product-specific fields first
    document.getElementById('coverage_amount_group').style.display = 'block';
    document.getElementById('policy_term_group').style.display = 'none';
    document.getElementById('monthly_benefit_group').style.display = 'none';
    document.getElementById('benefit_period_group').style.display = 'none';
    document.getElementById('waiting_period_group').style.display = 'none';

    // Show relevant fields based on product type
    if (productType === 'term_life' || productType === 'whole_life') {
        document.getElementById('policy_term_group').style.display = 'block';
    } else if (productType === 'disability_income') {
        document.getElementById('coverage_amount_group').style.display = 'none';
        document.getElementById('monthly_benefit_group').style.display = 'block';
        document.getElementById('benefit_period_group').style.display = 'block';
        document.getElementById('waiting_period_group').style.display = 'block';
    }
    // critical_illness uses default coverage_amount_group
};

// Generate quote function
async function generateQuote() {
    try {
        showLoading();
        hideError();
        hideResults();

        const formData = collectFormData();
        
        const response = await fetch('/api/quote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        hideLoading();

        if (result.success) {
            displayResults(result);
        } else {
            showError(result.error || 'An error occurred while generating the quote.');
        }

    } catch (error) {
        hideLoading();
        showError('Network error: Unable to generate quote. Please try again.');
        console.error('Quote generation error:', error);
    }
}

// Collect form data
function collectFormData() {
    const formData = new FormData(form);
    const data = {};

    // Basic form fields
    for (let [key, value] of formData.entries()) {
        if (key === 'medical_conditions' || key === 'hazardous_activities') {
            if (!data[key]) data[key] = [];
            data[key].push(value);
        } else {
            data[key] = value;
        }
    }

    // Handle checkboxes that weren't checked
    if (!data.medical_conditions) data.medical_conditions = [];
    if (!data.hazardous_activities) data.hazardous_activities = [];

    // Convert numeric fields
    const numericFields = ['age', 'coverage_amount', 'policy_term', 'monthly_benefit', 
                          'waiting_period', 'height', 'weight', 'occupation_class', 
                          'annual_income', 'net_worth', 'total_debt'];
    
    numericFields.forEach(field => {
        if (data[field]) {
            data[field] = parseFloat(data[field]) || 0;
        }
    });

    return data;
}

// Display results
function displayResults(result) {
    const quote = result.quote;
    const riskAssessment = result.risk_assessment;

    // Update quote summary
    updateQuoteSummary(quote);
    
    // Update risk assessment
    updateRiskAssessment(riskAssessment);
    
    // Update premium breakdown
    updatePremiumBreakdown(quote);
    
    // Update policy details
    updatePolicyDetails(quote);
    
    // Update underwriter notes
    updateUnderwriterNotes(quote);

    showResults();
}

function updateQuoteSummary(quote) {
    const summaryDiv = document.getElementById('quote-summary');
    
    const decisionColor = getDecisionColor(quote.underwriting_decision);
    const decisionText = formatDecision(quote.underwriting_decision);
    
    summaryDiv.innerHTML = `
        <h3>${quote.product_name}</h3>
        <div class="premium-amount">$${quote.monthly_premium.toFixed(2)}${t('results.monthly_premium')}</div>
        <div class="coverage-info">
            ${t('results.coverage')}: $${quote.coverage_amount.toLocaleString()}<br>
            ${t('results.annual_premium')} $${quote.annual_premium.toLocaleString()}<br>
            <span style="color: ${decisionColor}; font-weight: bold;">
                ${t('results.decision')} ${decisionText}
            </span>
        </div>
        <div style="margin-top: 15px; font-size: 0.9rem;">
            ${t('results.risk_multiplier')} ${quote.risk_multiplier}x | 
            ${t('results.quote_valid_until')} ${quote.quote_valid_until}
        </div>
    `;
}

function updateRiskAssessment(riskAssessment) {
    const riskDiv = document.getElementById('risk-assessment');
    
    let riskFactorsHtml = '';
    if (riskAssessment.risk_factors && riskAssessment.risk_factors.length > 0) {
        riskFactorsHtml = `
            <h4>${t('results.risk_factors_identified')}:</h4>
            <div class="risk-factors">
                ${riskAssessment.risk_factors.map(factor => `
                    <div class="risk-factor">${factor}</div>
                `).join('')}
            </div>
        `;
    } else {
        riskFactorsHtml = `<p style="color: #28a745;">${t('results.no_risk_factors')}</p>`;
    }

    riskDiv.innerHTML = `
        <h3>${t('results.risk_assessment')}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
            <div><strong>${t('results.overall_risk')}:</strong> ${riskAssessment.overall_risk_multiplier.toFixed(2)}x</div>
            <div><strong>${t('results.medical_risk')}:</strong> ${riskAssessment.medical_risk_multiplier.toFixed(2)}x</div>
            <div><strong>${t('results.lifestyle_risk')}:</strong> ${riskAssessment.lifestyle_risk_multiplier.toFixed(2)}x</div>
            <div><strong>${t('results.occupation_risk')}:</strong> ${riskAssessment.occupation_risk_multiplier.toFixed(2)}x</div>
        </div>
        ${riskFactorsHtml}
    `;
}

function updatePremiumBreakdown(quote) {
    const breakdownDiv = document.getElementById('premium-breakdown');
    
    let breakdownTable = `
        <h3>${t('results.premium_breakdown')}</h3>
        <table class="breakdown-table">
            <thead>
                <tr>
                    <th>Component</th>
                    <th>Amount</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
    `;

    // Add breakdown items based on what's available
    if (quote.breakdown) {
        const breakdown = quote.breakdown;
        
        if (breakdown.net_premium) {
            breakdownTable += `
                <tr>
                    <td>Net Premium</td>
                    <td>$${(breakdown.net_premium * 12).toFixed(2)}</td>
                    <td>Base mortality/morbidity cost</td>
                </tr>
            `;
        }
        
        if (breakdown.expense_loading) {
            breakdownTable += `
                <tr>
                    <td>Expense Loading</td>
                    <td>$${(breakdown.expense_loading * 12).toFixed(2)}</td>
                    <td>Administrative and acquisition costs</td>
                </tr>
            `;
        }
        
        if (breakdown.profit_margin) {
            breakdownTable += `
                <tr>
                    <td>Profit Margin</td>
                    <td>$${(breakdown.profit_margin * 12).toFixed(2)}</td>
                    <td>Company profit and contingencies</td>
                </tr>
            `;
        }
        
        if (breakdown.commission) {
            breakdownTable += `
                <tr>
                    <td>Commission</td>
                    <td>$${(breakdown.commission * 12).toFixed(2)}</td>
                    <td>Agent/broker compensation</td>
                </tr>
            `;
        }
        
        if (breakdown.policy_reserves) {
            breakdownTable += `
                <tr>
                    <td>Policy Reserves</td>
                    <td>$${breakdown.policy_reserves.toLocaleString()}</td>
                    <td>Required regulatory reserves</td>
                </tr>
            `;
        }
    }

    breakdownTable += `
                <tr style="font-weight: bold; background-color: #e3f2fd;">
                    <td>Total Annual Premium</td>
                    <td>$${quote.annual_premium.toLocaleString()}</td>
                    <td>Complete annual premium</td>
                </tr>
            </tbody>
        </table>
    `;

    breakdownDiv.innerHTML = breakdownTable;
}

function updatePolicyDetails(quote) {
    const detailsDiv = document.getElementById('policy-details');
    
    let detailsHtml = `<h3>${t('results.policy_details')}</h3><div class="policy-grid">`;
    
    if (quote.policy_details) {
        for (const [key, value] of Object.entries(quote.policy_details)) {
            if (typeof value === 'object' && Array.isArray(value)) {
                detailsHtml += `
                    <div class="policy-item">
                        <strong>${formatKey(key)}:</strong>
                        <ul style="margin-top: 5px; padding-left: 20px;">
                            ${value.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                `;
            } else if (typeof value === 'string' || typeof value === 'number') {
                detailsHtml += `
                    <div class="policy-item">
                        <strong>${formatKey(key)}:</strong>
                        ${value}
                    </div>
                `;
            }
        }
    }
    
    detailsHtml += '</div>';
    detailsDiv.innerHTML = detailsHtml;
}

function updateUnderwriterNotes(quote) {
    const notesDiv = document.getElementById('underwriter-notes');
    
    notesDiv.innerHTML = `
        <h3>${t('results.underwriter_notes')}</h3>
        <pre style="white-space: pre-wrap; font-family: inherit;">${quote.underwriter_notes}</pre>
        <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #dee2e6;">
            <h4>${t('results.actuarial_explanation')}</h4>
            <p style="font-family: 'Segoe UI', sans-serif; line-height: 1.6;">
                ${quote.explanation}
            </p>
        </div>
    `;
}

// Utility functions
function getDecisionColor(decision) {
    switch (decision) {
        case 'approved_preferred': return '#28a745';
        case 'approved_standard': return '#17a2b8';
        case 'approved_substandard': return '#ffc107';
        case 'declined': return '#dc3545';
        case 'postponed': return '#6c757d';
        default: return '#495057';
    }
}

function formatDecision(decision) {
    return decision.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function formatKey(key) {
    return key.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function showLoading() {
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
}

function hideLoading() {
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
}

function showResults() {
    if (resultsSection) {
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function hideResults() {
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
}

function showError(message) {
    if (errorDisplay) {
        errorDisplay.textContent = message;
        errorDisplay.style.display = 'block';
        errorDisplay.scrollIntoView({ behavior: 'smooth' });
    }
}

function hideError() {
    if (errorDisplay) {
        errorDisplay.style.display = 'none';
    }
}

// Reset form function
window.resetForm = function() {
    if (form) {
        form.reset();
        hideResults();
        hideError();
        hideLoading();
        toggleProductFields(); // Reset product-specific fields
    }
};

function updateBMI() {
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    
    if (heightInput && weightInput) {
        const height = parseFloat(heightInput.value);
        const weight = parseFloat(weightInput.value);
        
        if (height > 0 && weight > 0) {
            const bmi = (weight * 703) / (height * height);
            const bmiCategory = getBMICategory(bmi);
            
            // You could display BMI info here if desired
            console.log(`BMI: ${bmi.toFixed(1)} (${bmiCategory})`);
        }
    }
}

function getBMICategory(bmi) {
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal';
    if (bmi < 30) return 'Overweight';
    if (bmi < 35) return 'Obese Class I';
    if (bmi < 40) return 'Obese Class II';
    return 'Obese Class III';
}

// Utility function for formatting currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Print functionality
function printQuote() {
    window.print();
}

// Export functionality (if needed)
function exportQuote() {
    const results = document.getElementById('results');
    if (results && results.style.display !== 'none') {
        // This could be enhanced to generate PDF or other formats
        alert('Export functionality would be implemented here for production use.');
    }
}