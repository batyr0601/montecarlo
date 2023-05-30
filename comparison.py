import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import concurrent.futures
import time

e = math.e

def cardGame(iterations):
    
    approximation = [] # Stores the result after each iteration

    startTimer = time.perf_counter() # Begin trial timer

    wins = 0

    for i in range(iterations):
        # Deck of cards
        deck = []
        # First selected 19 cards
        randomArray = []

        # Arbitrary numbers that will be changed by the program
        highestRank = 2000
        randomCard = 1999
        chosenCard = 1998
        
        # Adding 52 cards to the list
        for x in range(1,53):
            deck.append(x)

        # Picking random 19 cards
        for x in range(19):
            randomCard = random.choice(deck)
            randomArray.append(randomCard)
            deck.remove(randomCard)

        # Finding the highest in the first 19
        for x in randomArray:
            if x < highestRank:
                highestRank = x

        if (highestRank != 1): # If Ace of Clubs was not among the first 19
            while (highestRank < chosenCard):
                chosenCard = random.choice(deck) # pulling a random card from the deck
                deck.remove(chosenCard)

        if (chosenCard == 1): # If it is Ace of Clubs
            wins+=1
        
        if (wins != 0): # To avoid dividing by 0
            ratio = (i+1)/wins # Approximate e

        else:  
            ratio = 0 # 0 if there are no wins

        approximation.append(ratio) # Save the ratio for that iteration

    endTimer = time.perf_counter() - startTimer # Finish trial timer 

    print(f'{(approximation[-1]):.6f}: {(endTimer*1000):8.4f}ms') # Output info about the trial
    return [approximation, endTimer]

def alternativeMethod(iterations):
    approximation = [] # Stores the result after each iteration
    array = np.array([]) # np array to store how many numbers it took to exceed 1
    startTimer = time.perf_counter() # Begin trial timer
    
    for i in range(iterations):

        total = 0
        numberOfNumbers = 0

        while (total < 1):
            randomNumber = random.random()
            total += randomNumber
            numberOfNumbers += 1
        
        array = np.append(array, numberOfNumbers)
        approximation.append((np.mean(array)))

    endTimer = time.perf_counter() - startTimer # Finish trial timer 

    print(f'{(approximation[-1]):.6f}: {(endTimer*1000):8.4f}ms') # Output info about the trial
    return [approximation, endTimer]

def improvedCardGame(iterations):
    approximation = [] # Stores the result after each iteration

    startTimer = time.perf_counter() # Begin trial timer

    wins = 0

    for i in range(iterations):
        # Deck of cards
        deck = []
        # First selected 368 cards
        randomArray = []

        # Arbitrary numbers that will be changed by the program
        highestRank = 2000
        randomCard = 1999
        chosenCard = 1998
        
        # Adding 1000 cards to the list
        for x in range(1,1001):
            deck.append(x)

        # Picking random 368 cards
        for x in range(368):
            randomCard = random.choice(deck)
            randomArray.append(randomCard)
            deck.remove(randomCard)

        # Finding the highest in the first 368
        for x in randomArray:
            if x < highestRank:
                highestRank = x

        if (highestRank != 1): # If Ace of Clubs was not among the first 368
            while (highestRank < chosenCard):
                chosenCard = random.choice(deck) # pulling a random card from the deck
                deck.remove(chosenCard)

        if (chosenCard == 1): # If it is Ace of Clubs
            wins+=1
        
        if (wins != 0): # To avoid dividing by 0
            ratio = (i+1)/wins # Approximate e

        else:  
            ratio = 0 # 0 if there are no wins

        approximation.append(ratio) # Save the ratio for that iteration

    endTimer = time.perf_counter() - startTimer # Finish trial timer 

    print(f'{(approximation[-1]):.6f}: {(endTimer*1000):8.4f}ms') # Output info about the trial
    return [approximation, endTimer]

def simulation(function,iterations,trials):
    allTrials = []
    allTimes = []

    # Asynchronous trials running at the same time for efficiency
    with concurrent.futures.ProcessPoolExecutor() as executor:
        trialResults = [executor.submit(function, iterations) for _ in range(trials)]

        for trialResult in concurrent.futures.as_completed(trialResults):
            allTrials.append(trialResult.result()[0]) # Append the final result of each trial
            allTimes.append(trialResult.result()[1]) # Append how much it took for each trial

    return(allTrials,allTimes)

