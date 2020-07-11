# CatMario

## Summary

Syobon Action(aka. Cat Mario), is a Super Mario-like game which features numerous unorthodox traps that are intentionally placed to kill the character and cause extreme frustration. The goal of this project is to develop an AI that can control the agent(cat) to pass the horizontal game level by going around the traps. We are implementing the project by using NEAT method and extracting data with our own CV-capture unit.

## CV-Capture Unit

Most gaming AIs were developed and embedded in its host game that grant them direct accesses to the in-game data for training and evaluation. Since we are building AI on a stand alone application, the only real-time game data that are accessible from Cat Mario are the final gameplay. All of the game information, such as the agent, object locations, colors, etc, must be recognized in the forms of pixels from the video feed. As a result, the first challenge in developing the Cat Mario AI is to analyze the gameplay frame in real-time and extract useful datasets for AI training and validation. This is accomplished with computer vision (CV) using tools in OpenCV, a popular open source CV library.

## NEAT (Neuroevolution of augmenting topologies)

NEAT combines the uses of genetic algorithm and NN. At each generation (loop over list of NN), we will get a fitness(reward) for how each genome (NN) perform our task. Then the genome with least performance(fitness) in each species(cluster) will be removed and the new genomes produced by mutation or crossover will join the population (list of NN) in the species they belong to (or create a new species), then move forward to the next generation).

![CatMario](https://github.com/jawadefaj/CatMario/blob/master/main/Capture.PNG)
![CatMario](https://github.com/jawadefaj/CatMario/blob/master/main/temp.jpg)
