import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def load_data(chunk_ranges):
    df_combined = pd.DataFrame()

    for chunk_idx in chunk_ranges:
        df_chunk = pd.read_csv(f'./data/snp_20/chunk_{chunk_idx}.csv')
        df_chunk = df_chunk.set_index('Unnamed: 0')
        df_chunk = df_chunk.rename_axis(None)
        df_combined = pd.concat([df_combined, df_chunk])

    return df_combined

# 변수 중요도 추출 함수 (절댓값만 사용)
def extract_variable_importance(model, feature_names, kernel_type):
    if kernel_type == 'linear':
        return np.abs(model.coef_)[0]
    elif kernel_type == 'rbf':
        dual_coef = model.dual_coef_
        return np.abs(dual_coef)[0]
    else:
        raise ValueError("지원하지 않는 커널 유형입니다.")

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

    # 변수 중요도 추출
    kernel_type = best_svm_model.kernel
    importances = extract_variable_importance(best_svm_model, X.columns, kernel_type)

    # 변수 중요도를 기준으로 피처 정렬
    important_features_idx = np.argsort(importances)[-100:]

    # 상위 100개의 변수 이름 출력
    top_100_features_names = X.columns[important_features_idx]

    # 'chr'로 시작하지 않는 열 이름만 필터링하여 추출
    filtered_features_names = [name for name in top_100_features_names if not name.startswith('chr')]

    # 'Population code', 'Population', 'Region' 열을 다시 추가하여 출력
    selected_columns = filtered_features_names + ['Population code', 'Population', 'Region']

    # 새로운 데이터프레임 생성
    selected_df = df_combined[selected_columns]

    return best_params, svm_accuracy, best_svm_model, selected_df

