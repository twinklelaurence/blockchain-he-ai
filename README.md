README:  Confidential Student Score Dashboard

A secure and intelligent prototype that enables encrypted student score analysis, risk prediction, and tamper-proof logging using Homomorphic Encryption (HE), AI-driven logic, and Blockchain-style audit trails — all in an intuitive Streamlit dashboard.



Features

Encrypted Score Entry: Students’ academic scores and engagement levels are entered through a simple UI and encrypted using the CKKS scheme via TenSEAL.



AI-based Risk Assessment: Automatically computes academic risk (Low, Medium, High) based on encrypted scores and engagement levels — without exposing raw data.



Homomorphic Encryption: All input data is encrypted using TenSEAL before any analysis, preserving confidentiality.



Blockchain-style Logging: Each submission is hashed and stored in a secure, verifiable JSON chain.



Multi-term Progress Tracking: Track student performance and engagement across multiple terms.



Visual Dashboard: Streamlit-based charts for average scores, engagement trends, and overall risk level.



Technologies Used

Component	Technology Used

Language	Python 3.12

UI Framework	Streamlit

Encryption	TenSEAL (CKKS Scheme)

Data Handling	NumPy, pandas

Hashing	SHA-256 via hashlib

Audit Log	JSON-based blockchain file



How It Works

User Input: Enter student ID, subject scores (out of 100), and engagement percentage for each term.



Encryption: Scores are encrypted using the CKKS scheme via TenSEAL.



AI Logic: Risk level is computed based on average score and engagement (rule-based logic).



Blockchain Log: Each submission is logged in student\_chain.json with timestamp and SHA-256 hash.



Visualization: View student trends, risk level changes, and progress over time.



Getting Started

1\. Clone the Repository

git clone https://github.com/twinklelaurence/blockchain-he-ai.git

cd Research-work



2\. Install Dependencies

pip install streamlit pandas numpy tenseal

⚠️ Note: You may need to install cmake, g++, or ninja if TenSEAL fails to compile.



3\. Generate the Encryption Context

python generate\_context.py

This creates tenseal\_context.tenseal with both public and secret keys saved at:

/encryption/tenseal\_context.tenseal



4\. Run the Dashboard

streamlit run dashboard.py



📂 File Structure



📁 Research-work/

├── dashboard.py               # Main Streamlit dashboard

├── generate\_context.py        # One-time setup for CKKS encryption context

├── encryption/

│   └── tenseal\_context.tenseal  # Serialized TenSEAL context

├── student\_chain.json         # Blockchain-style audit log

├── Studentdata.csv            # (Optional) Sample dataset

└── README.md

📦 Sample Blockchain Log Entry



{

  "timestamp": "2025-07-22T13:45:23Z",

  "student\_id": "student1",

  "term": "Term 1",

  "data": {

    "average\_score": 72.4,

    "engagement": 80.0,

    "risk": "Low Risk"

  },

  "prev\_hash": "000000000000000...",

  "hash": "93a49a7f3dbf09..."

}

🔒 Security Notes

All scores and engagement data are encrypted before any computation.



Private key access is required to decrypt and analyze the data outside the dashboard.



Blockchain log is immutable: tampering breaks hash verification.



📈 Future Improvements

✅ Federated Learning compatibility (decentralized risk model training)



✅ DID (Decentralized Identity) integration



✅ Visual Explainability (XAI on encrypted inference)



✅ IPFS or Layer-2 Blockchain storage for large-scale logs

