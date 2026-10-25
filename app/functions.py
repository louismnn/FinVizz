from math import exp, sqrt, log, pi
from scipy.stats import norm
import blackscholes as bs
from sympy import erf



class OptionWrapper:
    def __init__(self, option, sign = 1 or -1):
        self.option = option
        self.sign = sign
    def vega(self):
        return self.sign * self.option.vega()
    def theta(self):
        return self.sign * self.option.theta()
    def rho(self):
        return self.sign * self.option.rho()
    def delta(self):
        return self.sign * self.option.delta()
    def gamma(self):
        return self.sign * self.option.gamma()

class BlackScholesCallShort(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(bs.BlackScholesCall(S=S, K=K, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesPutShort(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(bs.BlackScholesPut(S=S, K=K, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesBearSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBearSpread(S=S, K1=K2, K2=K1, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesBearSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBearSpread(S=S, K1=K2, K2=K1, T=T, sigma=sigma, q=q, r=r),sign=1)

class BlackScholesBullSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBullSpread(S=S, K1=K1, K2=K2, T=T, sigma=sigma, q=q, r=r),sign=1)

class BlackScholesBullSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBullSpread(S=S, K1=K1, K2=K2, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackscholesCalendarCallSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarCallSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=1)

class BlackscholesCalendarCallSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarCallSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesCalendarPutSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarPutSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=1)

class BlackScholesCalendarPutSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarPutSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=-1)

class BinaryCallLong:
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, q: float):
        self.S, self.K, self.T, self.r, self.sigma, self.q = S, K, T, r, sigma, q
        self.d1 = (1 / (self.sigma * sqrt(self.T))) * (log(self.S / self.K) + (self.r - self.q + self.sigma**2 / 2) * self.T)
        self.price = self.S * exp(-self.q * self.T) * norm.cdf(self.d1)

    def delta(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return exp(-T*q)*erf(-sqrt(2)*sqrt(T)*q/(2*sigma) + sqrt(2)*sqrt(T)*r/(2*sigma) + sqrt(2)*sqrt(T)*sigma/4 + sqrt(2)*log(S**2/K**2)/(4*sqrt(T)*sigma))/2 + exp(-T*q)/2 + sqrt(2)*exp(-T*q - (-2*T*q + 2*T*r + T*sigma**2 + log(S**2/K**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sqrt(T)*sigma)

    def gamma(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return sqrt(2)*(2*T*sigma**2 - T*(-2*q + 2*r + sigma**2) - log(S**2/K**2))*exp(-T*q - (T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))**2/(8*T*sigma**2))/(4*sqrt(pi)*S*T**(3/2)*sigma**3)

    def vega(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return sqrt(2)*S*(2*T*sigma**2 - T*(-2*q + 2*r + sigma**2) - log(S**2/K**2))*exp(-T*q - (T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))**2/(8*T*sigma**2))/(4*sqrt(pi)*sqrt(T)*sigma**2)

    def rho(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return sqrt(2)*S*sqrt(T)*exp(-T*q - (T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sigma)

    def theta(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        d1_time = (
            r - q + sigma**2 / 2 - log(S / K) / T
        ) / (2 * sigma * sqrt(T))
        return S * exp(-q * T) * (
            q * norm.cdf(self.d1) - norm.pdf(self.d1) * d1_time
        )

class BinaryPutLong:
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, q: float):
        self.S, self.K, self.T, self.r, self.sigma, self.q = S, K, T, r, sigma, q
        self.d1 = (log(self.S / self.K) + (self.r - self.q + self.sigma**2 / 2) * self.T) / (self.sigma * sqrt(self.T))
        self.price = self.S * exp(-self.q * self.T) * norm.cdf(-self.d1)

    def delta(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return -exp(-T*q)*erf(-sqrt(2)*sqrt(T)*q/(2*sigma) + sqrt(2)*sqrt(T)*r/(2*sigma) + sqrt(2)*sqrt(T)*sigma/4 + sqrt(2)*log(S**2/K**2)/(4*sqrt(T)*sigma))/2 + exp(-T*q)/2 - sqrt(2)*exp(-T*q - (-2*T*q + 2*T*r + T*sigma**2 + log(S**2/K**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sqrt(T)*sigma)

    def gamma(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return sqrt(2)*(-2*T*sigma**2 + T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))*exp(-T*q - (T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))**2/(8*T*sigma**2))/(4*sqrt(pi)*S*T**(3/2)*sigma**3)

    def vega(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return sqrt(2)*S*(-2*T*sigma**2 + T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))*exp(-T*q - (T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))**2/(8*T*sigma**2))/(4*sqrt(pi)*sqrt(T)*sigma**2)

    def rho(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        return -sqrt(2)*S*sqrt(T)*exp(-T*q - (T*(-2*q + 2*r + sigma**2) + log(S**2/K**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sigma)

    def theta(self):
        S, T, K, r, q, sigma = self.S, self.T, self.K, self.r, self.q, self.sigma
        d1_time = (
            r - q + sigma**2 / 2 - log(S / K) / T
        ) / (2 * sigma * sqrt(T))
        return S * exp(-q * T) * (
            q * norm.cdf(-self.d1) + norm.pdf(self.d1) * d1_time
        )

class BinaryCallShort(BinaryCallLong):
    def __init__(self, S, K, T, r, sigma, q):
        super().__init__(S, K, T, r, sigma, q)
    def delta(self):
        return super().delta() * -1
    def gamma(self):
        return super().gamma() * -1
    def vega(self):
        return super().vega() * -1
    def theta(self):
        return super().theta() * -1
    def rho(self):
        return super().rho() * -1

class BinaryPutShort(BinaryPutLong):
    def __init__(self, S, K, T, r, sigma, q):
        super().__init__(S, K, T, r, sigma, q)
    def delta(self):
        return super().delta() * -1
    def gamma(self):
        return super().gamma() * -1
    def vega(self):
        return super().vega() * -1
    def theta(self):
        return super().theta() * -1
    def rho(self):
        return super().rho() * -1

class PerpetualCallOptionLong:
    def __init__(self, S: float, K: float, r: float, q: float, sigma: float):

        self.sigma = sigma
        self.S = S
        self.K = K
        self.r = r
        self.q = q

        if r <=0:
            self.price = None
        else:
            self.alpha_1 = sqrt((r / sigma**2 + 1/2)**2 + (2*r + 2*q)/sigma**2) - r/sigma**2 + 1/2

            if self.S < (self.K * self.alpha_1 / (self.alpha_1 - 1)):
                self.price = (K / (self.alpha_1 - 1)) * (((self.alpha_1 - 1) * self.S) / (self.alpha_1 * self.K))**self.alpha_1
            else:
                self.price = self.S - K

    def theta(self):
        return 0

    def delta(self):
        if self.r <= 0:
            return 0
        if self.S <= self.K * self.alpha_1 / (self.alpha_1 - 1):
            return ((self.alpha_1 - 1) * self.S)**(self.alpha_1-1) / (self.alpha_1*self.K)**(self.alpha_1-1)
        else:
            return 1

    def gamma(self):
        S, K, r, q, sigma = self.S, self.K, self.r, self.q, self.sigma
        if r <= 0:
            return 0
        if self.S <= (self.K * self.alpha_1 / (self.alpha_1 - 1)):
            return ((self.alpha_1 - 1) * S)**(self.alpha_1 - 2) / (self.alpha_1 * K)**(self.alpha_1 - 2) * (self.alpha_1 - 1)**2 / (self.alpha_1 * K)
        else:
            return 0

    def vega(self):
        S, K, r, q, sigma = self.S, self.K, self.r, self.q, self.sigma
        if r <= 0:
            return 0
        if (self.S < self.K * self.alpha_1 / (self.alpha_1 - 1)):
            return 2*K*(-S*(r + 0.5*sigma**2 - sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))/(K*(-r + 0.5*sigma**2 + sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))))**((-r + 0.5*sigma**2 + sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))/sigma**2)*(r*(r + 0.5*sigma**2) - r*sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2) + sigma**2*(q + r))*log(-S*(r + 0.5*sigma**2 - sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))/(K*(-r + 0.5*sigma**2 + sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))))/(sigma*sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2)*(r + 0.5*sigma**2 - sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2)))
        else:
            return 0

    def rho(self):
        S, K, r, q, sigma = self.S, self.K, self.r, self.q, self.sigma
        if r <= 0:
            return 0
        if (self.S < self.K * self.alpha_1 / (self.alpha_1 - 1)):
            return -K*(-S*(r + 0.5*sigma**2 - sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))/(K*(-r + 0.5*sigma**2 + sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))))**((-r + 0.5*sigma**2 + sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))/sigma**2)*(r + 1.5*sigma**2 - sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))*log(-S*(r + 0.5*sigma**2 - sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))/(K*(-r + 0.5*sigma**2 + sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2))))/(sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2)*(r + 0.5*sigma**2 - sqrt(2*sigma**2*(q + r) + (r + 0.5*sigma**2)**2)))
        else:
            return 0

