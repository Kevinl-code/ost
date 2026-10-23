import streamlit as st

st.set_page_config(
    page_title="Open Source Data Analytics Lab",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Open Source Data Analytics Lab")
st.write(
    "Browse all Python programs by title, view syntax-highlighted code, "
    "and download individual programs or the complete collection."
)

PROGRAMS = {
    1: ("Customer Segmentation using K-Means Clustering", '''
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("Mall_Customers.csv")
X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = KMeans(n_clusters=5, random_state=42, n_init=10)
df["Cluster"] = model.fit_predict(X_scaled)

plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=df["Cluster"])
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score")
plt.title("Customer Segmentation using K-Means")
plt.show()

print(df.groupby("Cluster")[[
    "Annual Income (k$)", "Spending Score (1-100)"
]].mean())

2. Sentiment Analysis
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("sentiment.csv")

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["sentiment"], test_size=0.2,
    random_state=42, stratify=df["sentiment"]
)

vectorizer = TfidfVectorizer(stop_words="english")
Xtr = vectorizer.fit_transform(X_train)
Xte = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(Xtr, y_train)
pred = model.predict(Xte)

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

print(model.predict(vectorizer.transform([
    "This product is excellent and useful"
])

3. Fraud Detection in Credit Card Transactions
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("creditcard.csv")
X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100, random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)
pred = model.predict(X_test)

print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred, digits=4))

5. Stock Price Prediction using Pandas and NumPy
        
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("AAPL.csv", parse_dates=["Date"])
df = df.sort_values("Date").dropna(subset=["Close"])

df["MA7"] = df["Close"].rolling(7).mean()
df["Prediction"] = df["MA7"].shift(1)

mae = np.mean(
    np.abs(df["Close"] - df["Prediction"]).dropna()
)
print("Mean Absolute Error:", round(mae, 3))

plt.plot(df["Date"], df["Close"], label="Actual")
plt.plot(df["Date"], df["Prediction"], label="7-day MA Prediction")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.title("Stock Price Analysis")
plt.legend()
plt.show()

6. Customer Churn Prediction 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("Customer Churn.csv")
X = pd.get_dummies(df.drop(columns=["Churn"]), drop_first=True)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

plt.figure(figsize=(16, 8))
plot_tree(
    model, feature_names=X.columns,
    class_names=True, filled=False, max_depth=3
)
plt.show()

    7: COVID-19 Data Visualization using Seaborn
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url, parse_dates=["date"])

country = df[df["location"] == "India"].copy()
country["new_cases_7d"] = country["new_cases"].rolling(7).mean()

sns.lineplot(data=country, x="date", y="new_cases_7d")
plt.title("COVID-19 7-Day Average New Cases - India")
plt.xlabel("Date")
plt.ylabel("New Cases (7-day average)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

    8:Sales Dashboard using Plotly and Dash
 from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")
df = df.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice"])

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Sales"] = df["Quantity"] * df["UnitPrice"]

monthly = (
    df.set_index("InvoiceDate")["Sales"]
    .resample("ME").sum().reset_index()
)

fig = px.line(monthly, x="InvoiceDate", y="Sales", title="Monthly Sales")
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard"),
    html.H3(f"Total Sales: {df['Sales'].sum():,.2f}"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)

9: IoT Sensor Data Visualization using Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("IoT Sensor Monitoring Dashboard")

df = pd.read_csv("sensor_data.csv", parse_dates=["timestamp"])
st.write(df.describe())

metric = st.selectbox(
    "Select sensor", ["temperature", "humidity", "pressure"]
)

fig = px.line(
    df, x="timestamp", y=metric,
    title=f"{metric.title()} over Time"
)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(df.tail(20))

10:Customer Churn Analysis
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("Customer Churn.csv")

print(df.info())
print(df.isna().sum())
print(df["Churn"].value_counts(normalize=True))

sns.countplot(data=df, x="Churn")
plt.title("Churn Distribution")
plt.show()

sns.boxplot(data=df, x="Churn", y="Customer Value")
plt.title("Customer Value by Churn Status")
plt.show()

print(pd.crosstab(
    df["Complains"], df["Churn"], normalize="index"
))

11: Marketing Campaign Performance Analysis
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("bank.csv", sep=";")
df["response"] = (df["y"] == "yes").astype(int)

print(
    "Overall response rate:",
    round(df["response"].mean() * 100, 2), "%"
)

rate = (
    df.groupby("contact")["response"]
    .mean().sort_values(ascending=False)
)

print((rate * 100).round(2))
sns.barplot(x=rate.index, y=rate.values)
plt.ylabel("Response Rate")
plt.xlabel("Contact Method")
plt.title("Marketing Campaign Response by Contact Method")
plt.xticks(rotation=20)
plt.show()

12: Weather Pattern Visualization using Matplotlib

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("weather.csv", parse_dates=["Date"])
df = df.sort_values("Date")

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df["Date"], df["Temperature"], label="Temperature")
ax1.set_xlabel("Date")
ax1.set_ylabel("Temperature")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.bar(df["Date"], df["Rainfall"], alpha=0.25, label="Rainfall")
ax2.set_ylabel("Rainfall")

plt.title("Weather Pattern Visualization")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()''')
}

# Display every program on the same page
