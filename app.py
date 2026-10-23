
import streamlit as st
import zipfile
import io

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
    1: (
        "Customer Segmentation using K-Means Clustering",
        '''import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("Mall_Customers.csv")

X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = KMeans(n_clusters=5, random_state=42, n_init=10)
df["Cluster"] = model.fit_predict(X_scaled)

plt.figure(figsize=(8, 5))
plt.scatter(
    X.iloc[:, 0],
    X.iloc[:, 1],
    c=df["Cluster"],
    cmap="viridis"
)

plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score")
plt.title("Customer Segmentation using K-Means")
plt.colorbar(label="Cluster")
plt.tight_layout()
plt.show()

print(df.groupby("Cluster")[
    ["Annual Income (k$)", "Spending Score (1-100)"]
].mean())
'''
    ),

    2: (
        "Sentiment Analysis using Logistic Regression",
        '''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("sentiment.csv")

X = df["text"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

vectorizer = TfidfVectorizer(stop_words="english")

Xtr = vectorizer.fit_transform(X_train)
Xte = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(Xtr, y_train)

pred = model.predict(Xte)

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

sample = ["This product is excellent and useful"]
sample_vector = vectorizer.transform(sample)

print("Predicted Sentiment:", model.predict(sample_vector)[0])
'''
    ),

    3: (
        "Fraud Detection in Credit Card Transactions",
        '''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, pred))

print("Classification Report:")
print(classification_report(y_test, pred, digits=4))
'''
    ),

    4: (
        "Stock Price Prediction using Pandas and NumPy",
        '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("AAPL.csv", parse_dates=["Date"])

df = df.sort_values("Date").dropna(subset=["Close"])

df["MA7"] = df["Close"].rolling(window=7).mean()

# Predict the current closing price using the previous
# seven-day moving average to avoid using current-day data.
df["Prediction"] = df["MA7"].shift(1)

evaluation = df.dropna(subset=["Close", "Prediction"])

mae = mean_absolute_error(
    evaluation["Close"],
    evaluation["Prediction"]
)

print("Mean Absolute Error:", round(mae, 3))

plt.figure(figsize=(10, 5))

plt.plot(
    df["Date"],
    df["Close"],
    label="Actual Closing Price"
)

plt.plot(
    df["Date"],
    df["Prediction"],
    label="7-Day Moving Average Prediction"
)

plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.title("Stock Price Analysis")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
'''
    ),

    5: (
        "Customer Churn Prediction using Decision Tree",
        '''import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("Customer Churn.csv")

X = pd.get_dummies(
    df.drop(columns=["Churn"]),
    drop_first=True
)

y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

plt.figure(figsize=(16, 8))

plot_tree(
    model,
    feature_names=X.columns,
    class_names=[str(c) for c in model.classes_],
    filled=True,
    max_depth=3,
    fontsize=8
)

plt.title("Customer Churn Decision Tree")
plt.tight_layout()
plt.show()
'''
    ),

    6: (
        "COVID-19 Data Visualization using Seaborn",
        '''import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

url = (
    "https://covid.ourworldindata.org/"
    "data/owid-covid-data.csv"
)

df = pd.read_csv(url, parse_dates=["date"])

country = df[df["location"] == "India"].copy()

country = country.sort_values("date")

country["new_cases_7d"] = (
    country["new_cases"].rolling(window=7).mean()
)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 5))

sns.lineplot(
    data=country,
    x="date",
    y="new_cases_7d"
)

plt.title("COVID-19 7-Day Average New Cases - India")
plt.xlabel("Date")
plt.ylabel("New Cases (7-Day Average)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
'''
    ),

    7: (
        "Sales Dashboard using Plotly and Dash",
        '''import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

df = pd.read_csv(
    "Online_Retail.csv",
    encoding="ISO-8859-1"
)

df = df.dropna(
    subset=["InvoiceDate", "Quantity", "UnitPrice"]
)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Sales"] = df["Quantity"] * df["UnitPrice"]

monthly = (
    df.set_index("InvoiceDate")["Sales"]
    .resample("ME")
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="InvoiceDate",
    y="Sales",
    title="Monthly Sales"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales",
    template="plotly_white"
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard"),
    html.H3(f"Total Sales: {df['Sales'].sum():,.2f}"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=False)
'''
    ),

    8: (
        "IoT Sensor Data Visualization using Streamlit",
        '''import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="IoT Sensor Monitoring",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ IoT Sensor Monitoring Dashboard")

df = pd.read_csv(
    "sensor_data.csv",
    parse_dates=["timestamp"]
)

st.subheader("Sensor Data Summary")
st.write(df.describe())

metrics = ["temperature", "humidity", "pressure"]

available_metrics = [
    metric for metric in metrics
    if metric in df.columns
]

if not available_metrics:
    st.error("No supported sensor columns were found.")
else:
    metric = st.selectbox(
        "Select Sensor",
        available_metrics
    )

    fig = px.line(
        df,
        x="timestamp",
        y=metric,
        title=f"{metric.title()} Over Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Recent Sensor Readings")
st.dataframe(df.tail(20), use_container_width=True)
'''
    ),

    9: (
        "Customer Churn Analysis using Seaborn",
        '''import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("Customer Churn.csv")

print("Dataset Information:")
df.info()

print("\\nMissing Values:")
print(df.isna().sum())

print("\\nChurn Distribution:")
print(df["Churn"].value_counts(normalize=True))

sns.set_theme(style="whitegrid")

plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Churn"
)

plt.title("Churn Distribution")
plt.xlabel("Churn Status")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()

if "Customer Value" in df.columns:
    plt.figure(figsize=(7, 5))

    sns.boxplot(
        data=df,
        x="Churn",
        y="Customer Value"
    )

    plt.title("Customer Value by Churn Status")
    plt.tight_layout()
    plt.show()

if "Complains" in df.columns:
    print("\\nComplaint Status vs Churn:")
    print(
        pd.crosstab(
            df["Complains"],
            df["Churn"],
            normalize="index"
        )
    )
'''
    ),

    10: (
        "Marketing Campaign Performance Analysis",
        '''import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("bank.csv", sep=";")

df["response"] = (df["y"] == "yes").astype(int)

overall_rate = df["response"].mean() * 100

print(
    "Overall Response Rate:",
    round(overall_rate, 2),
    "%"
)

rate = (
    df.groupby("contact")["response"]
    .mean()
    .sort_values(ascending=False)
)

print("\\nResponse Rate by Contact Method (%):")
print((rate * 100).round(2))

sns.set_theme(style="whitegrid")

plt.figure(figsize=(8, 5))

sns.barplot(
    x=rate.index,
    y=rate.values
)

plt.ylabel("Response Rate")
plt.xlabel("Contact Method")
plt.title("Marketing Campaign Response by Contact Method")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()
'''
    ),

    11: (
        "Weather Pattern Visualization using Matplotlib",
        '''import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "weather.csv",
    parse_dates=["Date"]
)

