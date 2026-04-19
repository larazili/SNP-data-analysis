import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

from sklearn.svm import SVC
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

import warnings
# 경고 메시지 무시
warnings.filterwarnings("ignore")

def load_data(chunk_ranges):
    df_combined = pd.DataFrame()

    for chunk_idx in chunk_ranges:
        df_chunk = pd.read_csv(f'./data/snp_20/chunk_{chunk_idx}.csv')
        df_chunk = df_chunk.set_index('Unnamed: 0')
        df_chunk = df_chunk.rename_axis(None)
        df_combined = pd.concat([df_combined, df_chunk])

    return df_combined

# 청크 파일들을 합친 후에 실행하는 함수
def SVM_model(chunk_ranges):
    df_combined = load_data(chunk_ranges)

    # 데이터 프레임에서 타겟 변수와 특성 데이터 추출
    X = df_combined.drop(columns=['Population code', 'Population', 'Region'])
    y = df_combined['Population code']

    # 데이터 스케일링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 학습 데이터와 검증 데이터로 나누기
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # SVM 모델 생성
    svm_model = SVC()

    # 파라미터 그리드 설정
    param_grid = {
        'C': [0.1, 1, 10],  # 규제 파라미터
        'kernel': ['linear', 'rbf'],  # 커널 종류
        'gamma': ['scale', 'auto']  # rbf 커널에서의 gamma 값
    }

    # GridSearchCV를 사용하여 최적의 파라미터 탐색
    grid_search = GridSearchCV(svm_model, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # 최적의 파라미터 출력
    best_params = grid_search.best_params_

    # 최적의 파라미터로 모델 생성 및 학습
    best_svm_model = SVC(**best_params)
    best_svm_model.fit(X_train, y_train)

    # 검증 데이터로 예측
    svm_predictions = best_svm_model.predict(X_val)

    # 예측 결과 클래스로 변환
    svm_predictions_class = np.round(svm_predictions).astype(int)
    
    # 정확도 계산
    svm_accuracy = accuracy_score(y_val, svm_predictions_class)

    return best_params, svm_accuracy, best_svm_model, X

# 변수 중요도 추출 함수 (절댓값만 사용)
def extract_variable_importance(model, feature_names, kernel_type):
    if kernel_type == 'linear':
        return np.abs(model.coef_)[0]
    elif kernel_type == 'rbf':
        dual_coef = model.dual_coef_
        return np.abs(dual_coef)[0]
    else:
        raise ValueError("지원하지 않는 커널 유형입니다.")

def Ridge_model(chunk_ranges):
    df_combined = load_data(chunk_ranges)
    
    X = df_combined.drop(columns=['Population code', 'Population', 'Region'])
    y = df_combined['Population code']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Ridge 모델의 alpha 후보값 설정
    param_grid_ridge = {'alpha': np.logspace(-6, 10, 13)}

    # Ridge 모델 그리드 서치
    ridge_grid = GridSearchCV(Ridge(), param_grid_ridge, cv=5, scoring='accuracy')
    ridge_grid.fit(X_train, y_train)

    # 최적 파라미터 확인
    best_params = ridge_grid.best_params_

    # 최적 파라미터를 사용하여 Ridge 모델 학습
    best_ridge_model = Ridge(**best_params)
    best_ridge_model.fit(X_train, y_train)

    # 검증 데이터로 예측
    ridge_predictions = best_ridge_model.predict(X_val)

    ridge_predictions_class = np.round(ridge_predictions).astype(int)

    # 정확도 계산
    ridge_accuracy = accuracy_score(y_val, ridge_predictions_class)
    
    return best_params, ridge_accuracy, best_ridge_model, X

# 청크 파일들을 합친 후에 실행하는 함수 (결정 트리 버전)
def DT_model(chunk_ranges):
    df_combined = load_data(chunk_ranges)

    # 데이터 프레임에서 타겟 변수와 특성 데이터 추출
    X = df_combined.drop(columns=['Population code', 'Population', 'Region'])
    y = df_combined['Population code']

    # 데이터 스케일링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 학습 데이터와 검증 데이터로 나누기
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # DecisionTreeClassifier 모델 생성
    dt_model = DecisionTreeClassifier()

    # 파라미터 그리드 설정
    param_grid = {
        'max_depth': [10, 20, 30],  # 트리의 최대 깊이
        'min_samples_split': [2, 5, 10]  # 노드를 분할하기 위한 최소 샘플 수
    }

    # GridSearchCV를 사용하여 최적의 파라미터 탐색
    grid_search = GridSearchCV(dt_model, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # 최적의 파라미터 출력
    best_params = grid_search.best_params_

    # 최적의 파라미터로 모델 생성 및 학습
    best_dt_model = DecisionTreeClassifier(**best_params)
    best_dt_model.fit(X_train, y_train)

    # 검증 데이터로 예측
    dt_predictions = best_dt_model.predict(X_val)

    # 정확도 계산
    dt_accuracy = accuracy_score(y_val, dt_predictions)

    return best_params, dt_accuracy, best_dt_model, X

# 청크 파일들을 합친 후에 실행하는 함수
def RF_model(chunk_ranges):
    df_combined = load_data(chunk_ranges)

    # 데이터 프레임에서 타겟 변수와 특성 데이터 추출
    X = df_combined.drop(columns=['Population code', 'Population', 'Region'])
    y = df_combined['Population code']

    # 데이터 스케일링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 학습 데이터와 검증 데이터로 나누기
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # RandomForestClassifier 모델 생성
    rf_model = RandomForestClassifier()

    # 파라미터 그리드 설정
    param_grid = {
        'n_estimators': [100, 200, 300],  # 트리 개수
        'max_depth': [10, 20, 30],  # 트리의 최대 깊이
        'min_samples_split': [2, 5, 10]  # 노드를 분할하기 위한 최소 샘플 수
    }

    # GridSearchCV를 사용하여 최적의 파라미터 탐색
    grid_search = GridSearchCV(rf_model, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # 최적의 파라미터 출력
    best_params = grid_search.best_params_

    # 최적의 파라미터로 모델 생성 및 학습
    best_rf_model = RandomForestClassifier(**best_params)
    best_rf_model.fit(X_train, y_train)

    # 검증 데이터로 예측
    rf_predictions = best_rf_model.predict(X_val)

    # 정확도 계산
    rf_accuracy = accuracy_score(y_val, rf_predictions)

    return best_params, rf_accuracy, best_rf_model, X


# 청크 파일들을 합친 후에 실행하는 함수
def XGB_model(chunk_ranges):
    df_combined = load_data(chunk_ranges)

    # 데이터 프레임에서 타겟 변수와 특성 데이터 추출
    X = df_combined.drop(columns=['Population code', 'Population', 'Region'])
    y = df_combined['Population code']
    
    # 데이터 스케일링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 타겟 레이블 인코딩
    le = LabelEncoder()
    y = le.fit_transform(y)

    # 학습 데이터와 검증 데이터로 나누기
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # XGBoost 모델 생성
    xgb_model = XGBClassifier()

    # 파라미터 그리드 설정
    param_grid = {
        'learning_rate': [0.01, 0.1],  # 학습률
        'n_estimators': [50, 100],  # 트리 개수
        'max_depth': [3, 5],  # 최대 깊이
        'subsample': [0.5, 1],  # 데이터 샘플링 비율
        'colsample_bytree': [0.5, 1],  # 열 샘플링 비율
    }

    # GridSearchCV를 사용하여 최적의 파라미터 탐색
    grid_search = GridSearchCV(xgb_model, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # 최적의 파라미터 출력
    best_params = grid_search.best_params_

    # 최적의 파라미터로 모델 생성 및 학습
    best_xgb_model = XGBClassifier(**best_params)
    best_xgb_model.fit(X_train, y_train)

    # 검증 데이터로 예측
    xgb_predictions = best_xgb_model.predict(X_val)

    # 정확도 계산
    xgb_accuracy = accuracy_score(y_val, xgb_predictions)

    return best_params, xgb_accuracy, best_xgb_model, X

