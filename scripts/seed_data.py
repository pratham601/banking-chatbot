#!/usr/bin/env python3
"""
Seed the vector database with synthetic banking documents.
Run once before starting the server: python seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

from rag_pipeline import RAGPipeline

DOCUMENTS = {
    "personal_loan_policy.txt": """
PERSONAL LOAN POLICY DOCUMENT
===============================

1. ELIGIBILITY CRITERIA
Applicants must be between 21-60 years of age. Minimum monthly income: ₹25,000 for salaried individuals, ₹40,000 net monthly profit for self-employed. Minimum credit score: 700 (CIBIL). Employment stability: Minimum 2 years of total work experience with at least 6 months in current job.

2. LOAN AMOUNT & TENURE
Minimum loan amount: ₹50,000. Maximum loan amount: ₹40,00,000 (forty lakhs). Loan tenure options: 12 months to 60 months. Processing fee: 1% to 2.5% of loan amount + GST.

3. INTEREST RATES
Interest rates are linked to the bank's MCLR (Marginal Cost of Funds Based Lending Rate).
- Excellent credit (750+): 10.5% - 12% per annum
- Good credit (700-749): 12% - 15% per annum
- Standard credit (650-699): 15% - 18% per annum
All rates are subject to change quarterly based on RBI policy.

4. DOCUMENTS REQUIRED
- Identity proof: Aadhaar, PAN Card, Passport, or Voter ID
- Address proof: Utility bill, rent agreement, or bank statement
- Income proof: Last 3 months salary slips, Form 16, ITR of last 2 years
- Bank statements: Last 6 months

5. REPAYMENT
Repayment via Equated Monthly Instalments (EMI). EMI auto-debited from registered bank account on the 5th of every month. Prepayment allowed after 6 months with 2% foreclosure charge. Part-prepayment allowed: minimum ₹10,000 per transaction.

6. DEFAULT & PENALTIES
Late payment penalty: 2% per month on overdue EMI. Bounced cheque/ECS charges: ₹500 per instance. After 90 days of non-payment, account classified as NPA (Non-Performing Asset).
""",

    "credit_card_terms.txt": """
CREDIT CARD TERMS AND CONDITIONS
===================================

1. CARD TYPES OFFERED
a) Classic Card: Credit limit ₹50,000 - ₹2,00,000. Annual fee: ₹499. Rewards: 1 point per ₹100.
b) Gold Card: Credit limit ₹2,00,000 - ₹5,00,000. Annual fee: ₹999. Rewards: 2 points per ₹100. Lounge access: 4 visits/year.
c) Platinum Card: Credit limit ₹5,00,000+. Annual fee: ₹2,999. Rewards: 3 points per ₹100. Unlimited lounge access. Concierge service.

2. INTEREST CHARGES
APR (Annual Percentage Rate): 36% to 42% per annum (3% to 3.5% per month).
Interest-free period: Up to 50 days from purchase date if full outstanding is paid by due date.
Minimum payment due: 5% of total outstanding or ₹500, whichever is higher.
Finance charges apply from transaction date if minimum payment not made.

3. FEES & CHARGES
Annual fee: As per card type (waived if annual spend exceeds ₹1,50,000 for Gold; ₹3,00,000 for Platinum).
Cash advance fee: 2.5% of amount or ₹500, whichever is higher.
Foreign transaction fee: 3.5% of transaction amount.
Overlimit fee: ₹500 per instance.
Duplicate statement fee: ₹100 per statement.

4. REWARDS & REDEMPTION
Reward points validity: 3 years from date of earning.
Redemption options: Cashback (1 point = ₹0.25), flight miles, hotel bookings, merchandise.
Minimum redemption: 500 points.
Bonus categories: 5X rewards on dining and online shopping (Platinum only).

5. SECURITY FEATURES
3D Secure OTP for online transactions. Instant block via mobile app or customer care. Zero liability on fraudulent transactions reported within 7 days. Transaction alerts via SMS and email.

6. CREDIT LIMIT ENHANCEMENT
Can apply after 6 months of card usage. Automatic enhancement for good payment history after 12 months. Enhancement based on income proof, credit score, and payment behaviour.

7. BILLING CYCLE
Statement generated on 15th of each month. Payment due date: 5th of the following month. Grace period: 3 days after due date before late payment fee applied.
""",

    "banking_faqs.txt": """
BANKING FREQUENTLY ASKED QUESTIONS
=====================================

Q: How do I open a savings account?
A: Visit any branch with Aadhaar card, PAN card, and one passport-size photograph. Alternatively, open online via our website with video KYC. Minimum initial deposit: ₹1,000 for regular savings, zero balance for digital savings account.

Q: What is the interest rate on savings accounts?
A: Regular savings account: 3.5% per annum. High-yield savings account (balance above ₹1 lakh): 4.5% per annum. Interest calculated daily and credited quarterly.

Q: How do I reset my net banking password?
A: Click "Forgot Password" on the login page. Authenticate via OTP sent to registered mobile. Set a new password with minimum 8 characters including uppercase, lowercase, number, and special character. If account is locked after 3 failed attempts, visit branch or call 1800-XXX-XXXX.

Q: What are the NEFT/RTGS/IMPS transaction limits?
A: IMPS: Up to ₹5,00,000 per transaction, 24x7 available. NEFT: No limit, available in half-hourly batches from 8 AM to 7 PM on bank working days. RTGS: Minimum ₹2,00,000, for high-value transfers, available 7 AM to 6 PM on bank working days. UPI: ₹1,00,000 per transaction (₹2,00,000 for verified merchants).

Q: How do I link Aadhaar to my bank account?
A: Via net banking: Go to Profile > Link Aadhaar > Enter Aadhaar number > OTP verification. Via branch: Fill Aadhaar seeding form with a photocopy. Via ATM: Select "Services" > "Aadhaar Registration". Via mobile app: Profile settings > Aadhaar linking.

