# Challenge for the QEC Hackathon 2023 at ETH Zurich

## Summary
We can use quantum computers to help us with machine learning. By utilizing variational quantum circuits, we can use quantum computers to learn patterns in data.

In order for this to work well, we need to come up with a way to encode the patterns we want to learn into the quantum computer. Especially on near-term quantum hardware, this requires quite some resources. One way to reduce these resource requirements and learn more efficiently is to take advantage of symmetries in the data we are trying to learn.

One approach is taken in [this paper](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.4.010328) (CC-BY 4.0, Johannes Jakob Meyer, Marian Mularski, Elies Gil-Fuster, Antonio Anna Mele, Francesco Arzani, Alissa Wilms, and Jens Eisert) and we will use it as a guideline for this challenge. A huge thank you to the authors for providing this idea and explaing it so well :-)

## What's inside
This repository contains a Jupyter Notebook that walks you through the basic idea of constructing a circuit that utilizes the problem symmetry and applies it to Tic-Tac-Toe.

## What we did
- Implemented the Tic-Tac-Toe Quantum Machine Learning model for an arbitrary number of layers, with or without including drawn positions, and with and without leveraging the symmetry of the problem.
- Implemented a similar model to find whether there exists a path between any two corners of a 3x3 maze, with and without leveraging the symmetry.
- Implemented the same for a 5x5 maze, however, takes too long to run (it's hard to simulate 25 qubits).

## Files
- <code>hackhathon_notebook_layers</code> implements the Tic-Tac-Toe model for an arbitray number of layers, with or without draws, using the symmetry of the problem.
