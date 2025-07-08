# 1. Создание самоподписанного сертификата
$cert = New-SelfSignedCertificate `
  -Type CodeSigningCert `
  -Subject "CN=FletDeveloper" `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -KeyExportPolicy Exportable `
  -KeySpec Signature `
  -HashAlgorithm sha256 `
  -NotAfter (Get-Date).AddYears(10)


# 2. Экспорт .pfx с паролем
$pwd = ConvertTo-SecureString -String "YourStrongPassword123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "D:\Etc\Source\halter\CERTIFICATE.pfx" -Password $pwd

# 3. Импорт в доверенные корневые центры сертификации
Import-PfxCertificate -FilePath "D:\Etc\Source\halter\CERTIFICATE.pfx" `
  -CertStoreLocation "Cert:\CurrentUser\Root" `
  -Password $pwd