Q: What is the process for a fixed deposit?
A: FD can be opened online or at branch. Minimum amount: ₹10,000. Tenure: 7 days to 10 years. Interest rates: 5.5% (7-90 days), 6.0% (91-364 days), 6.75% (1-2 years), 7.0% (2-5 years), 7.25% (5-10 years). Senior citizens get additional 0.5% interest. TDS deducted at 10% if interest exceeds ₹40,000/year (₹50,000 for senior citizens).

Q: How to apply for a debit card?
A: Automatically issued with new account opening. Replacement card: Apply via mobile app, net banking, or visit branch. Charges: ₹200 for duplicate card. Activation: First transaction at ATM with PIN. International usage: Enable via mobile app before travel.

Q: What is the home loan process?
A: Step 1 - Check eligibility online. Step 2 - Submit application with documents. Step 3 - Property evaluation by our empanelled valuers. Step 4 - Legal verification of property documents. Step 5 - Loan sanction letter issued. Step 6 - Disbursement upon property registration. Processing time: 7-15 working days.

Q: How can I dispute a transaction?
A: Report via: Mobile app (Raise Dispute), Net banking (Transaction History > Dispute), Customer care: 1800-XXX-XXXX. Time limit: Within 60 days of transaction. Provisional credit within 10 days for debit card fraud. Resolution within 45 days as per RBI guidelines.

Q: What happens if I lose my debit/credit card?
A: Immediately block via: Mobile app > Card Management > Block Card. Call 24x7 helpline: 1800-XXX-XXXX. SMS "BLOCK XXXX" (last 4 digits) to 56789. Apply for replacement card online or at branch. Zero liability for fraud reported within 7 days of loss notification.

Q: What is CIBIL score and how does it affect loans?
A: CIBIL (Credit Information Bureau India Limited) score ranges from 300-900. 750-900: Excellent - best rates available. 700-749: Good - standard rates. 650-699: Fair - higher rates, may need collateral. Below 650: Poor - loan may be rejected. Score updated monthly. Check free score once per year at CIBIL website.

Q: How to apply for internet banking?
A: Visit branch with account number and registered mobile number. OR Apply online using debit card details. First-time login: Use temporary credentials sent to registered mobile. Set permanent login ID and password. Enable 2FA for additional security.
""",

    "rbi_guidelines.txt": """
RBI GUIDELINES & COMPLIANCE INFORMATION
==========================================

1. KNOW YOUR CUSTOMER (KYC) NORMS
As per RBI Master Direction on KYC, all customers must complete KYC. 
Full KYC: Officially Valid Documents (OVD) required - Passport, Voter ID, Driving License, Aadhaar, NREGA Job Card, or National Population Register letter.
Periodic KYC update: Every 2 years for high-risk customers, 8 years for medium-risk, 10 years for low-risk.
Video KYC (V-CIP): Live photograph and OVD verification via video call acceptable as per RBI circular dated January 9, 2020.

2. FAIR PRACTICES CODE FOR LENDERS
Loan application acknowledgment within 2 working days. Loan sanction/rejection communication with reasons within stipulated time. No changes in loan terms without prior notice. All charges disclosed upfront in a standardized format. Right of customer to receive loan agreement copy before disbursement.

3. DEPOSIT INSURANCE
All deposits (savings, current, FD, RD) insured up to ₹5,00,000 per depositor per bank under DICGC (Deposit Insurance and Credit Guarantee Corporation). Insurance covers principal + interest up to ₹5 lakh.

4. BANKING OMBUDSMAN SCHEME
If grievance not resolved by bank within 30 days, customers can file complaint with Banking Ombudsman. Online complaint: https://cms.rbi.org.in. No fee for filing complaint. Ombudsman can award compensation up to ₹20 lakhs. Covers: ATM/debit card issues, credit card complaints, internet banking, loans, deposits, remittances.

5. INTEREST RATE POLICY
MCLR (Marginal Cost of Funds Based Lending Rate) revised monthly by bank. External Benchmark Lending Rate (EBLR) linked to RBI Repo Rate for home loans and MSME loans. All floating rate loans to be linked to EBLR from October 1, 2019. Repo rate as of latest RBI policy: As announced in the latest Monetary Policy Committee meeting.

6. DATA PRIVACY & SECURITY
Banks must comply with IT Act 2000 and RBI cybersecurity guidelines. Customer data cannot be shared with third parties without consent. Right to data privacy under Digital Personal Data Protection Act, 2023. SMS/email alerts mandatory for all transactions above ₹5,000.

7. PRIORITY SECTOR LENDING
Banks required to lend 40% of adjusted net credit to priority sectors including agriculture (18%), MSMEs, education, housing, and social infrastructure.

8. GRIEVANCE REDRESSAL
Every bank must have a nodal officer for grievance redressal. Customer can escalate: Branch Manager > Regional Manager > Nodal Officer > Banking Ombudsman > Consumer Court. Response within 30 days mandatory as per RBI guidelines.
"""
}


def main():
    print("Initializing RAG Pipeline...")
    pipeline = RAGPipeline()

    print(f"\nSeeding {len(DOCUMENTS)} documents into ChromaDB...")
    for filename, content in DOCUMENTS.items():
        chunks = pipeline.ingest_bytes(
            content.encode("utf-8"),
            filename=filename,
            ext=".txt"
        )
        print(f"  ✓ {filename}: {chunks} chunks")

    print(f"\nDone! Total chunks in vector store: {pipeline.doc_count()}")
    print("\nYou can now start the backend server:")
    print("  cd backend && uvicorn main:app --reload")


if __name__ == "__main__":
    main()
