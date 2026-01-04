import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Period Tracker",
    layout="centered"
)

st.title("🌸 Period Tracker")
st.caption("Log your period dates and get a predicted cycle schedule.")

DATA_FILE = "period_data.csv"


if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["Start Date"] = pd.to_datetime(df["Start Date"])
else:
    df = pd.DataFrame(columns=["Start Date"])


st.subheader("📝 Log Period Start Date")

start_date = st.date_input(
    "Select the first day of your period",
    value=date.today()
)

if st.button("Save Date"):
    
    start_date = pd.to_datetime(start_date)

    if start_date not in df["Start Date"].values:
        df = pd.concat(
            [df, pd.DataFrame([{"Start Date": start_date}])],
            ignore_index=True
        )
        df = df.sort_values("Start Date")
        df.to_csv(DATA_FILE, index=False)
        st.success("Period date saved successfully 🌷")
    else:
        st.warning("This date is already logged.")


if df.empty:
    st.info("No period dates logged yet.")
    st.stop()


st.subheader("⚙️ Cycle Settings")

cycle_length = st.slider(
    "Average cycle length (days)",
    21, 35, 28
)

period_length = st.slider(
    "Average period duration (days)",
    3, 7, 5
)


last_period = df["Start Date"].max()

next_period = last_period + timedelta(days=cycle_length)
next_end = next_period + timedelta(days=period_length - 1)

future_cycles = []

for i in range(3):
    start = last_period + timedelta(days=cycle_length * (i + 1))
    end = start + timedelta(days=period_length - 1)
    future_cycles.append({
        "Cycle": f"Cycle {i + 1}",
        "Predicted Start": start,
        "Predicted End": end
    })

schedule_df = pd.DataFrame(future_cycles)


st.subheader("🔔 Next Expected Period")

st.success(
    f"Your next period is expected to start on **{next_period.strftime('%d %b %Y')}** "
    f"and may last until **{next_end.strftime('%d %b %Y')}**."
)


schedule_display = schedule_df.copy()
schedule_display["Predicted Start"] = schedule_display["Predicted Start"].dt.strftime("%d %b %Y")
schedule_display["Predicted End"] = schedule_display["Predicted End"].dt.strftime("%d %b %Y")

st.subheader("📅 Upcoming Cycle Schedule")
st.table(schedule_display)


period_days = pd.date_range(start=next_period, end=next_end)

calendar_df = pd.DataFrame({
    "Date": period_days.strftime("%d %b %Y"),
    "Status": ["🩸 Period Day"] * len(period_days)
})

st.subheader("🗓️ Upcoming Period Days")
st.table(calendar_df)


with st.expander("📖 View Logged Period History"):
    history_df = df.copy()
    history_df["Start Date"] = history_df["Start Date"].dt.strftime("%d %b %Y")
    st.table(history_df.sort_values("Start Date", ascending=False))


st.caption(
    "🫶 This tracker provides estimated dates only and is not a medical tool."
)
