# Design document for the werewolf simulator

## Class Simulator
- description
    - Wraps around Game objects. Make repeated simulations and summarize results

## Class Game
- description
    - game engine for one game
    - contains all game information and history
    - request reponses from Player objects
- member 
    - List of Player objects
    - Game progress history
    - Current stage
- methods

## Class GameStage
- description 
    - Enum of all game stages
    - such as nightVotingStage, sheriffVotingStage, etc. 

## Class Role
- description
    - Enum of all game roles
    - such as werewolf, villager, etc. 

## Class Player
- description
    - a player that will react and make decisions, based on his Role and skill level
- member
    - Role
    - skill level
- methods
    - react(Game)
        - make decision about voting or choosing target, based on the current status of the game


