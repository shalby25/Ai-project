# Sokoban Puzzle – Search Algorithms Project

## Overview

This project implements and compares several **Artificial Intelligence search algorithms** using the **Sokoban puzzle** as the problem environment. Sokoban is a classic logic-based puzzle that is widely used in AI research and education because it represents a challenging and constrained search problem with a very large state space.

The goal of the project is to demonstrate how different search strategies behave when applied to the same problem, and to highlight their strengths, weaknesses, and performance differences.

---

## What is Sokoban?

Sokoban is a grid-based puzzle game where a player (agent) moves inside a warehouse-like environment that contains:

* Walls
* Empty cells
* Boxes
* Target (goal) locations

The player can move in four directions (up, down, left, right) and can **push boxes** one cell at a time. Boxes cannot be pulled, and a box can only be pushed if the cell behind it is empty.

---

## Objective of the Game

The main objective of Sokoban is:

> **To move all boxes onto their designated goal positions.**

The puzzle is considered solved when every box is placed on a goal cell, regardless of the player’s final position.

---

## Game Rules and Constraints

* The player cannot move through walls.
* The player cannot pull boxes, only push them.
* A box cannot be pushed into a wall or another box.
* Some moves may lead to irreversible situations (deadlocks), making the puzzle unsolvable.

These constraints make Sokoban a non-trivial problem that requires careful planning and intelligent search strategies.

---

## Sokoban as a Search Problem

From an AI perspective, Sokoban can be formally modeled as a **search problem**:

### State Representation

A state is defined by:

* The current position of the player
* The positions of all boxes on the grid

Any change in the player or box positions results in a new state.

### Initial State

The initial state represents the starting configuration of:

* Player position
* Box positions
* Goal positions
* Map layout

### Actions

The available actions are:

* Move Up
* Move Down
* Move Left
* Move Right

An action is valid only if it follows the game rules.

### Goal Test

The goal test checks whether:

* **All boxes are placed on goal positions**

If this condition is satisfied, the solution is found.

### Path Cost

The path cost can be defined in different ways, such as:

* Each move has a cost of 1
* Pushing a box has a higher cost than a normal move

This flexibility allows the use of cost-based search algorithms.

---

## Why Sokoban is Suitable for Search Algorithms

Sokoban is an ideal benchmark problem for search algorithms because:

* It has a very large state space
* It includes strict constraints and illegal moves
* It contains deadlocks that must be avoided
* Not all solutions are optimal or even valid

These characteristics make it suitable for evaluating both uninformed and informed search techniques.

---

## Relation to Search Algorithms

This project uses Sokoban to apply and analyze different search algorithms, showing how each algorithm explores the state space and attempts to reach the goal under the same problem conditions.
