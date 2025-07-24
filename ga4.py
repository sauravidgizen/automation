# ===========================
# SEO Insight Engine: GA4 Enabled, GSC + SEMrush Commented
# ===========================

# ---------- Imports ----------
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Metric, Dimension
)
from google.oauth2 import service_account
import pandas as pd

# from gsc_insight_engine import GSCInsightEngine  # 🔒 GSC - Commented
# from semrush_scraper import SemrushScraper      # 🔒 SEMrush - Commented


# ---------- Config ----------
GA4_PROPERTY_ID = "419299062"
CREDENTIALS_PATH = r"C:\Users\ksaur\Downloads\gscapi-461308-a75100a45b10.json"


# ---------- GA4 Insight Engine ----------
class GA4InsightEngine:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
        self.client = BetaAnalyticsDataClient(credentials=credentials)
        self.date_range = DateRange(start_date="7daysAgo", end_date="today")

    def run_report(self, dimensions=[], metrics=[], filters=None):
        request = RunReportRequest(
            property=f"properties/{GA4_PROPERTY_ID}",
            date_ranges=[self.date_range],
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            dimension_filter=filters
        )
        response = self.client.run_report(request)
        rows = [{dim.name: row.dimension_values[i].value
                 for i, dim in enumerate(dimensions)}
                | {met.name: float(row.metric_values[i].value)
                 for i, met in enumerate(metrics)}
                for row in response.rows]
        return pd.DataFrame(rows)

    def total_sessions(self):
        df = self.run_report(metrics=["sessions"])
        return int(df['sessions'].sum())

    def organic_sessions_percent(self):
        total = self.total_sessions()
        df = self.run_report(
            dimensions=["sessionDefaultChannelGroup"],
            metrics=["sessions"]
        )
        organic = df[df['sessionDefaultChannelGroup'] == 'Organic Search']['sessions'].sum()
        return round((organic / total) * 100, 2) if total else 0

    def top_traffic_sources(self):
        return self.run_report(
            dimensions=["sessionDefaultChannelGroup"],
            metrics=["sessions"]
        ).sort_values(by="sessions", ascending=False)

    def engagement_rate(self):
        df = self.run_report(metrics=["engagementRate"])
        return f"{round(df['engagementRate'].iloc[0] * 100, 2)}%"

    def avg_session_duration(self):
        df = self.run_report(metrics=["averageSessionDuration"])
        seconds = float(df['averageSessionDuration'].iloc[0])
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d} min"

    def geo_breakdown(self, dimension="country"):
        return self.run_report(
            dimensions=[dimension],
            metrics=["sessions"]
        ).sort_values(by="sessions", ascending=False).head(5)

    def new_vs_returning(self):
        return self.run_report(
            dimensions=["newVsReturning"],
            metrics=["sessions"]
        )

    def device_breakdown(self):
        return self.run_report(
            dimensions=["deviceCategory"],
            metrics=["sessions"]
        ).sort_values(by="sessions", ascending=False)

    def all_insights(self):
        return {
            "Total Sessions": self.total_sessions(),
            "% Organic Traffic": f"{self.organic_sessions_percent()}%",
            "Engagement Rate": self.engagement_rate(),
            "Avg Session Duration": self.avg_session_duration(),
            "Top Sources": self.top_traffic_sources(),
            "Top Countries": self.geo_breakdown("country"),
            "Top Cities": self.geo_breakdown("city"),
            "New vs Returning": self.new_vs_returning(),
            "Device Breakdown": self.device_breakdown()
        }


# ---------- Main ----------
if __name__ == "__main__":
    # -------- GA4 --------
    print("\n GA4 Insights")
    ga4 = GA4InsightEngine()
    ga4_data = ga4.all_insights()

    print(f"Total Sessions: {ga4_data['Total Sessions']}")
    print(f"% Organic Traffic: {ga4_data['% Organic Traffic']}")
    print(f"Engagement Rate: {ga4_data['Engagement Rate']}")
    print(f"Avg Session Duration: {ga4_data['Avg Session Duration']}")
    
    print("\nTop Traffic Sources:")
    print(ga4_data['Top Sources'])

    print("\nTop Countries:")
    print(ga4_data['Top Countries'])

    print("\nTop Cities:")
    print(ga4_data['Top Cities'])

    print("\nNew vs Returning:")
    print(ga4_data['New vs Returning'])

    print("\nDevice Breakdown:")
    print(ga4_data['Device Breakdown'])

    # -------- GSC --------
    # print("\n🟡 GSC Insights")
    # gsc = GSCInsightEngine(df_now, df_prev, brand_term="vypzee")
    # gsc_insights = gsc.all_insights()

    # -------- SEMrush --------
    # print("\n🔵 SEMrush Insights")
    # semrush = SemrushScraper(driver)
    # semrush_data = semrush.get_data()