def plotLines(allTrials, allTimes, colors, axis):
    axis1 = axis
    color1, color2, color3, color4 = colors

    allTrialsArray = np.array(allTrials)

    # Average e approximation for each iteration across trials
    averageLine = np.mean(allTrialsArray,axis=0) 

    # Calculate the upper quartile of data 
    upperQuartile = np.abs(allTrialsArray - e) # Zero values in relation to e and take the absolute values
    upperQuartile = np.quantile(upperQuartile, 0.75, axis=0) # Find the upper quartile to plot a line
    upperQuartile += e # Reset the values

    # Median e approximation for each iteration across trials
    medianLine = np.median(allTrialsArray, axis=0)

    # Calculate the accuracy of all trials
    accuracyOfTrials = np.abs(e-allTrialsArray)/e

    # Calculate the accuracy of the upper quartile of trials
    upperQuartileAccuracy = np.abs(e-upperQuartile)/e

    # Calculate the standard deviation for all trials
    standardDeviation = np.std(allTrialsArray, axis=0)

    for trial in allTrials:
        axis1.plot(trial, c=color1, lw=0.1, zorder=-1)
    axis1.plot(averageLine, c=color3,  lw=1, label='Average')
    axis1.plot(upperQuartile, c=color2, lw=2.0, label='75th Quantile')
    axis1.plot(medianLine, c=color4, lw=1, label='Median')

    # Bonus stats
    averageTrialTime = np.average(allTimes)*1000
    averageIterationTime = averageTrialTime/len(allTrials[0])
    
    print(f'Final Results') # Output final results of the simulation
    print(f'Average: {averageLine[-1]:.6f} {((abs(e-averageLine[-1])/e)*100):.6f}%')
    print(f'Median: {medianLine[-1]:.6f} {((abs(e-medianLine[-1])/e)*100):.6f}%')
    print(f'Standard Deviation: {standardDeviation[-1]:.6f}')
    print(f'Average Time Taken Per Trial: {averageTrialTime:8.4f}ms')
    print(f'Average Time Taken per Iteration: {averageIterationTime:8.4f}ms')


if __name__ == "__main__":
    # Parameters 
    iterations = 10000
    trials = 100
 
    sim1Trial, sim1Time = simulation(cardGame,iterations, trials)
    print('-----------------------------------------')
    sim2Trial, sim2Time = simulation(alternativeMethod,iterations, trials)
    print('-----------------------------------------')
    sim3Trial, sim3Time = simulation(improvedCardGame,iterations, trials)

    graph = plt.figure(figsize=(7,8)) # Create the window

    axis1 = plt.subplot(111) # Plot the initial graph
    axis1.axhline(e, c='black', ls='dashed', zorder = 10, label='e') # Plot the value of e
    axis1.set_xlim(0,iterations)
    axis1.set_ylim(e-(e/2), e+(e/2))

    axis1.set_xlabel("Iterations")

    axs = axis1
    alternativeMethodColors = ('yellow','red','darkred', 'coral')
    cardGameColors = ('silver','green','darkolivegreen', 'lightgreen')
    improvedCardGameColors = ('lightcyan','dodgerblue', 'navy', 'mediumslateblue')

    # Line colors
    quantileC1 = Patch(fc='red',)
    quantileC2 = Patch(fc='green',)
    quantileC3 = Patch(fc='dodgerblue',)
    averageC1 = Patch(fc='darkred',)
    averageC2 = Patch(fc='darkolivegreen',)
    averageC3 = Patch(fc='navy',)
    medianC1 = Patch(fc='coral',)
    medianC2 = Patch(fc='lightgreen',)
    medianC3 = Patch(fc='mediumslateblue',)
    trialC1 = Patch(fc='yellow',)
    trialC2 = Patch(fc='silver',)
    trialC3 = Patch(fc='lightcyan',)
    eColor = Patch(fc='black', ls='dashed')
    blank = Patch(fc='white')

    axis1.legend(handles=[quantileC1,averageC1,medianC1,trialC1,blank,quantileC2,averageC2,medianC2,trialC2,blank,quantileC3,averageC3,medianC3,trialC3,eColor], labels=['','','','','','','','','','','75th Quantile','Mean','Median','Trial', 'e'], columnspacing=-0.8, ncol=3, loc=1)

    print("\nCard Game ", end="")
    plotLines(sim1Trial, sim1Time, cardGameColors, axs)

    print("\nAlternative Method ", end="")
    plotLines(sim2Trial, sim2Time, alternativeMethodColors, axs)

    print("\nImproved Card Game ", end="")
    plotLines(sim3Trial, sim3Time, improvedCardGameColors, axs)

    plt.subplots_adjust(hspace=.1)
    plt.show() # Show graph