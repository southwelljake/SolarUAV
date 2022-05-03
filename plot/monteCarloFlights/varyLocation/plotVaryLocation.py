from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt

locations = ['barrow', 'london', 'la', 'mexicocity', 'singapore', 'brisbane', 'melbourne', 'ushuaia']
latitude = ['70', '50', '35', '20', '0', '-25', '-40', '-55']

fig, ax = plt.subplots(nrows=4, ncols=2)

col = 0
row = 0
for i in range(0, 8):

    low = []
    high = []

    months = [i for i in range(1, 13)]
    for month in months:
        p = ProcessSensitivity('../../../data/monte_carlo_results/varyLocation/' +
                               locations[i].capitalize() + '/' + locations[i] +
                               '_low_cloud_' + str(month) + '.txt')

        low.append(sum(p.outcome) / p.no_sims)

        p2 = ProcessSensitivity('../../../data/monte_carlo_results/varyLocation/' +
                                locations[i].capitalize() + '/' + locations[i].lower() +
                                '_high_cloud_' + str(month) + '.txt')

        high.append(sum(p2.outcome) / p2.no_sims)

    ax[row, col].plot(months, low, label='Low Cloud Cover')
    ax[row, col].plot(months, high, label='High Cloud Cover')
    ax[row, col].legend(loc='lower left')
    ax[row, col].set_title(locations[i].capitalize() + ', Latitude: ' + latitude[i])
    ax[row, col].set_ylim([-5, 105])

    row += 1
    if row == 4:
        col += 1
        row = 0

ax[2, 0].set_title('Los Angeles, Latitude: 35')
ax[3, 0].set_title('Mexico City, Latitude: 20')
ax[0, 0].set_ylabel('Percentage Complete (%)')
ax[1, 0].set_ylabel('Percentage Complete (%)')
ax[2, 0].set_ylabel('Percentage Complete (%)')
ax[3, 0].set_ylabel('Percentage Complete (%)')
ax[3, 0].set_xlabel('Month')
ax[3, 1].set_xlabel('Month')


plt.subplots_adjust(left=0.075, right=0.925, top=0.95, bottom=0.075, wspace=0.25, hspace=0.275)

plt.show()