df = df.sort_values("Date")

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(
    df["Date"],
    df["Temperature"],
    label="Temperature"
)

ax1.set_xlabel("Date")
ax1.set_ylabel("Temperature")
ax1.grid(True)

ax2 = ax1.twinx()

ax2.bar(
    df["Date"],
    df["Rainfall"],
    alpha=0.25,
    label="Rainfall"
)

ax2.set_ylabel("Rainfall")

plt.title("Weather Pattern Visualization")
plt.xticks(rotation=45)
fig.tight_layout()
plt.show()
'''
    ),

    12: (
        "Exploratory Data Analysis using Pandas",
        '''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv")

print("First Five Rows:")
print(df.head())

print("\\nDataset Shape:")
print(df.shape)

print("\\nColumn Information:")
print(df.info())

print("\\nMissing Values:")
print(df.isnull().sum())

print("\\nStatistical Summary:")
print(df.describe(include="all"))

print("\\nDuplicate Rows:", df.duplicated().sum())

numeric_df = df.select_dtypes(include="number")

if not numeric_df.empty:
    print("\\nCorrelation Matrix:")
    print(numeric_df.corr())

    plt.figure(figsize=(10, 6))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.show()

    numeric_df.hist(figsize=(12, 8))
    plt.suptitle("Numerical Feature Distributions")
    plt.tight_layout()
    plt.show()
'''
    )
}


# --------------------------------------------------
# SEARCH AND FILTER
# --------------------------------------------------

st.sidebar.header("🔍 Program Navigation")

search = st.sidebar.text_input(
    "Search programs",
    placeholder="Enter a program title..."
)

filtered_programs = {
    number: program
    for number, program in PROGRAMS.items()
    if search.lower() in program[0].lower()
}

st.sidebar.write(
    f"Available programs: {len(filtered_programs)} / {len(PROGRAMS)}"
)


# --------------------------------------------------
# DOWNLOAD ALL PROGRAMS AS ZIP
# --------------------------------------------------

zip_buffer = io.BytesIO()

with zipfile.ZipFile(
    zip_buffer,
    mode="w",
    compression=zipfile.ZIP_DEFLATED
) as zip_file:

    for number, (title, code) in PROGRAMS.items():
        safe_title = (
            title.replace("/", "-")
            .replace("\\\\", "-")
            .replace(":", "")
        )

        filename = f"{number:02d}_{safe_title}.py"

        zip_file.writestr(filename, code.strip() + "\\n")

st.download_button(
    label="📦 Download All Programs (ZIP)",
    data=zip_buffer.getvalue(),
    file_name="Open_Source_Data_Analytics_Lab.zip",
    mime="application/zip",
    use_container_width=True
)


# --------------------------------------------------
# DISPLAY ALL PROGRAMS ON THE SAME PAGE
# --------------------------------------------------

st.divider()

if not filtered_programs:
    st.warning("No programs match your search.")
else:
    for number, (title, code) in filtered_programs.items():

        with st.expander(
            f"📘 {number}. {title}",
            expanded=False
        ):

            st.subheader(title)

            st.code(
                code.strip(),
                language="python",
                line_numbers=True
            )

            safe_title = (
                title.replace("/", "-")
                .replace("\\\\", "-")
                .replace(":", "")
            )

            filename = f"{number:02d}_{safe_title}.py"

            st.download_button(
                label=f"⬇️ Download Program {number}",
                data=code.strip() + "\\n",
                file_name=filename,
                mime="text/x-python",
                key=f"download_{number}"
            )

st.divider()

st.success(
    f"Open Source Data Analytics Lab contains "
    f"{len(PROGRAMS)} Python programs."
)

st.caption(
    "Note: Install the required Python libraries and provide the "
    "corresponding datasets before running individual programs. "
    "COVID-19 visualization requires an internet connection to retrieve "
    "the dataset. Dash and Streamlit programs run as separate applications."
)
