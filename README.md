# Football Game Sequence Generator

### 1. Exploratory Data Analysis (EDA):
   - Please refer to the `EDA.ipynb` file for a comprehensive data analysis.

---
### 2. Approaches for Recreating the Game:
Below is a list of some approaches brainstormed as a potentiel solution to the task :

1. **Time Series Forecasting**:
   - Using methods like ARIMA, Prophet, or LSTM neural networks to predict future values of the acceleration norms.
   - A model can be trained to predict sequences of acceleration data, which could simulate player movement.
   
2. **Generative Models**:
   - Using Generative Adversarial Networks (GANs) or Variational Autoencoders (VAEs) to generate new sequences of accelerometer data.
   - Such models can learn the distribution of the existing data and produce new, similar data that can recreate player movements.

3. **Markov Models**:
   - Model player actions as states in a Markov Chain.
   - Using transition probabilities (derived from existing data) to simulate sequences of actions in a game.

4. **Behavior Cloning**:
   - Using deep learning methods like Long short-term memory (LSTM) networks to train a model to imitate the observed sequences of accelerometer data.
   - This approach directly uses the provided data to teach the model how a player moves.

5. **Agent-Based Modeling**:
   - Create virtual agents that represent players.
   - Define behaviors for these agents based on the provided data, and let them interact in a virtual environment to recreate game scenarios.

6. **Hybrid Models**:
   - Combining multiple approaches. For instance, use a Markov model to decide the next action and a generative model to produce the acceleration data for that action.

7. **Synthetic Data Generation Tools**:
   - Using tools like DataSynthesizer or SDV to create synthetic datasets based on the original data, which can be used to simulate additional game scenarios.

---
### 3. Recreating the Game:
   
- ### Approach

The Markov Models approach allows us to use historical game data to predict future actions based on the current state. By analyzing the transition probabilities between different actions, the model can simulate a sequence of actions for a given duration and style of play.

The detailed methodology and tests I did to implement this solution are available in the `workshop.ipynb` notebook.

- ### Running the Code

To run the code and generate a game sequence, use the provided shell script `init.sh`. 
Call the shell script with the desired arguments for the starting action (`pass, run, walk, etc.`), game duration (`intger`), and game style(`attacking, neutral, defensive`).

```bash
./init.sh pass 9 neutral
```

This command will start the game with a pass, aiming for a 9-minute duration and a neutral style of play. The generated game sequence will be downloaded as a `game.json` file in the current directory.

- ### API and Further Experimentation

Running the shell script will also start the FastAPI server and automatically open the API documentation URL in your default web browser. You can use the interactive API documentation to further experiment with the game generation parameters and understand the API endpoints.

URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- ### Project Structure and Details

    - `main.py`: The main file that orchestrates the game generation.
    - `generate_game_v1.py`: Contains the logic for generating the game sequence based on the Markov Model.
    - `prepare_data.py`: Used for reading and preprocessing the game data.
    - `api.py`: Defines the FastAPI application and the API endpoints.
    - `data/`: Directory containing the JSON files with historical game data.

All the necessary packages will be installed when running the shell script.

- ### TODO list :
    - Add a 4th argument representing the number of games desired.
    - Add more logical constraints to the model. (example : a game can't realistically start with a cross)
    - Fix the distibution of the gaits' duration.
    - Implement and experiment with more machine learning based approaches.
    - Add more customized game styles like a `ball possession play style` with higher passing and dribbling or `high intensity play style` with extra running and less walking.
    - Error handling.
    - More robust approach for handling missing or irrelevant data.
    - ...
---
### 4. Detailed Approach Documentation:

### **Stochastic Transition Matrix-Based Game Generation**

- #### **Pitch**:
The core idea is to utilize historical data to create a transition matrix, which captures the likelihood of transitioning from one player action to another. With this matrix as a foundation, we can recreate new games that mirror the patterns and tendencies observed in the original matches.


- #### Why a Matrix-Based Approach?

In simulating a football game sequence, the choice of using a Markov Chain and a matrix-based approach is both strategic and practical. 

- #### 1. **Represents Transitions Between States:**

   In football, actions transition from one to another, forming a sequence. A matrix-based approach, particularly using a transition matrix, naturally models these transitions. Each entry \(a_{ij}\) in the transition matrix represents the probability of transitioning from action \(i\) to action \(j\). This representation provides a structured and efficient way to model the game dynamics.

- #### 2. **Utilizes Historical Data:**

   The transition matrix is constructed using historical game data. This data-driven approach ensures that the simulated game sequences reflect real-world patterns and strategies. The probabilities in the matrix are not arbitrary but are derived from actual game data, enhancing the realism and reliability of the generated sequences.

- #### 3. **Efficient Computation:**

   Matrix operations are highly optimized and efficient. The matrix-based approach allows for rapid computation, enabling the generation of game sequences in real-time or near-real-time. This efficiency is crucial for applications that require instantaneous results.

- #### 4. **Facilitates Stochastic Simulation:**

   The use of a transition matrix introduces stochasticity into the simulation. The generated game sequences are not deterministic but are influenced by the probabilities in the transition matrix. This stochastic nature aligns with the unpredictable and dynamic environment of a football game.

- #### 5. **Adaptable to Different Game Styles:**

   The transition matrix can be easily adapted to simulate different styles of play (e.g., offensive, defensive, neutral). By adjusting the transition probabilities, the matrix-based approach can generate game sequences that align with various tactical approaches, providing flexibility and adaptability in simulation.



- #### **More advantages**:


1. **Flexibility**: We can easily modify the transition matrix or impose additional constraints to tailor the generated games to specific scenarios.
2. **Scalability**: The matrix-based approach can accommodate additional actions or nuances as more data becomes available.
3. **Consistency**: The transition matrix enforces a logical flow of actions, reducing the likelihood of generating improbable game sequences.

- #### **Limitations**:

1. **Limited Diversity**: If the provided historical data has limited variability, the generated games might lack diversity and closely resemble the original matches.
2. **Assumption of Independence**: The approach assumes that the next action is dependent solely on the current action, disregarding any longer sequences or overarching game strategies.
3. **Historical Bias**: The approach is dependent on the provided data. If the original matches have inherent biases or unique patterns, the generated games will reflect those biases.
4. **Lacks Contextual Awareness**: The matrix doesn't account for external factors, such as game score, player fatigue, or strategic decisions, which might influence player actions.

---
- ### The pre-/post- processing of data :

    - The raw data, stored in JSON files (e.g., match_1.json, match_2.json), is read into the program.
    - Users can specify their customized file paths in a .env file to adapt to different data sources.
    - Additional features and statistics that are essential for the Markov model, such as the average and standard deviation of norm values for each action, are calculated and stored for easy access.

---

$