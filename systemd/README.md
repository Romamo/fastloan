cp -R /home/fastloan/main/systemd/fastloan.service /etc/systemd/system/fastloan.service
systemctl daemon-reload
systemctl start fastloan
systemctl status fastloan

systemctl restart fastloan
