import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import mlflow
import mlflow.sklearn

def main():
    df = pd.read_csv("data/housing.csv")
    X = df[["area"]]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        lr = 0.01
        epochs = 100  
        mlflow.log_param("learning_rate", lr)
        mlflow.log_param("epochs", epochs)

        model = LinearRegression()
        model.fit(X_train, y_train)

        score = model.score(X_test, y_test)
        mlflow.log_metric("r2_score", score)

        print("Model R^2 Score:", score)

        joblib.dump(model, "model.pkl")

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="linear_regression_model",
            input_example=X_test[:1]
        )

if __name__ == "__main__":
    main()