import certifi

with open('certificate.pem') as certificate:   
    with open(certifi.where(), 'a') as CertRepo:
        CertRepo.write(f"\n\n{certificate.read()}")
