
import streamlit as st
from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np


def PDF(x, mean):
    # Probability Distribution Function
    rate = 1/mean

    return rate * np.exp(-rate*x)

def probability(func, mean, a, b):
    # integrate PDF (can be done analytically, just testing the quad function)
    ans = integrate.quad(func, a, b, args=mean)
    return ans


st.title('Pokémon Shiny Odds Calculator')

st.markdown(
    'One of the feature of the pokemon is the existence of shiny Pokemon -- rare ' \
    'pokemon that exhibit different colours than what they usually are. Shiny pokemon are encountered after an' \
    'amount of wild pokemon encounters (usually with a mean encounter rate of 1 in 8192, depending ' \
    'on the game). What this page allows us to do is calculate the probability that the number of wild encounters ' \
    'to find a shiny pokemon lies in a user-defined range.' \
    '' \
)

st.markdown(
    """
    The Probability Distribution Function (PDF) used for this calculation takes on the form of

    $$f(x) = r e^{-rx}$$

    where x represents the number of encounters and r = 1/mean. The quad function from the scipy.integrate package is then used
    to calculate the probability (even though it can be done analytically)

    $$P(a<x<b) = \int_a^b f(x)dx $$
    """
)


# Mean encounters, varies per game
mean_count = st.number_input(label='Mean', value = 8192)

# decides wether the probability is P(a<x<b) or P(x>a)
radio_val = st.radio(label='Options',
                     options=['With upper bound',
                              'Without upper bound']
)

# define bounds
columns = st.columns(2)
lower_bound = columns[0].number_input('Lower bound', value=0)
upper_bound = np.inf
if radio_val == 'With upper bound':
    upper_bound = columns[1].number_input('Upper bound', value=0)

if st.button('Calculate'):

    if lower_bound >= upper_bound:
        st.text('Lower bound needs to be less than upper bound!')

    else:
        # calculate and display
        ans = probability(PDF, mean_count, lower_bound, upper_bound)[0]

        st.metric(label='Probability of this shiny hunt:', value=f'{ans*100:.2f} %')

        making_plot_text = st.text('Making plot...')

        x = np.linspace(0, 50000, 100000)
        y = PDF(mean=mean_count, x = x)
        fig, ax = plt.subplots()
        ax.plot(x, PDF(mean=mean_count, x = x), 'k-')
        ax.set_xlabel('Number of encounters', size = 15)
        ax.set_ylabel('PDF', size = 15)
        if upper_bound == np.inf:
            ax.fill_between(x, y, 0, where=(x>lower_bound), color='grey')
        else:
            ax.fill_between(x, y, 0, where=(x>=lower_bound) & (x<=upper_bound), color = 'grey')
        st.pyplot(fig)

        making_plot_text.text("")