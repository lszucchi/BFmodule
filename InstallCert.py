import certifi

with open(__file__.rsplit('\\', 1)[0] + '\\certificate.pem') as certificate:   
    with open(certifi.where(), 'a') as CertRepo:
        CertRepo.write(f"\n\n{certificate.read()}")
        print(f"Certificate added to {certifi.where()}")