class PerpetualCallOptionShort(PerpetualCallOptionLong):
    def __init__(self, S: float, K: float, r: float, q: float, sigma: float):
        super().__init__(S, K, r, q, sigma)
    def delta(self):
        return super().delta() * -1
    def gamma(self):
        return super().gamma() * -1
    def vega(self):
        return super().vega() * -1
    def rho(self):
        return super().rho() * -1

class PerpetualPutOptionLong:
    def __init__(self, S: float, K: float, r: float, q: float, sigma: float):

        self.sigma = sigma
        self.S = S
        self.K = K
        self.r = r
        self.q = q

        if r <= 0:
            self.price = None
        else:
            self.alpha_2 = sqrt((r / sigma**2 + 1/2)**2 + (2*r + 2*q)/sigma**2) + r/sigma**2 - 1/2

            if self.S > (self.K * self.alpha_2 / (self.alpha_2 + 1)):
                self.price = (K / (self.alpha_2 + 1)) * ((self.alpha_2 + 1) * self.S / (self.alpha_2 * self.K)) ** (-self.alpha_2)
            else:
                self.price = K - self.S

    def theta(self):
        return 0

    def delta(self):
        if self.r <= 0:
            return 0
        if self.S > (self.K * self.alpha_2 / (self.alpha_2 + 1)):
            return -((self.alpha_2*self.K)/((self.alpha_2+1)*self.S))**(self.alpha_2+1)
        else:
            return -1

    def gamma(self):
        S, K, r, q, sigma = self.S, self.K, self.r, self.q, self.sigma
        if r <= 0:
            return 0
        if (self.S > self.K * self.alpha_2 / (self.alpha_2 + 1)):
            ratio = (self.alpha_2 * K) / ((self.alpha_2 + 1) * S)
            return (self.alpha_2 + 1) * ratio ** (self.alpha_2 + 1) / S
        else:
            return 0

    def vega(self):
        S, K, r, q, sigma = self.S, self.K, self.r, self.q, self.sigma
        if r <= 0:
            return 0
        if (self.S > self.K * self.alpha_2 / (self.alpha_2 + 1)):
            ratio = (self.alpha_2 * K) / ((self.alpha_2 + 1) * S)
            denominator = sqrt((r + sigma**2 / 2)**2 + 2 * sigma**2 * (q + r))
            return (
                self.price
                * log(ratio)
                * (-sigma * self.alpha_2 * (self.alpha_2 + 1) / denominator)
            )
        else:
            return 0

    def rho(self):
        S, K, r, q, sigma = self.S, self.K, self.r, self.q, self.sigma
        if r <= 0:
            return 0
        if (self.S > self.K * self.alpha_2 / (self.alpha_2 + 1)):
            ratio = (self.alpha_2 * K) / ((self.alpha_2 + 1) * S)
            denominator = sqrt((r + sigma**2 / 2)**2 + 2 * sigma**2 * (q + r))
            return (
                self.price
                * log(ratio)
                * ((self.alpha_2 + 2) / denominator)
            )
        else:
            return 0

