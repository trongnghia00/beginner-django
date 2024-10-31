from django.shortcuts import render
from .models import Question, Choice
from .forms import QuizForm
import numpy as np
import pandas as pd

from opytimizer.optimizers.science import MVO
from opytimizer.spaces import SearchSpace
from opytimizer.utils import logging

# Khởi tạo trọng số ban đầu cho các tiêu chí
initial_weights = {
    'expected_return': 5, # Lợi nhuận kỳ vọng
    'risk': 5, # Rủi ro
    'liquidity': 5, # Thanh khoản
    'diversification': 5, # Đa dạng hóa
    'investment_horizon': 5, # Thời gian đầu tư
    'cost': 5, # Chi phí
    'cash_flow_stability': 5 # Tính ổn định dòng tiền
}

portfolios = [
    {"name": "Đầu tư vàng", "expected_return": 3, "risk": 2, "liquidity": 8, "diversification": 3, "investment_horizon": 6, "cost": 2, "cash_flow_stability": 7},
    {"name": "Bất động sản", "expected_return": 5, "risk": 4, "liquidity": 3, "diversification": 6, "investment_horizon": 8, "cost": 5, "cash_flow_stability": 6},
    {"name": "Gửi ngân hàng", "expected_return": 2, "risk": 1, "liquidity": 9, "diversification": 2, "investment_horizon": 4, "cost": 1, "cash_flow_stability": 9},
    {"name": "Cổ phiếu Top thị trường", "expected_return": 7, "risk": 5, "liquidity": 8, "diversification": 7, "investment_horizon": 5, "cost": 3, "cash_flow_stability": 4},
    {"name": "Cổ phiếu không thuộc top", "expected_return": 8, "risk": 7, "liquidity": 7, "diversification": 4, "investment_horizon": 5, "cost": 4, "cash_flow_stability": 3},
    {"name": "Trái phiếu doanh nghiệp", "expected_return": 4, "risk": 3, "liquidity": 5, "diversification": 6, "investment_horizon": 7, "cost": 3, "cash_flow_stability": 8},
    {"name": "Trái phiếu chính phủ", "expected_return": 3, "risk": 2, "liquidity": 9, "diversification": 7, "investment_horizon": 8, "cost": 2, "cash_flow_stability": 9},
    {"name": "Quỹ cổ phiếu", "expected_return": 6, "risk": 4, "liquidity": 6, "diversification": 7, "investment_horizon": 6, "cost": 4, "cash_flow_stability": 5},
    {"name": "Quỹ trái phiếu", "expected_return": 4, "risk": 2, "liquidity": 7, "diversification": 8, "investment_horizon": 7, "cost": 3, "cash_flow_stability": 8},
    {"name": "Quỹ hỗn hợp cân bằng", "expected_return": 5, "risk": 3, "liquidity": 6, "diversification": 7, "investment_horizon": 6, "cost": 3, "cash_flow_stability": 6},
    {"name": "Crypto (BTC)", "expected_return": 9, "risk": 9, "liquidity": 8, "diversification": 5, "investment_horizon": 5, "cost": 4, "cash_flow_stability": 3},
    {"name": "ALT Coin", "expected_return": 8, "risk": 8, "liquidity": 7, "diversification": 5, "investment_horizon": 4, "cost": 5, "cash_flow_stability": 2},
    {"name": "Meme Coin", "expected_return": 9, "risk": 9, "liquidity": 7, "diversification": 2, "investment_horizon": 3, "cost": 7, "cash_flow_stability": 1},
    {"name": "Shit Coin", "expected_return": 9, "risk": 9, "liquidity": 6, "diversification": 1, "investment_horizon": 2, "cost": 8, "cash_flow_stability": 1},
    {"name": "Quỹ đầu tư bất động sản (REITs)", "expected_return": 6, "risk": 3, "liquidity": 6, "diversification": 7, "investment_horizon": 7, "cost": 4, "cash_flow_stability": 7},
    {"name": "Chứng chỉ tiền gửi (CDs)", "expected_return": 2, "risk": 1, "liquidity": 9, "diversification": 2, "investment_horizon": 4, "cost": 1, "cash_flow_stability": 9},
    {"name": "Hợp đồng tương lai", "expected_return": 8, "risk": 8, "liquidity": 6, "diversification": 4, "investment_horizon": 3, "cost": 6, "cash_flow_stability": 2},
    {"name": "Hợp đồng quyền chọn", "expected_return": 7, "risk": 9, "liquidity": 6, "diversification": 4, "investment_horizon": 3, "cost": 6, "cash_flow_stability": 2},
    {"name": "Vốn đầu tư mạo hiểm", "expected_return": 9, "risk": 9, "liquidity": 3, "diversification": 5, "investment_horizon": 7, "cost": 6, "cash_flow_stability": 1},
    {"name": "Đầu tư công nghệ tài chính (Fintech)", "expected_return": 8, "risk": 8, "liquidity": 6, "diversification": 5, "investment_horizon": 6, "cost": 5, "cash_flow_stability": 3}
]

