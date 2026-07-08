# Practice Guide: Chapter 12 (Volume 4)

## Objective
To conceptually trace the HTTP redirects and XML payloads of a standard SAML (Security Assertion Markup Language) Single Sign-On (SSO) flow.

## Assignment 1: The Initial Request
Understand how the Service Provider (SP) initiates the login.

1. You open your browser and navigate to `https://jira.company.com` (The SP).
2. The Jira server sees that you do not have an active session cookie. 
3. Because Jira is configured for SAML SSO, it generates a **SAML AuthnRequest**. This is an XML document containing Jira's unique ID and the destination URL.
4. Jira returns an `HTTP 302 Redirect` to your browser, telling it to go to Okta (The IdP). It appends the XML document (Base64 encoded) to the URL.

## Assignment 2: The Authentication
Understand how the Identity Provider (IdP) handles the user.

1. Your browser follows the redirect and lands on `https://company.okta.com/login`.
2. Okta reads the SAML AuthnRequest from the URL and knows you are trying to access Jira.
3. Okta presents a login screen. You enter your username and password.
4. Okta sends a Push Notification to your phone (MFA). You approve it.
5. Okta checks its Device Posture policies. It verifies your laptop has the corporate CrowdStrike antivirus installed. 

## Assignment 3: The Assertion
Understand how the IdP securely hands you back to the SP.

1. Because you passed all checks, Okta generates a **SAML Assertion**. This is a large XML document containing your username, your email, and your group memberships (e.g., `group=engineering`).
2. **CRITICAL STEP:** Okta cryptographically signs this XML document using a Private Key that only Okta possesses. 
3. Okta returns an `HTTP 200` with an invisible HTML form containing the signed XML document. The form contains Javascript that automatically submits itself (an HTTP POST) back to `https://jira.company.com/saml/acs`.
4. Your browser automatically POSTs the XML to Jira.
5. Jira receives the XML. It uses Okta's Public Key to verify the cryptographic signature. 
6. The signature matches! Jira now trusts that Okta generated this document. It reads your username from the XML, creates a local session cookie for you, and logs you in.

## Success Criteria
You have successfully completed this practice if you can clearly explain why the Service Provider (Jira) can trust the user's identity without ever actually seeing the user's password or MFA code (Answer: Because it verifies the cryptographic signature of the IdP's Assertion).
