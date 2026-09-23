import os
import pickle
import boto3
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

# Загружаем переменные окружения из .env файла
load_dotenv()


def upload_to_s3():
    # Настройки для Yandex Cloud S3
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    bucket_name = os.getenv('S3_BUCKET_NAME', 'ml-model-storage')
    
    # Загружаем файл модели
    try:
        s3.upload_file('iris_model.pkl', bucket_name, 'models/iris_model.pkl')
        logger.info(f"Модель загружена в S3: s3://{bucket_name}/models/iris_model.pkl")
    except Exception as e:
        logger.error(f"Ошибка при загрузке в S3: {e}")

def main():
    # Загружаем данные ирисок
    logger.info("Загрузка данных ирисок...")
    iris = load_iris()
    
    logger.info("Преобразование данных в DataFrame...")
    # Создаем DataFrame с переименованными колонками
    df = pd.DataFrame(iris.data, columns=[
        'sepal_length', 'sepal_width', 'petal_length', 'petal_width'
    ])
    df['species'] = iris.target
    
    # Разделяем на признаки и целевую переменную
    X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
    y = df['species']
    
    # Разделяем на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    logger.info("Обучение модели...")
    # Обучаем модель
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    logger.info("Модель обучена, теперь оцениваем точность...")
    # Оцениваем точность
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Точность модели: {accuracy:.4f}")
    
    # Сохраняем модель локально
    with open('iris_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Загружаем модель в S3
    upload_to_s3()

    logger.info("Модель успешно обучена и сохранена в iris_model.pkl")
    logger.info("Модель успешно загружена в S3")
    
    print("Модель успешно обучена и загружена в S3!")


if __name__ == "__main__":
    main()