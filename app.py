
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
company_df = pd.read_csv("company_info.csv")
audience_df = pd.read_csv("audience_info.csv")
budget_df = pd.read_csv("event_budget.csv")
history_df = pd.read_csv("history_event.csv")

# Sidebar navigation
st.sidebar.title("📊 Expo Management Dashboard")
page = st.sidebar.radio("Select a page:", ["Dashboard", "Companies", "Finance", "Audience Insights", "History"])

st.title("Expo Data Visualization Platform")

if page == "Dashboard":
    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Companies", len(company_df))
    col2.metric("Total Audience", len(audience_df))
    col3.metric("Total Revenue", f"${budget_df['ActualRevenue'].sum():,.0f}")

    st.subheader("📊 Budget vs Revenue")
    fig = px.bar(budget_df, x="EventName", y=["PlannedBudget", "ActualRevenue"], barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Companies":
    st.subheader("🏢 Company Participation")
    industry_filter = st.selectbox("Select Industry:", options=["All"] + sorted(company_df["Industry"].unique().tolist()))
    if industry_filter != "All":
        filtered_df = company_df[company_df["Industry"] == industry_filter]
    else:
        filtered_df = company_df
    st.dataframe(filtered_df)
    st.bar_chart(filtered_df["ParticipationTimes"].value_counts().sort_index())

elif page == "Finance":
    st.subheader("💰 Financial Breakdown")
    selected_event = st.selectbox("Choose an Event:", options=budget_df["EventName"].tolist())
    event_data = budget_df[budget_df["EventName"] == selected_event].iloc[0]
    values = [event_data["PromotionCost"], event_data["VenueCost"], event_data["ActualRevenue"]]
    labels = ["Promotion Cost", "Venue Cost", "Actual Revenue"]
    fig_pie = px.pie(values=values, names=labels, title=f"{selected_event} Financial Breakdown")
    st.plotly_chart(fig_pie)

elif page == "Audience Insights":
    st.subheader("👥 Audience Demographics")
    gender_chart = px.pie(audience_df, names="Gender", title="Gender Distribution")
    st.plotly_chart(gender_chart, use_container_width=True)

    age_hist = px.histogram(audience_df, x="Age", nbins=10, title="Age Distribution")
    st.plotly_chart(age_hist, use_container_width=True)

    ticket_chart = px.pie(audience_df, names="TicketType", title="Ticket Type")
    st.plotly_chart(ticket_chart, use_container_width=True)

elif page == "History":
    st.subheader("📅 Historical Events")
    year_range = st.slider("Select Year Range:", 2019, 2024, (2019, 2024))
    history_df["Year"] = pd.to_datetime(history_df["Date"]).dt.year
    filtered_history = history_df[history_df["Year"].between(year_range[0], year_range[1])]
    st.dataframe(filtered_history)
    fig_line = px.line(filtered_history, x="Date", y="AudienceCount", title="Audience Count Over Time")
    st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit and Plotly | CUHK 2025")
