from __future__ import with_statement
import random
import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
import time
import math

def sim(iterations):

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

if __name__ == "__main__":
    # Parameters 
    nOfIterations = 10000
    nOfTrials = 100
    e = math.e

    allTrials = []
    allTimes = []
    horizontalAx = np.arange(0,nOfIterations,1) # X axis of iterations

    # Asynchronous trials running at the same time for efficiency
    with concurrent.futures.ProcessPoolExecutor() as executor:
        trialResults = [executor.submit(sim, nOfIterations) for _ in range(nOfTrials)]

        for trialResult in concurrent.futures.as_completed(trialResults):
            allTrials.append(trialResult.result()[0]) # Append the final result of each trial
            allTimes.append(trialResult.result()[1]) # Append how much it took for each trial

    allTrialsArray = np.array(allTrials) # Make it an np array

    graph = plt.figure(figsize=(7,8)) # Create the window

    # Average e approximation for each iteration across trials
    averageLine = np.mean(allTrials,axis=0) 

    # Median e approximation for each iteration across trials
    medianLine = np.median(allTrialsArray, axis=0)

    # Calculate the upper quartile of data 
    uppperQuartile = np.abs(allTrialsArray - e) # Zero values in relation to e and take the absolute values
    uppperQuartile = np.quantile(uppperQuartile, 0.75, axis=0) # Find the upper quartile to plot a line
    uppperQuartile += e # Reset the values

    graph1 = plt.subplot(311) # Plot initial figure
    for trial in allTrials: # Plot each trial
        plt.plot(horizontalAx,trial, c='k', lw=0.2)

    graph1.plot(averageLine, c='tab:green', lw=1, label='Average') # Plot the average line
    graph1.plot(uppperQuartile, c='tab:blue', lw=1.25, label='75th quantile') # Plot the upper quartile line
    graph1.plot(medianLine, c='tab:cyan', lw=1, label='Median') # Plot the median line
    graph1.axhline(e, c='tab:red', linestyle='dashed', label='e') # Plot the value of e
    graph1.set_xlim(0,nOfIterations)
    graph1.set_xticklabels([])
    graph1.set_ylim(e-(e/2), e+(e/2))
    graph1.legend(loc="lower right")

    # Calculate the accuracy of all trials
    accuracyOfTrials = np.abs(e-allTrialsArray)/e

    # Calculate the accuracy of the upper quartile of trials
    upperQuartileAccuracy = np.abs(e-uppperQuartile)/e

    graph2 = plt.subplot(312, sharex=graph1) # Plot the accuracy graphs
    for trial in accuracyOfTrials: 
        plt.plot(trial, c='k', lw=0.2)
    
    graph2.plot(upperQuartileAccuracy, c='tab:blue', lw=1.25, label='75th Quantile')
    graph2.set_ylim(0,1)
    graph2.set_ylabel("% difference")
    graph2.legend()


    # Calculate the standard deviation for all trials
    standardDeviation = np.std(allTrialsArray, axis=0)

    graph3 = plt.subplot(313) # Plot the standard deviation line
    graph3.plot(standardDeviation, c='tab:blue', lw=1)
    graph3.set_xlim(0,nOfIterations)
    graph3.set_xlabel("Iterations")
    graph3.set_ylabel("Standard deviation")


    print(f'Final Results') # Output final results of the simulation
    print(f'Average: {averageLine[-1]:.6f} {((abs(e-averageLine[-1])/e)*100):.6f}%')

    print(f'Median: {medianLine[-1]:.6f} {((abs(e-medianLine[-1])/e)*100):.6f}%')

    print(f'Standard Deviation: {standardDeviation[-1]:.6f}')

    print(f'Average Time Taken: {(np.average(allTimes)*1000):8.4f}ms')
    plt.subplots_adjust(hspace=.1)
    plt.show() # Display the graph