class PerpetualPutOptionShort(PerpetualPutOptionLong):
    def __init__(self, S: float, K: float, r: float, q: float, sigma: float):
        super().__init__(S, K, r, q, sigma)
    def delta(self):
        return super().delta() * -1
    def gamma(self):
        return super().gamma() * -1
    def vega(self):
        return super().vega() * -1
    def rho(self):
        return super().rho() * -1

def _gap_gamma(S, K1, K2, T, r, q, sigma):
    volatility_time = sigma * sqrt(T)
    d1 = (log(S / K2) + (r - q + sigma**2 / 2) * T) / volatility_time
    d2 = d1 - volatility_time

    return (
        exp(-q * T) * norm.pdf(d1) / (S * volatility_time)
        * (1 - d1 / volatility_time)
        + K1 * exp(-r * T) * norm.pdf(d2) / (S**2 * volatility_time)
        * (1 + d2 / volatility_time)
    )


def _gap_vega(S, K1, K2, T, r, q, sigma):
    volatility_time = sigma * sqrt(T)
    d1 = (log(S / K2) + (r - q + sigma**2 / 2) * T) / volatility_time
    d2 = d1 - volatility_time

    return (
        S * exp(-q * T) * norm.pdf(d1) * (sqrt(T) - d1 / sigma)
        + K1 * exp(-r * T) * norm.pdf(d2) * d1 / sigma
    )


