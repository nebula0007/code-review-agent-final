# Code Review Environment (OpenEnv)

## Overview
This project implements an OpenEnv-compatible environment for evaluating AI agents on real-world code review tasks.

## Features
- Deterministic grading system (0.0–1.0 reward)
- Multi-difficulty tasks (easy, medium, hard)
- Real-world code issues: syntax, logic, performance
- Lightweight and reproducible environment

## Task Description
The agent receives a code diff and must:
1. Identify the issue type
2. Describe the issue
3. Suggest a fix

## API Endpoints
- POST /reset → returns new task
- POST /step → evaluates agent action
- GET /state → returns current state

## Reward Function
- Issue type match: 0.4
- Description match: 0.3
- Fix match: 0.3

## Example
Input: