# Sources

## SAML SSO sources
- https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0-cd-02.html - Overview of the whole SAML framework
- https://www.oasis-open.org/committees/download.php/56776/sstc-saml-core-errata-2.0-wd-07.pdf - SAML "core" specification which defines the protocol messages and the basic request/response protocol.
- https://www.oasis-open.org/committees/download.php/56779/sstc-saml-bindings-errata-2.0-wd-06.pdf - SAML binding specification (for the SAML SSO project we use only HTTP POST Binding).
- https://www.oasis-open.org/committees/download.php/56782/sstc-saml-profiles-errata-2.0-wd-07.pdf - SAML profiles specification AKA specific protocol specification. Section 4 defines the Single Sign-On (SSO) protocol.
## TLS sources
- https://www.cloudflare.com/en-gb/learning/ssl/transport-layer-security-tls/ - Nice brief TLS overview.
- https://en.wikipedia.org/wiki/Transport_Layer_Security
- https://en.wikipedia.org/wiki/HTTPS
- https://tls13.xargs.org/ - In depth explanation of TLS 1.3.
- https://www.rfc-editor.org/rfc/rfc8446 - TLS 1.3 specification. I think only the introduction might be helpful for the report.
## Cryptography sources (digital signatures, certificates etc.)
- https://en.wikipedia.org/wiki/Digital_signature
- https://en.wikipedia.org/wiki/Public-key_cryptography
- https://en.wikipedia.org/wiki/Symmetric-key_algorithm
- https://en.wikipedia.org/wiki/Public_key_infrastructure
- https://en.wikipedia.org/wiki/Certificate_authority
- https://en.wikipedia.org/wiki/Public_key_certificate
- https://cacr.uwaterloo.ca/hac/about/chap1.pdf
- https://cacr.uwaterloo.ca/hac/about/chap10.pdf - Talks about authentication - could be useful for the report when discussing multifactor authentication
- https://cacr.uwaterloo.ca/hac/about/chap11.pdf - Detailed explanation of the digital signature algorithms - heavy math

## Implementation sources
- https://flask.palletsprojects.com/en/3.0.x/ - Python library for creating HTTP web servers.
- https://lxml.de/ - Python library for parsing/processing XML documents (SAML messages are XML documents).
- https://cryptography.io/en/latest/ - Python library for cryptographic operations - hashing, signature creation/verification, certificate validation.