class GapOptionCallLong:
    def __init__(self, S, K1, K2, T, r, q, sigma):
        self.q = q
        self.r = r
        self.S = S
        self.K1 = K1
        self.K2 = K2
        self.T = T
        self.sigma = sigma

        self.d_1 = (log(S / K2) + ((r - q + sigma**2 / 2) * T)) / (sigma * sqrt(T))
        self.d_2 = self.d_1 - sigma * sqrt(T)

        self.price = (S * exp(-q*T) * norm.cdf(self.d_1) ) - (K1 * exp(-r*T) * norm.cdf(self.d_2))

    def delta(self):
        K2, K1, S, sigma, T, q, r= self.K2, self.K1, self.S, self.sigma, self.T, self.q, self.r
        return -sqrt(2)*K1*exp(-T*r - (2*T*q - 2*T*r + T*sigma**2 - log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*S*sqrt(T)*sigma) + exp(-T*q)*erf(-sqrt(2)*sqrt(T)*q/(2*sigma) + sqrt(2)*sqrt(T)*r/(2*sigma) + sqrt(2)*sqrt(T)*sigma/4 + sqrt(2)*log(S**2/K2**2)/(4*sqrt(T)*sigma))/2 + exp(-T*q)/2 + sqrt(2)*exp(-T*q - (-2*T*q + 2*T*r + T*sigma**2 + log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sqrt(T)*sigma)

    def gamma(self):
        return _gap_gamma(self.S, self.K1, self.K2, self.T, self.r, self.q, self.sigma)

    def vega(self):
        return _gap_vega(
            self.S, self.K1, self.K2, self.T, self.r, self.q, self.sigma
        )

    def rho(self):
        K2, K1, S, sigma, T, q, r= self.K2, self.K1, self.S, self.sigma, self.T, self.q, self.r
        return -sqrt(2)*K1*sqrt(T)*exp(-T*r - (2*T*q - 2*T*r + T*sigma**2 - log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sigma) - K1*T*exp(-T*r)*erf(sqrt(2)*sqrt(T)*q/(2*sigma) - sqrt(2)*sqrt(T)*r/(2*sigma) + sqrt(2)*sqrt(T)*sigma/4 - sqrt(2)*log(S**2/K2**2)/(4*sqrt(T)*sigma))/2 + K1*T*exp(-T*r)/2 + sqrt(2)*S*sqrt(T)*exp(-T*q - (-2*T*q + 2*T*r + T*sigma**2 + log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sigma)

    def theta(self):
        K2, K1, S, sigma, T, q, r= self.K2, self.K1, self.S, self.sigma, self.T, self.q, self.r
        return -1 * (-K1*r*(erf(sqrt(2)*(sqrt(T)*sigma - (T*(-q + r + sigma**2/2) + log(S/K2))/(sqrt(T)*sigma))/2)/2 - 1/2)*exp(-T*r) + sqrt(2)*K1*(sigma/(2*sqrt(T)) - (-q + r + sigma**2/2)/(sqrt(T)*sigma) + (T*(-q + r + sigma**2/2) + log(S/K2))/(2*T**(3/2)*sigma))*exp(-T*r)*exp(-(sqrt(T)*sigma - (T*(-q + r + sigma**2/2) + log(S/K2))/(sqrt(T)*sigma))**2/2)/(2*sqrt(pi)) - S*q*(erf(sqrt(2)*(T*(-q + r + sigma**2/2) + log(S/K2))/(2*sqrt(T)*sigma))/2 + 1/2)*exp(-T*q) + S*(sqrt(2)*(-q + r + sigma**2/2)/(2*sqrt(T)*sigma) - sqrt(2)*(T*(-q + r + sigma**2/2) + log(S/K2))/(4*T**(3/2)*sigma))*exp(-T*q)*exp(-(T*(-q + r + sigma**2/2) + log(S/K2))**2/(2*T*sigma**2))/sqrt(pi))

class GapOptionCallShort(GapOptionCallLong):

    def __init__(self, S, K1, K2, T, r, q, sigma):
        super().__init__(S, K1, K2, T, r, q, sigma)
    def delta(self):
        return super().delta() * -1
    def gamma(self):
        return super().gamma() * -1
    def vega(self):
        return super().vega() * -1
    def theta(self):
        return super().theta() * -1
    def rho(self):
        return super().rho() * -1

class GapOptionPutLong():

    def __init__(self, S, K1, K2, T, r, q, sigma):

        self.q = q
        self.r = r
        self.S = S
        self.K1 = K1
        self.K2 = K2
        self.T = T
        self.sigma = sigma

        self.d_1 = (log(S / K2) + (r - q + sigma**2 / 2)*T) / (sigma * sqrt(T))
        self.d_2 = self.d_1 - sigma * sqrt(T)

        self.price = K1 * exp(-r*T) * norm.cdf(-self.d_2) - S * exp(-q*T) * norm.cdf(-self.d_1)

    def delta(self):
        K2, K1, S, sigma, T, q, r = self.K2, self.K1, self.S, self.sigma, self.T, self.q, self.r
        return -sqrt(2)*K1*exp(-T*r - (2*T*q - 2*T*r + T*sigma**2 - log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*S*sqrt(T)*sigma) + exp(-T*q)*erf(-sqrt(2)*sqrt(T)*q/(2*sigma) + sqrt(2)*sqrt(T)*r/(2*sigma) + sqrt(2)*sqrt(T)*sigma/4 + sqrt(2)*log(S**2/K2**2)/(4*sqrt(T)*sigma))/2 - exp(-T*q)/2 + sqrt(2)*exp(-T*q - (-2*T*q + 2*T*r + T*sigma**2 + log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sqrt(T)*sigma)

    def gamma(self):
        return _gap_gamma(self.S, self.K1, self.K2, self.T, self.r, self.q, self.sigma)

    def vega(self):
        return _gap_vega(
            self.S, self.K1, self.K2, self.T, self.r, self.q, self.sigma
        )

    def rho(self):
        K2, K1, S, sigma, T, q, r = self.K2, self.K1, self.S, self.sigma, self.T, self.q, self.r
        return -sqrt(2)*K1*sqrt(T)*exp(-T*r - (2*T*q - 2*T*r + T*sigma**2 - log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sigma) - K1*T*exp(-T*r)*erf(sqrt(2)*sqrt(T)*q/(2*sigma) - sqrt(2)*sqrt(T)*r/(2*sigma) + sqrt(2)*sqrt(T)*sigma/4 - sqrt(2)*log(S**2/K2**2)/(4*sqrt(T)*sigma))/2 - K1*T*exp(-T*r)/2 + sqrt(2)*S*sqrt(T)*exp(-T*q - (-2*T*q + 2*T*r + T*sigma**2 + log(S**2/K2**2))**2/(8*T*sigma**2))/(2*sqrt(pi)*sigma)

    def theta(self):
        K2, K1, S, sigma, T, q, r = self.K2, self.K1, self.S, self.sigma, self.T, self.q, self.r
        return -1*(-K1*r*(erf(sqrt(2)*(sqrt(T)*sigma - (T*(-q + r + sigma**2/2) + log(S/K2))/(sqrt(T)*sigma))/2)/2 + 1/2)*exp(-T*r) + sqrt(2)*K1*(sigma/(2*sqrt(T)) - (-q + r + sigma**2/2)/(sqrt(T)*sigma) + (T*(-q + r + sigma**2/2) + log(S/K2))/(2*T**(3/2)*sigma))*exp(-T*r)*exp(-(sqrt(T)*sigma - (T*(-q + r + sigma**2/2) + log(S/K2))/(sqrt(T)*sigma))**2/2)/(2*sqrt(pi)) - S*q*(erf(sqrt(2)*(T*(-q + r + sigma**2/2) + log(S/K2))/(2*sqrt(T)*sigma))/2 - 1/2)*exp(-T*q) + S*(sqrt(2)*(-q + r + sigma**2/2)/(2*sqrt(T)*sigma) - sqrt(2)*(T*(-q + r + sigma**2/2) + log(S/K2))/(4*T**(3/2)*sigma))*exp(-T*q)*exp(-(T*(-q + r + sigma**2/2) + log(S/K2))**2/(2*T*sigma**2))/sqrt(pi))

class GapOptionPutShort(GapOptionPutLong):

    def __init__(self, S, K1, K2, T, r, q, sigma):
        super().__init__(S, K1, K2, T, r, q, sigma)
    def delta(self):
        return super().delta() * -1
    def gamma(self):
        return super().gamma() * -1
    def vega(self):
        return super().vega() * -1
    def theta(self):
        return super().theta() * -1
    def rho(self):
        return super().rho() * -1

class ForwardCallOptionLong:
    def __init__(self, S, T1, T2, q, r, sigma):

        self.S = S
        self.T1 = T1
        self.T2 = T2
        self.q = q
        self.r = r
        self.sigma = sigma

        parameters = {
            "S": self.S,
            "K": self.S,
            "T": T2 - T1,
            "r": self.r,
            "q": self.q,
            "sigma": self.sigma,
            }

        self.european_option = bs.BlackScholesCall(**parameters)
        self.price = exp(-self.q * self.T1) * self.european_option.price()

    def delta(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return ((erf(sqrt(2)*sqrt(-T1 + T2)*(-2*q + 2*r + sigma**2)/(4*sigma)) + 1)*exp(q*(T1 - T2)) + (erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) - 1)*exp(r*(T1 - T2)))*exp(-T1*q)/2

    def gamma(self):
        return 0

    def vega(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return S*sqrt(-2*T1 + 2*T2)*((-2*q + 2*r + sigma**2)*exp(r*(T1 - T2)) + (2*q - 2*r + sigma**2)*exp((8*q*sigma**2*(T1 - T2) + (-T1 + T2)*(2*q - 2*r + sigma**2)**2 + (T1 - T2)*(-2*q + 2*r + sigma**2)**2)/(8*sigma**2)))*exp((-8*T1*q*sigma**2 - (-T1 + T2)*(2*q - 2*r + sigma**2)**2)/(8*sigma**2))/(4*sqrt(pi)*sigma**2)

    def rho(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return S*(T1*erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) - T1 - T2*erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) + T2)*exp(-T1*q + T1*r - T2*r)/2

    def theta(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return S*q*(exp(T1*q + T2*r)*erf(sqrt(2)*sqrt(-T1 + T2)*(-2*q + 2*r + sigma**2)/(4*sigma)) + exp(T1*q + T2*r) + exp(T1*r + T2*q)*erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) - exp(T1*r + T2*q))*exp(-T1*q - T2*q - T2*r)/2

class ForwardCallOptionShort(ForwardCallOptionLong):
    def __init__(self, S, T1, T2, q, r, sigma):
        super().__init__(S, T1, T2, q, r, sigma)
    def delta(self):
        return super().delta() * -1
    def vega(self):
        return super().vega() * -1
    def theta(self):
        return super().theta() * -1
    def rho(self):
        return super().rho() * -1

class ForwardPutOptionLong():

    def __init__(self, S, T1, T2, q, r, sigma):

        self.S = S
        self.T1 = T1
        self.T2 = T2
        self.q = q
        self.r = r
        self.sigma = sigma

        parameters = {
            "S": self.S,
            "K": self.S,
            "T": T2 - T1,
            "r": self.r,
            "q": self.q,
            "sigma": self.sigma,
            }

        self.european_option = bs.BlackScholesPut(**parameters)
        self.price = exp(-self.q * self.T1) * self.european_option.price()

    def delta(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return ((erf(sqrt(2)*sqrt(-T1 + T2)*(-2*q + 2*r + sigma**2)/(4*sigma)) - 1)*exp(q*(T1 - T2)) + (erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) + 1)*exp(r*(T1 - T2)))*exp(-T1*q)/2
    
    def gamma(self):
        return 0

    def vega(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return S*sqrt(-2*T1 + 2*T2)*((-2*q + 2*r + sigma**2)*exp(r*(T1 - T2)) + (2*q - 2*r + sigma**2)*exp((8*q*sigma**2*(T1 - T2) + (-T1 + T2)*(2*q - 2*r + sigma**2)**2 + (T1 - T2)*(-2*q + 2*r + sigma**2)**2)/(8*sigma**2)))*exp((-8*T1*q*sigma**2 - (-T1 + T2)*(2*q - 2*r + sigma**2)**2)/(8*sigma**2))/(4*sqrt(pi)*sigma**2)
    
    def rho(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return S*(T1*erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) + T1 - T2*erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) - T2)*exp(-T1*q + T1*r - T2*r)/2

    def theta(self):
        T2, T1, sigma, S, q, r = self.T2, self.T1, self.sigma, self.S, self.q, self.r
        return S*q*((erf(sqrt(2)*sqrt(-T1 + T2)*(-2*q + 2*r + sigma**2)/(4*sigma)) - 1)*exp(q*(T1 - T2)) + (erf(sqrt(2)*sqrt(-T1 + T2)*(2*q - 2*r + sigma**2)/(4*sigma)) + 1)*exp(r*(T1 - T2)))*exp(-T1*q)/2

class ForwardPutOptionShort(ForwardPutOptionLong):
    def __init__(self, S, T1, T2, q, r, sigma):
        super().__init__(S, T1, T2, q, r, sigma)
    def delta(self):
        return super().delta() * -1
    def vega(self):
        return super().vega() * -1
    def theta(self):
        return super().theta() * -1
    def rho(self):
        return super().rho() * -1
