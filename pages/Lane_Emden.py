import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


m_H = 1.673557e-27
G = 6.6743e-11
c = 299792458
mu = 0.6
k_B = 1.380649e-23
solar_mass = 1.989e30
solar_radius = 6.957e+8

def RK4(x0, y0, dx, func, n):
    k1 = func(x0, y0, n)
    k2 = func(x0 + dx/2, y0 + k1*(dx/2), n)
    k3 = func(x0 + dx/2, y0 + k2*(dx/2), n)
    k4 = func(x0 + dx, y0 + dx*k3, n)

    y1 = y0 + (dx/6)*(k1 + 2*k2 + 2*k3 + k4)

    return y1

def dy_dx(x, y, n):
    return np.array([y[1], -2*(y[1]/x) - y[0]**n])

def model(n):

    theta = [1]
    beta = [0]

    z = np.array([theta, beta])
    print(z)

    x = [1e-6]
    dx = 0.001

    while z[0,-1] > 0:
        try:
            y0 = z[:,-1]
            print(y0)

            y1 = RK4(x[-1], y0, dx, func=dy_dx, n=n)

            if y1[1] == np.nan:
                break

            z = np.append(z, y1.reshape(-1, 1), axis = 1)

            x.append(x[-1] + dx)
        except RuntimeWarning:
            print('Reached end')
            break

    return np.array(x), z

def central_density(M, R, xi_R, dtheta_R):
    return (-M/xi_R)/(4*np.pi*R**3 * dtheta_R)

def density(M, R, n, xi, z):
    rho_c = central_density(M, R, xi[-1], z[1, -1])
    rho = z[0]**n * rho_c
    return rho

def Pressure(R, xi_R, n, rho):
    P = ((4*np.pi*G)/(n + 1))*(R/xi_R)**2
    return P*rho**2

def Temperature(P, rho):
    # return (P*mu)/(k_B * rho_c * theta ** (1/n))
    return (P*mu*m_H)/(k_B*rho)

st.title('Polytrope')

st.markdown(
    """
    One of the ways we can approximate the internal density profile of a star is 
    to assume it can take on the form of a Polytrope -- a self-gravitating ball of gas.
    The solutions to the density profile can be found by first finding a solution to the 
    Lane-Emden equation    
"""
)

st.latex(r"""
\frac{1}{\xi^2}\frac{d}{d\xi}\left(\xi^2\frac{d\theta}{d\xi}\right) + \theta^n = 0
         """)

st.markdown(
    """
This can be solved numerically by splitting it into two 1st-Order differential equations where
"""
)

st.latex(
    r"""
    \frac{d\theta}{d\xi} = \beta
    """
)

st.latex(
    r"""
\frac{d\beta}{d\xi} = -\frac{2\beta}{\xi} - \theta^n
"""
)

st.markdown(r"""
    The n here refers to the polytropic index and we let it vary between 0 and 4
    From solving for $\theta$, we can find the density $\rho = \rho_c \theta^n$, from which the Pressure $P$ can 
            be calculated. More information can be found in this [book](https://www.cambridge.org/highereducation/books/an-introduction-to-modern-astrophysics/140DDF8A480C3841DCCD76D66984D858#overview)
""")

n = st.number_input('Polytropic index, n', value = 1.0, max_value=4.0)
columns = st.columns(2)

M = columns[0].number_input('Mass [solar masses]', value = 1)*solar_mass
R = columns[1].number_input('Radius [solar radii]', value = 1)*solar_radius


if st.button('Calculate'):
    x, y = model(n)

    
    rho = density(M, R, n, x, y)
    P = Pressure(R, x[-1], n, rho)
    # T = Temperature(P, rho)

    data = {
        'xi':x,
        'theta':y[0],
        'dtheta/dxi':y[1],
        'Density':rho,
        'Pressure':P
    }

    df = pd.DataFrame(data)
    # df['Temp_prop'] = df['Temperature']/df['Temperature'][0]
    df['Density_prop'] = df['Density']/df['Density'][0]
    df['Pressure_prop'] = df['Pressure']/df['Pressure'][0]
    
    
    # data = {
    #     'xi':x,
    #     'theta':y[0],
    #     'dtheta/dxi':y[1]
    # }

    df = pd.DataFrame(data).round(3)
    st.write(df) 

    fig, ax = plt.subplots()
    ax.plot(x, y[0], 'k-')
    ax.set_xlabel(r'$\xi$', size = 15)
    ax.set_ylabel(r'$\theta$', size = 15)
    st.pyplot(fig)

    
    fig, ax = plt.subplots()
    r_frac = x/x[-1]
    ax.plot(r_frac, rho/rho[0], label = r'$\rho/\rho_c$')
    ax.plot(r_frac, P/P[0], label = r'$P/P_c$')
    # ax.plot(r_frac, T/T[0], label = r'$T/T_c$')
    ax.set_xlabel('$r/R$', size = 15)
    ax.legend()
    st.pyplot(fig)

    




