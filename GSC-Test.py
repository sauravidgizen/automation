import datetime
import pandas as pd
import smtplib
from dotenv import dotenv_values
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Constants
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
CLIENT_SECRET_FILE = r"C:\Users\ksaur\OneDrive\Desktop\GSC\client_secret_200862790853-oi474mpfs5i9siicfb0rk8lkm9g4icq9.apps.googleusercontent.com.json"
PROPERTY_URL = 'sc-domain:vypzee.com'
DIMENSIONS = ['date']
ROW_LIMIT = 1000
RECIPIENT_EMAILS = ['reports@idigizen.com', 'saurav5121998@gmail.com']

# Authenticate to GSC
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

# Get the last 7 full days
def get_last_7_days():
    today = datetime.date.today()
    end_date = today - datetime.timedelta(days=3)  # GSC delay buffer
    start_date = end_date - datetime.timedelta(days=6)
    return start_date, end_date

# Send alert for low CTR
def send_alert_email(avg_ctr, sender_email, sender_password, alert_date):
    msg = EmailMessage()
    msg.set_content(f"⚠️ Alert!\n\nCTR for Vypzee.com dropped below 1% on {alert_date}.\nCTR: {avg_ctr:.2f}%")
    msg['Subject'] = f'Low CTR Alert: {alert_date}'
    msg['From'] = sender_email
    msg['To'] = ', '.join(RECIPIENT_EMAILS)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    print(f"✅ Alert email sent for {alert_date}!")

# Send summary report with attachment
def send_summary_report(csv_path, sender_email, sender_password, start_date, end_date):
    msg = EmailMessage()
    msg['Subject'] = f'Vypzee CTR Report: {start_date} to {end_date}'
    msg['From'] = sender_email
    msg['To'] = ', '.join(RECIPIENT_EMAILS)
    msg.set_content(f"📈 Attached is the Vypzee.com CTR report from {start_date} to {end_date}.\n\nRegards,\nCTR Monitor Bot")

    with open(csv_path, 'rb') as file:
        file_data = file.read()
        file_name = os.path.basename(csv_path)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    print("📩 CTR report email sent to all recipients!")

# Fetch data from GSC
def get_gsc_data(service, site_url, start_date, end_date):
    request = {
        'startDate': start_date.isoformat(),
        'endDate': end_date.isoformat(),
        'dimensions': DIMENSIONS,
        'rowLimit': ROW_LIMIT
    }
    try:
        response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
        print(f"\n📊 GSC API returned {len(response.get('rows', []))} rows from {start_date} to {end_date}")
        return response.get('rows', [])
    except Exception as e:
        print(f"❌ Error fetching GSC data: {e}")
        return []

# Main execution
def main():
    creds = authenticate()
    service = build('searchconsole', 'v1', credentials=creds)
    start_date, end_date = get_last_7_days()
    print(f"\n📅 Fetching data from {start_date} to {end_date}...")

    rows = get_gsc_data(service, PROPERTY_URL, start_date, end_date)

    # Prepare date range
    full_dates = [(start_date + datetime.timedelta(days=i)).isoformat() for i in range(7)]
    ctr_map = {row['keys'][0]: row.get('ctr', 0) * 100 for row in rows}

    # Load .env credentials
    env_creds = dotenv_values(r"C:\Users\ksaur\OneDrive\Desktop\GSC\.env")
    sender_email = env_creds.get("SENDER_EMAIL")
    sender_password = env_creds.get("SENDER_PASSWORD")

    final_data = []

    for date in full_dates:
        if date in ctr_map:
            ctr = ctr_map[date]
            is_healthy = "Yes" if ctr >= 1.0 else "No"
            alert_sent = "No"

            if ctr < 1.0 and sender_email and sender_password:
                send_alert_email(ctr, sender_email, sender_password, date)
                alert_sent = "Yes"

            final_data.append([date, f"{ctr:.2f}%", is_healthy, alert_sent])
        else:
            final_data.append([date, "No data", "No data", "No data"])

    df = pd.DataFrame(final_data, columns=['Date', 'CTR', 'Is CTR Healthy', 'Alert Sent'])

    # Save CSV
    csv_path = fr"C:\Users\ksaur\Downloads\gsc_ctr_daily_report_{start_date}_to_{end_date}.csv"
    df.to_csv(csv_path, index=False)

    print(f"\n✅ CTR Report saved to:\n{csv_path}")
    print("\n🧾 Final CTR Summary:\n")
    print(df)

    # Send report to all recipients
    if sender_email and sender_password:
        send_summary_report(csv_path, sender_email, sender_password, start_date, end_date)

if __name__ == '__main__':
    main()
