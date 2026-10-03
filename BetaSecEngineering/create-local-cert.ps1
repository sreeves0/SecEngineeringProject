# PowerShell 7: generate disposable lab material without touching certificate stores.
$ErrorActionPreference = 'Stop'
$certDirectory = Join-Path $PSScriptRoot 'local-certs'
if (Test-Path -LiteralPath $certDirectory) {
    throw 'local-certs already exists. Preserve it, or remove it manually before regenerating.'
}
$rsa = [System.Security.Cryptography.RSA]::Create(2048)
try {
    $request = [System.Security.Cryptography.X509Certificates.CertificateRequest]::new(
        'CN=localhost', $rsa, [System.Security.Cryptography.HashAlgorithmName]::SHA256,
        [System.Security.Cryptography.RSASignaturePadding]::Pkcs1)
    $san = [System.Security.Cryptography.X509Certificates.SubjectAlternativeNameBuilder]::new()
    $san.AddDnsName('localhost')
    $san.AddIpAddress([System.Net.IPAddress]::Parse('127.0.0.1'))
    $request.CertificateExtensions.Add($san.Build())
    $certificate = $request.CreateSelfSigned([DateTimeOffset]::UtcNow.AddMinutes(-5), [DateTimeOffset]::UtcNow.AddDays(30))
    try {
        New-Item -ItemType Directory -Path $certDirectory | Out-Null
        [System.IO.File]::WriteAllText((Join-Path $certDirectory 'localhost.pem'), $certificate.ExportCertificatePem())
        [System.IO.File]::WriteAllText((Join-Path $certDirectory 'localhost-key.pem'), $rsa.ExportPkcs8PrivateKeyPem())
    } finally {
        $certificate.Dispose()
    }
} finally {
    $rsa.Dispose()
}
Write-Output 'Created a 30-day self-signed localhost lab certificate. No system trust was changed.'
