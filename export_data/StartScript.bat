echo "======START======" >> D:\Scripts\Script\log\export_data.log
PowerShell -Command "get-date" >> D:\Scripts\Script\log\export_data.log
python D:\Scripts\Script\export_data\APP_Q_DATA
PowerShell -Command "get-date" >> D:\Scripts\Script\log\export_data.log
echo "======END======" >> D:\Scripts\Script\log\export_data.log