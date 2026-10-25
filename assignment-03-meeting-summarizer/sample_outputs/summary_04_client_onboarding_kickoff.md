# Meeting Summary — Sample 04

**Source Transcript:** `sample_04_client_onboarding_kickoff.txt`

### Executive Overview
- MedCore Health and the engineering solutions team kicked off onboarding for a 250-clinician pilot scheduled to go live on November 16, 2026, agreeing on key HIPAA BAA agreements, Okta SAML 2.0 integration, and a three-phase rollout timeline.

### Key Points
- MedCore's legal requirement mandates a signed BAA, Okta SAML 2.0 SSO, and zero model training retention on Azure OpenAI endpoints.
- Dedicated Azure OpenAI deployments in East US 2 provide zero-data retention with abuse monitoring exemption already approved by Microsoft.
- Automated SCIM provisioning will map MedCore-Physicians to Creator role and MedCore-Nurses to Reviewer role.
- 50 historical clinical note templates will be sanitized and imported into the sandbox.

### Decisions Made
- Proceed with a 3-phase rollout: Phase 1 Sandbox & SSO by October 28, Phase 2 UAT with 15 champion clinicians November 2–11, and Phase 3 Full Pilot Launch on November 16.
- Adopt role mapping from Okta AD groups directly to application permission tiers.

### Action Items
- **Bao Dang**: Send executed HIPAA BAA and Azure zero-data-retention compliance package to MedCore legal *(Due: October 19)*
- **Dr. Kevin Chu**: Provide Okta SAML metadata XML and 50 anonymized clinical templates *(Due: October 21)*
- **Hannah Brooks**: Configure dedicated MedCore sandbox tenant, Okta group mappings, and template library *(Due: October 26)*
- **Rachel Green**: Circulate weekly onboarding status reports and schedule clinician training sessions for Nov 12–13 *(Due: Weekly / November 12)*