# Dữ liệu danh mục đầu tư
investment_data = {
    'investment': [portfolio['name'] for portfolio in portfolios],
    'expected_return': [portfolio['expected_return'] for portfolio in portfolios],
    'risk': [portfolio['risk'] for portfolio in portfolios],
    'liquidity': [portfolio['liquidity'] for portfolio in portfolios],
    'diversification': [portfolio['diversification'] for portfolio in portfolios],
    'investment_horizon': [portfolio['investment_horizon'] for portfolio in portfolios],
    'cost': [portfolio['cost'] for portfolio in portfolios],
    'cash_flow_stability': [portfolio['cash_flow_stability'] for portfolio in portfolios]
}

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(investment_data)

# Hàm tính toán giá trị mục tiêu
def objective_function(allocation, df, weights):
    total_score = 0
    for i in range(len(df)):
        score = (weights['expected_return'] * df['expected_return'][i] -
                 weights['risk'] * df['risk'][i] +
                 weights['liquidity'] * df['liquidity'][i] +
                 weights['diversification'] * df['diversification'][i] +
                 weights['investment_horizon'] * df['investment_horizon'][i] -
                 weights['cost'] * df['cost'][i] +
                 weights['cash_flow_stability'] * df['cash_flow_stability'][i])
        total_score += score * allocation[i]
    return total_score

def genetic_algorithm(df, weights, population_size=20, generations=1000, mutation_rate=0.1):
    # Khởi tạo quần thể
    population = np.random.dirichlet(np.ones(len(df)), population_size)

    for _ in range(generations):
        # Đánh giá quần thể
        scores = np.array([objective_function(individual, df, weights) for individual in population])
        # Chọn cha mẹ
        parents_indices = scores.argsort()[-population_size // 2:]
        parents = population[parents_indices]

        # Giao phối
        offspring = []
        for _ in range(population_size // 2):
            p1, p2 = parents[np.random.choice(len(parents), 2, replace=False)]
            child = (p1 + p2) / 2  # Giao phối đơn giản
            offspring.append(child)

        # Đột biến
        for i in range(len(offspring)):
            if np.random.rand() < mutation_rate:
                mutation_value = np.random.uniform(-0.05, 0.05, size=len(df))
                offspring[i] = np.clip(offspring[i] + mutation_value, 0, None)
                offspring[i] /= offspring[i].sum()  # Đảm bảo tổng bằng 1

        # Tạo thế hệ mới
        population = np.vstack((parents, offspring))

    # Đánh giá thế hệ cuối cùng
    final_scores = np.array([objective_function(individual, df, weights) for individual in population])
    best_index = final_scores.argmax()
    best_allocation = population[best_index]

    return best_allocation

def calculate_ahp_matrix(weights):
    criteria = list(weights.keys())
    matrix = np.zeros((len(criteria), len(criteria)))

    for i, crit1 in enumerate(criteria):
        for j, crit2 in enumerate(criteria):
            if i == j:
                matrix[i][j] = 1
            else:
                matrix[i][j] = weights[crit1] / weights[crit2]

    return matrix

def quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            adjusted_weights = initial_weights.copy()

            # Lấy câu trả lời của người dùng và điều chỉnh trọng số
            for question_id, choice_id in form.cleaned_data.items():
                choice = Choice.objects.get(id=choice_id)
                for key, value in choice.weight_adjustments.items():
                    adjusted_weights[key] += value

            # Tính toán ma trận AHP
            ahp_matrix = calculate_ahp_matrix(adjusted_weights)

            # Chuyển ma trận AHP thành dạng bảng dễ hiển thị
            ahp_matrix_table = np.round(ahp_matrix, 2).tolist()
            weight_keys = list(adjusted_weights.keys())
            table_data = list(zip(weight_keys, ahp_matrix_table))

            # Thực hiện GA
            best_allocation = genetic_algorithm(df, initial_weights)

            # Kết quả
            results = pd.DataFrame({
                'investment': df['investment'],
                'allocation': best_allocation  # Trọng số chưa được chuyển đổi thành phần trăm
            })

            # Lọc 5 danh mục hàng đầu và chuẩn hóa lại
            top_investments = results.nlargest(5, 'allocation')
            sum_inv = top_investments['allocation'].sum()
            top_investments['allocation'] = (top_investments['allocation'] / sum_inv) * 100
            top_investments['allocation (%)'] = top_investments['allocation'].astype(int)
            top_investment_names = list(top_investments['investment'])
            top_investment_weights = list(top_investments['allocation (%)'])
            top_investment_weights[-1] = 100 - sum(top_investment_weights[:-1])
            investments = list(zip(top_investment_names, top_investment_weights))

            return render(request, 'quiz/result.html', {
                'ahp_matrix': ahp_matrix_table,
                'weights': adjusted_weights,
                'keys': weight_keys,
                'table_data': table_data,
                'investments': investments,
            })
    else:
        form = QuizForm()

    return render(request, 'quiz/quiz.html', {'form': form})

def homepage(request):
    return render(request, "quiz/index.html")