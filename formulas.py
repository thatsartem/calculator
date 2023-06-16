from scipy.stats import norm

def get_percentage(score, mean, dis):
    z_value = norm.cdf(score, loc=mean, scale=dis**0.5) * 100
    return int(z_value)