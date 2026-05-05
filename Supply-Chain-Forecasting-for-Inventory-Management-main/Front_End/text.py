import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data
data = {
    'Learning Rate': [0.05, 0.05, 0.01, 0.01],
    'Estimators': [1000, 1000, 500, 500],
    'Model': ['XGBoost', 'CatBoost', 'XGBoost', 'CatBoost'],
    'MAE': [8.8190, 10.2918, 8.8192, 10.0883],
    'MSE': [138.3043, 176.7446, 131.4190, 176.5254],
    'RMSE': [11.4638, 13.8832, 11.4638, 13.2862],
    'R2': [0.9889, 0.9723, 0.9889, 0.9850]
}

df = pd.DataFrame(data)

# Combine LR and Estimators for legend
df['Config'] = df.apply(lambda row: f"LR={row['Learning Rate']} | Est={row['Estimators']}", axis=1)

# Improved royal-style colors
royal_palette = {
    'LR=0.05 | Est=1000': '#6A0DAD',  # Royal Purple
    'LR=0.01 | Est=500': '#002366'    # Royal Blue
}

# Metrics to plot
metrics = ['MAE', 'MSE', 'RMSE', 'R2']
fig, axes = plt.subplots(2, 2, figsize=(10, 9))
axes = axes.flatten()

# Plotting
for i, metric in enumerate(metrics):
    sns.barplot(
        data=df, x='Model', y=metric,
        hue='Config', palette=royal_palette, ax=axes[i]
    )
    axes[i].set_title(f'{metric} Comparison', fontsize=12, fontweight='bold')
    axes[i].set_xlabel('Model', fontsize=10)
    axes[i].set_ylabel(metric, fontsize=10)
    axes[i].tick_params(axis='both', labelsize=9)
    axes[i].legend(title='Configuration', fontsize=9, title_fontsize=12, loc='lower right')

# Main title
plt.suptitle('Performance analysis of XGBoost and CatBoost with hyper parameter tuning', fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
