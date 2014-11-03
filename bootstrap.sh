#!/bin/bash

# this updates and installs lxc-docker
curl -sSL https://get.docker.io/ubuntu/ | sudo sh

# add the vagrant user to the docker group
usermod -g docker vagrant

# install registry cert
mkdir -p /etc/docker/certs.d/r.iadops.com/
echo "-----BEGIN CERTIFICATE-----" > /etc/docker/certs.d/r.iadops.com/ca.crt
echo "MIID7TCCAtWgAwIBAgIJAO/As4eaf7Q6MA0GCSqGSIb3DQEBCwUAMIGMMQswCQYD" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "VQQGEwJVUzERMA8GA1UECAwITmV3IFlvcmsxETAPBgNVBAcMCE5ldyBZb3JrMQww" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "CgYDVQQKDANPQU8xDzANBgNVBAsMBkJUU0RFVjEVMBMGA1UEAwwMci5pYWRvcHMu" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "Y29tMSEwHwYJKoZIhvcNAQkBFhJqbWlsbGVyQGlhZG9wcy5jb20wHhcNMTQxMTAz" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "MTc0MzIyWhcNMTUxMTAzMTc0MzIyWjCBjDELMAkGA1UEBhMCVVMxETAPBgNVBAgM" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "CE5ldyBZb3JrMREwDwYDVQQHDAhOZXcgWW9yazEMMAoGA1UECgwDT0FPMQ8wDQYD" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "VQQLDAZCVFNERVYxFTATBgNVBAMMDHIuaWFkb3BzLmNvbTEhMB8GCSqGSIb3DQEJ" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "ARYSam1pbGxlckBpYWRvcHMuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "CgKCAQEArfCOIOdG7UodiPGQdOsfyILnvTKjH3+YEmwOLIENbI50kDcs9tav/AC5" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "GwPT+IblrhcmmJX0DeVPXzBf7FNweCl1r5bkabc9gnUPIHDSObC/ej3r7/+gF6bF" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "qbJDqM/3QX/ePx8hhsnmb8n7NGF9lfSlMvxp2F9RFuxL29sXvt4tLrZZj1B/VBzg" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "yHcZt5UGhK+1CNQsvPbY1S852RBacSMP3X34v74w9G6GEepI5dpQQ4PHQiAqBPeE" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "27wqYBKBcsbzAWcSRLXFhf/w4AFMsOJUaPNLkfRsO93/P2OsDX95O+oAnDEDsZMV" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "PQJs52Ky3/yAp5aJZZ/FtHvg9aYr4wIDAQABo1AwTjAdBgNVHQ4EFgQUCi3oa93J" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "xGSTxImMIQWFBhPjkA0wHwYDVR0jBBgwFoAUCi3oa93JxGSTxImMIQWFBhPjkA0w" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAZzJ9vlTQJRtjpTrMMQ9f" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "0vnTIbPHg4/Nk1Em7XO3GdDZ89mSv1sPS9X/meWpCzm2+2yBR2+rSoQbQfI7NgjX" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "rjFsvb6mcaNpja+kC6xlMCTu5mP5hLxAWCZNtBHYJ/btObq1A/4kofhlUSRN6hqH" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "WFWAA5xKyll1rZSP5ZvyIokQbZWuJLe5v53K4hv5MCnAIOi1PQbpUwMNebU+fP9v" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "H3gz4vWuBn8XFWPjlDUmF6UzquI+Qjyqz4FUq3XRdb0pc2V4JCvpzJhjPkVb2ZiS" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "6Dxh5QX1XKXPuz3g4roeBIzSb1Cd8nGleVnE4I2zXaQVJH3qXJKueBqUj24ER0GI" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "ZA==" >> /etc/docker/certs.d/r.iadops.com/ca.crt
echo "-----END CERTIFICATE-----" >> /etc/docker/certs.d/r.iadops.com/ca.crt
